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

async def debug_routes_tool():
    """Debug routes tool functionality in both modes"""
    
    print("🔍 DEBUGGING ROUTES_TOOL - COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
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
        # Initialize causal agent
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        
        print("🔧 STEP 1: Initialize Causal Agent")
        print("-" * 30)
        
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(),
            config_path="dashboard_analyzer/anomaly_explanation/config/prompts/causal_explanation.yaml",
            silent_mode=True,
            detection_mode="mean",
            causal_filter="vs L7d",
            study_mode="comparative"  # COMPARATIVE MODE
        )
        print("   ✅ Causal agent initialized")
        print()
        
        # STEP 2: Test Routes Tool SINGLE MODE
        print("🔧 STEP 2: Test Routes Tool - SINGLE MODE")
        print("-" * 30)
        
        try:
            single_result = await agent._routes_tool_single_period(
                node_path=node_path,
                start_date=start_date,
                end_date=end_date,
                min_surveys=2,
                anomaly_type="negative"
            )
            
            print(f"   📊 Single mode result length: {len(single_result)}")
            print(f"   📋 Single mode result structure check:")
            
            # Check expected elements in single mode
            expected_single_elements = [
                "RUTAS - PERIODO ÚNICO",
                "RUTAS CON NPS",
                "RUTAS CON INCIDENTES OPERACIONALES",
                "Valores NPS absolutos"
            ]
            
            for element in expected_single_elements:
                if element in single_result:
                    print(f"     ✅ Found: {element}")
                else:
                    print(f"     ❌ Missing: {element}")
            
            print(f"   📋 Single mode preview:")
            print(f"   {single_result[:500]}...")
            
        except Exception as e:
            print(f"   ❌ Error in single mode: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # STEP 3: Test Routes Tool COMPARATIVE MODE
        print("🔧 STEP 3: Test Routes Tool - COMPARATIVE MODE")
        print("-" * 30)
        
        try:
            # First, simulate some explanatory drivers data
            agent.collected_data['explanatory_drivers'] = {
                'significant_drivers': ['Punctuality', 'Crew', 'Aircraft interior'],
                'all_drivers': [
                    {'touchpoint': 'Punctuality', 'shap_value': -0.125},
                    {'touchpoint': 'Crew', 'shap_value': -0.087},
                    {'touchpoint': 'Aircraft interior', 'shap_value': -0.043}
                ]
            }
            
            comparative_result = await agent._routes_tool(
                node_path=node_path,
                start_date=start_date,
                end_date=end_date,
                min_surveys=3,
                anomaly_type="negative"
            )
            
            print(f"   📊 Comparative mode result length: {len(comparative_result)}")
            print(f"   📋 Comparative mode result structure check:")
            
            # Check expected elements in comparative mode
            expected_comparative_elements = [
                "COMPREHENSIVE ROUTES ANALYSIS",
                "EXPLANATORY DRIVERS ROUTES",
                "NCS OPERATIONAL INCIDENTS ROUTES",
                "CUSTOMER VERBATIMS ROUTES",
                "CONSOLIDATED ROUTES FROM ALL SOURCES",
                "ROUTES SIMILARITY ANALYSIS"
            ]
            
            for element in expected_comparative_elements:
                if element in comparative_result:
                    print(f"     ✅ Found: {element}")
                else:
                    print(f"     ❌ Missing: {element}")
            
            print(f"   📋 Comparative mode preview:")
            print(f"   {comparative_result[:800]}...")
            
        except Exception as e:
            print(f"   ❌ Error in comparative mode: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # STEP 4: Test Individual Components
        print("🔧 STEP 4: Test Individual Route Sources")
        print("-" * 30)
        
        try:
            # Test explanatory drivers routes
            print("   🔍 Testing explanatory drivers routes...")
            
            cabins, companies, hauls = agent.pbi_collector._get_node_filters(node_path)
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            exp_drivers_routes = await agent._get_explanatory_drivers_routes(
                node_path, cabins, companies, hauls, start_dt, end_dt, "negative", 3
            )
            
            print(f"     📊 Explanatory drivers routes: {len(exp_drivers_routes.get('routes', []))} routes")
            print(f"     📋 Analysis: {exp_drivers_routes.get('analysis', 'No analysis')[:200]}...")
            
            # Test NCS routes
            print("   🔍 Testing NCS routes...")
            ncs_routes = await agent._get_ncs_routes(
                node_path, cabins, companies, hauls, start_dt, end_dt
            )
            
            print(f"     📊 NCS routes: {len(ncs_routes.get('routes', []))} routes")
            print(f"     📋 Analysis: {ncs_routes.get('analysis', 'No analysis')[:200]}...")
            
            # Test verbatims routes
            print("   🔍 Testing verbatims routes...")
            verbatims_routes = await agent._get_verbatims_routes(
                node_path, cabins, companies, hauls, start_dt, end_dt
            )
            
            print(f"     📊 Verbatims routes: {len(verbatims_routes.get('routes', []))} routes")
            print(f"     📋 Analysis: {verbatims_routes.get('analysis', 'No analysis')[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Error testing individual components: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # STEP 5: Check Expected Data Structure
        print("🔧 STEP 5: Check Routes Data Structure")
        print("-" * 30)
        
        try:
            # Check if routes_data is stored in collected_data
            if 'routes_data' in agent.collected_data:
                routes_data = agent.collected_data['routes_data']
                print(f"   ✅ Routes data stored in collected_data")
                print(f"   📊 Routes data keys: {list(routes_data.keys())}")
                
                # Check for expected keys
                expected_keys = [
                    'all_routes', 'exp_drivers_routes', 'ncs_routes', 
                    'verbatims_routes', 'similarities_analysis', 'total_routes'
                ]
                
                for key in expected_keys:
                    if key in routes_data:
                        if key == 'all_routes':
                            print(f"     ✅ {key}: {len(routes_data[key])} routes")
                        elif key == 'total_routes':
                            print(f"     ✅ {key}: {routes_data[key]}")
                        else:
                            print(f"     ✅ {key}: present")
                    else:
                        print(f"     ❌ Missing: {key}")
            else:
                print(f"   ⚠️ No routes_data found in collected_data")
                
        except Exception as e:
            print(f"   ❌ Error checking data structure: {str(e)}")
        
        print()
        print("🎉 DEBUG COMPLETE - ROUTES TOOL")
        
    except Exception as e:
        print(f"❌ General error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_routes_tool()) 