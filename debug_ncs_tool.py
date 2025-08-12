#!/usr/bin/env python3
"""
Debug script para NCS_TOOL
Verifica DAX query, columnas devueltas, procesamiento de datos y adaptación a la estructura esperada por el causal agent
"""

import os
import sys
import asyncio
import pandas as pd
from datetime import datetime, timedelta
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("🔍 DEBUGGING NCS_TOOL")
print("="*50)
print("📋 Test Parameters:")
print("   Node Path: Global/LH/Business")
print("   Start Date: 2025-08-01")
print("   End Date: 2025-08-07")
print()

async def debug_ncs_tool():
    """Debug NCS tool flow from data collection to causal agent response"""
    
    # Test parameters
    node_path = "Global/LH/Business"
    start_date = "2025-08-01"
    end_date = "2025-08-07"
    
    print("🔧 STEP 1: Testing NCS Data Collector")
    print("-" * 30)
    
    try:
        from dashboard_analyzer.data_collection.ncs_collector import NCSDataCollector
        
        # Initialize collector with temp credentials
        temp_creds_file = "dashboard_analyzer/temp_aws_credentials.env"
        ncs_collector = NCSDataCollector(temp_env_file=temp_creds_file)
        print("   ✅ NCS collector initialized")
        
        # Test data collection for current period
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        print(f"   📅 Collecting NCS data for period: {start_date} to {end_date}")
        current_data = ncs_collector.collect_ncs_data_for_date_range(start_dt, end_dt)
        print(f"   📊 Current period data shape: {current_data.shape}")
        print(f"   📋 Current period columns: {list(current_data.columns) if not current_data.empty else 'No data'}")
        
        # Test comparison period data (for comparative mode)
        total_days = (end_dt - start_dt).days + 1
        comparison_end_dt = start_dt - timedelta(days=1)
        comparison_start_dt = comparison_end_dt - timedelta(days=total_days - 1)
        
        print(f"   📅 Collecting comparison data: {comparison_start_dt.strftime('%Y-%m-%d')} to {comparison_end_dt.strftime('%Y-%m-%d')}")
        comparison_data = ncs_collector.collect_ncs_data_for_date_range(comparison_start_dt, comparison_end_dt)
        print(f"   📊 Comparison period data shape: {comparison_data.shape}")
        
    except Exception as e:
        print(f"   ❌ Error in NCS collector: {str(e)}")
        return
    
    print()
    print("🔧 STEP 2: Testing Segment Filtering")
    print("-" * 30)
    
    try:
        # Import and initialize causal explanation agent for filtering
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        
        # Initialize agent correctly like in the main application
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/causal_explanation.yaml",
            silent_mode=True,
            detection_mode="mean",
            causal_filter="vs L7d",
            study_mode="comparative"
        )
        
        print("   ✅ Causal explanation agent initialized")
        
        # Test segment filtering
        if not current_data.empty:
            filtered_current = await agent._filter_ncs_by_segment(current_data, node_path)
            print(f"   🔧 Filtered current data shape: {filtered_current.shape}")
            print(f"   📊 Current data sample: {filtered_current.head(3).to_dict('records') if not filtered_current.empty else 'No data after filtering'}")
        
        if not comparison_data.empty:
            filtered_comparison = await agent._filter_ncs_by_segment(comparison_data, node_path)
            print(f"   🔧 Filtered comparison data shape: {filtered_comparison.shape}")
        else:
            filtered_comparison = pd.DataFrame()
            
    except Exception as e:
        print(f"   ❌ Error in segment filtering: {str(e)}")
        return
    
    print()
    print("🔧 STEP 3: Testing Enhanced Single Period Analysis")
    print("-" * 30)
    
    try:
        if not filtered_current.empty:
            # Test the ENHANCED structure expected by single period mode
            single_analysis = ncs_collector.analyze_ncs_incidents_for_period(filtered_current, analysis_focus="all")
            print(f"   📊 Enhanced single analysis keys: {list(single_analysis.keys())}")
            
            # Check for required causal agent structure
            required_keys = ['incident_counts', 'detailed_incidents', 'route_analysis', 'flight_analysis']
            for key in required_keys:
                if key in single_analysis:
                    print(f"   ✅ Found required key: {key}")
                    if key == 'incident_counts':
                        print(f"      📋 Incident counts: {single_analysis[key]}")
                else:
                    print(f"   ❌ Missing required key: {key}")
            
            # Test the new methods directly
            print("   🔍 Testing new _extract_incident_counts_from_data method...")
            incident_counts = ncs_collector._extract_incident_counts_from_data(filtered_current)
            print(f"   📊 Direct incident counts: {incident_counts}")
            
            print("   🔍 Testing new _extract_route_analysis_from_data method...")
            route_analysis = ncs_collector._extract_route_analysis_from_data(filtered_current)
            print(f"   📊 Direct route analysis: {route_analysis}")
            
        else:
            print(f"   ⚠️ No current data for enhanced single analysis")
            
    except Exception as e:
        print(f"   ❌ Error in enhanced single period analysis: {str(e)}")
    
    print()
    print("🔧 STEP 4: Testing Enhanced Comparative Analysis")
    print("-" * 30)
    
    try:
        if not filtered_current.empty or not filtered_comparison.empty:
            # Test the new temporal comparison functionality
            print("   🔍 Testing new create_temporal_comparison_analysis method...")
            
            current_period_str = f"{start_date} to {end_date}"
            comparison_period_str = f"{comparison_start_dt.strftime('%Y-%m-%d')} to {comparison_end_dt.strftime('%Y-%m-%d')}"
            
            temporal_analysis = ncs_collector.create_temporal_comparison_analysis(
                filtered_current, 
                filtered_comparison,
                current_period_str,
                comparison_period_str,
                node_path
            )
            
            print(f"   📊 Temporal analysis keys: {list(temporal_analysis.keys())}")
            
            # Check for required comparative structure
            required_comparative_keys = ['current_period', 'comparison_period', 'route_incident_matrix', 
                                       'incident_type_deltas', 'improvement_patterns', 'analysis_summary']
            for key in required_comparative_keys:
                if key in temporal_analysis:
                    print(f"   ✅ Found required comparative key: {key}")
                    if key == 'incident_type_deltas':
                        print(f"      📈 Incident type deltas: {temporal_analysis[key]}")
                    elif key == 'analysis_summary':
                        print(f"      📋 Analysis summary: {temporal_analysis[key]}")
                else:
                    print(f"   ❌ Missing required comparative key: {key}")
            
            # Test structured data extraction
            print("   🔍 Testing _extract_structured_data_for_comparison method...")
            current_structured = ncs_collector._extract_structured_data_for_comparison(filtered_current, "current")
            comparison_structured = ncs_collector._extract_structured_data_for_comparison(filtered_comparison, "comparison")
            
            print(f"   📊 Current structured keys: {list(current_structured.keys())}")
            print(f"   📊 Current incident types: {current_structured.get('incident_types', {})}")
            print(f"   📊 Comparison incident types: {comparison_structured.get('incident_types', {})}")
            
        else:
            print(f"   ⚠️ No data for enhanced comparative analysis")
            
    except Exception as e:
        print(f"   ❌ Error in enhanced comparative analysis: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🔧 STEP 5: Testing Agent NCS Tool Integration - SINGLE MODE")
    print("-" * 30)
    
    try:
        # Test single period mode
        print("   🔍 Testing _ncs_tool_single_period...")
        single_result = await agent._ncs_tool_single_period(node_path, start_date, end_date)
        print(f"   📊 Single period result length: {len(single_result)}")
        print(f"   📋 Single period preview: {single_result[:300]}...")
        
        # Check that the single mode uses our enhanced structure
        print("   ✅ Single mode NCS tool executed successfully")
        
    except Exception as e:
        print(f"   ❌ Error in single period agent integration: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🔧 STEP 6: Testing Agent NCS Tool Integration - COMPARATIVE MODE") 
    print("-" * 30)
    
    try:
        # Test comparative mode
        print("   🔍 Testing _ncs_tool (comparative mode)...")
        comparative_result = await agent._ncs_tool(node_path, start_date, end_date, analysis_focus="flights", temporal_comparison=True)
        
        print(f"   📊 Comparative mode result length: {len(comparative_result)}")
        print(f"   📋 Comparative mode preview: {comparative_result[:200]}...")
        
        print("   ✅ NCS tool integration successful")
        
    except Exception as e:
        print(f"   ❌ Error in causal agent integration: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ncs_tool()) 