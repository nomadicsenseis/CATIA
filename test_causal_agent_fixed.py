#!/usr/bin/env python3
"""
Test script to verify all causal agent tools work with corrected DAX queries
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

async def test_causal_agent_fixed():
    """Test the causal agent with corrected DAX queries"""
    
    print("🧪 TESTING CAUSAL AGENT WITH FIXED DAX QUERIES")
    print("=" * 60)
    
    # Configuration
    node_path = "Global/SH/Business/YW"
    start_date = "2025-08-01"
    end_date = "2025-08-07"
    comparison_filter = "vs L7d"
    
    print(f"🎯 Segment: {node_path}")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"🔍 Comparison: {comparison_filter}")
    print(f"📊 Mode: comparative")
    print()
    
    try:
        # Initialize PBI collector
        print("📊 Initializing PBI Data Collector...")
        pbi_collector = PBIDataCollector()
        
        # Initialize causal agent
        print("🔧 Initializing Causal Explanation Agent...")
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(),
            silent_mode=False  # Enable logging to see what's happening
        )
        agent.pbi_collector = pbi_collector
        
        print("✅ Agent initialized successfully")
        print()
        
        # Execute the causal analysis
        print("🚀 Starting causal analysis...")
        print("-" * 40)
        
        result = await agent.investigate_anomaly(
            node_path=node_path,
            start_date=start_date,
            end_date=end_date,
            anomaly_type="negative",  # Default anomaly type
            anomaly_magnitude=-10.0,   # Default magnitude
            causal_filter=comparison_filter
        )
        
        print("✅ Causal analysis completed!")
        print()
        
        # Display results summary
        print("📋 ANALYSIS RESULTS SUMMARY:")
        print("=" * 40)
        
        if result:
            print(f"✅ Analysis completed successfully")
            print(f"📊 Result type: {type(result)}")
            
            # Check if all tools were executed
            if hasattr(agent, 'collected_data'):
                print(f"🔧 Tools executed: {list(agent.collected_data.keys())}")
                
                # Check specific tools
                tools_to_check = [
                    'explanatory_drivers',
                    'operative_data', 
                    'ncs_data',
                    'routes_data',
                    'customer_profile',
                    'verbatims'
                ]
                
                for tool in tools_to_check:
                    if tool in agent.collected_data:
                        data = agent.collected_data[tool]
                        if data:
                            print(f"  ✅ {tool}: Data available ({type(data)})")
                        else:
                            print(f"  ⚠️ {tool}: No data")
                    else:
                        print(f"  ❌ {tool}: Not executed")
            else:
                print("⚠️ No collected_data found in agent")
        else:
            print("❌ Analysis failed or returned no result")
        
        print()
        print("🎯 TEST COMPLETED - Check the output above for any errors")
        
    except Exception as e:
        print(f"❌ Error during causal agent test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Causal Agent Test with Fixed DAX...")
    asyncio.run(test_causal_agent_fixed())
    print("✅ Test completed") 