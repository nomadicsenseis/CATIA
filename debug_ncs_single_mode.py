#!/usr/bin/env python3
import os
import sys
import asyncio
import pandas as pd
from datetime import datetime, timedelta
import logging

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def debug_ncs_single_mode():
    """Debug NCS tool single mode specifically"""
    
    print("🔍 DEBUGGING NCS_TOOL - SINGLE MODE ONLY")
    print("=" * 50)
    
    # Test parameters
    node_path = "Global/LH/Business"
    start_date = "2025-08-01"
    end_date = "2025-08-07"
    
    print(f"📋 Test Parameters:")
    print(f"   Node Path: {node_path}")
    print(f"   Start Date: {start_date}")
    print(f"   End Date: {end_date}")
    print()
    
    try:
        # Step 1: Collect limited NCS data (just one day for faster testing)
        from dashboard_analyzer.data_collection.ncs_collector import NCSDataCollector
        
        print("🔧 STEP 1: Testing NCS Data Collection (Limited)")
        print("-" * 30)
        
        ncs_collector = NCSDataCollector(temp_env_file="dashboard_analyzer/temp_aws_credentials.env")
        print("   ✅ NCS collector initialized")
        
        # Collect just one day for faster testing
        test_start_dt = datetime.strptime("2025-08-05", '%Y-%m-%d')  # Just one day
        test_end_dt = datetime.strptime("2025-08-05", '%Y-%m-%d')
        
        test_data = ncs_collector.collect_ncs_data_for_date_range(test_start_dt, test_end_dt)
        print(f"   📊 Test data shape: {test_data.shape}")
        print(f"   📋 Test data columns: {list(test_data.columns)[:10]}...")  # Show first 10 columns
        print()
        
        # Step 2: Initialize causal agent
        print("🔧 STEP 2: Initialize Causal Agent")
        print("-" * 30)
        
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/causal_explanation.yaml",
            silent_mode=True,
            detection_mode="mean",
            causal_filter="vs L7d",
            study_mode="single"  # SINGLE MODE
        )
        print("   ✅ Causal agent initialized in SINGLE mode")
        print()
        
        # Step 3: Test Enhanced analyze_ncs_incidents_for_period
        print("🔧 STEP 3: Test Enhanced analyze_ncs_incidents_for_period")
        print("-" * 30)
        
        if not test_data.empty:
            # Test our enhanced method directly
            enhanced_analysis = ncs_collector.analyze_ncs_incidents_for_period(test_data, analysis_focus="all")
            print(f"   📊 Enhanced analysis keys: {list(enhanced_analysis.keys())}")
            
            # Check for required structure
            required_keys = ['incident_counts', 'detailed_incidents', 'route_analysis', 'flight_analysis']
            for key in required_keys:
                if key in enhanced_analysis:
                    print(f"   ✅ Found required key: {key}")
                    if key == 'incident_counts':
                        print(f"      📋 Incident counts: {enhanced_analysis[key]}")
                    elif key == 'detailed_incidents':
                        detailed = enhanced_analysis[key]
                        print(f"      📋 Detailed incidents count: {detailed.get('count', 0)}")
                        print(f"      📋 Sample incidents: {len(detailed.get('sample_incidents', []))}")
                else:
                    print(f"   ❌ Missing required key: {key}")
        print()
        
        # Step 4: Test agent's _ncs_tool_single_period
        print("🔧 STEP 4: Test Agent's _ncs_tool_single_period")
        print("-" * 30)
        
        try:
            # Use the single day for testing
            single_result = await agent._ncs_tool_single_period(node_path, "2025-08-05", "2025-08-05")
            print(f"   📊 Single mode result length: {len(single_result)}")
            print(f"   📋 Single mode result:")
            print(f"   {single_result}")
            print("   ✅ Single mode NCS tool executed successfully")
            
        except Exception as e:
            print(f"   ❌ Error in single mode agent integration: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
        print("🎉 DEBUG COMPLETE - NCS SINGLE MODE")
        
    except Exception as e:
        print(f"❌ General error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ncs_single_mode()) 