#!/usr/bin/env python3
"""
Debug script for explanatory_drivers_tool
Tests the tool directly to see what drivers are actually being returned
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type

async def debug_explanatory_drivers_tool():
    """Debug the explanatory_drivers_tool for the specific segment"""
    
    print("🔍 DEBUG EXPLANATORY DRIVERS TOOL")
    print("=" * 50)
    
    # Configuration
    node_path = "Global/SH/Business/YW"
    start_date_str = "2025-08-01"
    end_date_str = "2025-08-07"
    start_date_dt = datetime(2025, 8, 1)
    end_date_dt = datetime(2025, 8, 7)
    comparison_filter = "vs L7d"
    
    print(f"🎯 Segment: {node_path}")
    print(f"📅 Period: {start_date_str} to {end_date_str}")
    print(f"🔍 Comparison: {comparison_filter}")
    print()
    
    try:
        # Initialize PBI collector
        print("📊 Initializing PBI Data Collector...")
        pbi_collector = PBIDataCollector()
        
        # Initialize causal agent (we only need it for the explanatory drivers logic)
        print("🔧 Initializing Causal Explanation Agent...")
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(),
            silent_mode=True
        )
        agent.pbi_collector = pbi_collector
        
        # Collect explanatory drivers data directly using the agent's method
        print("🔍 Collecting explanatory drivers data...")
        drivers_data = await agent.pbi_collector.collect_explanatory_drivers_for_date_range(
            node_path=node_path,
            start_date=start_date_dt,
            end_date=end_date_dt,
            comparison_filter=comparison_filter
        )
        
        print(f"✅ Data collected successfully")
        print(f"📊 Raw data shape: {drivers_data.shape if hasattr(drivers_data, 'shape') else 'No shape'}")
        print()
        
        # Display raw data structure
        print("📋 RAW DATA STRUCTURE:")
        print("-" * 30)
        if hasattr(drivers_data, 'columns'):
            print(f"Columns: {list(drivers_data.columns)}")
        if hasattr(drivers_data, 'head'):
            print(f"First few rows:")
            print(drivers_data.head())
        print()
        
        # Now call the actual explanatory drivers tool method
        print("🔍 Calling explanatory_drivers_tool method...")
        tool_result = await agent._explanatory_drivers_tool(
            node_path=node_path,
            start_date=start_date_str,
            end_date=end_date_str,
            min_surveys=10
        )
        
        print("✅ Tool execution completed successfully")
        print()
        
        # Display the tool result
        print("📊 TOOL RESULT:")
        print("=" * 30)
        print(tool_result)
        print()
        
        # Display the collected data structure
        if 'explanatory_drivers' in agent.collected_data:
            print("🔍 COLLECTED DATA STRUCTURE:")
            print("=" * 40)
            drivers_info = agent.collected_data['explanatory_drivers']
            
            print(f"Survey Count: {drivers_info.get('survey_count', 'N/A')}")
            print(f"Threshold: {drivers_info.get('threshold', 'N/A')}")
            print(f"All Drivers Found: {len(drivers_info.get('all_drivers', []))}")
            print(f"Significant Drivers: {len(drivers_info.get('significant_drivers', []))}")
            print()
            
            # Display all drivers
            all_drivers = drivers_info.get('all_drivers', [])
            if all_drivers:
                print("🎯 ALL DRIVERS FOUND:")
                print("-" * 30)
                for i, driver in enumerate(all_drivers, 1):
                    print(f"{i:2d}. {driver.get('touchpoint', 'Unknown')}:")
                    print(f"     SHAP: {driver.get('shap_value', 'N/A')}")
                    print(f"     Sat_diff: {driver.get('sat_diff', 'N/A')}")
                    print(f"     Significance: {driver.get('is_significant', 'N/A')}")
                    print()
            
            # Display significant drivers
            significant_drivers = drivers_info.get('significant_drivers', [])
            if significant_drivers:
                print("⭐ SIGNIFICANT DRIVERS:")
                print("-" * 30)
                for i, driver in enumerate(significant_drivers, 1):
                    print(f"{i:2d}. {driver.get('touchpoint', 'Unknown')}:")
                    print(f"     SHAP: {driver.get('shap_value', 'N/A')}")
                    print(f"     Sat_diff: {driver.get('sat_diff', 'N/A')}")
                    print()
            
            # Display workflow info
            print(f"🔄 Workflow Type: {drivers_info.get('workflow_type', 'Unknown')}")
            print(f"📋 Recommendation: {drivers_info.get('recommendation', 'N/A')}")
            
        else:
            print("❌ No explanatory drivers data found in collected_data")
        
        # Display full collected data for debugging
        print()
        print("🔍 FULL COLLECTED DATA (for debugging):")
        print("=" * 50)
        import json
        print(json.dumps(agent.collected_data, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Explanatory Drivers Tool Debug...")
    asyncio.run(debug_explanatory_drivers_tool())
    print("✅ Debug completed") 