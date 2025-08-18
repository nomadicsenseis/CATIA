#!/usr/bin/env python3
"""
Detailed debug script for explanatory_drivers_tool
Shows exactly what happens at each step of processing
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

async def debug_explanatory_drivers_detailed():
    """Detailed debug of explanatory drivers processing"""
    
    print("🔍 DETAILED DEBUG EXPLANATORY DRIVERS TOOL")
    print("=" * 60)
    
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
        
        # Initialize causal agent
        print("🔧 Initializing Causal Explanation Agent...")
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(),
            silent_mode=True
        )
        agent.pbi_collector = pbi_collector
        
        # STEP 1: Collect raw data from PBI
        print("🔍 STEP 1: Collecting raw data from PBI...")
        drivers_data = await agent.pbi_collector.collect_explanatory_drivers_for_date_range(
            node_path=node_path,
            start_date=start_date_dt,
            end_date=end_date_dt,
            comparison_filter=comparison_filter
        )
        
        print(f"✅ Raw data collected: {len(drivers_data)} rows")
        print(f"📊 Raw data shape: {drivers_data.shape}")
        print()
        
        # Display raw data structure
        print("📋 RAW DATA STRUCTURE:")
        print("-" * 40)
        if hasattr(drivers_data, 'columns'):
            print(f"Columns: {list(drivers_data.columns)}")
        if hasattr(drivers_data, 'head'):
            print(f"First few rows:")
            print(drivers_data.head())
        print()
        
        # STEP 2: Analyze the raw data manually
        print("🔍 STEP 2: Manual analysis of raw data...")
        print("-" * 40)
        
        if 'Shapdiff' in drivers_data.columns:
            print("✅ 'Shapdiff' column found")
            shap_values = drivers_data['Shapdiff'].tolist()
            print(f"SHAP values: {shap_values}")
            
            # Check for any touchpoint mapping
            touchpoint_col = 'TouchPoint_Master[filtered_name'
            if touchpoint_col in drivers_data.columns:
                print(f"✅ '{touchpoint_col}' column found")
                touchpoints = drivers_data[touchpoint_col].tolist()
                print(f"Touchpoints: {touchpoints}")
                
                # Check for any touchpoint transformations
                print("\n🔍 Checking for touchpoint transformations...")
                for i, (tp, shap) in enumerate(zip(touchpoints, shap_values)):
                    print(f"  {i+1:2d}. {tp}: SHAP={shap}")
                    
                    # Check if this touchpoint gets mapped/transformed
                    if tp and isinstance(tp, str):
                        tp_lower = tp.lower()
                        if any(op_keyword in tp_lower for op_keyword in 
                               ['otp', 'delay', 'punctual', 'baggage', 'misconex', 'mishandling', 'load factor', 'operational']):
                            print(f"      → Classified as OPERATIONAL")
                        else:
                            print(f"      → Classified as PRODUCT/SERVICE")
        else:
            print("❌ 'Shapdiff' column NOT found")
            print(f"Available columns: {list(drivers_data.columns)}")
        
        print()
        
        # STEP 3: Check if there's any data transformation happening
        print("🔍 STEP 3: Checking for data transformations...")
        print("-" * 40)
        
        # Look for any touchpoint mapping or transformation logic
        print("🔍 Looking for touchpoint mapping logic...")
        
        # Check if there are any hardcoded touchpoint mappings
        print("🔍 Checking for hardcoded touchpoint mappings...")
        
        # STEP 4: Call the tool method and see what happens
        print("🔍 STEP 4: Calling explanatory_drivers_tool method...")
        print("-" * 40)
        
        tool_result = await agent._explanatory_drivers_tool(
            node_path=node_path,
            start_date=start_date_str,
            end_date=end_date_str,
            min_surveys=10
        )
        
        print("✅ Tool execution completed")
        print()
        
        # STEP 5: Compare raw data vs processed data
        print("🔍 STEP 5: Comparing raw vs processed data...")
        print("-" * 40)
        
        print("📊 TOOL RESULT:")
        print("=" * 40)
        print(tool_result)
        print()
        
        # Check what was stored in collected_data
        if 'explanatory_drivers' in agent.collected_data:
            print("🔍 COLLECTED DATA ANALYSIS:")
            print("=" * 40)
            drivers_info = agent.collected_data['explanatory_drivers']
            
            print(f"Survey Count: {drivers_info.get('survey_count', 'N/A')}")
            print(f"All Drivers: {len(drivers_info.get('all_drivers', []))}")
            print(f"Significant Drivers: {len(drivers_info.get('significant_drivers', []))}")
            print(f"Operational Drivers: {drivers_info.get('operational_drivers', [])}")
            print(f"Product Drivers: {drivers_info.get('product_drivers', [])}")
            print()
            
            # Display all drivers from collected_data
            all_drivers = drivers_info.get('all_drivers', [])
            if all_drivers:
                print("🎯 ALL DRIVERS FROM COLLECTED_DATA:")
                print("-" * 40)
                for i, driver in enumerate(all_drivers, 1):
                    if isinstance(driver, dict):
                        print(f"{i:2d}. {driver.get('touchpoint', 'Unknown')}:")
                        print(f"     SHAP: {driver.get('shap_value', 'N/A')}")
                        print(f"     Sat_diff: {driver.get('satisfaction_diff', 'N/A')}")
                        print(f"     Significant: {driver.get('significant', 'N/A')}")
                    else:
                        print(f"{i:2d}. {driver} (not a dict)")
                    print()
        else:
            print("❌ No explanatory drivers data found in collected_data")
        
        # STEP 6: Check for any discrepancies
        print("🔍 STEP 6: Checking for discrepancies...")
        print("-" * 40)
        
        print("🔍 COMPARISON SUMMARY:")
        print("Raw PBI data has:")
        if 'Shapdiff' in drivers_data.columns:
            raw_shap = drivers_data['Shapdiff'].tolist()
            raw_touchpoints = drivers_data['TouchPoint_Master[filtered_name'].tolist()
            print(f"  - {len(raw_shap)} SHAP values: {raw_shap}")
            print(f"  - Touchpoints: {raw_touchpoints}")
        
        print("\nProcessed data shows:")
        if 'explanatory_drivers' in agent.collected_data:
            processed_drivers = agent.collected_data['explanatory_drivers'].get('all_drivers', [])
            print(f"  - {len(processed_drivers)} processed drivers")
            for driver in processed_drivers:
                if isinstance(driver, dict):
                    print(f"    * {driver.get('touchpoint', 'Unknown')}: SHAP={driver.get('shap_value', 'N/A')}")
        
        print("\n🔍 DISCREPANCIES FOUND:")
        print("=" * 40)
        
        # Check if there are any touchpoints in processed data that don't exist in raw data
        if 'explanatory_drivers' in agent.collected_data:
            processed_drivers = agent.collected_data['explanatory_drivers'].get('all_drivers', [])
            raw_touchpoints = drivers_data['TouchPoint_Master[filtered_name'].tolist() if 'TouchPoint_Master[filtered_name' in drivers_data.columns else []
            
            for driver in processed_drivers:
                if isinstance(driver, dict):
                    processed_tp = driver.get('touchpoint', 'Unknown')
                    if processed_tp not in raw_touchpoints:
                        print(f"❌ TOUCHPOINT NOT IN RAW DATA: '{processed_tp}'")
                        print(f"   This suggests data transformation or mapping is happening somewhere")
        
        print("\n✅ Detailed debug completed")
        
    except Exception as e:
        print(f"❌ Error during detailed analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Detailed Explanatory Drivers Debug...")
    asyncio.run(debug_explanatory_drivers_detailed())
    print("✅ Detailed debug completed") 