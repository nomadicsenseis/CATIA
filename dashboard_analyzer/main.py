#!/usr/bin/env python3
"""
Enhanced Flexible NPS Anomaly Detection System
Shows all periods with anomalies and includes explanations
"""

import asyncio
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
import sys
import os
import json
from contextlib import redirect_stdout, redirect_stderr
import pandas as pd

from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
from dashboard_analyzer.anomaly_detection.flexible_detector import FlexibleAnomalyDetector
from dashboard_analyzer.anomaly_detection.flexible_anomaly_interpreter import FlexibleAnomalyInterpreter
from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_summary_agent import AnomalySummaryAgent
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type

# Global debug flag
DEBUG_MODE = True

def debug_print(message):
    """Print debug message only when debug mode is enabled"""
    if DEBUG_MODE:
        print(f"🔍 DEBUG: {message}")

def generate_comparison_context(anomaly_detection_mode: str, aggregation_days: int, baseline_periods: int = 7) -> str:
    """
    Generate comparison context explanation based on anomaly detection mode, aggregation days and baseline periods
    
    Args:
        anomaly_detection_mode: 'vslast', 'mean', or 'target'
        aggregation_days: Number of days per period (1, 7, 14, 30, etc.)
        baseline_periods: Number of periods to use as baseline (default: 7)
    
    Returns:
        String explaining the comparison context
    """
    if anomaly_detection_mode == 'vslast':
        if aggregation_days == 7:
            return "• **Comparación**: vs última semana (período previo de 7 días)"
        elif aggregation_days == 1:
            return "• **Comparación**: vs día anterior (período previo de 1 día)"
        else:
            return f"• **Comparación**: vs período previo ({aggregation_days} días)"
    elif anomaly_detection_mode == 'mean':
        if aggregation_days == 1:
            return f"• **Comparación**: vs media de los últimos {baseline_periods} días"
        else:
            return f"• **Comparación**: vs media de los últimos {baseline_periods} períodos ({aggregation_days} días cada uno)"
    elif anomaly_detection_mode == 'target':
        return "• **Comparación**: vs target mensual establecido"
    else:
        return f"• **Comparación**: modo '{anomaly_detection_mode}' no reconocido"

def debug_save_hierarchical_data(hierarchical_explanation: str, period: int, date_param: Optional[str] = None, 
                                causal_explanations: Optional[dict] = None, relationships: Optional[dict] = None):
    """Save hierarchical explanation data for interpreter debugging"""
    try:
        # Create debug folder
        debug_folder = Path("dashboard_analyzer/agent_conversations/interpreter_debug")
        debug_folder.mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hierarchical_data_period_{period}_{timestamp}.json"
        filepath = debug_folder / filename
        
        # Prepare debug data
        debug_data = {
            "timestamp": timestamp,
            "period": period,
            "date_param": date_param,
            "hierarchical_explanation": hierarchical_explanation,
            "causal_explanations": causal_explanations or {},
            "relationships": relationships or {},
            "metadata": {
                "total_nodes": len(causal_explanations) if causal_explanations else 0,
                "explanation_length": len(hierarchical_explanation),
                "nodes_analyzed": list(causal_explanations.keys()) if causal_explanations else []
            }
        }
        
        # Save to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
        
        print(f"🔧 DEBUG: Hierarchical data saved to {filepath}")
        
    except Exception as e:
        print(f"⚠️ DEBUG: Failed to save hierarchical data: {e}")

async def debug_run_interpreter_only(debug_file: str):
    """Run only the interpreter agent using saved hierarchical data"""
    try:
        # Load debug data
        debug_path = Path(debug_file)
        if not debug_path.exists():
            print(f"❌ Debug file not found: {debug_file}")
            return
        
        with open(debug_path, 'r', encoding='utf-8') as f:
            debug_data = json.load(f)
        
        print(f"📂 Loading debug data from {debug_file}")
        print(f"   • Period: {debug_data['period']}")
        print(f"   • Date: {debug_data['date_param']}")
        print(f"   • Nodes: {debug_data['metadata']['nodes_analyzed']}")
        print(f"   • Data length: {debug_data['metadata']['explanation_length']} chars")
        
        # Parse the hierarchical explanation to extract anomalies and deviations
        anomalies = {}
        deviations = {}
        
        # Parse the hierarchical explanation text to extract data
        hierarchical_text = debug_data['hierarchical_explanation']
        
        # Extract segments with anomalies from the text
        import re
        
        # Find all anomaly lines like "• Global: NEGATIVE ANOMALY (-7.8 points)"
        anomaly_pattern = r'• ([^:]+): (POSITIVE|NEGATIVE) ANOMALY \(([+-]?\d+\.?\d*) points\)'
        matches = re.findall(anomaly_pattern, hierarchical_text)
        
        for node_path, anomaly_type, deviation_str in matches:
            state = "+" if anomaly_type == "POSITIVE" else "-"
            anomalies[node_path] = state
            deviations[node_path] = float(deviation_str)
        
        # Also extract normal variations from the detailed hierarchy section
        lines = hierarchical_text.split('\n')
        for line in lines:
            line = line.strip()
            # Match patterns like "Global: NEGATIVE ANOMALY (-7.8 pts)" or "YW: Normal (-4.7 pts - within normal range)"
            if ':' in line and ('ANOMALY' in line or 'Normal' in line):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    node_name = parts[0].strip()
                    description = parts[1].strip()
                    
                    # Extract deviation value
                    dev_match = re.search(r'\(([+-]?\d+\.?\d*) pts', description)
                    if dev_match:
                        deviation_val = float(dev_match.group(1))
                        
                        if 'POSITIVE ANOMALY' in description:
                            anomalies[node_name] = "+"
                            deviations[node_name] = deviation_val
                        elif 'NEGATIVE ANOMALY' in description:
                            anomalies[node_name] = "-"
                            deviations[node_name] = deviation_val
                        elif 'Normal' in description:
                            anomalies[node_name] = "N"
                            deviations[node_name] = deviation_val
        
        # Generate interpretations from the detailed hierarchy section
        interpretations = {}
        lines = hierarchical_text.split('\n')
        current_node = None
        
        for line in lines:
            line = line.strip()
            # Look for pattern lines like "└─ Pattern: ..."
            if '└─ Pattern:' in line:
                pattern = line.replace('└─ Pattern:', '').strip()
                if current_node:
                    interpretations[current_node] = pattern
            # Track current node context
            elif ':' in line and ('ANOMALY' in line or 'Normal' in line):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    current_node = parts[0].strip()
        
        # Use the causal explanations from the JSON
        explanations = debug_data.get('causal_explanations', {})
        
        # Calculate date range (approximate from the date_param)
        from datetime import datetime, timedelta
        try:
            analysis_date = datetime.strptime(debug_data['date_param'], '%Y-%m-%d')
            period = debug_data['period']
            # Approximate date range calculation
            start_date = analysis_date - timedelta(days=7*(period-1))
            end_date = start_date + timedelta(days=6)
            date_range = (start_date, end_date)
        except:
            # Default date range if parsing fails
            today = datetime.now()
            date_range = (today, today)
        
        # Build the proper hierarchical input using build_ai_input_string
        hierarchical_input = build_ai_input_string(
            period=debug_data['period'],
            anomalies=anomalies,
            deviations=deviations,
            interpretations=interpretations,
            explanations=explanations,
            date_range=date_range,
            segment_filter="Global"
        )
        
        print(f"\n🔧 RECONSTRUCTED HIERARCHICAL INPUT:")
        print("-" * 60)
        print(hierarchical_input[:500] + "..." if len(hierarchical_input) > 500 else hierarchical_input)
        print("-" * 60)
        
        # Initialize interpreter agent
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_interpreter_agent import AnomalyInterpreterAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        
        ai_agent = AnomalyInterpreterAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml",
            logger=logging.getLogger("debug_interpreter"),
            study_mode="comparative"
        )
        
        print("\n🤖 Running hierarchical interpretation...")
        print("="*80)
        
        # Run the hierarchical interpretation with the properly formatted input
        ai_interpretation = await asyncio.wait_for(
            ai_agent.interpret_anomaly_tree_hierarchical(
                hierarchical_input, 
                debug_data['date_param']
            ),
                            timeout=600.0  # 10 minutes for O3 with large prompts
        )
        
        print(ai_interpretation)
        print("="*80)
        
        print(f"\n✅ Interpreter debugging complete!")
        
    except Exception as e:
        print(f"❌ Debug interpreter failed: {e}")
        import traceback
        traceback.print_exc()

async def collect_flexible_data(aggregation_days: int, target_folder: str, segment: str = "Global", analysis_date: datetime = None):
    """
    Collect flexible NPS data for all nodes in the specified segment
    
    Args:
        aggregation_days: Number of days per period
        target_folder: Where to save the data
        segment: Root segment to collect (Global, SH, LH, etc.)
        analysis_date: Optional analysis date to use instead of TODAY() in queries
    """
    print(f"📥 Collecting flexible NPS data")
    print(f"   🔧 Aggregation: {aggregation_days} days per period")
    print(f"   📁 Target folder: {target_folder}")
    print(f"   🎯 Segment: {segment}")
    if analysis_date:
        print(f"   📅 Analysis date: {analysis_date.strftime('%Y-%m-%d')}")
    
    collector = PBIDataCollector()
    node_paths = get_segment_node_paths(segment)
    
    total_attempted = 0
    total_success = 0
    
    for node_path in node_paths:
        try:
            debug_print(f"Collecting data for node: {node_path}")
            results = await collector.collect_flexible_data_for_node(
                node_path, aggregation_days, target_folder, analysis_date
            )
            total_attempted += len(results)
            total_success += sum(results.values())
            debug_print(f"Node {node_path}: {sum(results.values())}/{len(results)} files successful")
        except Exception as e:
            print(f"❌ Error collecting data for {node_path}: {e}")
            debug_print(f"Error details for {node_path}: {type(e).__name__}: {str(e)}")
    
    print(f"\n📊 Flexible Data Collection Summary:")
    print(f"   Total files attempted: {total_attempted}")
    print(f"   Successful files: {total_success}")
    if total_attempted > 0:
        print(f"   Success rate: {total_success/total_attempted*100:.1f}%")
    else:
        print(f"   Success rate: 0.0% (no files attempted)")
    
    if total_success > 0:
        print(f"✅ Flexible data collection completed: {total_success}/{total_attempted} successful")
        return True
    else:
        print("❌ No data collected successfully")
        return False

async def generate_explanations(analysis_data: dict, causal_filter: str = "vs L7d"):
    """Generate comprehensive explanations for nodes with anomalies"""
    if not analysis_data:
        return
    
    print(f"\n📝 STEP 3: Comprehensive Anomaly Explanations")
    print("-" * 60)
    
    detector = analysis_data['detector']
    data_folder = analysis_data['data_folder']
    anomaly_periods = analysis_data['anomaly_periods']
    aggregation_days = analysis_data['aggregation_days']
    
    # Initialize PBI collector and interpreter with full capabilities
    print("🔧 Initializing data collectors...")
    pbi_collector = PBIDataCollector()
    interpreter = FlexibleAnomalyInterpreter(data_folder, pbi_collector=pbi_collector, causal_filter=causal_filter)
    
    explanation_count = 0
    total_nodes_analyzed = 0
    
    for period in anomaly_periods[:4]:  # Analyze up to 4 periods with anomalies
        print(f"\n{'='*50}")
        print(f"🔍 PERIOD {period} EXPLANATIONS")
        print("="*50)
        
        # Get anomalies for this period
        period_anomalies, period_deviations, _, _ = await detector.analyze_period(data_folder, period, analysis_data.get('analysis_date'))
        
        # Find nodes with anomalies
        nodes_needing_explanation = [
            node for node, state in period_anomalies.items() 
            if state in ['+', '-']
        ]
        
        if not nodes_needing_explanation:
            print(f"   ✅ No anomalies found in period {period}")
            continue
        
        # Get date range for this period
        date_range = interpreter._get_period_date_range(period, aggregation_days)
        if date_range:
            start_date, end_date = date_range
            print(f"📅 Period {period} Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        else:
            print(f"⚠️ Could not determine date range for period {period}")
        
        print(f"🎯 Found {len(nodes_needing_explanation)} anomalies to explain:")
        
        # Generate explanations for each anomalous node
        for i, node_path in enumerate(nodes_needing_explanation, 1):  # Process ALL anomalous nodes
            total_nodes_analyzed += 1
            try:
                print(f"\n   {i}. 📊 Analyzing {node_path}")
                print(f"      {'─' * 40}")
                
                # Get the anomaly details
                deviation = period_deviations.get(node_path, 0)
                state = period_anomalies.get(node_path, "?")
                state_desc = "📈 Higher than expected" if state == "+" else "📉 Lower than expected"
                state_icon = "🔺" if state == "+" else "🔻"
                
                print(f"      {state_icon} Status: {state_desc} ({deviation:+.1f} points)")
                
                # Generate comprehensive explanation with timeout
                print(f"      🔍 Collecting explanatory data...")
                explanation = await asyncio.wait_for(
                    interpreter.explain_anomaly(
                        node_path=node_path,
                        target_period=period,
                        aggregation_days=aggregation_days,
                        anomaly_state=state,
                        causal_filter=causal_filter
                    ),
                    timeout=600.0  # 10 minute timeout for comprehensive analysis
                )
                
                # Display the explanation in a structured way
                print(f"      💡 EXPLANATION:")
                explanation_lines = explanation.split(" | ")
                for line in explanation_lines:
                    if line.strip():
                        print(f"         • {line.strip()}")
                
                explanation_count += 1
                
            except asyncio.TimeoutError:
                print(f"      ⏰ Timeout generating explanation for {node_path} (>60s)")
                print(f"         This node requires manual investigation")
            except Exception as e:
                print(f"      ❌ Error generating explanation for {node_path}: {str(e)}")
                print(f"         Check data availability and node path validity")
    
    # Final explanation summary
    print(f"\n{'='*60}")
    print(f"📋 EXPLANATION SUMMARY")
    print("="*60)
    print(f"   📊 Total anomalous nodes analyzed: {total_nodes_analyzed}")
    print(f"   ✅ Successful explanations generated: {explanation_count}")
    if total_nodes_analyzed > 0:
        success_rate = (explanation_count / total_nodes_analyzed) * 100
        print(f"   📈 Success rate: {success_rate:.1f}%")
    
    if explanation_count == 0:
        print(f"   ⚠️ No explanations could be generated")
        print(f"   💡 Possible issues:")
        print(f"      • Missing operational data files")
        print(f"      • PBI connection issues for verbatims")
        print(f"      • Invalid date ranges")
    else:
        print(f"   🎉 Explanations successfully generated!")
        print(f"   💡 Each explanation includes:")
        print(f"      • 🔧 Operational metrics analysis")
        print(f"      • 💬 Customer verbatims sentiment")
        print(f"      • 📅 Date-filtered data for specific periods")

async def show_all_anomaly_periods_with_explanations(analysis_data: dict, segment: str = "Global", explanation_mode: str = "agent", causal_filter: str = "vs L7d"):
    """Show trees for all periods analyzed INCLUDING explanations and parent interpretations"""
    if not analysis_data:
        return
    
    print(f"\n🌳 ANOMALY PERIOD ANALYSIS")
    print("-" * 50)
    
    detector = analysis_data['detector']
    data_folder = analysis_data['data_folder']
    aggregation_days = analysis_data['aggregation_days']
    anomaly_periods = analysis_data['anomaly_periods']
    periods_analyzed = analysis_data.get('periods_analyzed', anomaly_periods)
    
    # Initialize interpreter for explanations with specified mode
    pbi_collector = PBIDataCollector()
    interpreter = FlexibleAnomalyInterpreter(data_folder, pbi_collector=pbi_collector, explanation_mode=explanation_mode, causal_filter=causal_filter)
    print(f"🔧 Explanation mode: {explanation_mode.upper()}")
    
    # Initialize AI agent for interpretation
    try:
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_interpreter_agent import AnomalyInterpreterAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType, get_default_llm_type
        
        ai_agent = AnomalyInterpreterAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml",
            logger=logging.getLogger("ai_interpreter"),
            study_mode="comparative"
        )
        ai_available = True
        print("🤖 AI Agent initialized for interpretations")
    except Exception as e:
        print(f"⚠️ AI Agent not available: {str(e)}")
        ai_available = False
    
    # Initialize Summary Agent for final report
    try:
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_summary_agent import AnomalySummaryAgent
        
        summary_agent = AnomalySummaryAgent(
            llm_type=get_default_llm_type(),
            logger=logging.getLogger("summary_agent")
        )
        summary_available = True
        print("📋 Summary Agent initialized for executive report")
    except Exception as e:
        print(f"⚠️ Summary Agent not available: {str(e)}")
        summary_available = False
    
    # Collect data for all periods for summary
    all_periods_data = []
    
    # Show all periods with anomalies (remove the [:3] limit)
    periods_with_anomalies = [p for p in periods_analyzed if p in anomaly_periods]
    
    # Show detailed analysis for all periods with anomalies
    for period in periods_with_anomalies:
        print(f"\n{'='*60}")
        print(f"PERIOD {period} ANALYSIS")
        print("="*60)
        
        # Get anomalies for this period (silently)
        print(f"🔍 DEBUG ANALYZE_PERIOD: About to call detector.analyze_period", file=sys.stderr)
        analyze_result = await detector.analyze_period(data_folder, period, analysis_data.get('analysis_date'))
        print(f"🔍 DEBUG ANALYZE_PERIOD: Result type: {type(analyze_result)}", file=sys.stderr)
        print(f"🔍 DEBUG ANALYZE_PERIOD: Result length: {len(analyze_result) if hasattr(analyze_result, '__len__') else 'No length'}", file=sys.stderr)
        
        period_anomalies, period_deviations, _, period_nps_values = analyze_result
        print(f"🔍 DEBUG ANALYZE_PERIOD: period_nps_values type: {type(period_nps_values)}", file=sys.stderr)
        print(f"🔍 DEBUG ANALYZE_PERIOD: period_nps_values content: {period_nps_values}", file=sys.stderr)
        
        # DEBUG: Check if NPS values are available
        print(f"🔍 DEBUG: NPS values available: {list(period_nps_values.keys()) if period_nps_values else 'None'}")
        if period_nps_values:
            for node, nps_data in list(period_nps_values.items())[:3]:  # Show first 3
                print(f"   {node}: {nps_data}")
        
        # Get date range for this period
        date_range = interpreter._get_period_date_range(period, aggregation_days)
        if date_range:
            start_date, end_date = date_range
            print(f"📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        else:
            date_range_str = "Unknown dates"
        
        # Generate parent interpretations
        parent_interpretations = generate_parent_interpretations(period_anomalies)
        
        # Collect explanations for anomalous nodes (quietly, no verbose output)
        explanations = {}
        nodes_with_anomalies = [node for node, state in period_anomalies.items() if state in ['+', '-']]

        # ENHANCEMENT: Always include Global segment in causal analysis if it has valid data
        if nodes_with_anomalies:
            # Check if Global has valid data (not "?" or missing)
            global_state = period_anomalies.get("Global", "?")
            print(f"🔍 DEBUG GLOBAL STATE: global_state='{global_state}', period_anomalies keys: {list(period_anomalies.keys())}")
            
            # Always recalculate Global's anomaly state based on deviation (override detector's decision)
            global_deviation = period_deviations.get("Global", 0.0)
            print(f"🔍 DEBUG GLOBAL CALCULATION: global_deviation={global_deviation}")
            if global_deviation > 0:
                global_state = "+"  # Positive anomaly
            elif global_deviation < 0:
                global_state = "-"  # Negative anomaly
            else:
                global_state = "N"  # Neutral (only when deviation is exactly 0)
            # Always update Global in period_anomalies with calculated state
            period_anomalies["Global"] = global_state
            print(f"      🔍 DEBUG GLOBAL: Override Global state='{global_state}' based on deviation={global_deviation}")
            
            if "Global" not in nodes_with_anomalies:
                # Always add Global to the analysis (it's always analyzed)
                nodes_with_anomalies.append("Global")
                print(f"      🔍 ENHANCED: Analyzing {len(nodes_with_anomalies)} segments (added Global with state '{global_state}' + {len([n for n in nodes_with_anomalies if n != 'Global'])} anomalous nodes)")
            elif "Global" in nodes_with_anomalies:
                print(f"      📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (including Global)")
            else:
                print(f"      📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (Global has no valid data)")
            
            # PRIORITY: Move Global to the front to ensure it's always processed first
            if "Global" in nodes_with_anomalies:
                nodes_with_anomalies.remove("Global")
                nodes_with_anomalies.insert(0, "Global")
                print(f"      🎯 PRIORITY: Global moved to front of processing queue")

        if nodes_with_anomalies:
            # Collect explanations for anomalous nodes
            total_nodes = len(nodes_with_anomalies)
            successful_explanations = 0

            print(f"      📊 Processing {total_nodes} anomalous nodes for causal explanations...")
            
            for i, node_path in enumerate(nodes_with_anomalies, 1):
                try:
                    anomaly_state = period_anomalies.get(node_path, "?")
                    deviation_value = period_deviations.get(node_path, 0.0)  # Get actual deviation
                    print(f"🔍 DEBUG GLOBAL ANOMALY: node_path='{node_path}', period_anomalies.get()='{anomaly_state}', deviation_value={deviation_value}")
                    print(f"🔍 DEBUG GLOBAL ANOMALY: period_anomalies keys: {list(period_anomalies.keys())}")
                    print(f"🔍 DEBUG GLOBAL ANOMALY: period_anomalies values: {list(period_anomalies.values())}")
                    
                    # For Global node, determine anomaly state based on sign of change (using same nomenclature as other nodes)
                    if node_path == "Global" and anomaly_state == "?":
                        if deviation_value > 0:
                            anomaly_state = "+"  # Positive anomaly
                        elif deviation_value < 0:
                            anomaly_state = "-"  # Negative anomaly
                        else:
                            anomaly_state = "N"  # Neutral
                    
                    print(f"      🔍 [{i}/{total_nodes}] Collecting explanation for {node_path} (state: {anomaly_state}, deviation: {deviation_value:+.1f})")
                    
                    # Calculate correct date range if analysis_date is available
                    start_date, end_date = None, None
                    analysis_date = analysis_data.get('analysis_date')
                    if analysis_date:
                        print(f"🔍 DEBUG DATE FLOW: analysis_date={analysis_date}, period={period}, aggregation_days={aggregation_days}")
                        start_date, end_date = calculate_period_date_range(analysis_date, period, aggregation_days)
                        print(f"🔍 DEBUG DATE FLOW: calculate_period_date_range returned: start_date={start_date}, end_date={end_date}")
                        print(f"         📅 Using calculated date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                    
                    # Build enriched NPS context for the causal agent
                    nps_context = ""
                    comparison_context = ""
                    print(f"🔍 DEBUG NPS CONTEXT BUILD: period_nps_values keys: {list(period_nps_values.keys()) if period_nps_values else 'None'}", file=sys.stderr)
                    print(f"🔍 DEBUG NPS CONTEXT BUILD: Looking for node_path: {node_path}", file=sys.stderr)
                    print(f"🔍 DEBUG NPS CONTEXT BUILD: Node in period_nps_values: {node_path in period_nps_values if period_nps_values else False}", file=sys.stderr)
                    if period_nps_values and node_path in period_nps_values:
                        nps_data = period_nps_values[node_path]
                        print(f"🔍 DEBUG Causal agent NPS for {node_path}: {nps_data}", file=sys.stderr)
                        if isinstance(nps_data, dict):
                            current_nps = nps_data.get('current', 'N/A')
                            baseline_nps = nps_data.get('baseline', 'N/A')
                            nps_context = f"Current NPS: {current_nps}, Baseline NPS: {baseline_nps}"
                            
                            # Generate comparison context
                            comparison_context = generate_comparison_context(
                                analysis_data.get('anomaly_detection_mode', 'target'), 
                                analysis_data.get('aggregation_days', 7),
                                analysis_data.get('baseline_periods', 7)
                            )
                        else:
                            nps_context = f"NPS: {nps_data}"
                    else:
                        print(f"🔍 DEBUG Causal agent NO NPS for {node_path}", file=sys.stderr)
                    
                    explanation = await asyncio.wait_for(
                        interpreter.explain_anomaly(
                            node_path=node_path,
                            target_period=period,
                            aggregation_days=aggregation_days,
                            anomaly_state=anomaly_state,
                            start_date=start_date,
                            end_date=end_date,
                            anomaly_magnitude=deviation_value,  # ✅ Now passing actual deviation
                            nps_context=nps_context,  # ✅ Now passing NPS context
                            causal_filter=causal_filter,
                            # New parameters for enriched context
                            anomaly_detection_mode=analysis_data.get('anomaly_detection_mode', 'target'),
                            comparison_context=comparison_context,
                            baseline_periods=analysis_data.get('baseline_periods', 7)
                        ),
                        timeout=600.0
                    )
                    explanations[node_path] = explanation
                    successful_explanations += 1
                    print(f"         ✅ [{i}/{total_nodes}] Explanation collected: {len(explanation)} chars")
                except Exception as e:
                    error_details = f"Type: {type(e).__name__}, Message: '{str(e)}', Args: {e.args}"
                    print(f"         ❌ [{i}/{total_nodes}] Explanation failed: {error_details}")
                    # Also try to get traceback
                    import traceback
                    traceback_str = traceback.format_exc()
                    print(f"         🔍 Full traceback: {traceback_str}")
                    explanations[node_path] = f"Analysis failed: {error_details}"
            
            print(f"      📋 Summary: {successful_explanations}/{total_nodes} explanations collected successfully")
        
        # Debug: Print collected explanations
        debug_print(f"📊 Collected {len(explanations)} explanations:")
        for node_path, explanation in explanations.items():
            debug_print(f"  {node_path}: {explanation[:200] if explanation else 'None'}...")
        
        # Show the enhanced tree with explanations and parent interpretations
        analysis_date = analysis_data.get('analysis_date')
        date_parameter = analysis_data.get('date_parameter')
        await print_enhanced_tree_with_explanations_and_interpretations(
            period_anomalies, period_deviations, explanations, parent_interpretations,
            aggregation_days, period, date_range, segment, analysis_date, date_parameter, period_nps_values
        )
        
        # AI Interpretation (ensure it completes)
        ai_interpretation = None
        if ai_available and nodes_with_anomalies:
            print(f"\n🤖 AI INTERPRETATION:")
            print("-" * 40)
            
            try:
                # Check if we have causal agent explanations that should go directly to interpreter
                causal_explanations = {}
                for node_path, explanation in explanations.items():
                    if explanation and ("🤖 **AGENT CAUSAL ANALYSIS**" in explanation or "AI Causal Investigation:" in explanation):
                        # This is a full causal agent explanation - pass it directly
                        if "🤖 **AGENT CAUSAL ANALYSIS**" in explanation:
                            clean_explanation = explanation.replace("🤖 **AGENT CAUSAL ANALYSIS**\n", "").strip()
                        else:
                            clean_explanation = explanation.replace("• AI Causal Investigation:", "").strip()
                        causal_explanations[node_path] = clean_explanation
                
                if causal_explanations:
                    # Use direct causal agent explanation instead of tree format
                    print("🔍 Using direct causal agent explanation for tree interpretation")
                    
                    # For single node with causal explanation, pass it directly
                    if len(causal_explanations) == 1:
                        node_path, causal_explanation = next(iter(causal_explanations.items()))
                        
                        ai_interpretation = await asyncio.wait_for(
                            ai_agent.interpret_anomaly_tree(causal_explanation, 
                                                           start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                            timeout=600.0
                        )
                    else:
                        # Multiple causal explanations - combine them
                        combined_explanation = f"Multiple anomalous nodes analyzed:\n\n"
                        for node_path, explanation in causal_explanations.items():
                            combined_explanation += f"NODO: {node_path}\n{explanation}\n\n"
                        
                        ai_interpretation = await asyncio.wait_for(
                            ai_agent.interpret_anomaly_tree(combined_explanation, 
                                                           start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                            timeout=600.0
                        )
                else:
                    # Fallback to tree format for non-causal explanations
                    ai_input = build_ai_input_string(period, period_anomalies, period_deviations, 
                                                     parent_interpretations, explanations, date_range, segment, period_nps_values)
                    
                    print(f"🔍 Using tree format: {len(ai_input)} characters")
                    
                    ai_interpretation = await asyncio.wait_for(
                        ai_agent.interpret_anomaly_tree(ai_input, 
                                                       start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                        timeout=600.0
                    )
                
                print(ai_interpretation)
                
            except Exception as e:
                ai_interpretation = f"AI interpretation failed: {str(e)}"
                print(ai_interpretation)
        
        # Collect period data for summary
        if summary_available:
            period_data = {
                'period': period,
                'date_range': date_range_str,
                'ai_interpretation': ai_interpretation or "No AI interpretation available"
            }
            all_periods_data.append(period_data)
    
    # Summary of all 7 periods
    print(f"\n📋 SUMMARY OF 7 PERIODS ANALYZED:")
    print("-" * 40)
    for period in periods_analyzed:
        period_anomalies, period_deviations, _, _ = await detector.analyze_period(data_folder, period, analysis_data.get('analysis_date'))
        anomaly_count = sum(1 for state in period_anomalies.values() if state in ['+', '-'])
        
        if period in anomaly_periods:
            status = f"🚨 {anomaly_count} anomalies"
        else:
            status = "✅ Normal"
        
        date_range = interpreter._get_period_date_range(period, aggregation_days)
        if date_range:
            start_date, end_date = date_range
            date_str = f"({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
        else:
            date_str = ""
        
        print(f"  Period {period}: {status} {date_str}")
    
    print(f"\n🎯 Total periods with anomalies: {len(anomaly_periods)}/7")
    
    # Generate Executive Summary Report (COMMENTED OUT - Using Interpreter Agent Final Summary Instead)
    # if summary_available and all_periods_data:
    #     print(f"\n" + "="*80)
    #     print(f"📋 EXECUTIVE SUMMARY REPORT")
    #     print("="*80)
    #     
    #     try:
    #         print("🤖 Generating comprehensive summary across all periods...")
    #         summary_report = await asyncio.wait_for(
    #             summary_agent.generate_summary_report(all_periods_data),
    #             timeout=60.0
    #         )
    #         
    #         print(f"\n{summary_report}")
    #         
    #         # Performance metrics
    #         metrics = summary_agent.get_performance_metrics()
    #         print(f"\n📊 Summary Generation Metrics:")
    #         print(f"   • Input tokens: {metrics.get('input_tokens', 0)}")
    #         print(f"   • Output tokens: {metrics.get('output_tokens', 0)}")
    #         print(f"   • LLM: {metrics.get('llm_type', 'Unknown')}")
    #         
    #     except Exception as e:
    #         print(f"❌ Executive summary generation failed: {str(e)}")
    #         print(f"   Manual review recommended for the {len(all_periods_data)} periods with anomalies")
    #     
    #     print("="*80)
    # 
    # elif summary_available and not all_periods_data:
    #     print(f"\n📋 EXECUTIVE SUMMARY:")
    #     print("No anomalies detected in any of the 7 periods analyzed.")
    #     print("All segments are operating within normal NPS variation ranges.")
    
    if not summary_available:
        print(f"\n⚠️ Executive summary not available (Summary Agent initialization failed)")
        print(f"   Individual period analyses completed for {len(periods_with_anomalies)} periods with anomalies")

def generate_parent_interpretations(anomalies: dict) -> dict:
    """Generate parent node interpretations based on children states"""
    interpretations = {}
    
    # Helper function to format child lists
    def format_children(children_list):
        if len(children_list) == 0:
            return "none"
        elif len(children_list) == 1:
            return children_list[0]
        elif len(children_list) == 2:
            return f"{children_list[0]}, {children_list[1]}"
        else:
            return ", ".join(children_list[:-1]) + f", {children_list[-1]}"
    
    # NOTE: IB/YW are leaf nodes - they don't get patterns since they have no children
    
    # Global interpretation (has LH, SH children)
    lh_state = anomalies.get("Global/LH", "?")
    sh_state = anomalies.get("Global/SH", "?")
    global_state = anomalies.get("Global", "?")
    
    if lh_state != "?" and sh_state != "?":
        if global_state == "N":
            # Normal parent
            if lh_state == "N" and sh_state == "N":
                interpretations["Global"] = "All children normal (LH, SH)"
            elif lh_state in ["+", "-"] and sh_state == "N":
                interpretations["Global"] = f"{lh_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (LH) diluted by normal nodes (SH)"
            elif sh_state in ["+", "-"] and lh_state == "N":
                interpretations["Global"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (SH) diluted by normal nodes (LH)"
            elif lh_state in ["+", "-"] and sh_state in ["+", "-"]:
                if lh_state != sh_state:
                    interpretations["Global"] = "LH and SH anomalies cancel each other out"
                else:
                    interpretations["Global"] = f"{lh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (LH, SH)"
        elif global_state in ["+", "-"]:
            # Anomalous parent
            if lh_state == "N" and sh_state == "N":
                interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite all children being normal (LH, SH)"
            elif lh_state in ["+", "-"] and sh_state == "N":
                if lh_state == global_state:
                    interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {lh_state.replace('+', 'positive').replace('-', 'negative')} LH, SH normal"
                else:
                    interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {lh_state.replace('+', 'positive').replace('-', 'negative')} LH offsetting SH normal"
            elif sh_state in ["+", "-"] and lh_state == "N":
                if sh_state == global_state:
                    interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {sh_state.replace('+', 'positive').replace('-', 'negative')} SH, LH normal"
                else:
                    interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {sh_state.replace('+', 'positive').replace('-', 'negative')} SH offsetting LH normal"
            elif lh_state in ["+", "-"] and sh_state in ["+", "-"]:
                if lh_state == sh_state == global_state:
                    interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (LH, SH)"
                else:
                    interpretations["Global"] = f"{global_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly from mixed LH ({lh_state}) and SH ({sh_state}) effects"

    # LH interpretation (has Economy, Business, Premium children)
    lh_children = ["Economy", "Business", "Premium"]
    lh_child_states = [anomalies.get(f"Global/LH/{child}", "?") for child in lh_children]
    valid_lh_children = [(child, state) for child, state in zip(lh_children, lh_child_states) if state != "?"]
    
    if valid_lh_children:
        normal_children = [child for child, state in valid_lh_children if state == "N"]
        positive_children = [child for child, state in valid_lh_children if state == "+"]
        negative_children = [child for child, state in valid_lh_children if state == "-"]
        
        if lh_state == "N":
            # Normal parent
            if len(positive_children) == 0 and len(negative_children) == 0:
                interpretations["Global/LH"] = f"All children normal ({format_children([c for c, _ in valid_lh_children])})"
            elif len(positive_children) > 0 and len(negative_children) > 0:
                interpretations["Global/LH"] = f"Mixed anomalies: positive ({format_children(positive_children)}), negative ({format_children(negative_children)}) balance out with normal ({format_children(normal_children)})"
            elif len(positive_children) > 0:
                interpretations["Global/LH"] = f"Positive nodes ({format_children(positive_children)}) diluted by normal nodes ({format_children(normal_children)})"
            elif len(negative_children) > 0:
                interpretations["Global/LH"] = f"Negative nodes ({format_children(negative_children)}) diluted by normal nodes ({format_children(normal_children)})"
        elif lh_state in ["+", "-"]:
            # Anomalous parent
            contributing_children = positive_children if lh_state == "+" else negative_children
            if contributing_children:
                interpretations["Global/LH"] = f"{lh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {lh_state.replace('+', 'positive').replace('-', 'negative')} {format_children(contributing_children)}"
            else:
                interpretations["Global/LH"] = f"{lh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite all children having different states"

    # SH interpretation (has Economy, Business children)
    economy_state = anomalies.get("Global/SH/Economy", "?")
    business_state = anomalies.get("Global/SH/Business", "?")
    sh_state = anomalies.get("Global/SH", "?")
    
    if economy_state != "?" and business_state != "?":
        if sh_state == "N":
            # Normal parent
            if economy_state == "N" and business_state == "N":
                interpretations["Global/SH"] = "All children normal (Economy, Business)"
            elif economy_state in ["+", "-"] and business_state == "N":
                interpretations["Global/SH"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (Economy) diluted by normal nodes (Business)"
            elif business_state in ["+", "-"] and economy_state == "N":
                interpretations["Global/SH"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (Business) diluted by normal nodes (Economy)"
            elif economy_state in ["+", "-"] and business_state in ["+", "-"]:
                if economy_state != business_state:
                    interpretations["Global/SH"] = "Economy and Business anomalies cancel each other out"
                else:
                    interpretations["Global/SH"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (Economy, Business)"
        elif sh_state in ["+", "-"]:
            # Anomalous parent
            if economy_state == "N" and business_state == "N":
                interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite all children being normal (Economy, Business)"
            elif economy_state in ["+", "-"] and business_state == "N":
                if economy_state == sh_state:
                    interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {economy_state.replace('+', 'positive').replace('-', 'negative')} Economy, Business normal"
                else:
                    interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {economy_state.replace('+', 'positive').replace('-', 'negative')} Economy offsetting Business normal"
            elif business_state in ["+", "-"] and economy_state == "N":
                if business_state == sh_state:
                    interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {business_state.replace('+', 'positive').replace('-', 'negative')} Business, Economy normal"
                else:
                    interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {business_state.replace('+', 'positive').replace('-', 'negative')} Business offsetting Economy normal"
            elif economy_state in ["+", "-"] and business_state in ["+", "-"]:
                if economy_state == business_state == sh_state:
                    interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (Economy, Business)"
                else:
                    interpretations["Global/SH"] = f"{sh_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly from mixed Economy ({economy_state}) and Business ({business_state}) effects"

    # SH/Economy interpretation (has IB, YW children)
    ib_eco_state = anomalies.get("Global/SH/Economy/IB", "?")
    yw_eco_state = anomalies.get("Global/SH/Economy/YW", "?")
    
    if ib_eco_state != "?" and yw_eco_state != "?":
        if economy_state == "N":
            # Normal parent
            if ib_eco_state == "N" and yw_eco_state == "N":
                interpretations["Global/SH/Economy"] = "All children normal (IB, YW)"
            elif ib_eco_state in ["+", "-"] and yw_eco_state == "N":
                interpretations["Global/SH/Economy"] = f"{ib_eco_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (IB) diluted by normal nodes (YW)"
            elif yw_eco_state in ["+", "-"] and ib_eco_state == "N":
                interpretations["Global/SH/Economy"] = f"{yw_eco_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (YW) diluted by normal nodes (IB)"
            elif ib_eco_state in ["+", "-"] and yw_eco_state in ["+", "-"]:
                if ib_eco_state != yw_eco_state:
                    interpretations["Global/SH/Economy"] = "IB and YW anomalies cancel each other out"
                else:
                    interpretations["Global/SH/Economy"] = f"{ib_eco_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)"
        elif economy_state in ["+", "-"]:
            # Anomalous parent
            if ib_eco_state == "N" and yw_eco_state == "N":
                interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite all children being normal (IB, YW)"
            elif ib_eco_state in ["+", "-"] and yw_eco_state == "N":
                if ib_eco_state == economy_state:
                    interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {ib_eco_state.replace('+', 'positive').replace('-', 'negative')} IB, YW normal"
                else:
                    interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {ib_eco_state.replace('+', 'positive').replace('-', 'negative')} IB offsetting YW normal"
            elif yw_eco_state in ["+", "-"] and ib_eco_state == "N":
                if yw_eco_state == economy_state:
                    interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {yw_eco_state.replace('+', 'positive').replace('-', 'negative')} YW, IB normal"
                else:
                    interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {yw_eco_state.replace('+', 'positive').replace('-', 'negative')} YW offsetting IB normal"
            elif ib_eco_state in ["+", "-"] and yw_eco_state in ["+", "-"]:
                if ib_eco_state == yw_eco_state == economy_state:
                    interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)"
                else:
                    interpretations["Global/SH/Economy"] = f"{economy_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly: mixed IB ({ib_eco_state}) and YW ({yw_eco_state}) effects"

    # SH/Business interpretation (has IB, YW children)
    ib_bus_state = anomalies.get("Global/SH/Business/IB", "?")
    yw_bus_state = anomalies.get("Global/SH/Business/YW", "?")
    
    if ib_bus_state != "?" and yw_bus_state != "?":
        if business_state == "N":
            # Normal parent
            if ib_bus_state == "N" and yw_bus_state == "N":
                interpretations["Global/SH/Business"] = "All children normal (IB, YW)"
            elif ib_bus_state in ["+", "-"] and yw_bus_state == "N":
                interpretations["Global/SH/Business"] = f"{ib_bus_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (IB) diluted by normal nodes (YW)"
            elif yw_bus_state in ["+", "-"] and ib_bus_state == "N":
                interpretations["Global/SH/Business"] = f"{yw_bus_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (YW) diluted by normal nodes (IB)"
            elif ib_bus_state in ["+", "-"] and yw_bus_state in ["+", "-"]:
                if ib_bus_state != yw_bus_state:
                    interpretations["Global/SH/Business"] = "IB and YW anomalies cancel each other out"
                else:
                    interpretations["Global/SH/Business"] = f"{ib_bus_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)"
        elif business_state in ["+", "-"]:
            # Anomalous parent
            if ib_bus_state == "N" and yw_bus_state == "N":
                interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite all children being normal (IB, YW)"
            elif ib_bus_state in ["+", "-"] and yw_bus_state == "N":
                if ib_bus_state == business_state:
                    interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {ib_bus_state.replace('+', 'positive').replace('-', 'negative')} IB, YW normal"
                else:
                    interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {ib_bus_state.replace('+', 'positive').replace('-', 'negative')} IB offsetting YW normal"
            elif yw_bus_state in ["+", "-"] and ib_bus_state == "N":
                if yw_bus_state == business_state:
                    interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly driven by {yw_bus_state.replace('+', 'positive').replace('-', 'negative')} YW, IB normal"
                else:
                    interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly despite {yw_bus_state.replace('+', 'positive').replace('-', 'negative')} YW offsetting IB normal"
            elif ib_bus_state in ["+", "-"] and yw_bus_state in ["+", "-"]:
                if ib_bus_state == yw_bus_state == business_state:
                    interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)"
                else:
                    # Complex mixed case - check which child contributes more to the parent anomaly
                    interpretations["Global/SH/Business"] = f"{business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly: mixed IB ({ib_bus_state}) and YW ({yw_bus_state}) effects"

    return interpretations

def build_ai_input_string(period: int, anomalies: dict, deviations: dict, 
                         interpretations: dict, explanations: dict, date_range: tuple, segment_filter: str = "Global", nps_values: dict = None) -> str:
    """Build comprehensive input string for AI interpretation, filtered by segment"""
    
    # Normalize segment_filter to match the same logic as get_segment_node_paths
    if segment_filter == 'SH':
        segment_filter = 'Global/SH'
    elif segment_filter == 'LH':
        segment_filter = 'Global/LH'
    elif segment_filter == 'Economy' and '/' not in segment_filter:
        segment_filter = 'Global/SH/Economy'
    elif segment_filter == 'Business' and '/' not in segment_filter:
        segment_filter = 'Global/SH/Business'
    
    # Filter data to only include relevant nodes for the selected segment
    relevant_nodes = get_segment_node_paths(segment_filter)
    filtered_anomalies = {node: state for node, state in anomalies.items() if node in relevant_nodes}
    filtered_deviations = {node: dev for node, dev in deviations.items() if node in relevant_nodes}
    filtered_nps_values = {k: v for k, v in nps_values.items() if k in relevant_nodes} if nps_values else {}
    
    # DEBUG: Show what's being filtered
    print(f"🔍 DEBUG build_ai_input_string FILTERING:", file=sys.stderr)
    print(f"   segment_filter: {segment_filter}", file=sys.stderr)
    print(f"   relevant_nodes: {relevant_nodes}", file=sys.stderr)
    print(f"   original anomalies: {list(anomalies.keys())}", file=sys.stderr)
    print(f"   filtered_anomalies: {list(filtered_anomalies.keys())}", file=sys.stderr)
    print(f"   original explanations: {list(explanations.keys())}", file=sys.stderr)
    print(f"   nps_values available: {list(filtered_nps_values.keys()) if filtered_nps_values else 'None'}", file=sys.stderr)
    if filtered_nps_values:
        print(f"   Sample NPS data: {list(filtered_nps_values.items())[:3]}", file=sys.stderr)
        # Add more detailed debug for NPS values
        for node_path, nps_data in list(filtered_nps_values.items())[:3]:
            print(f"   NPS data for {node_path}: {nps_data}", file=sys.stderr)
    
    if date_range:
        start_date, end_date = date_range
        ai_input = f"NPS ANOMALY ANALYSIS - PERIOD {period} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})\n\n"
    else:
        ai_input = f"NPS ANOMALY ANALYSIS - PERIOD {period}\n\n"
    
    # Count actual anomalies vs normal variations
    actual_anomalies = [node for node, state in filtered_anomalies.items() if state in ['+', '-']]
    normal_segments = [node for node, state in filtered_anomalies.items() if state == 'N']
    
    ai_input += f"ANOMALY SUMMARY:\n"
    ai_input += f"• Total segments analyzed: {len(filtered_anomalies)}\n"
    ai_input += f"• Actual anomalies detected: {len(actual_anomalies)}\n"
    ai_input += f"• Normal variations: {len(normal_segments)}\n\n"
    
    if actual_anomalies:
        ai_input += f"SEGMENTS WITH ACTUAL ANOMALIES:\n"
        for node_path in actual_anomalies:
            state = filtered_anomalies[node_path]
            deviation = filtered_deviations.get(node_path, 0)
            anomaly_type = "POSITIVE" if state == "+" else "NEGATIVE"
            ai_input += f"• {node_path}: {anomaly_type} ANOMALY ({deviation:+.1f} points)\n"
        ai_input += "\n"
    
    ai_input += "DETAILED HIERARCHY:\n\n"
    
    # Helper function to get state description
    def get_state_desc(state, deviation):
        if state == "+":
            return f"POSITIVE ANOMALY ({deviation:+.1f} pts)"
        elif state == "-":
            return f"NEGATIVE ANOMALY ({deviation:+.1f} pts)"
        elif state == "N":
            if abs(deviation) < 10:
                return f"Normal ({deviation:+.1f} pts - within normal range)"
            else:
                return f"Normal ({deviation:+.1f} pts)"
        else:
            return f"State: {state}"
    
    # Build hierarchical structure with interpretations - filtered by segment
    def add_node_info(node_path: str, name: str, indent: str = ""):
        print(f"🔍 DEBUG add_node_info called for {node_path}", file=sys.stderr)
        
        # Include nodes that are in the relevant segment (whether anomalous or normal)
        if node_path not in relevant_nodes:
            print(f"   → SKIPPED: not in relevant_nodes", file=sys.stderr)
            return ""  # Skip nodes not in the filtered segment
        
        print(f"   → INCLUDED: in relevant_nodes", file=sys.stderr)
        
        # Get state and deviation - default to "N" (Normal) for nodes not in anomalies
        state = filtered_anomalies.get(node_path, "N")
        deviation = filtered_deviations.get(node_path, 0)
        
        # Add NPS values if available
        nps_info = ""
        if filtered_nps_values and node_path in filtered_nps_values:
            nps_data = filtered_nps_values[node_path]
            print(f"🔍 DEBUG add_node_info NPS for {node_path}: {nps_data}", file=sys.stderr)
            if isinstance(nps_data, dict):
                current_nps = nps_data.get('current', 'N/A')
                baseline_nps = nps_data.get('baseline', 'N/A')
                nps_info = f" (NPS: {current_nps} vs baseline: {baseline_nps})"
            else:
                nps_info = f" (NPS: {nps_data})"
        else:
            print(f"🔍 DEBUG add_node_info NO NPS for {node_path}", file=sys.stderr)
        
        ai_input_part = f"{indent}{name}: {get_state_desc(state, deviation)}{nps_info}\n"
        
        # Add interpretation if available
        if node_path in interpretations:
            ai_input_part += f"{indent}  └─ Pattern: {interpretations[node_path]}\n"
        
        # Add note for normal segments with NPS values
        elif state == "N" and filtered_nps_values and node_path in filtered_nps_values:
            nps_data = filtered_nps_values[node_path]
            if isinstance(nps_data, dict):
                current_nps = nps_data.get('current', 'N/A')
                baseline_nps = nps_data.get('baseline', 'N/A')
                ai_input_part += f"{indent}  └─ Note: No significant changes detected. Current period maintained stable performance.\n"
                ai_input_part += f"{indent}      • NPS Period: {current_nps:.1f} | NPS Baseline: {baseline_nps:.1f}\n"
        
        # Add note for normal segments WITHOUT NPS data
        elif state == "N" and (not filtered_nps_values or node_path not in filtered_nps_values):
            ai_input_part += f"{indent}  └─ Note: No significant changes detected. NPS data not available for this segment.\n"
        
        # Add explanation if available and is actual anomaly
        if state in ['+', '-']:
            ai_input_part += f"{indent}  └─ ANALYSIS:\n"
            
            if node_path in explanations:
                explanation = explanations[node_path]
                
                # DEBUG: Show what we're processing
                print(f"🔍 DEBUG build_ai_input_string for {node_path}:", file=sys.stderr)
                print(f"   Explanation length: {len(explanation) if explanation else 0}", file=sys.stderr)
                print(f"   First 100 chars: {repr(explanation[:100])}", file=sys.stderr)
                print(f"   Contains AGENT header: {'🤖 **AGENT CAUSAL ANALYSIS**' in explanation}", file=sys.stderr)
                
                if explanation and explanation != "Analysis timeout":
                    # Check if this is an AI Causal Investigation or Agent explanation
                    if "AI Causal Investigation:" in explanation:
                        # Extract the AI analysis directly
                        ai_analysis = explanation.replace("• AI Causal Investigation:", "").strip()
                        ai_input_part += f"{indent}     • AI Causal Investigation: {ai_analysis}\n"
                    elif "🤖 **AGENT CAUSAL ANALYSIS**" in explanation:
                        # Extract the agent analysis directly
                        ai_analysis = explanation.replace("🤖 **AGENT CAUSAL ANALYSIS**\n", "").strip()
                        ai_input_part += f"{indent}     • AI Causal Investigation: {ai_analysis}\n"
                    elif "## SÍNTESIS FINAL" in explanation:
                        # This is a full causal agent report - include it directly
                        ai_input_part += f"{indent}     • CAUSAL AGENT INVESTIGATION:\n"
                        # Add the full explanation with proper indentation
                        for line in explanation.split('\n'):
                            ai_input_part += f"{indent}       {line}\n"
                    else:
                        # Legacy format - try to parse the components
                        # Initialize with default values
                        routes_content = "Not enough answers for statistical analysis"
                        verbatims_content = "Not enough answers for statistical analysis"
                        drivers_content = "Not enough answers for statistical analysis"
                        
                        # Split explanation into components and clean them up
                        parts = explanation.split(" | ")
                        
                        for part in parts:
                            part = part.strip()
                            if not part or part.startswith("Period"):
                                continue
                            
                            # Clean up and format different explanation types (look for text patterns, not emojis)
                            if "Customer feedback:" in part or "verbatims collected" in part or "predominantly" in part:
                                if "predominantly negative" in part:
                                    sentiment = "negative feedback"
                                elif "predominantly positive" in part:
                                    sentiment = "positive feedback"
                                else:
                                    sentiment = "mixed feedback"
                                
                                topics = ""
                                if "main topics:" in part:
                                    topics_part = part.split("main topics:")[1].strip()
                                    if topics_part and not topics_part.endswith("("):
                                        topics = f", topics: {topics_part}"
                                
                                count = ""
                                if "verbatims collected" in part:
                                    try:
                                        count_part = part.split(" verbatims collected")[0]
                                        count_num = count_part.split()[-1]
                                        count = f"{count_num} verbatims, "
                                    except:
                                        pass
                                
                                # Remove emoji and clean the part
                                clean_part = part.replace("💬", "").replace("Customer feedback:", "").strip()
                                if clean_part:
                                    verbatims_content = f"{count}{sentiment}{topics} - {clean_part}"
                                else:
                                    verbatims_content = f"{count}{sentiment}{topics}"
                            
                            elif "routes analyzed" in part or "Routes:" in part:
                                clean_part = part.replace("🛣️ Routes:", "").replace("🛣️", "").replace("Routes:", "").strip()
                                if clean_part:
                                    routes_content = clean_part
                            
                            elif "Operational:" in part:
                                clean_part = part.replace("🔧 Operational:", "").replace("🔧", "").strip()
                                if clean_part:
                                    # We can add operational data here if needed, or skip it
                                    pass
                            
                            elif "NPS change:" in part or "touchpoints analyzed" in part or "Drivers:" in part:
                                clean_part = part.replace("🚚 Drivers:", "").replace("🚚", "").replace("Drivers:", "").strip()
                                if clean_part:
                                    drivers_content = clean_part
                        
                        # Show legacy format components
                        ai_input_part += f"{indent}     • Routes: {routes_content}\n"
                        ai_input_part += f"{indent}     • Verbatims: {verbatims_content}\n"
                        ai_input_part += f"{indent}     • Explanatory Drivers: {drivers_content}\n"
                else:
                    ai_input_part += f"{indent}     • No analysis available\n"
            else:
                ai_input_part += f"{indent}     • No analysis available\n"
        
        return ai_input_part
    
    # Build hierarchical structure based on segment filter
    if segment_filter == "Global":
        # Full tree
        ai_input += add_node_info("Global", "Global")
        ai_input += add_node_info("Global/LH", "Long Haul (LH)", "  ")
        ai_input += add_node_info("Global/LH/Economy", "├─ Economy", "    ")
        ai_input += add_node_info("Global/LH/Business", "├─ Business", "    ")
        ai_input += add_node_info("Global/LH/Premium", "└─ Premium", "    ")
        ai_input += add_node_info("Global/SH", "Short Haul (SH)", "  ")
        ai_input += add_node_info("Global/SH/Economy", "├─ Economy", "    ")
        ai_input += add_node_info("Global/SH/Economy/IB", "    └─ IB", "      ")
        ai_input += add_node_info("Global/SH/Economy/YW", "    └─ YW", "      ")
        ai_input += add_node_info("Global/SH/Business", "└─ Business", "    ")
        ai_input += add_node_info("Global/SH/Business/IB", "    └─ IB", "      ")
        ai_input += add_node_info("Global/SH/Business/YW", "    └─ YW", "      ")
    elif segment_filter == "Global/LH":
        # LH tree only
        ai_input += add_node_info("Global/LH", "Long Haul (LH)")
        ai_input += add_node_info("Global/LH/Economy", "├─ Economy", "  ")
        ai_input += add_node_info("Global/LH/Business", "├─ Business", "  ")
        ai_input += add_node_info("Global/LH/Premium", "└─ Premium", "  ")
    elif segment_filter == "Global/SH":
        # SH tree only
        ai_input += add_node_info("Global/SH", "Short Haul (SH)")
        ai_input += add_node_info("Global/SH/Economy", "├─ Economy", "  ")
        ai_input += add_node_info("Global/SH/Economy/IB", "  └─ IB", "    ")
        ai_input += add_node_info("Global/SH/Economy/YW", "  └─ YW", "    ")
        ai_input += add_node_info("Global/SH/Business", "└─ Business", "  ")
        ai_input += add_node_info("Global/SH/Business/IB", "  └─ IB", "    ")
        ai_input += add_node_info("Global/SH/Business/YW", "  └─ YW", "    ")
    elif segment_filter == "Global/SH/Economy":
        # SH Economy tree only
        ai_input += add_node_info("Global/SH/Economy", "SH Economy")
        ai_input += add_node_info("Global/SH/Economy/IB", "├─ IB", "  ")
        ai_input += add_node_info("Global/SH/Economy/YW", "└─ YW", "  ")
    elif segment_filter == "Global/SH/Business":
        # SH Business tree only
        ai_input += add_node_info("Global/SH/Business", "SH Business")
        ai_input += add_node_info("Global/SH/Business/IB", "├─ IB", "  ")
        ai_input += add_node_info("Global/SH/Business/YW", "└─ YW", "  ")
    else:
        # Single node
        node_name = segment_filter.split('/')[-1] if '/' in segment_filter else segment_filter
        ai_input += add_node_info(segment_filter, node_name)
    
    ai_input += "\nINTERPRETATION INSTRUCTIONS:\n"
    ai_input += "• Focus ONLY on segments marked as 'POSITIVE ANOMALY' or 'NEGATIVE ANOMALY'\n"
    ai_input += "• 'Normal' segments (even with deviations) are NOT anomalies - they are expected variations\n"
    ai_input += "• Explain the root causes using the analysis data provided for anomalous segments\n"
    if segment_filter != "Global":
        ai_input += f"• Analysis scope limited to {segment_filter} segment and its children\n"
    else:
        ai_input += "• If Global shows 'Normal' despite segment anomalies, this means the anomalies are localized and balanced out\n"
    
    return ai_input

async def print_enhanced_tree_with_explanations_and_interpretations(
    anomalies: dict, deviations: dict, explanations: dict, interpretations: dict,
    aggregation_days: int, target_period: int, date_range=None, segment_filter: str = "Global",
    analysis_date: datetime = None, date_parameter: str = None, nps_values: dict = None):
    """Print enhanced tree with explanations and parent interpretations"""
    

    
    # Filter data based on segment
    filtered_anomalies = {k: v for k, v in anomalies.items() if segment_filter in k or segment_filter == "Global"}
    filtered_deviations = {k: v for k, v in deviations.items() if segment_filter in k or segment_filter == "Global"}
    filtered_explanations = {k: v for k, v in explanations.items() if segment_filter in k or segment_filter == "Global"}
    filtered_interpretations = {k: v for k, v in interpretations.items() if segment_filter in k or segment_filter == "Global"}
    filtered_nps_values = {k: v for k, v in nps_values.items() if segment_filter in k or segment_filter == "Global"} if nps_values else {}
    
    # Create a more descriptive title with date range
    if analysis_date and date_parameter:
        # Calculate correct date range based on analysis_date and date_parameter
        start_date, end_date = calculate_period_date_range(analysis_date, target_period, aggregation_days)
        period_title = f"Period {target_period} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
    elif date_range:
        start_date, end_date = date_range
        period_title = f"Period {target_period} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
    else:
        period_title = f"Period {target_period} ({aggregation_days}d aggregation)"
    
    print(f"\n📊 NPS Anomaly Analysis - {period_title}")
    print("-" * 70)
    
    # Normalize segment_filter for tree printing comparison
    normalized_segment = segment_filter
    if segment_filter == 'SH':
        normalized_segment = 'Global/SH'
    elif segment_filter == 'LH':
        normalized_segment = 'Global/LH'
    elif segment_filter == 'Economy' and '/' not in segment_filter:
        normalized_segment = 'Global/SH/Economy'
    elif segment_filter == 'Business' and '/' not in segment_filter:
        normalized_segment = 'Global/SH/Business'
    
    # DEBUG: Show what's in the filtered data
    debug_print(f"Filtered anomalies for segment {segment_filter} (normalized: {normalized_segment}):")
    debug_print(f"  Anomalies: {filtered_anomalies}")
    debug_print(f"  Deviations: {filtered_deviations}")
    debug_print(f"  Explanations available: {list(filtered_explanations.keys())}")
    debug_print(f"  Interpretations available: {list(filtered_interpretations.keys())}")
    
    def get_state_description(state):
        """Get clear state description"""
        if state == "+":
            return "POSITIVE ANOMALY"
        elif state == "-":
            return "NEGATIVE ANOMALY"
        elif state == "N":
            return "Normal"
        elif state == "S":
            return "Low Sample"
        else:
            return "No Data"
    
    def get_deviation_text(node_path):
        deviation = deviations.get(node_path, 0)
        deviation_text = f" ({deviation:+.1f} pts)" if deviation != 0 else ""
        
        # Add NPS values if available - show them more prominently
        nps_info = ""
        if nps_values and node_path in nps_values:
            nps_data = nps_values[node_path]
            if isinstance(nps_data, dict):
                current_nps = nps_data.get('current', 'N/A')
                baseline_nps = nps_data.get('baseline', 'N/A')
                if isinstance(current_nps, (int, float)) and isinstance(baseline_nps, (int, float)):
                    difference = current_nps - baseline_nps
                    nps_info = f" [NPS: {current_nps:.1f} vs {baseline_nps:.1f}, diff: {difference:+.1f}]"
                else:
                    nps_info = f" [NPS: {current_nps} vs {baseline_nps}]"
            else:
                nps_info = f" [NPS: {nps_data}]"
        
        return deviation_text + nps_info
    
    def print_interpretation(node_path, indent=""):
        if node_path in filtered_interpretations:
            print(f"{indent}  └─ Pattern: {filtered_interpretations[node_path]}")
    
    def print_explanation(node_path, indent=""):
        print(f"{indent}  └─ ANALYSIS:")
        
        if node_path in filtered_explanations:
            explanation = filtered_explanations[node_path]
            
            if explanation == "Analysis timeout":
                print(f"{indent}     • Analysis timeout occurred")
                return
            elif explanation and explanation.strip() != "":
                
                # Check if this is an agent explanation (contains AI Causal Investigation or Agent header)
                if "AI Causal Investigation:" in explanation:
                    # Agent mode: Show the narrative explanation directly
                    agent_content = explanation.replace("• AI Causal Investigation:", "").strip()
                    print(f"{indent}     • AI Causal Investigation: {agent_content}")
                    return
                elif "🤖 **AGENT CAUSAL ANALYSIS**" in explanation:
                    # Agent mode: Show the narrative explanation directly
                    agent_content = explanation.replace("🤖 **AGENT CAUSAL ANALYSIS**\n", "").strip()
                    print(f"{indent}     • AI Causal Investigation: {agent_content}")
                    return
                
                # Raw mode: Parse structured explanation with separators
                # Initialize with default values
                operational_content = "No operational data available"
                routes_content = "Not enough answers for statistical analysis"
                verbatims_content = "Not enough answers for statistical analysis"
                drivers_content = "Not enough answers for statistical analysis"
                
                # Split explanation into components and clean them up
                parts = explanation.split(" | ")
                
                for part in parts:
                    part = part.strip()
                    if not part or part.startswith("Period"):
                        continue
                    
                    # Clean up and format different explanation types (look for text patterns, not emojis)
                    if "Customer feedback:" in part or "verbatims collected" in part or "predominantly" in part:
                        if "predominantly negative" in part:
                            sentiment = "negative feedback"
                        elif "predominantly positive" in part:
                            sentiment = "positive feedback"
                        else:
                            sentiment = "mixed feedback"
                        
                        topics = ""
                        if "main topics:" in part:
                            topics_part = part.split("main topics:")[1].strip()
                            if topics_part and not topics_part.endswith("("):
                                topics = f", topics: {topics_part}"
                        
                        count = ""
                        if "verbatims collected" in part:
                            try:
                                count_part = part.split(" verbatims collected")[0]
                                count_num = count_part.split()[-1]
                                count = f"{count_num} verbatims, "
                            except:
                                pass
                        
                        # Remove emoji and clean the part
                        clean_part = part.replace("💬", "").replace("Customer feedback:", "").strip()
                        if clean_part:
                            verbatims_content = f"{count}{sentiment}{topics} - {clean_part}"
                        else:
                            verbatims_content = f"{count}{sentiment}{topics}"
                    
                    elif "Routes:" in part or "🛣️" in part:
                        clean_part = part.replace("🛣️ Routes:", "").replace("🛣️", "").replace("Routes:", "").strip()
                        if clean_part:
                            routes_content = clean_part
                    
                    elif "Operational:" in part:
                        clean_part = part.replace("🔧 Operational:", "").replace("🔧", "").replace("Operational:", "").strip()
                        if clean_part:
                            operational_content = clean_part
                    
                    elif "Drivers:" in part or "🚚" in part:
                        clean_part = part.replace("🚚 Drivers:", "").replace("🚚", "").replace("Drivers:", "").strip()
                        if clean_part:
                            drivers_content = clean_part
                
                # Show all four categories in consistent order for raw mode
                print(f"{indent}     • Operational: {operational_content}")
                print(f"{indent}     • Routes: {routes_content}")
                print(f"{indent}     • Verbatims: {verbatims_content}")
                print(f"{indent}     • Explanatory Drivers: {drivers_content}")
        else:
            # No explanation available
            print(f"{indent}     • No analysis available for this node")
    
    # Print tree based on normalized segment filter
    if normalized_segment == "Global":
        # Show full tree
        print_full_tree(filtered_anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation)
    elif normalized_segment == "Global/LH":
        # Show only LH tree
        print_lh_tree(filtered_anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation)
    elif normalized_segment == "Global/SH":
        # Show only SH tree
        print_sh_tree(filtered_anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation)
    elif normalized_segment == "Global/SH/Economy":
        # Show only SH Economy tree
        print_sh_economy_tree(filtered_anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation)
    elif normalized_segment == "Global/SH/Business":
        # Show only SH Business tree
        print_sh_business_tree(filtered_anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation)
    else:
        # Show single node for leaf segments
        print_single_node(normalized_segment, filtered_anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation)
    
    # Summary
    actual_anomalies = [node for node, state in filtered_anomalies.items() if state in ['+', '-']]
    print(f"\n📋 SUMMARY:")
    if actual_anomalies:
        print(f"  • Anomalies detected in: {', '.join(actual_anomalies)}")
        print(f"  • Total anomalous segments: {len(actual_anomalies)}")
    else:
        print(f"  • No anomalies detected - all segments within normal variation")

async def run_flexible_data_download_with_date(aggregation_days: int, periods: int, start_date, date_parameter: str, segment: str = "Global"):
    """Run flexible data download with custom date and parameter naming"""
    # Generate folder name with new naming convention: {parameter}_{date}_flexible_{aggregation_days}d
    date_str = start_date.strftime('%Y_%m_%d')
    timestamp = datetime.now().strftime('%H%M')  # Add time for uniqueness if needed
    
    # Include segment in folder name if not Global
    if segment != "Global":
        segment_suffix = f"_{segment.replace('/', '_')}"
    else:
        segment_suffix = ""
    
    target_folder = f"tables/{date_parameter}_{date_str}_flexible_{aggregation_days}d{segment_suffix}_{timestamp}"
    
    print(f"📁 Target folder: {target_folder}")
    print(f"📅 Analysis start date: {start_date.strftime('%Y-%m-%d')}")
    print(f"🏷️ Date parameter: {date_parameter}")
    print(f"🎯 Segment focus: {segment}")
    
    success = await collect_flexible_data(aggregation_days, target_folder, segment, start_date)
    
    if success:
        print(f"✅ Data collection completed successfully")
        return target_folder
    else:
        print(f"❌ Data collection failed")
        return None

async def run_flexible_data_download_silent_with_date(aggregation_days: int, periods: int, start_date, date_parameter: str, segment: str = "Global"):
    """Run flexible data download completely silently with custom date and parameter naming"""
    # Generate folder name with new naming convention
    date_str = start_date.strftime('%Y_%m_%d')
    timestamp = datetime.now().strftime('%H%M')  
    
    # Include segment in folder name if not Global
    if segment != "Global":
        segment_suffix = f"_{segment.replace('/', '_')}"
    else:
        segment_suffix = ""
    
    target_folder = f"tables/{date_parameter}_{date_str}_flexible_{aggregation_days}d{segment_suffix}_{timestamp}"
    
    collector = PBIDataCollector()
    
    # Get node paths for the specified segment
    node_paths = get_segment_node_paths(segment)
    
    # Collect data for selected nodes completely silently
    total_success = 0
    total_attempted = 0
    
    # Suppress all output during data collection
    with open(os.devnull, 'w') as devnull:
        with redirect_stdout(devnull), redirect_stderr(devnull):
            for node_path in node_paths:
                try:
                    results = await collector.collect_flexible_data_for_node(
                        node_path, aggregation_days, target_folder, start_date
                    )
                    total_attempted += len(results)
                    total_success += sum(results.values())
                except Exception:
                    pass
    
    if total_success > 0:
        return target_folder
    else:
        return None

def get_segment_node_paths(segment: str) -> list:
    """
    Generate the list of node paths based on the selected segment.
    
    Args:
        segment: Root segment to analyze (e.g., 'Global', 'SH', 'Global/SH/Economy')
        
    Returns:
        List of node paths to collect and analyze
    """
    # Normalize segment input - handle shortcuts
    if segment == 'SH':
        segment = 'Global/SH'
    elif segment == 'LH':
        segment = 'Global/LH'
    elif segment == 'Economy/LH':
        segment = 'Global/LH/Economy'
    elif segment == 'Business/LH':
        segment = 'Global/LH/Business'
    elif segment == 'Premium/LH':
        segment = 'Global/LH/Premium'
    elif segment == 'Economy/SH':
        segment = 'Global/SH/Economy'
    elif segment == 'Business/SH':
        segment = 'Global/SH/Business'
    elif segment == 'Economy' and '/' not in segment:
        # Ambiguous - default to SH/Economy
        segment = 'Global/SH/Economy'
    elif segment == 'Business' and '/' not in segment:
        # Ambiguous - default to SH/Business  
        segment = 'Global/SH/Business'
    
    # Define the complete hierarchy
    all_nodes = {
        "Global": [
            "Global",
            "Global/LH",
            "Global/LH/Economy", 
            "Global/LH/Business", 
            "Global/LH/Premium",
            "Global/SH",
            "Global/SH/Economy", 
            "Global/SH/Business",
            "Global/SH/Economy/IB", 
            "Global/SH/Economy/YW",
            "Global/SH/Business/IB", 
            "Global/SH/Business/YW"
        ],
        "Global/LH": [
            "Global/LH",
            "Global/LH/Economy", 
            "Global/LH/Business", 
            "Global/LH/Premium"
        ],
        "Global/SH": [
            "Global/SH",
            "Global/SH/Economy", 
            "Global/SH/Business",
            "Global/SH/Economy/IB", 
            "Global/SH/Economy/YW",
            "Global/SH/Business/IB", 
            "Global/SH/Business/YW"
        ],
        "Global/LH/Economy": [
            "Global/LH/Economy"
        ],
        "Global/LH/Business": [
            "Global/LH/Business"
        ],
        "Global/LH/Premium": [
            "Global/LH/Premium"
        ],
        "Global/SH/Economy": [
            "Global/SH/Economy",
            "Global/SH/Economy/IB", 
            "Global/SH/Economy/YW"
        ],
        "Global/SH/Business": [
            "Global/SH/Business",
            "Global/SH/Business/IB", 
            "Global/SH/Business/YW"
        ],
        "Global/SH/Economy/IB": [
            "Global/SH/Economy/IB"
        ],
        "Global/SH/Economy/YW": [
            "Global/SH/Economy/YW"
        ],
        "Global/SH/Business/IB": [
            "Global/SH/Business/IB"
        ],
        "Global/SH/Business/YW": [
            "Global/SH/Business/YW"
        ]
    }
    
    if segment in all_nodes:
        return all_nodes[segment]
    else:
        # If segment not found, try to find partial matches
        matching_segments = [key for key in all_nodes.keys() if segment in key]
        if matching_segments:
            # Use the first match
            return all_nodes[matching_segments[0]]
        else:
            # Fallback to Global if no match found
            print(f"⚠️ Segment '{segment}' not found. Using Global as fallback.")
            return all_nodes["Global"]

async def run_comprehensive_analysis(
    analysis_date: datetime,
    date_parameter: str,
    segment: str = "Global",
    explanation_mode: str = "agent",
    causal_filter: str = "vs L7d",
    comparison_start_date: Optional[datetime] = None,
    comparison_end_date: Optional[datetime] = None,
    date_flight_local: Optional[str] = None,
    # Parameters for daily analysis with defaults matching old hardcoded values
    daily_anomaly_detection_mode: str = 'mean',
    daily_baseline_periods: int = 7,
    daily_aggregation_days: int = 1,
    daily_periods: int = 7
):
    """
    Refactored comprehensive analysis to be a clean orchestrator.
    It executes two distinct analysis flows:
    1. A weekly comparative analysis.
    2. A daily single analysis for each of the last 7 days.
    Finally, it consolidates the results.
    """
    print("🚀 ENHANCED COMPREHENSIVE NPS ANALYSIS (Refactored)")
    print("=" * 80)
    print(f"📅 Analysis Date: {analysis_date.strftime('%Y-%m-%d')} ({date_parameter})")
    print(f"🎯 Segment Focus: {segment}")

    generated_reports = []

    # --- 1. Weekly Comparative Analysis ---
    print("\n" + "=" * 40)
    print("📊 STEP 1: Running Weekly Comparative Analysis")
    print("=" * 40)
    try:
        weekly_report_path = await execute_analysis_flow(
            analysis_date=analysis_date,
            date_parameter=date_parameter,
            segment=segment,
            explanation_mode=explanation_mode,
            anomaly_detection_mode='vslast',
            baseline_periods=7,
            aggregation_days=7,
            periods=1,
            causal_filter=causal_filter,
            comparison_start_date=comparison_start_date,
            comparison_end_date=comparison_end_date,
            date_flight_local=date_flight_local,
            study_mode="comparative",
        )
        if weekly_report_path and "Error" not in str(weekly_report_path):
            # Store the actual data, not just the path
            generated_reports.append({
                'type': 'weekly',
                'data': weekly_report_path
            })
            print(f"✅ Weekly analysis completed. Data length: {len(str(weekly_report_path))} chars")
        else:
            print(f"⚠️ Weekly analysis completed but no anomalies found or insufficient data.")
            # Even if no anomalies found, we should still include the weekly analysis
            if weekly_report_path and "Error" not in str(weekly_report_path):
                generated_reports.append({
                    'type': 'weekly',
                    'data': weekly_report_path
                })

    except Exception as e:
        print(f"❌ CRITICAL ERROR during weekly analysis: {e}")
        import traceback
        traceback.print_exc()

    # --- 2. Daily Analysis ---
    print("\n" + "=" * 40)
    print("📊 STEP 2: Running Daily Analysis")
    print("=" * 40)
    try:
        daily_report_path = await execute_analysis_flow(
            analysis_date=analysis_date,
            date_parameter=date_parameter,
            segment=segment,
            explanation_mode=explanation_mode,
            anomaly_detection_mode=daily_anomaly_detection_mode,
            baseline_periods=daily_baseline_periods,
            aggregation_days=daily_aggregation_days,
            periods=daily_periods,
            causal_filter=None,
            comparison_start_date=None,
            comparison_end_date=None,
            date_flight_local=date_flight_local,
            study_mode="single",
        )
        if daily_report_path and "Error" not in str(daily_report_path):
            # Store the actual data, not just the path
            generated_reports.append({
                'type': 'daily',
                'data': daily_report_path
            })
            print(f"✅ Daily analysis completed. Data length: {len(str(daily_report_path))} chars")
        else:
            print(f"❌ Daily analysis failed. Reason: {daily_report_path}")
    except Exception as e:
        print(f"❌ CRITICAL ERROR during daily analysis: {e}")
        import traceback
        traceback.print_exc()


    # --- 3. Final Summary ---
    print("\n" + "=" * 40)
    print("📝 STEP 3: Consolidating All Reports")
    print("=" * 40)
    if generated_reports:
        print(f"✅ Found {len(generated_reports)} reports to summarize.")
        
        # Separate weekly and daily reports
        weekly_comparative_analysis = None
        daily_single_analyses = []

        # Process the reports from memory
        weekly_comparative_analysis = ""
        daily_single_analyses = []
        
        for report in generated_reports:
            if report['type'] == 'weekly':
                # Weekly report is already in the correct format (string)
                weekly_comparative_analysis = report['data']
                print(f"✅ Found weekly report: {len(weekly_comparative_analysis)} chars")
            elif report['type'] == 'daily':
                # Daily report is a list of dictionaries with the structure expected by summary agent
                daily_single_analyses = report['data']
                print(f"✅ Found daily analysis data: {len(daily_single_analyses)} periods")
        
        # Convert daily data to the format expected by summary agent if needed
        if daily_single_analyses and isinstance(daily_single_analyses, list):
            # The data is already in the correct format from show_silent_anomaly_analysis
            # Just need to ensure it has the right structure
            formatted_daily_analyses = []
            for daily in daily_single_analyses:
                if isinstance(daily, dict) and 'ai_interpretation' in daily:
                    formatted_daily_analyses.append({
                        'date': daily.get('date_range', daily.get('period', 'Unknown')),
                        'analysis': daily.get('ai_interpretation', ''),
                        'anomalies': ['daily_analysis']
                    })
            daily_single_analyses = formatted_daily_analyses
            print(f"✅ Formatted daily analyses: {len(daily_single_analyses)} periods")

        try:
            print("\n🤖 Initializing Summary Agent...")
            summary_agent = AnomalySummaryAgent(
                llm_type=get_default_llm_type(),
                logger=logging.getLogger("summary_agent")
            )
            print("✅ Summary Agent initialized. Generating executive summary...")
            
            # Call the correct method with the correct arguments
            final_summary = await summary_agent.generate_comprehensive_summary(
                weekly_comparative_analysis=weekly_comparative_analysis,
                daily_single_analyses=daily_single_analyses
            )
            
            print("\n" + "=" * 80)
            print("👑 EXECUTIVE SUMMARY 👑")
            print("=" * 80)
            print(final_summary)
            final_result = final_summary

        except Exception as e:
            print(f"❌ CRITICAL ERROR during summary generation: {e}")
            import traceback
            traceback.print_exc()
            final_result = "Error: Failed to generate a consolidated summary."

    else:
        print("❌ No reports were generated. Cannot create a summary.")
        final_result = "Error: Comprehensive analysis failed to generate any reports."

    print("\n" + "=" * 80)
    print("🏁 Comprehensive Analysis Finished")
    print("=" * 80)

    return final_result

async def analyze_single_day(target_date: datetime, segment: str, explanation_mode: str) -> str:
    """
    Analyze a single day using the complete hierarchical analysis flow with study_mode = "single"
    """
    try:
        print(f"         📅 Analyzing single day: {target_date.strftime('%Y-%m-%d')}")
        
        # Create a temporary folder for this single day analysis
        from pathlib import Path
        import tempfile
        
        temp_folder = Path(tempfile.mkdtemp(prefix=f"single_day_{target_date.strftime('%Y%m%d')}_"))
        
        # Download data for this specific day
        from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
        pbi_collector = PBIDataCollector()
        
        # Collect data for the specific day - collect ALL hierarchical nodes for the segment
        node_paths = get_segment_node_paths(segment)
        
        print(f"🔍 Collecting data for {len(node_paths)} hierarchical nodes: {node_paths}")
        
        for node_path in node_paths:
            await pbi_collector.collect_flexible_data_for_node(
                node_path=node_path,
                aggregation_days=1,
                target_folder=str(temp_folder),
                analysis_date=target_date
            )
        
        # Create detector for anomaly detection
        from dashboard_analyzer.anomaly_detection.flexible_detector import FlexibleAnomalyDetector
        detector = FlexibleAnomalyDetector(
            aggregation_days=1,
            threshold=5.0,
            min_sample_size=5,
            detection_mode="mean",  # Use mean comparison for single mode
            baseline_periods=7
        )
        
        # Create interpreter with single mode
        from dashboard_analyzer.anomaly_detection.flexible_anomaly_interpreter import FlexibleAnomalyInterpreter
        
        interpreter = FlexibleAnomalyInterpreter(
            data_folder=str(temp_folder),
            pbi_collector=pbi_collector,
            explanation_mode=explanation_mode,
            detection_mode="mean",
            causal_filter=None,  # No causal_filter for single mode
            study_mode="single"
        )
        
        # Initialize AI agent for interpretation
        try:
            from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_interpreter_agent import AnomalyInterpreterAgent
            from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType, get_default_llm_type
            
            ai_agent = AnomalyInterpreterAgent(
                llm_type=get_default_llm_type(),
                config_path="dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml",
                logger=logging.getLogger("ai_interpreter"),
                study_mode="single"
            )
            ai_available = True
        except Exception as e:
            print(f"⚠️ AI Agent not available: {str(e)}")
            ai_available = False
            return f"Error: AI Agent not available - {str(e)}"
        
        # Analyze the specific day (period 1)
        period = 1
        period_anomalies, period_deviations, _, period_nps_values = await detector.analyze_period(str(temp_folder), period, target_date)
        
        # Get date range
        date_range = (target_date, target_date)
        start_date, end_date = date_range
        date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        
        # Generate parent interpretations
        parent_interpretations = generate_parent_interpretations(period_anomalies)
        
        # Show the clean tree first
        print(f"\n🌳 ANOMALY TREE (SINGLE MODE):")
        print("-" * 40)
        await print_clean_tree_only(period_anomalies, period_deviations, parent_interpretations, segment, None)
        
        # Collect explanations for anomalous nodes
        explanations = {}
        nodes_with_anomalies = [node for node, state in period_anomalies.items() if state in ['+', '-']]

        # ENHANCEMENT: Always include Global segment in causal analysis if it has valid data
        if nodes_with_anomalies:
            # Check if Global has valid data (not "?" or missing)
            global_state = period_anomalies.get("Global", "?")
            print(f"🔍 DEBUG GLOBAL STATE: global_state='{global_state}', period_anomalies keys: {list(period_anomalies.keys())}")
            
            # Always recalculate Global's anomaly state based on deviation (override detector's decision)
            global_deviation = period_deviations.get("Global", 0.0)
            print(f"🔍 DEBUG GLOBAL CALCULATION: global_deviation={global_deviation}")
            if global_deviation > 0:
                global_state = "+"  # Positive anomaly
            elif global_deviation < 0:
                global_state = "-"  # Negative anomaly
            else:
                global_state = "N"  # Neutral (only when deviation is exactly 0)
            # Always update Global in period_anomalies with calculated state
            period_anomalies["Global"] = global_state
            print(f"      🔍 DEBUG GLOBAL: Override Global state='{global_state}' based on deviation={global_deviation}")
            
            if "Global" not in nodes_with_anomalies and global_state != "?":
                # Add Global to the analysis even if it doesn't have anomalies but has valid data
                nodes_with_anomalies.append("Global")
                print(f"🔍 ENHANCED: Analyzing {len(nodes_with_anomalies)} segments (added Global with state '{global_state}' + {len([n for n in nodes_with_anomalies if n != 'Global'])} anomalous nodes)")
            elif "Global" in nodes_with_anomalies:
                print(f"🔍 📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (including Global)")
            else:
                print(f"🔍 📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (Global has no valid data)")
            
            # PRIORITY: Move Global to the front to ensure it's always processed first
            if "Global" in nodes_with_anomalies:
                nodes_with_anomalies.remove("Global")
                nodes_with_anomalies.insert(0, "Global")
                print(f"🎯 PRIORITY: Global moved to front of processing queue")

        if nodes_with_anomalies:
            print(f"🔍 Collecting explanations for {len(nodes_with_anomalies)} anomalous nodes: {nodes_with_anomalies}")
            
            for node_path in nodes_with_anomalies:
                try:
                    # Get anomaly info - determine type based on sign of change for Global
                    anomaly_type = period_anomalies.get(node_path, 'unknown')
                    print(f"🔍 DEBUG GLOBAL ANOMALY: node_path='{node_path}', period_anomalies.get()='{anomaly_type}', deviation_value={period_deviations.get(node_path, 0.0)}")
                    
                    # For Global node, determine anomaly state based on sign of change (using same nomenclature as other nodes)
                    if node_path == "Global" and anomaly_type == "unknown":
                        deviation_value = period_deviations.get(node_path, 0.0)
                        if deviation_value > 0:
                            anomaly_type = "+"  # Positive anomaly
                        elif deviation_value < 0:
                            anomaly_type = "-"  # Negative anomaly
                        else:
                            anomaly_type = "N"  # Neutral
                    
                    # Calculate magnitude from NPS values if available, fallback to period_deviations
                    anomaly_magnitude = 0.0
                    if node_path in period_nps_values and 'current' in period_nps_values[node_path] and 'baseline' in period_nps_values[node_path]:
                        current_nps = period_nps_values[node_path]['current']
                        baseline_nps = period_nps_values[node_path]['baseline']
                        anomaly_magnitude = current_nps - baseline_nps
                    else:
                        # Fallback to period_deviations
                        anomaly_magnitude = period_deviations.get(node_path, 0.0)
                    
                    print(f"🔍 DEBUG GLOBAL ANOMALY: node_path='{node_path}', anomaly_type='{anomaly_type}', anomaly_magnitude={anomaly_magnitude}")
                    
                    # Generate explanation using the interpreter
                    explanation = await interpreter.explain_anomaly(
                        node_path=node_path,
                        target_period=period,
                        aggregation_days=1,
                        anomaly_state=anomaly_type,  # Pass the determined anomaly type
                        start_date=start_date,
                        end_date=end_date,
                        causal_filter=None  # Single mode
                    )
                    
                    explanations[node_path] = explanation
                    print(f"      ✅ Explanation generated for {node_path}")
                    
                except Exception as e:
                    print(f"      ❌ Error generating explanation for {node_path}: {str(e)}")
                    explanations[node_path] = f"Error: {str(e)}"
        else:
            print(f"      ✅ No anomalies detected for this day")
        
        # Build AI input string for hierarchical analysis
        ai_input = build_ai_input_string(
            period, period_anomalies, period_deviations, 
            parent_interpretations, explanations, date_range, segment, period_nps_values
        )
        
        # Execute AI interpretation with timeout
        try:
            ai_interpretation = await asyncio.wait_for(
                ai_agent.interpret_anomaly_tree(ai_input, target_date.strftime('%Y-%m-%d'), segment),
                timeout=600.0
            )
            
            print(f"✅ AI interpretation completed for single day analysis")
            
            # Display the interpreter result
            print(f"\n" + "="*80)
            print(f"🤖 SINGLE DAY INTERPRETER ANALYSIS ({target_date.strftime('%Y-%m-%d')})")
            print("="*80)
            print(ai_interpretation)
            print("="*80)
            
            # Clean up temp folder
            import shutil
            shutil.rmtree(temp_folder, ignore_errors=True)
            
            return ai_interpretation
            
        except Exception as e:
            print(f"❌ AI interpretation failed: {str(e)}")
            return f"AI interpretation failed: {str(e)}"
        
    except Exception as e:
        print(f"❌ Error analyzing single day {target_date.strftime('%Y-%m-%d')}: {str(e)}")
        return f"Error analyzing day {target_date.strftime('%Y-%m-%d')}: {str(e)}"

async def run_flexible_analysis_silent(data_folder: str, analysis_date: datetime = None, date_parameter: str = None, anomaly_detection_mode: str = "target", baseline_periods: int = 7, causal_filter: str = "vs L7d", periods: int = 7):
    """Run flexible analysis completely silently"""
    import os
    from contextlib import redirect_stdout, redirect_stderr
    
    # Extract aggregation days from folder name
    folder_name = Path(data_folder).name
    if 'flexible_' in folder_name and 'd_' in folder_name:
        try:
            aggregation_days = int(folder_name.split('flexible_')[1].split('d_')[0])
        except:
            aggregation_days = 7  # Default
    else:
        aggregation_days = 7
    
    # Configure anomaly detection based on mode
    detector = FlexibleAnomalyDetector(
        aggregation_days=aggregation_days,
        threshold=5.0,
        min_sample_size=5,
        detection_mode=anomaly_detection_mode,
        baseline_periods=baseline_periods
    )
    
    # Calculate the correct period numbers based on date parameter type and periods parameter
    reference_period = None  # Will be used for baseline calculation when date_flight_local is specified
    if analysis_date and date_parameter:
        if any(param in date_parameter for param in ['flight_local', 'available']):
            # For date_flight_local or default available: treat analysis_date as the most recent period (period 1)
            # Analyze the specified number of most recent periods relative to that date
            periods_to_analyze = list(range(1, periods + 1))  # Periods 1, 2, 3, ... up to specified count
            if 'flight_local' in date_parameter:
                # When date_flight_local is specified, use period 1 as reference for baseline calculation
                reference_period = 1
        elif date_parameter == 'insert_ci':
            # For insert_date_ci: calculate actual period numbers relative to today
            base_period = calculate_actual_period_number(analysis_date)
            # Analyze specified number of periods starting from the analysis date
            periods_to_analyze = list(range(base_period, base_period + periods))
        else:
            # Unknown parameter type, default to specified periods
            periods_to_analyze = list(range(1, periods + 1))
    else:
        # Default behavior: analyze the specified number of most recent periods
        periods_to_analyze = list(range(1, periods + 1))
    
    anomaly_periods = []
    
    # Suppress all output during analysis
    with open(os.devnull, 'w') as devnull:
        with redirect_stdout(devnull), redirect_stderr(devnull):
            try:
                for period in periods_to_analyze:
                    period_anomalies, period_deviations, period_explanations, period_nps_values = await detector.analyze_period(data_folder, period, analysis_date, reference_period)
                    
                    # Check if any node has an anomaly
                    has_anomaly = any(state in ['+', '-'] for state in period_anomalies.values())
                    if has_anomaly:
                        anomaly_periods.append(period)
            
            except Exception:
                return None
    
    # DEBUG: Check NPS values after silenced analysis
    print(f"🔍 DEBUG SILENT_ANALYSIS: period_nps_values type: {type(period_nps_values) if 'period_nps_values' in locals() else 'Not defined'}", file=sys.stderr)
    if 'period_nps_values' in locals():
        print(f"🔍 DEBUG SILENT_ANALYSIS: period_nps_values content: {period_nps_values}", file=sys.stderr)
    
    return {
        'detector': detector,
        'data_folder': data_folder,
        'aggregation_days': aggregation_days,
        'anomaly_periods': anomaly_periods,
        'total_periods': periods,
        'periods_analyzed': periods_to_analyze,
        'analysis_date': analysis_date,
        'date_parameter': date_parameter,
        'anomaly_detection_mode': anomaly_detection_mode,
        'baseline_periods': baseline_periods
    }

async def run_flexible_analysis(data_folder: str, explanation_mode: str = "agent", analysis_date=None, anomaly_detection_mode: str = "target", baseline_periods: int = 7, periods: int = 7):
    """Run flexible period analysis and return results"""
    print(f"🔄 Analyzing periods in: {data_folder}")
    
    # Extract aggregation days from folder name
    folder_name = Path(data_folder).name
    if 'flexible_' in folder_name and 'd_' in folder_name:
        try:
            aggregation_days = int(folder_name.split('flexible_')[1].split('d_')[0])
        except:
            aggregation_days = 7  # Default
    else:
        aggregation_days = 7
    
    # Configure anomaly detection based on mode
    detector = FlexibleAnomalyDetector(
        aggregation_days=aggregation_days,
        threshold=5.0,
        min_sample_size=5,
        detection_mode=anomaly_detection_mode,
        baseline_periods=baseline_periods
    )
    
    # Analyze the specified number of most recent periods
    print(f"🔍 Analyzing the {periods} most recent periods...")
    periods_to_analyze = list(range(1, periods + 1))  # Periods 1, 2, 3, ... up to specified count
    anomaly_periods = []
    
    try:
        for period in periods_to_analyze:
            period_anomalies, period_deviations, period_explanations, period_nps_values = await detector.analyze_period(data_folder, period, analysis_date)
            
            # Check if any node has an anomaly
            has_anomaly = any(state in ['+', '-'] for state in period_anomalies.values())
            if has_anomaly:
                anomaly_periods.append(period)
    
    except Exception as e:
        print(f"⚠️ Analysis stopped: {str(e)}")
    
    if anomaly_periods:
        print(f"🚨 Found anomalies in {len(anomaly_periods)} of {periods} periods: {anomaly_periods}")
        return {
            'detector': detector,
            'data_folder': data_folder,
            'aggregation_days': aggregation_days,
            'anomaly_periods': anomaly_periods,
            'total_periods': periods,
            'periods_analyzed': periods_to_analyze,
            'analysis_date': analysis_date,
            'anomaly_detection_mode': anomaly_detection_mode,
            'baseline_periods': baseline_periods
        }
    else:
        print(f"✅ No anomalies detected in the {periods} most recent periods")
        return {
            'detector': detector,
            'data_folder': data_folder,
            'aggregation_days': aggregation_days,
            'anomaly_periods': [],
            'total_periods': periods,
            'periods_analyzed': periods_to_analyze,
            'analysis_date': analysis_date,
            'anomaly_detection_mode': anomaly_detection_mode,
            'baseline_periods': baseline_periods
        }

async def run_weekly_current_vs_average_analysis_silent(data_folder: str, analysis_date=None, anomaly_detection_mode: str = "target", baseline_periods: int = 7):
    """Run weekly analysis silently focusing only on current week (period 1) vs 3-week average"""
    import os
    from contextlib import redirect_stdout, redirect_stderr
    
    # Extract aggregation days from folder name (should be 7 for weekly)
    folder_name = Path(data_folder).name
    if 'flexible_' in folder_name and 'd_' in folder_name:
        try:
            aggregation_days = int(folder_name.split('flexible_')[1].split('d_')[0])
        except:
            aggregation_days = 7  # Default for weekly
    else:
        aggregation_days = 7
    
    # Configure anomaly detection based on mode
    detector = FlexibleAnomalyDetector(
        aggregation_days=aggregation_days,
        threshold=5.0,
        min_sample_size=5,
        detection_mode=anomaly_detection_mode,
        baseline_periods=baseline_periods
    )
    
    # Analyze only period 1 (current week vs 3-week moving average) silently
    current_week_period = 1
    anomaly_periods = []
    
    # Suppress all output during analysis
    with open(os.devnull, 'w') as devnull:
        with redirect_stdout(devnull), redirect_stderr(devnull):
            try:
                # Analyze only the current week (period 1)
                period_anomalies, period_deviations, period_explanations, period_nps_values = await detector.analyze_period(data_folder, current_week_period, analysis_date)
                
                # Check if current week has any anomaly
                has_anomaly = any(state in ['+', '-'] for state in period_anomalies.values())
                if has_anomaly:
                    anomaly_periods.append(current_week_period)
            
            except Exception:
                return None
    
    return {
        'detector': detector,
        'data_folder': data_folder,
        'aggregation_days': aggregation_days,
        'anomaly_periods': anomaly_periods,
        'total_periods': 1,  # Only analyzing current week
        'periods_analyzed': [current_week_period],
        'analysis_date': analysis_date,
        'anomaly_detection_mode': anomaly_detection_mode,
        'baseline_periods': baseline_periods
    }

async def show_silent_anomaly_analysis(analysis_data: dict, analysis_type: str, show_all_periods=False, segment: str = "Global", explanation_mode: str = "agent", causal_filter: str = "vs L7d", comparison_start_date: datetime = None, comparison_end_date: datetime = None):
    """Show only trees and AI summaries for periods with anomalies - silent version"""
    import os
    from contextlib import redirect_stdout, redirect_stderr
    
    detector = analysis_data['detector']
    data_folder = analysis_data['data_folder']
    aggregation_days = analysis_data['aggregation_days']
    anomaly_periods = analysis_data['anomaly_periods']
    periods_analyzed = analysis_data.get('periods_analyzed', anomaly_periods)
    
    # Initialize interpreter for explanations with specified mode
    pbi_collector = PBIDataCollector()
    
    # Determine study_mode based on analysis_type and causal_filter
    if analysis_type == "WEEKLY_COMPARATIVE" or causal_filter == "vs Sel. Period":
        study_mode = "comparative"
    elif analysis_type == "DIARIO_SINGLE" or causal_filter is None:
        study_mode = "single"
    else:
        study_mode = "comparative"  # Default to comparative
    
    interpreter = FlexibleAnomalyInterpreter(
        data_folder, 
        pbi_collector=pbi_collector, 
        explanation_mode=explanation_mode, 
        silent_mode=True, 
        detection_mode=analysis_data['detector'].detection_mode, 
        causal_filter=causal_filter, 
        comparison_start_date=comparison_start_date, 
        comparison_end_date=comparison_end_date,
        study_mode=study_mode
    )
    print(f"🔧 Explanation mode: {explanation_mode.upper()}")
    
    # Initialize AI agent for interpretation
    try:
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_interpreter_agent import AnomalyInterpreterAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType, get_default_llm_type
        
        # Determine study_mode based on analysis_type and causal_filter (same logic as interpreter)
        if analysis_type == "WEEKLY_COMPARATIVE" or causal_filter == "vs Sel. Period":
            ai_study_mode = "comparative"
        elif analysis_type == "DIARIO_SINGLE" or causal_filter is None:
            ai_study_mode = "single"
        else:
            ai_study_mode = "comparative"  # Default to comparative
        
        ai_agent = AnomalyInterpreterAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml",
            logger=logging.getLogger("ai_interpreter"),
            study_mode=ai_study_mode
        )
        ai_available = True
    except Exception:
        ai_available = False
    
    # Collect data for summary
    all_periods_data = []
    
    # If show_all_periods is True, show all periods analyzed, not just those with anomalies
    if show_all_periods:
        periods_to_show = periods_analyzed
    else:
        periods_to_show = [p for p in periods_analyzed if p in anomaly_periods]
    
    if not periods_to_show:
        print(f"✅ No periods to analyze in {analysis_type.lower()} analysis")
        return []
    
    # Show detailed analysis for selected periods
    for period in periods_to_show:
        print(f"\n{'='*60}")
        print(f"{analysis_type} PERIOD {period} ANALYSIS")
        print("="*60)
        
        # Get anomalies for this period
        analysis_date = analysis_data.get('analysis_date')
        date_parameter = analysis_data.get('date_parameter')
        
                # Calculate reference_period for baseline (same logic as in run_flexible_analysis_silent)
        reference_period = None
        if analysis_date and date_parameter:
            if any(param in date_parameter for param in ['flight_local', 'available']):
                if 'flight_local' in date_parameter:
                    reference_period = 1
        
        print(f"🔍 DEBUG DAILY_ANALYSIS: About to call detector.analyze_period for period {period} with reference_period={reference_period}", file=sys.stderr)
        analyze_result = await detector.analyze_period(data_folder, period, analysis_date, reference_period)
        print(f"🔍 DEBUG DAILY_ANALYSIS: Result type: {type(analyze_result)}", file=sys.stderr)
        print(f"🔍 DEBUG DAILY_ANALYSIS: Result length: {len(analyze_result) if hasattr(analyze_result, '__len__') else 'No length'}", file=sys.stderr)
        
        period_anomalies, period_deviations, _, period_nps_values = analyze_result
        print(f"🔍 DEBUG DAILY_ANALYSIS: period_nps_values type: {type(period_nps_values)}", file=sys.stderr)
        print(f"🔍 DEBUG DAILY_ANALYSIS: period_nps_values content: {period_nps_values}", file=sys.stderr)
        
        # Get date range using the correct method based on date_parameter
        date_parameter = analysis_data.get('date_parameter')
        
        if analysis_date and date_parameter in ['flight_local', 'available']:
            # For date_flight_local or default available: calculate relative to analysis_date
            start_date, end_date = calculate_period_date_range(analysis_date, period, aggregation_days)
            date_range = (start_date, end_date)
        else:
            # For other parameters or fallback: use interpreter method
            date_range = interpreter._get_period_date_range(period, aggregation_days)
        
        if date_range:
            start_date, end_date = date_range
            print(f"📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        else:
            date_range_str = "Unknown dates"
        
        # Generate parent interpretations
        parent_interpretations = generate_parent_interpretations(period_anomalies)
        
        # Collect explanations for anomalous nodes silently
        explanations = {}
        nodes_with_anomalies = [node for node, state in period_anomalies.items() if state in ['+', '-']]

        # ENHANCEMENT: Always include Global segment in causal analysis if it has valid data
        if nodes_with_anomalies:
            # Check if Global has valid data (not "?" or missing)
            global_state = period_anomalies.get("Global", "?")
            print(f"🔍 DEBUG GLOBAL STATE: global_state='{global_state}', period_anomalies keys: {list(period_anomalies.keys())}")
            
            # Always recalculate Global's anomaly state based on deviation (override detector's decision)
            global_deviation = period_deviations.get("Global", 0.0)
            print(f"🔍 DEBUG GLOBAL CALCULATION: global_deviation={global_deviation}")
            if global_deviation > 0:
                global_state = "+"  # Positive anomaly
            elif global_deviation < 0:
                global_state = "-"  # Negative anomaly
            else:
                global_state = "N"  # Neutral (only when deviation is exactly 0)
            # Always update Global in period_anomalies with calculated state
            period_anomalies["Global"] = global_state
            print(f"      🔍 DEBUG GLOBAL: Override Global state='{global_state}' based on deviation={global_deviation}")
            
            if "Global" not in nodes_with_anomalies and global_state != "?":
                # Add Global to the analysis even if it doesn't have anomalies but has valid data
                nodes_with_anomalies.append("Global")
                print(f"🔍 ENHANCED: Analyzing {len(nodes_with_anomalies)} segments (added Global with state '{global_state}' + {len([n for n in nodes_with_anomalies if n != 'Global'])} anomalous nodes)", file=sys.stderr)
            elif "Global" in nodes_with_anomalies:
                print(f"🔍 📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (including Global)", file=sys.stderr)
            else:
                print(f"🔍 📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (Global has no valid data)", file=sys.stderr)
            
            # PRIORITY: Move Global to the front to ensure it's always processed first
            if "Global" in nodes_with_anomalies:
                nodes_with_anomalies.remove("Global")
                nodes_with_anomalies.insert(0, "Global")
                print(f"🎯 PRIORITY: Global moved to front of processing queue", file=sys.stderr)

        if nodes_with_anomalies:
            # DEBUG: Temporarily NOT suppressing output to see what explanations are being collected
            print(f"🔍 DEBUG: Collecting explanations for {len(nodes_with_anomalies)} anomalous nodes: {nodes_with_anomalies}", file=sys.stderr)
            # with open(os.devnull, 'w') as devnull:
            #     with redirect_stdout(devnull), redirect_stderr(devnull):
            if True:  # Changed from suppressed context
                    for node_path in nodes_with_anomalies:
                        try:
                            anomaly_state = period_anomalies.get(node_path, "?")
                            
                            # For Global node, determine anomaly state based on sign of change (using same nomenclature as other nodes)
                            if node_path == "Global" and anomaly_state == "?":
                                # Get deviation value to determine type
                                deviation_value = period_deviations.get(node_path, 0.0)
                                if deviation_value > 0:
                                    anomaly_state = "+"  # Positive anomaly
                                elif deviation_value < 0:
                                    anomaly_state = "-"  # Negative anomaly
                                else:
                                    anomaly_state = "N"  # Neutral
                            
                            # Calculate correct date range if analysis_date is available
                            start_date, end_date = None, None
                            analysis_date = analysis_data.get('analysis_date')
                            if analysis_date:
                                print(f"🔍 DEBUG SINGLE_MODE_DATES: analysis_date={analysis_date}, period={period}, aggregation_days={aggregation_days}")
                                start_date, end_date = calculate_period_date_range(analysis_date, period, aggregation_days)
                                print(f"🔍 DEBUG SINGLE_MODE_DATES: calculated start_date={start_date}, end_date={end_date}")
                            
                            # Build NPS context for the causal agent and calculate anomaly magnitude
                            nps_context = ""
                            anomaly_magnitude = 0.0
                            print(f"🔍 DEBUG SILENT_ANOMALY NPS BUILD: period_nps_values keys: {list(period_nps_values.keys()) if period_nps_values else 'None'}", file=sys.stderr)
                            print(f"🔍 DEBUG SILENT_ANOMALY NPS BUILD: Looking for node_path: {node_path}", file=sys.stderr)
                            if period_nps_values and node_path in period_nps_values:
                                nps_data = period_nps_values[node_path]
                                print(f"🔍 DEBUG SILENT_ANOMALY Causal agent NPS for {node_path}: {nps_data}", file=sys.stderr)
                                if isinstance(nps_data, dict):
                                    current_nps = nps_data.get('current', 'N/A')
                                    baseline_nps = nps_data.get('baseline', 'N/A')
                                    nps_context = f"Current NPS: {current_nps}, Baseline NPS: {baseline_nps}"
                                    
                                    # Generate comparison context
                                    comparison_context = generate_comparison_context(
                                        analysis_data.get('anomaly_detection_mode', 'target'), 
                                        analysis_data.get('aggregation_days', 7),
                                        analysis_data.get('baseline_periods', 7)
                                    )
                                    
                                    # Calculate anomaly magnitude from NPS values
                                    if isinstance(current_nps, (int, float)) and isinstance(baseline_nps, (int, float)):
                                        anomaly_magnitude = current_nps - baseline_nps
                                else:
                                    nps_context = f"NPS: {nps_data}"
                            else:
                                print(f"🔍 DEBUG SILENT_ANOMALY Causal agent NO NPS for {node_path}", file=sys.stderr)
                            
                            explanation = await asyncio.wait_for(
                                interpreter.explain_anomaly(
                                    node_path=node_path,
                                    target_period=period,
                                    aggregation_days=aggregation_days,
                                    anomaly_state=anomaly_state,
                                    anomaly_magnitude=anomaly_magnitude,  # ✅ Now passing anomaly magnitude
                                    start_date=start_date,
                                    end_date=end_date,
                                    nps_context=nps_context,  # ✅ Now passing NPS context
                                    causal_filter=causal_filter,
                                    comparison_start_date=comparison_start_date,
                                    comparison_end_date=comparison_end_date,
                                    # New parameters for enriched context
                                    anomaly_detection_mode=analysis_data.get('anomaly_detection_mode', 'target'),
                                    comparison_context=comparison_context,
                                    baseline_periods=analysis_data.get('baseline_periods', 7)
                                ),
                                timeout=1500.0  # 25 minutes for complex Claude Sonnet 4 analysis
                            )
                            explanations[node_path] = explanation
                            print(f"🔍 EXPLANATION COLLECTED for {node_path}: {len(explanation) if explanation else 0} chars", file=sys.stderr)
                            if explanation:
                                print(f"   Preview: {explanation[:300]}...", file=sys.stderr)
                        except Exception:
                            explanations[node_path] = "Analysis timeout"
        
        # Show the tree
        analysis_date = analysis_data.get('analysis_date')
        date_parameter = analysis_data.get('date_parameter')
        await print_enhanced_tree_with_explanations_and_interpretations(
            period_anomalies, period_deviations, explanations, parent_interpretations,
            aggregation_days, period, date_range, segment, analysis_date, date_parameter
        )
        
        # AI Interpretation
        ai_interpretation = None
        if ai_available:
            print(f"\n🤖 AI INTERPRETATION:")
            print("-" * 40)
            
            try:
                # Check if we have causal agent explanations that should go directly to interpreter
                causal_explanations = {}
                for node_path, explanation in explanations.items():
                    if explanation and ("🤖 **AGENT CAUSAL ANALYSIS**" in explanation or "AI Causal Investigation:" in explanation):
                        # This is a full causal agent explanation - pass it directly
                        if "🤖 **AGENT CAUSAL ANALYSIS**" in explanation:
                            clean_explanation = explanation.replace("🤖 **AGENT CAUSAL ANALYSIS**\n", "").strip()
                        else:
                            clean_explanation = explanation.replace("• AI Causal Investigation:", "").strip()
                        causal_explanations[node_path] = clean_explanation
                
                if causal_explanations:
                    # Use direct causal agent explanation instead of tree format
                    print("🔍 Using direct causal agent explanation for tree interpretation")
                    
                    # For single node with causal explanation, pass it directly
                    if len(causal_explanations) == 1:
                        node_path, causal_explanation = next(iter(causal_explanations.items()))
                        
                        ai_interpretation = await asyncio.wait_for(
                            ai_agent.interpret_anomaly_tree(causal_explanation, 
                                                           start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                            timeout=600.0
                        )
                    else:
                        # Multiple causal explanations - combine them
                        combined_explanation = f"Multiple anomalous nodes analyzed:\n\n"
                        for node_path, explanation in causal_explanations.items():
                            combined_explanation += f"NODO: {node_path}\n{explanation}\n\n"
                        
                        ai_interpretation = await asyncio.wait_for(
                            ai_agent.interpret_anomaly_tree(combined_explanation, 
                                                           start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                            timeout=600.0
                        )
                else:
                    # Fallback to tree format for non-causal explanations
                    ai_input = build_ai_input_string(period, period_anomalies, period_deviations, 
                                                     parent_interpretations, explanations, date_range, segment, period_nps_values)
                    
                    debug_print(f"AI input string length: {len(ai_input)} characters")
                    debug_print(f"AI input preview: {ai_input[:500]}...")
                    
                    # Fix: Extract start_date from date_range if available
                    date_param = None
                    if date_range and len(date_range) >= 2:
                        range_start_date, _ = date_range
                        if range_start_date:
                            date_param = range_start_date.strftime('%Y-%m-%d')
                    
                    ai_interpretation = await asyncio.wait_for(
                        ai_agent.interpret_anomaly_tree(ai_input, date_param, segment),
                        timeout=600.0
                    )
                
                print(ai_interpretation)
                
            except Exception as e:
                ai_interpretation = f"AI interpretation failed: {str(e)}"
                print(ai_interpretation)
        
        # Collect period data for summary
        period_data = {
            'period': period,
            'date_range': date_range_str,
            'ai_interpretation': ai_interpretation or "No AI interpretation available"
        }
        all_periods_data.append(period_data)
    
    return all_periods_data

async def show_clean_anomaly_analysis(analysis_data: dict, segment: str = "Global", causal_filter: str = "vs L7d"):
    """Show clean, focused analysis: tree + agent workflow + summary"""
    from contextlib import redirect_stdout, redirect_stderr
    import os
    
    detector = analysis_data['detector']
    data_folder = analysis_data['data_folder']
    aggregation_days = analysis_data['aggregation_days']
    anomaly_periods = analysis_data['anomaly_periods']
    periods_analyzed = analysis_data.get('periods_analyzed', anomaly_periods)
    
    # Initialize interpreter for explanations
    pbi_collector = PBIDataCollector()
    interpreter = FlexibleAnomalyInterpreter(data_folder, pbi_collector=pbi_collector, silent_mode=True, causal_filter=causal_filter)
    
    # Initialize AI agent for interpretation
    try:
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_interpreter_agent import AnomalyInterpreterAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType, get_default_llm_type
        
        ai_agent = AnomalyInterpreterAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml",
            logger=logging.getLogger("ai_interpreter"),
            study_mode="comparative"
        )
        ai_available = True
    except Exception:
        ai_available = False
    
    # Show only periods with anomalies
    periods_with_anomalies = [p for p in periods_analyzed if p in anomaly_periods]
    
    all_periods_data = []
    
    for period in periods_with_anomalies:
        print(f"\n{'='*60}")
        print(f"📊 PERIOD {period} ANALYSIS")
        print("="*60)
        
        # Get anomalies for this period
        analysis_date = analysis_data.get('analysis_date')
        period_anomalies, period_deviations, _, _ = await detector.analyze_period(data_folder, period, analysis_date)
        
        # Calculate date range
        date_parameter = analysis_data.get('date_parameter')
        if analysis_date and date_parameter in ['flight_local', 'available']:
            start_date, end_date = calculate_period_date_range(analysis_date, period, aggregation_days)
            date_range = (start_date, end_date)
        else:
            date_range = interpreter._get_period_date_range(period, aggregation_days)
        
        if date_range:
            start_date, end_date = date_range
            print(f"📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        else:
            date_range_str = "Unknown dates"
        
        # Generate parent interpretations
        parent_interpretations = generate_parent_interpretations(period_anomalies)
        
        # Show the clean tree first
        print(f"\n🌳 ANOMALY TREE:")
        print("-" * 40)
        await print_clean_tree_only(period_anomalies, period_deviations, parent_interpretations, segment, None)
        
        # Collect explanations and show agent workflow SILENTLY for anomalous nodes
        explanations = {}
        workflow_decisions = {}
        nodes_with_anomalies = [node for node, state in period_anomalies.items() if state in ['+', '-']]

        # ENHANCEMENT: Always include Global segment in causal analysis if it has valid data
        if nodes_with_anomalies:
            # Check if Global has valid data (not "?" or missing)
            global_state = period_anomalies.get("Global", "?")
            print(f"🔍 DEBUG GLOBAL STATE: global_state='{global_state}', period_anomalies keys: {list(period_anomalies.keys())}")
            
            # Always recalculate Global's anomaly state based on deviation (override detector's decision)
            global_deviation = period_deviations.get("Global", 0.0)
            print(f"🔍 DEBUG GLOBAL CALCULATION: global_deviation={global_deviation}")
            if global_deviation > 0:
                global_state = "+"  # Positive anomaly
            elif global_deviation < 0:
                global_state = "-"  # Negative anomaly
            else:
                global_state = "N"  # Neutral (only when deviation is exactly 0)
            # Always update Global in period_anomalies with calculated state
            period_anomalies["Global"] = global_state
            print(f"      🔍 DEBUG GLOBAL: Override Global state='{global_state}' based on deviation={global_deviation}")
            
            if "Global" not in nodes_with_anomalies and global_state != "?":
                # Add Global to the analysis even if it doesn't have anomalies but has valid data
                nodes_with_anomalies.append("Global")
                print(f"🔍 ENHANCED: Analyzing {len(nodes_with_anomalies)} segments (added Global with state '{global_state}' + {len([n for n in nodes_with_anomalies if n != 'Global'])} anomalous nodes)")
            elif "Global" in nodes_with_anomalies:
                print(f"📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (including Global)")
            else:
                print(f"📊 Analyzing {len(nodes_with_anomalies)} anomalous segments (Global has no valid data)")
            
            # PRIORITY: Move Global to the front to ensure it's always processed first
            if "Global" in nodes_with_anomalies:
                nodes_with_anomalies.remove("Global")
                nodes_with_anomalies.insert(0, "Global")
                print(f"🎯 PRIORITY: Global moved to front of processing queue")

        if nodes_with_anomalies:
            print(f"\n🤖 AGENT WORKFLOW ANALYSIS:")
            print("-" * 40)
            
            for node_path in nodes_with_anomalies:
                print(f"\n📋 Analyzing: {node_path}")
                
                try:
                    anomaly_state = period_anomalies.get(node_path, "?")
                    deviation = period_deviations.get(node_path, 0)
                    
                    # For Global node, determine anomaly state based on sign of change (using same nomenclature as other nodes)
                    if node_path == "Global" and anomaly_state == "?":
                        if deviation > 0:
                            anomaly_state = "+"  # Positive anomaly
                        elif deviation < 0:
                            anomaly_state = "-"  # Negative anomaly
                        else:
                            anomaly_state = "N"  # Neutral
                    
                    # Calculate anomaly magnitude from deviation since NPS values not available
                    anomaly_magnitude = deviation
                    
                    # Collect explanation with agent workflow info
                    start_date, end_date = None, None
                    if analysis_date:
                        start_date, end_date = calculate_period_date_range(analysis_date, period, aggregation_days)
                    
                    # Capture workflow info during explanation
                    explanation = await asyncio.wait_for(
                        interpreter.explain_anomaly(
                            node_path=node_path,
                            target_period=period,
                            aggregation_days=aggregation_days,
                            anomaly_state=anomaly_state,
                            anomaly_magnitude=anomaly_magnitude,  # ✅ Now passing anomaly magnitude
                            start_date=start_date,
                            end_date=end_date
                        ),
                        timeout=600.0
                    )
                    
                    explanations[node_path] = explanation
                    
                    # Show clean summary of the explanation
                    if explanation and "🤖 **AGENT CAUSAL ANALYSIS**" in explanation:
                        clean_explanation = explanation.split("🤖 **AGENT CAUSAL ANALYSIS**\n")[1]
                        print(f"   📊 Result: {clean_explanation[:200]}...")
                    
                except Exception as e:
                    explanations[node_path] = f"Analysis failed: {str(e)}"
                    print(f"   ❌ Analysis failed: {str(e)}")
        
        # AI Tree Interpretation
        if ai_available and explanations:
            print(f"\n🧠 TREE INTERPRETER SUMMARY:")
            print("-" * 40)
            
            try:
                # Check if we have causal agent explanations that should go directly to interpreter
                causal_explanations = {}
                for node_path, explanation in explanations.items():
                    if explanation and ("🤖 **AGENT CAUSAL ANALYSIS**" in explanation or "AI Causal Investigation:" in explanation):
                        # This is a full causal agent explanation - pass it directly
                        if "🤖 **AGENT CAUSAL ANALYSIS**" in explanation:
                            clean_explanation = explanation.replace("🤖 **AGENT CAUSAL ANALYSIS**\n", "").strip()
                        else:
                            clean_explanation = explanation.replace("• AI Causal Investigation:", "").strip()
                        causal_explanations[node_path] = clean_explanation
                
                if causal_explanations:
                    # Use direct causal agent explanation instead of tree format
                    print("🔍 Using direct causal agent explanation for tree interpretation")
                    
                    # For single node with causal explanation, pass it directly
                    if len(causal_explanations) == 1:
                        node_path, causal_explanation = next(iter(causal_explanations.items()))
                        
                        ai_interpretation = await asyncio.wait_for(
                            ai_agent.interpret_anomaly_tree(causal_explanation, 
                                                           start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                            timeout=600.0
                        )
                    else:
                        # Multiple causal explanations - detect parent-child relationships for intelligent consolidation
                        relationships = detect_parent_child_relationships(list(causal_explanations.keys()))
                        
                        # Prepare hierarchical explanation format with NPS values
                        hierarchical_explanation = "Análisis jerárquico de anomalías de NPS:\n\n"
                        
                        # Helper function to get NPS info for a node
                        def get_nps_info(node_path):
                            # NPS values not available in this context
                            return ""
                        
                        # Group explanations by relationships
                        processed_groups = set()
                        
                        for node_path, rel_info in relationships.items():
                            # Skip if already processed as part of another group
                            group_key = tuple(sorted(rel_info['all_related']))
                            if group_key in processed_groups:
                                continue
                            processed_groups.add(group_key)
                            
                            if rel_info['type'] == 'parent' and len(rel_info['children']) > 0:
                                # Parent-child group
                                hierarchical_explanation += f"GRUPO JERÁRQUICO: {node_path} + HIJOS\n"
                                hierarchical_explanation += f"NODO PADRE: {node_path}{get_nps_info(node_path)}\n{causal_explanations.get(node_path, 'No disponible')}\n\n"
                                
                                for child_node in rel_info['children']:
                                    hierarchical_explanation += f"NODO HIJO: {child_node}{get_nps_info(child_node)}\n{causal_explanations.get(child_node, 'No disponible')}\n\n"
                            else:
                                # Standalone node
                                hierarchical_explanation += f"NODO INDEPENDIENTE: {node_path}{get_nps_info(node_path)}\n{causal_explanations[node_path]}\n\n"
                        
                        print(f"🔍 Clean analysis: Sending hierarchical tree to AI: {len(hierarchical_explanation)} chars")
                        
                        # Use the new hierarchical analysis method
                        # For weekly analysis, we need to pass the date range
                        if date_range and start_date and end_date:
                            date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
                        else:
                            date_range_str = start_date.strftime('%Y-%m-%d') if date_range else None
                        
                        ai_interpretation = await asyncio.wait_for(
                            ai_agent.interpret_anomaly_tree_hierarchical(hierarchical_explanation, 
                                                           date_range_str, segment),
                            timeout=600.0  # 10 minutes for O3 with conversational steps
                        )
                else:
                    # Fallback to tree format for non-causal explanations
                    ai_input = build_ai_input_string(period, period_anomalies, period_deviations, 
                                                   parent_interpretations, explanations, date_range, segment, None)
                    
                    ai_interpretation = await asyncio.wait_for(
                        ai_agent.interpret_anomaly_tree(ai_input, 
                                                       start_date.strftime('%Y-%m-%d') if date_range else None, segment),
                        timeout=600.0
                    )
                
                print(ai_interpretation)
                
            except Exception as e:
                print(f"❌ Tree interpretation failed: {str(e)}")
        
        # Collect period data for final summary
        period_data = {
            'period': period,
            'date_range': date_range_str,
            'ai_interpretation': ai_interpretation if 'ai_interpretation' in locals() else "No interpretation available"
        }
        all_periods_data.append(period_data)
    
    return all_periods_data

async def print_clean_tree_only(anomalies: dict, deviations: dict, interpretations: dict, segment_filter: str = "Global", nps_values: dict = None):
    """Print only the tree structure without explanations"""
    
    def get_state_description(state):
        if state == '+':
            return "POSITIVE ANOMALY"
        elif state == '-':
            return "NEGATIVE ANOMALY"
        else:
            return "Normal"
    
    def get_deviation_text(node_path):
        deviation = deviations.get(node_path, 0)
        deviation_text = f" ({deviation:+.1f} pts)" if deviation != 0 else ""
        
        # Add NPS values if available - show them more prominently
        nps_info = ""
        if nps_values and node_path in nps_values:
            nps_data = nps_values[node_path]
            if isinstance(nps_data, dict):
                current_nps = nps_data.get('current', 'N/A')
                baseline_nps = nps_data.get('baseline', 'N/A')
                if isinstance(current_nps, (int, float)) and isinstance(baseline_nps, (int, float)):
                    difference = current_nps - baseline_nps
                    nps_info = f" [NPS: {current_nps:.1f} vs {baseline_nps:.1f}, diff: {difference:+.1f}]"
                else:
                    nps_info = f" [NPS: {current_nps} vs {baseline_nps}]"
            else:
                nps_info = f" [NPS: {nps_data}]"
        
        return deviation_text + nps_info
    
    def print_interpretation(node_path, indent=""):
        interp = interpretations.get(node_path, "")
        if interp:
            print(f"{indent}  └─ Pattern: {interp}")
    
    # Print tree based on segment filter
    if segment_filter == "Global":
        print_full_tree_clean(anomalies, get_state_description, get_deviation_text, print_interpretation)
    elif segment_filter == "Global/LH":
        print_lh_tree_clean(anomalies, get_state_description, get_deviation_text, print_interpretation)
    elif segment_filter == "Global/SH":
        print_sh_tree_clean(anomalies, get_state_description, get_deviation_text, print_interpretation)
    else:
        print_single_node_clean(segment_filter, anomalies, get_state_description, get_deviation_text, print_interpretation)

def print_full_tree_clean(anomalies, get_state_description, get_deviation_text, print_interpretation):
    """Print clean full tree without explanations"""
    # Global
    global_state = get_state_description(anomalies.get("Global", "?"))
    global_dev = get_deviation_text("Global")
    print(f"Global: {global_state}{global_dev}")
    print_interpretation("Global", "")
    
    # LH branch
    lh_state = get_state_description(anomalies.get("Global/LH", "?"))
    lh_dev = get_deviation_text("Global/LH")
    print(f"├─ Long Haul (LH): {lh_state}{lh_dev}")
    print_interpretation("Global/LH", "│")
    
    lh_cabins = ["Economy", "Business", "Premium"]
    for i, cabin in enumerate(lh_cabins):
        node = f"Global/LH/{cabin}"
        if node in anomalies:
            state = get_state_description(anomalies[node])
            dev = get_deviation_text(node)
            print(f"│  ├── {cabin}: {state}{dev}")
            print_interpretation(node, "│  ")
    
    # SH branch
    sh_state = get_state_description(anomalies.get("Global/SH", "?"))
    sh_dev = get_deviation_text("Global/SH")
    print(f"└─ Short Haul (SH): {sh_state}{sh_dev}")
    print_interpretation("Global/SH", " ")
    
    # SH children
    for cabin in ["Economy", "Business"]:
        node = f"Global/SH/{cabin}"
        if node in anomalies:
            state = get_state_description(anomalies[node])
            dev = get_deviation_text(node)
            print(f"   ├── {cabin}: {state}{dev}")
            print_interpretation(node, "   ")
            
            # Show company breakdown for SH
            for company in ["IB", "YW"]:
                company_node = f"{node}/{company}"
                if company_node in anomalies:
                    comp_state = get_state_description(anomalies[company_node])
                    comp_dev = get_deviation_text(company_node)
                    print(f"   │  ├──── {company}: {comp_state}{comp_dev}")
                    print_interpretation(company_node, "   │  ")

def print_lh_tree_clean(anomalies, get_state_description, get_deviation_text, print_interpretation):
    """Print clean LH tree"""
    lh_state = get_state_description(anomalies.get("Global/LH", "?"))
    lh_dev = get_deviation_text("Global/LH")
    print(f"Long Haul (LH): {lh_state}{lh_dev}")
    print_interpretation("Global/LH", "")
    
    for cabin in ["Economy", "Business", "Premium"]:
        node = f"Global/LH/{cabin}"
        if node in anomalies:
            state = get_state_description(anomalies[node])
            dev = get_deviation_text(node)
            print(f"├── {cabin}: {state}{dev}")
            print_interpretation(node, "")

def print_sh_tree_clean(anomalies, get_state_description, get_deviation_text, print_interpretation):
    """Print clean SH tree"""
    sh_state = get_state_description(anomalies.get("Global/SH", "?"))
    sh_dev = get_deviation_text("Global/SH")
    print(f"Short Haul (SH): {sh_state}{sh_dev}")
    print_interpretation("Global/SH", "")
    
    for cabin in ["Economy", "Business"]:
        node = f"Global/SH/{cabin}"
        if node in anomalies:
            state = get_state_description(anomalies[node])
            dev = get_deviation_text(node)
            print(f"├── {cabin}: {state}{dev}")
            print_interpretation(node, "")
            
            for company in ["IB", "YW"]:
                company_node = f"{node}/{company}"
                if company_node in anomalies:
                    comp_state = get_state_description(anomalies[company_node])
                    comp_dev = get_deviation_text(company_node)
                    print(f"│  ├──── {company}: {comp_state}{comp_dev}")
                    print_interpretation(company_node, "│  ")

def print_single_node_clean(node_path, anomalies, get_state_description, get_deviation_text, print_interpretation):
    """Print single node clean"""
    if node_path in anomalies:
        state = get_state_description(anomalies[node_path])
        dev = get_deviation_text(node_path)
        node_name = node_path.split('/')[-1] if '/' in node_path else node_path
        print(f"{node_name}: {state}{dev}")
        print_interpretation(node_path, "")

async def generate_consolidated_summary(agent, consolidated_data: List[Dict], date_flight_local: str = None) -> str:
    """Generate a consolidated summary from multiple analysis types including weekly comparative and daily single analyses."""
    
    # Extract weekly comparative and daily single analyses
    weekly_comparative_analysis = ""
    daily_single_analyses = []
    
    for data in consolidated_data:
        analysis_type = data['analysis_type']
        
        if analysis_type == 'SEMANAL_COMPARATIVO':
            # Weekly comparative analysis
            periods_count = data['periods']
            summary_data = data['summary']
            
            weekly_section = f"=== ANÁLISIS SEMANAL COMPARATIVO ===\n"
            weekly_section += f"Períodos analizados: {periods_count} semanas\n"
            weekly_section += f"Modo: Comparative (vs Sel. Period)\n"
            weekly_section += f"Detección: vslast\n\n"
            
            for period_data in summary_data:
                period = period_data['period']
                date_range = period_data['date_range']
                interpretation = period_data['ai_interpretation']
                
                weekly_section += f"Período {period} ({date_range}):\n{interpretation}\n\n"
            
            weekly_comparative_analysis = weekly_section
            
        elif analysis_type == 'DIARIO_SINGLE':
            # Daily single analysis
            anomalous_days = data['anomalous_days']
            
            for day_data in anomalous_days:
                day = day_data['day']
                date = day_data['date']
                analysis = day_data['analysis']
                
                # Extract anomalies from the analysis if available
                anomalies = []
                if 'anomalías detectadas' in analysis.lower() or 'anomaly' in analysis.lower():
                    # Try to extract anomaly information
                    lines = analysis.split('\n')
                    for line in lines:
                        if any(keyword in line.lower() for keyword in ['anomalía', 'anomaly', 'negativa', 'positiva']):
                            anomalies.append(line.strip())
                
                daily_single_analyses.append({
                    'date': date,
                    'analysis': analysis,
                    'anomalies': anomalies
                })
    
    # Use the new comprehensive summary method
    if weekly_comparative_analysis and daily_single_analyses:
        # DEBUG: Show what data is being passed to summary agent
        print(f"🔍 DEBUG SUMMARY AGENT INPUT:", file=sys.stderr)
        print(f"   Weekly analysis length: {len(weekly_comparative_analysis)}", file=sys.stderr)
        print(f"   Daily analyses count: {len(daily_single_analyses)}", file=sys.stderr)
        print(f"   Weekly preview: {weekly_comparative_analysis[:200]}...", file=sys.stderr)
        for i, daily in enumerate(daily_single_analyses[:3]):
            print(f"   Daily {i+1} - Date: {daily.get('date', 'Unknown')}", file=sys.stderr)
            print(f"   Daily {i+1} - Analysis length: {len(daily.get('analysis', ''))}", file=sys.stderr)
            print(f"   Daily {i+1} - Preview: {daily.get('analysis', '')[:200]}...", file=sys.stderr)
        
        try:
            comprehensive_summary = await asyncio.wait_for(
                agent.generate_comprehensive_summary(
                    weekly_comparative_analysis=weekly_comparative_analysis,
                    daily_single_analyses=daily_single_analyses,
                    date_flight_local=date_flight_local
                ),
                timeout=600.0  # 10 minute timeout for comprehensive summary
            )
            return comprehensive_summary
        except Exception as e:
            print(f"⚠️ Error using comprehensive mode, falling back to legacy: {str(e)}")
    else:
        # DEBUG: Show why comprehensive mode is not being used
        print(f"🔍 DEBUG SUMMARY AGENT MISSING DATA:", file=sys.stderr)
        print(f"   Has weekly analysis: {bool(weekly_comparative_analysis)}", file=sys.stderr)
        print(f"   Has daily analyses: {bool(daily_single_analyses)}", file=sys.stderr)
        if weekly_comparative_analysis:
            print(f"   Weekly length: {len(weekly_comparative_analysis)}", file=sys.stderr)
        if daily_single_analyses:
            print(f"   Daily count: {len(daily_single_analyses)}", file=sys.stderr)
        else:
            print(f"   Daily analyses is empty/None", file=sys.stderr)
    
    # Fallback to legacy format if comprehensive mode fails
    formatted_sections = []
    
    for data in consolidated_data:
        analysis_type = data['analysis_type']
        
        if analysis_type == 'SEMANAL_COMPARATIVO':
            # Weekly comparative analysis
            periods_count = data['periods']
            summary_data = data['summary']
            
            # Create section with proper indentation
            section = f"\n=== ANÁLISIS SEMANAL COMPARATIVO ===\n"
            section += f"Períodos analizados: {periods_count} semanas\n"
            section += f"Modo: Comparative (vs Sel. Period)\n"
            section += f"Detección: vslast\n\n"
            
            for period_data in summary_data:
                period = period_data['period']
                date_range = period_data['date_range']
                interpretation = period_data['ai_interpretation']
                
                section += f"Período {period} ({date_range}):\n{interpretation}\n\n"
            
            formatted_sections.append(section)
            
        elif analysis_type == 'DIARIO_SINGLE':
            # Daily single analysis
            anomalous_days = data['anomalous_days']
            summary = data['summary']
            
            section = f"\n=== ANÁLISIS DIARIO SINGLE ===\n"
            section += f"{summary}\n"
            section += f"Modo: Single (sin comparación)\n"
            section += f"Detección: mean\n\n"
            
            for day_data in anomalous_days:
                day = day_data['day']
                date = day_data['date']
                analysis = day_data['analysis']
                
                section += f"Día {day} ({date}):\n{analysis}\n\n"
            
            formatted_sections.append(section)
            
        else:
            # Legacy format for backward compatibility
            periods_count = data.get('periods', 0)
            summary_data = data.get('summary', [])
        
        section = f"\n=== ANÁLISIS {analysis_type} ===\n"
        section += f"Períodos analizados: {periods_count}\n\n"
        
        for period_data in summary_data:
            period = period_data['period']
            date_range = period_data['date_range']
            interpretation = period_data['ai_interpretation']
            
            section += f"Período {period} ({date_range}):\n{interpretation}\n\n"
        
        formatted_sections.append(section)
    
    # Create consolidated input
    consolidated_input = "\n".join(formatted_sections)
    
    # Create enhanced prompt for comprehensive analysis
    enhanced_prompt = f"""
    Eres un analista experto en NPS (Net Promoter Score) que debe generar un reporte ejecutivo consolidado.

    Has recibido los siguientes análisis:

    {consolidated_input}

    Por favor, genera un reporte ejecutivo consolidado que incluya:

    1. **RESUMEN EJECUTIVO**: Principales hallazgos y anomalías detectadas
    2. **ANÁLISIS SEMANAL**: Tendencias y patrones semanales identificados
    3. **ANÁLISIS DIARIO**: Días específicos con anomalías y sus causas
    4. **CAUSAS PRINCIPALES**: Factores más relevantes que explican las anomalías
    5. **IMPACTO**: Efecto en el NPS y la experiencia del cliente
    6. **RUTAS CRÍTICAS**: Touchpoints más afectados

    El reporte debe ser:
    - Claro y conciso
    - Orientado a la acción
    - Con datos específicos cuando estén disponibles
    - Estructurado para facilitar la toma de decisiones

    Formato el reporte con emojis y secciones claras para facilitar la lectura.
    """
    
    # Use the enhanced prompt
    message_history = agent._get_message_history_for_consolidated(enhanced_prompt)
    
    response, _, _ = await agent.agent.invoke(messages=message_history.get_messages())
    return response.content.strip()

async def main():
    """Enhanced main entry point for comprehensive anomaly analysis"""
    print("🚀 Enhanced Flexible NPS Anomaly Detection System")
    print("=" * 60)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Enhanced Flexible NPS Anomaly Detection')
    parser.add_argument('--mode', choices=['download', 'analyze', 'both', 'comprehensive'], default='comprehensive',
                       help='Mode: download data, analyze existing data, both, or comprehensive (daily + weekly)')
    parser.add_argument('--study-mode', choices=['single', 'comparative'], default='comparative',
                       help='Analysis mode: single (no comparison) or comparative (with comparison). Default: comparative')
    parser.add_argument('--folder', type=str, 
                       help='Specific folder to analyze (e.g., tables/available_2025_06_04)')
    parser.add_argument('--aggregation-days', type=int, default=1,
                       help='Number of days per aggregation period (default: 1)')
    parser.add_argument('--periods', type=int, default=74, help="Number of periods to download/analyze")
    
    # New date-related parameters - clearer logic
    parser.add_argument('--insert-date-ci', type=str,
                       help='Simulate today being this date (YYYY-MM-DD). Data available until this date - 4 days')
    parser.add_argument('--date-flight-local', type=str,
                       help='Use this date directly as available in dashboard (YYYY-MM-DD)')
    
    # New segment parameter for focused analysis
    parser.add_argument('--segment', type=str, default='Global',
                       help='Root segment to analyze (e.g., Global, SH, Global/SH/Economy, Global/LH). Default: Global (full tree)')
    
    # Anomaly detection mode parameter
    parser.add_argument('--anomaly-detection-mode', choices=['target', 'mean', 'vslast'], default='target',
                       help='Anomaly detection mode: target (uses monthly targets), mean (uses mean of last n periods), or vslast (compares against previous period). Default: target')
    parser.add_argument('--baseline-periods', type=int, default=7,
                       help='Number of previous periods to use as a baseline for "mean" anomaly detection')
    
    # Causal comparison filter parameters
    parser.add_argument('--causal-filter-comparison',
                        type=str,
                        default="vs L7d",
                        help='Causal filter for comparative analysis (e.g., "vs L7d", "vs LM", "vs LY", "vs Target", "vs Sel. Period")')
    parser.add_argument('--causal-comparison-dates', nargs=2, metavar=('START_DATE', 'END_DATE'),
                        help='Comparison period dates (YYYY-MM-DD YYYY-MM-DD) when using --causal-filter-comparison "vs Sel. Period"')
    
    # Debug mode parameter
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode with verbose print statements')
    
    # Explanation mode parameter
    parser.add_argument('--explanation-mode', choices=['raw', 'agent'], default='agent',
                       help='Explanation mode: raw (detailed data dumps) or agent (intelligent causal analysis). Default: agent')
    
    # Clean output mode parameter
    parser.add_argument('--clean', action='store_true',
                       help='Enable clean output mode: shows only tree, workflow decisions, and summary (suppresses verbose logs)')
    
    # Interpreter debug mode parameter
    parser.add_argument('--debug-interpreter', type=str, metavar='JSON_FILE',
                        help='Debug interpreter agent only using saved hierarchical data from specified JSON file')
    
    args = parser.parse_args()

    # Add placeholders for arguments that might not be defined by the parser in all cases
    if not hasattr(args, 'comparison_start_date'):
        args.comparison_start_date = None
    if not hasattr(args, 'comparison_end_date'):
        args.comparison_end_date = None
    
    # Set global debug mode based on flag
    global DEBUG_MODE
    DEBUG_MODE = args.debug
    
    if DEBUG_MODE:
        print("🔍 DEBUG MODE ENABLED - Verbose output activated")
    
    # Calculate the analysis start date based on date parameters
    today = datetime.now().date()
    pbi_lag_days = 4  # PBI dashboard has 4-day lag
    
    # Determine which date parameter was used
    if args.insert_date_ci and args.date_flight_local:
        print("❌ Error: Cannot specify both --insert-date-ci and --date-flight-local. Choose one.")
        return
    elif args.insert_date_ci:
        try:
            simulated_today = datetime.strptime(args.insert_date_ci, '%Y-%m-%d').date()
            analysis_date = datetime.combine(simulated_today - timedelta(days=pbi_lag_days), datetime.min.time())  # Simulate 4-day lag
            date_parameter = 'insert_ci'
            date_description = f"Simulating today as {simulated_today.strftime('%Y-%m-%d')}"
        except ValueError:
            print("❌ Error: --insert-date-ci must be in YYYY-MM-DD format")
            return
    elif args.date_flight_local:
        try:
            analysis_date = datetime.strptime(args.date_flight_local, '%Y-%m-%d')
            date_parameter = 'flight_local'
            date_description = f"Using direct dashboard date"
        except ValueError:
            print("❌ Error: --date-flight-local must be in YYYY-MM-DD format")
            return
    else:
        # Default behavior: use available date (today - 4 days)
        analysis_date = datetime.combine(today - timedelta(days=pbi_lag_days), datetime.min.time())
        date_parameter = 'available'
        date_description = f"Using default available date (today - {pbi_lag_days} days)"
    
    # Display date information
    print(f"\n📅 DATE CONFIGURATION:")
    print(f"   • {date_description}")
    print(f"   • Analysis date: {analysis_date.strftime('%Y-%m-%d')}")
    if args.insert_date_ci:
        print(f"   • Note: Simulating {pbi_lag_days}-day lag from {args.insert_date_ci}")
    elif args.date_flight_local:
        print(f"   • Note: Using date directly from dashboard without lag simulation")
    
    # --- Date & Lag Configuration ---
    # ... (existing date logic) ...

    # --- Mode-Specific Configuration ---
    if args.mode != 'comprehensive':
        print("\n🔬 STUDY MODE CONFIGURATION:")
        # Determine study_mode automatically if not specified
        if not args.study_mode:
            if args.aggregation_days == 1:
                study_mode = "single"
            else:
                study_mode = "comparative"
        else:
            study_mode = args.study_mode
        
        print(f"   • Study mode: {study_mode.upper()}")
        
        # ... (rest of the existing configuration logic) ...
    
    # --- EXECUTION LOGIC ---
    try:
        # Handle comprehensive mode as a special, high-level orchestrator
        if args.mode == 'comprehensive':
            print("\n🔬 RUNNING COMPREHENSIVE ANALYSIS MODE")
            await run_comprehensive_analysis(
                analysis_date=analysis_date,
                date_parameter=date_parameter,
                segment=args.segment,
                explanation_mode=args.explanation_mode,
                daily_baseline_periods=args.baseline_periods,
                causal_filter=args.causal_filter_comparison,
                comparison_start_date=args.comparison_start_date,
                comparison_end_date=args.comparison_end_date,
                date_flight_local=args.date_flight_local
            )
            return
        
        # Handle flexible/both mode for custom analysis
        elif args.mode == 'both':
            print("\n🔬 RUNNING FLEXIBLE ANALYSIS MODE (custom parameters)")
            print("============================================================")
            await execute_analysis_flow(
                analysis_date=analysis_date,
                date_parameter=date_parameter,
                segment=args.segment,
                explanation_mode=args.explanation_mode,
                anomaly_detection_mode=args.anomaly_detection_mode,
                baseline_periods=args.baseline_periods,
                aggregation_days=args.aggregation_days,
                periods=args.periods,
                causal_filter=args.causal_filter_comparison,
                comparison_start_date=args.comparison_start_date,
                comparison_end_date=args.comparison_end_date,
                date_flight_local=args.date_flight_local,
                study_mode=args.study_mode
            )
            return
        
        # ... (rest of the execution logic for other modes) ...

    except KeyboardInterrupt:
        print("\n⏸️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        print(f"Debug info: {traceback.format_exc()}")

def print_full_tree(anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation):
    """Print the complete Global tree"""
    # Global summary
    global_state = anomalies.get("Global", "?")
    global_dev = get_deviation_text("Global")
    global_desc = get_state_description(global_state)
    
    print(f"Global: {global_desc} {global_dev}")
    actual_anomalies = [node for node, state in anomalies.items() if state in ['+', '-']]
    if global_state == "N" and actual_anomalies:
        print(f"  └─ Note: Global shows normal variation despite {len(actual_anomalies)} segment anomalies below")
    elif global_state in ["+", "-"]:
        print(f"  └─ Global anomaly detected: investigate segments below")
    print_interpretation("Global", "")
    if global_state in ["+", "-"]:
        print_explanation("Global", "")
    
    # Long Haul
    lh_state = anomalies.get("Global/LH", "?")
    lh_dev = get_deviation_text("Global/LH")
    lh_desc = get_state_description(lh_state)
    
    print(f"\n├─ Long Haul (LH): {lh_desc} {lh_dev}")
    print_interpretation("Global/LH", "│")
    if lh_state in ["+", "-"]:
        print_explanation("Global/LH", "│")
    
    lh_cabins = ["Economy", "Business", "Premium"]
    for i, cabin in enumerate(lh_cabins):
        cabin_path = f"Global/LH/{cabin}"
        cabin_state = anomalies.get(cabin_path, "?")
        cabin_dev = get_deviation_text(cabin_path)
        cabin_desc = get_state_description(cabin_state)
        
        connector = "├──" if i < len(lh_cabins) - 1 else "└──"
        print(f"│  {connector} {cabin}: {cabin_desc} {cabin_dev}")
        print_interpretation(cabin_path, "│  ")
        if cabin_state in ["+", "-"]:
            print_explanation(cabin_path, "│  ")
    
    # Short Haul
    sh_state = anomalies.get("Global/SH", "?")
    sh_dev = get_deviation_text("Global/SH")
    sh_desc = get_state_description(sh_state)
    
    print(f"\n└─ Short Haul (SH): {sh_desc} {sh_dev}")
    print_interpretation("Global/SH", " ")
    if sh_state in ["+", "-"]:
        print_explanation("Global/SH", "")
    
    sh_cabins = ["Economy", "Business"]
    for i, cabin in enumerate(sh_cabins):
        cabin_path = f"Global/SH/{cabin}"
        cabin_state = anomalies.get(cabin_path, "?")
        cabin_dev = get_deviation_text(cabin_path)
        cabin_desc = get_state_description(cabin_state)
        
        connector = "├──" if i < len(sh_cabins) - 1 else "└──"
        print(f"   {connector} {cabin}: {cabin_desc} {cabin_dev}")
        print_interpretation(cabin_path, "   ")
        if cabin_state in ["+", "-"]:
            print_explanation(cabin_path, "   ")
        
        # Company subdivisions for SH
        companies = ["IB", "YW"]
        for j, company in enumerate(companies):
            company_path = f"Global/SH/{cabin}/{company}"
            company_state = anomalies.get(company_path, "?")
            company_dev = get_deviation_text(company_path)
            company_desc = get_state_description(company_state)
            
            # Adjust indentation based on SH cabin position
            if i < len(sh_cabins) - 1:  # Not the last cabin
                company_connector = "├────" if j < len(companies) - 1 else "└────"
                print(f"   │  {company_connector} {company}: {company_desc} {company_dev}")
                company_indent = "   │  "
            else:  # Last cabin
                company_connector = "├────" if j < len(companies) - 1 else "└────"
                print(f"      {company_connector} {company}: {company_desc} {company_dev}")
                company_indent = "      "
            
            print_interpretation(company_path, company_indent)
            if company_state in ["+", "-"]:
                print_explanation(company_path, company_indent)

def print_lh_tree(anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation):
    """Print only the Long Haul tree"""
    # Long Haul root
    lh_state = anomalies.get("Global/LH", "?")
    lh_dev = get_deviation_text("Global/LH")
    lh_desc = get_state_description(lh_state)
    
    print(f"Long Haul (LH): {lh_desc} {lh_dev}")
    print_interpretation("Global/LH", "")
    if lh_state in ["+", "-"]:
        print_explanation("Global/LH", "")
    
    # LH cabins
    lh_cabins = ["Economy", "Business", "Premium"]
    for i, cabin in enumerate(lh_cabins):
        cabin_path = f"Global/LH/{cabin}"
        cabin_state = anomalies.get(cabin_path, "?")
        cabin_dev = get_deviation_text(cabin_path)
        cabin_desc = get_state_description(cabin_state)
        
        connector = "├──" if i < len(lh_cabins) - 1 else "└──"
        print(f"{connector} {cabin}: {cabin_desc} {cabin_dev}")
        print_interpretation(cabin_path, "")
        if cabin_state in ["+", "-"]:
            print_explanation(cabin_path, "")

def print_sh_tree(anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation):
    """Print only the Short Haul tree"""
    # Short Haul root
    sh_state = anomalies.get("Global/SH", "?")
    sh_dev = get_deviation_text("Global/SH")
    sh_desc = get_state_description(sh_state)
    
    print(f"Short Haul (SH): {sh_desc} {sh_dev}")
    print_interpretation("Global/SH", "")
    if sh_state in ["+", "-"]:
        print_explanation("Global/SH", "")
    
    # SH cabins
    sh_cabins = ["Economy", "Business"]
    for i, cabin in enumerate(sh_cabins):
        cabin_path = f"Global/SH/{cabin}"
        cabin_state = anomalies.get(cabin_path, "?")
        cabin_dev = get_deviation_text(cabin_path)
        cabin_desc = get_state_description(cabin_state)
        
        connector = "├──" if i < len(sh_cabins) - 1 else "└──"
        print(f"{connector} {cabin}: {cabin_desc} {cabin_dev}")
        print_interpretation(cabin_path, "")
        if cabin_state in ["+", "-"]:
            print_explanation(cabin_path, "")
        
        # Company subdivisions
        companies = ["IB", "YW"]
        for j, company in enumerate(companies):
            company_path = f"Global/SH/{cabin}/{company}"
            company_state = anomalies.get(company_path, "?")
            company_dev = get_deviation_text(company_path)
            company_desc = get_state_description(company_state)
            
            # Adjust indentation based on cabin position
            if i < len(sh_cabins) - 1:  # Not the last cabin
                company_connector = "├────" if j < len(companies) - 1 else "└────"
                print(f"│  {company_connector} {company}: {company_desc} {company_dev}")
                company_indent = "│  "
            else:  # Last cabin
                company_connector = "├────" if j < len(companies) - 1 else "└────"
                print(f"   {company_connector} {company}: {company_desc} {company_dev}")
                company_indent = "   "
            
            print_interpretation(company_path, company_indent)
            if company_state in ["+", "-"]:
                print_explanation(company_path, company_indent)

def print_sh_economy_tree(anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation):
    """Print only the SH Economy tree"""
    # SH Economy root
    economy_state = anomalies.get("Global/SH/Economy", "?")
    economy_dev = get_deviation_text("Global/SH/Economy")
    economy_desc = get_state_description(economy_state)
    
    print(f"SH Economy: {economy_desc} {economy_dev}")
    print_interpretation("Global/SH/Economy", "")
    if economy_state in ["+", "-"]:
        print_explanation("Global/SH/Economy", "")
    
    # IB/YW subdivisions
    companies = ["IB", "YW"]
    for j, company in enumerate(companies):
        company_path = f"Global/SH/Economy/{company}"
        company_state = anomalies.get(company_path, "?")
        company_dev = get_deviation_text(company_path)
        company_desc = get_state_description(company_state)
        
        connector = "├──" if j < len(companies) - 1 else "└──"
        print(f"{connector} {company}: {company_desc} {company_dev}")
        print_interpretation(company_path, "")
        if company_state in ["+", "-"]:
            print_explanation(company_path, "")

def print_sh_business_tree(anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation):
    """Print only the SH Business tree"""
    # SH Business root
    business_state = anomalies.get("Global/SH/Business", "?")
    business_dev = get_deviation_text("Global/SH/Business")
    business_desc = get_state_description(business_state)
    
    print(f"SH Business: {business_desc} {business_dev}")
    print_interpretation("Global/SH/Business", "")
    if business_state in ["+", "-"]:
        print_explanation("Global/SH/Business", "")
    
    # IB/YW subdivisions
    companies = ["IB", "YW"]
    for j, company in enumerate(companies):
        company_path = f"Global/SH/Business/{company}"
        company_state = anomalies.get(company_path, "?")
        company_dev = get_deviation_text(company_path)
        company_desc = get_state_description(company_state)
        
        connector = "├──" if j < len(companies) - 1 else "└──"
        print(f"{connector} {company}: {company_desc} {company_dev}")
        print_interpretation(company_path, "")
        if company_state in ["+", "-"]:
            print_explanation(company_path, "")

def print_single_node(node_path, anomalies, get_state_description, get_deviation_text, print_interpretation, print_explanation):
    """Print a single node (for leaf segments)"""
    node_state = anomalies.get(node_path, "?")
    node_dev = get_deviation_text(node_path)
    node_desc = get_state_description(node_state)
    
    # Extract readable name from path
    if node_path == "Global/LH/Economy":
        node_name = "LH Economy"
    elif node_path == "Global/LH/Business":
        node_name = "LH Business"
    elif node_path == "Global/LH/Premium":
        node_name = "LH Premium"
    elif node_path == "Global/SH/Economy/IB":
        node_name = "SH Economy IB"
    elif node_path == "Global/SH/Economy/YW":
        node_name = "SH Economy YW"
    elif node_path == "Global/SH/Business/IB":
        node_name = "SH Business IB"
    elif node_path == "Global/SH/Business/YW":
        node_name = "SH Business YW"
    else:
        node_name = node_path.split('/')[-1] if '/' in node_path else node_path
    
    print(f"{node_name}: {node_desc} {node_dev}")
    print_interpretation(node_path, "")
    if node_state in ["+", "-"]:
        print_explanation(node_path, "")

def calculate_period_date_range(analysis_date: datetime, target_period: int, aggregation_days: int) -> tuple:
    """
    Calculate the correct date range for a period relative to the analysis date
    
    Args:
        analysis_date: The reference date for the analysis (e.g., 2025-01-20)
        target_period: Period number (1 = most recent relative to analysis_date)
        aggregation_days: Days per period (1, 7, 14, 30, etc.)
        
    Returns:
        Tuple of (start_date, end_date) for the target period
        
    Examples:
        For daily analysis (aggregation_days=1) with analysis_date=2025-01-20:
        - Period 1: (2025-01-20, 2025-01-20) - the analysis date itself
        - Period 2: (2025-01-19, 2025-01-19) - 1 day before
        - Period 3: (2025-01-18, 2025-01-18) - 2 days before
        
        For weekly analysis (aggregation_days=7) with analysis_date=2025-01-20:
        - Period 1: (2025-01-14, 2025-01-20) - week ending on analysis date
        - Period 2: (2025-01-07, 2025-01-13) - previous week
    """
    print(f"🔍 DEBUG calculate_period_date_range: analysis_date={analysis_date}, target_period={target_period}, aggregation_days={aggregation_days}")
    
    # Calculate how many days back from analysis date
    days_back = (target_period - 1) * aggregation_days
    print(f"🔍 DEBUG calculate_period_date_range: days_back = (target_period - 1) * aggregation_days = ({target_period} - 1) * {aggregation_days} = {days_back}")
    
    # For daily analysis, each period is exactly one day
    # For weekly analysis, each period is 7 days, etc.
    period_end = analysis_date - timedelta(days=days_back)
    period_start = period_end - timedelta(days=aggregation_days - 1)
    
    print(f"🔍 DEBUG calculate_period_date_range: period_end = analysis_date - {days_back} days = {period_end}")
    print(f"🔍 DEBUG calculate_period_date_range: period_start = period_end - {aggregation_days - 1} days = {period_start}")
    print(f"🔍 DEBUG calculate_period_date_range: returning ({period_start}, {period_end})")
    
    return period_start, period_end

def calculate_actual_period_number(analysis_date: datetime, today_date: datetime = None) -> int:
    """
    Calculate the actual period number in the PBI data for a given analysis date
    
    Args:
        analysis_date: The date we want to analyze (e.g., 2025-01-20)
        today_date: Today's date (defaults to actual today)
        
    Returns:
        The period number in the PBI data that corresponds to the analysis date
        
    Example:
        If today is 2025-06-05 and analysis_date is 2025-01-20:
        Days difference = 137, so analysis_date is Period 137
    """
    if today_date is None:
        today_date = datetime.now().date()
    elif isinstance(today_date, datetime):
        today_date = today_date.date()
    
    if isinstance(analysis_date, datetime):
        analysis_date = analysis_date.date()
    
    # Calculate days between today and analysis date
    days_diff = (today_date - analysis_date).days
    
    # Period number = days difference + 1 (Period 1 = today)
    period_number = days_diff + 1
    
    return period_number

def detect_parent_child_relationships(node_paths: list) -> dict:
    """
    Detect parent-child relationships among anomalous nodes.
    Returns a dictionary with relationship information for each node.
    """
    relationships = {}
    
    for node_path in node_paths:
        relationships[node_path] = {
            'type': 'standalone',
            'parent': None,
            'children': [],
            'all_related': [node_path]
        }
    
    # Detect parent-child relationships
    for node_path in node_paths:
        path_parts = node_path.split('/')
        
        # Check if this node is a parent of any other nodes
        children = []
        for other_path in node_paths:
            if other_path != node_path and other_path.startswith(node_path + '/'):
                # Check if it's a direct child (not grandchild)
                other_parts = other_path.split('/')
                if len(other_parts) == len(path_parts) + 1:
                    children.append(other_path)
        
        if children:
            relationships[node_path]['type'] = 'parent'
            relationships[node_path]['children'] = children
            relationships[node_path]['all_related'] = [node_path] + children
            
            # Mark children as having this parent
            for child in children:
                relationships[child]['type'] = 'child'
                relationships[child]['parent'] = node_path
                relationships[child]['all_related'] = [node_path] + children
    
    return relationships

def should_consolidate_explanations(causal_explanations: dict, relationships: dict) -> bool:
    """
    Determine if parent-child explanations should be consolidated based on cause similarity.
    Returns True if causes appear to be common/related, False if distinct.
    """
    if len(causal_explanations) <= 1:
        return False
    
    # Look for parent-child groups
    for node_path, rel_info in relationships.items():
        if rel_info['type'] == 'parent' and len(rel_info['children']) > 0:
            parent_explanation = causal_explanations.get(node_path, "")
            
            # Check for operational/service-related keywords that suggest common causes
            operational_keywords = [
                'punctuality', 'delay', 'puntualidad', 'retraso', 'retrasos',
                'boarding', 'embarque', 'crew', 'tripulación', 'tripulacion',
                'arrivals', 'llegada', 'llegadas', 'operational', 'operacional',
                'operativo', 'service', 'servicio', 'incident', 'incidente',
                'technical', 'técnico', 'tecnico', 'system', 'sistema'
            ]
            
            # Count operational keywords in parent explanation
            parent_ops_count = sum(1 for keyword in operational_keywords 
                                  if keyword.lower() in parent_explanation.lower())
            
            # Check children explanations
            common_cause_indicators = 0
            total_children = len(rel_info['children'])
            
            for child_node in rel_info['children']:
                child_explanation = causal_explanations.get(child_node, "")
                child_ops_count = sum(1 for keyword in operational_keywords 
                                     if keyword.lower() in child_explanation.lower())
                
                # If both parent and child mention operational issues
                if parent_ops_count > 0 and child_ops_count > 0:
                    common_cause_indicators += 1
            
            # Consolidate if majority of children show similar operational causes
            if common_cause_indicators >= (total_children * 0.6):  # 60% threshold
                return True
    
    return False

def debug_save_interpreter_input_tree(
    tree_data: str,
    date: str,
    segment: str,
    mode: str = "single"
) -> str:
    """
    Save the exact input tree data given to the interpreter for debugging
    
    Args:
        tree_data: The exact tree data string passed to interpreter
        date: Analysis date
        segment: Segment analyzed
        mode: Analysis mode (single/comparative)
        
    Returns:
        Path to saved file
    """
    try:
        # Create debug directory if it doesn't exist
        debug_dir = Path("dashboard_analyzer/debug/interpreter_inputs")
        debug_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_segment = segment.replace("/", "_").replace(" ", "_")
        filename = f"interpreter_input_{mode}_{date}_{safe_segment}_{timestamp}.txt"
        filepath = debug_dir / filename
        
        # Save tree data
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# INTERPRETER INPUT TREE DATA\n")
            f.write(f"# Date: {date}\n")
            f.write(f"# Segment: {segment}\n")
            f.write(f"# Mode: {mode}\n")
            f.write(f"# Timestamp: {timestamp}\n")
            f.write(f"# Input size: {len(tree_data)} characters\n")
            f.write("="*80 + "\n\n")
            f.write(tree_data)
        
        debug_print(f"Interpreter input tree saved to: {filepath}")
        return str(filepath)
        
    except Exception as e:
        debug_print(f"Failed to save interpreter input tree: {e}")
        return ""

async def execute_analysis_flow(
    analysis_date: datetime,
    date_parameter: str,
    segment: str,
    explanation_mode: str,
    anomaly_detection_mode: str,
    baseline_periods: int,
    aggregation_days: int,
    periods: int,
    causal_filter: Optional[str],
    comparison_start_date: Optional[datetime] = None,
    comparison_end_date: Optional[datetime] = None,
    date_flight_local: Optional[str] = None,
    study_mode: str = "comparative",
) -> str:
    """
    Executes a complete analysis flow for a given configuration.
    This includes data download, anomaly detection, and interpretation.
    """

    # Adjust causal_filter based on study_mode
    if study_mode == "single":
        causal_filter = None
    
    print(f"\n{'='*60}")
    print(f"🚀 EXECUTING ANALYSIS FLOW")
    print(f"   - Study Mode: {study_mode.upper() if study_mode else 'AUTO-DETECTED'}")
    print(f"   - Aggregation: {aggregation_days} days")
    print(f"   - Periods: {periods}")
    print(f"   - Causal Filter: {causal_filter}")
    print(f"{'='*60}")

    # 1. Data Download
    data_folder = await run_flexible_data_download_silent_with_date(
        aggregation_days=aggregation_days,
        periods=periods,
        start_date=analysis_date,
        date_parameter=f"{date_parameter}_{study_mode}_{aggregation_days}d",
        segment=segment
    )

    if not data_folder:
        print(f"❌ Data collection failed for {study_mode} {aggregation_days}d analysis.")
        return None

    # 2. Analysis
    analysis_data = await run_flexible_analysis_silent(
        data_folder,
        analysis_date,
        date_parameter,
        anomaly_detection_mode,
        baseline_periods,
        causal_filter,
        periods=periods
    )

    if not analysis_data or not analysis_data.get('anomaly_periods'):
        print(f"✅ No anomalies found for {study_mode} {aggregation_days}d analysis.")
        return None

    # 3. Get Summary
    summary_data = await show_silent_anomaly_analysis(
        analysis_data,
        f"{study_mode.upper()}_ANALYSIS",
        segment=segment,
        explanation_mode=explanation_mode,
        causal_filter=causal_filter,
        comparison_start_date=comparison_start_date,
        comparison_end_date=comparison_end_date
    )
    
    return summary_data

if __name__ == "__main__":
    # To run this from the command line:
    # python -m dashboard_analyzer.main --mode both --segment "Global" --date-flight-local "2025-01-15"
    asyncio.run(main())
