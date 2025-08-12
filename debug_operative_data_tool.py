#!/usr/bin/env python3
"""
Debug script for operative_data_tool
Tests the complete flow from DAX query to agent response
"""

import asyncio
import pandas as pd
from datetime import datetime
import logging
import json

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def debug_operative_data_tool():
    print("🔍 DEBUGGING OPERATIVE_DATA_TOOL")
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
        # Step 1: Test PBI Collector
        print("🔧 STEP 1: Testing PBI Collector")
        print("-" * 30)
        
        from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
        
        pbi_collector = PBIDataCollector()
        
        # Convert dates
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Test the operative data query generation
        cabins, companies, hauls = pbi_collector._get_node_filters(node_path)
        print(f"   Filters - Cabins: {cabins}, Companies: {companies}, Hauls: {hauls}")
        
        # Generate the query
        try:
            # For operative data, we use the existing method for single date
            query = pbi_collector._get_flexible_operative_query(7, cabins, companies, hauls, start_dt)
            print(f"   📜 Generated DAX Query (Flexible Operative):")
            print("   " + "-" * 40)
            print("   " + query.replace('\n', '\n   '))
        except Exception as e:
            print(f"   ❌ Query generation failed: {e}")
            return
        print()
        
        # Step 2: Test query execution
        print("🔧 STEP 2: Testing Query Execution")
        print("-" * 30)
        
        try:
            df_operative = await pbi_collector.collect_operative_data_for_date(
                node_path=node_path,
                target_date=start_dt,
                comparison_days=7,
                use_flexible=True
            )
            
            print(f"   ✅ Query executed successfully")
            print(f"   📊 DataFrame shape: {df_operative.shape}")
            print(f"   📋 Columns: {list(df_operative.columns)}")
            print(f"   📋 First few rows:")
            print(df_operative.head(3).to_string(index=False))
            print()
            
        except Exception as e:
            print(f"   ❌ Query execution failed: {e}")
            return
        
        # Step 3: Test data analyzer
        print("🔧 STEP 3: Testing Data Analyzer")
        print("-" * 30)
        
        from dashboard_analyzer.anomaly_explanation.data_analyzer import OperationalDataAnalyzer
        
        analyzer = OperationalDataAnalyzer(comparison_mode="vslast")
        
        # Load data into analyzer
        analyzer.operative_data[node_path] = df_operative
        
        print(f"   📊 Data loaded into analyzer")
        print(f"   🔍 Testing column cleaning...")
        
        # Test the column cleaning
        cleaned_df = analyzer._clean_dax_columns(df_operative.copy())
        print(f"   📋 Cleaned columns: {list(cleaned_df.columns)}")
        
        if 'Date' in cleaned_df.columns:
            print(f"   ✅ Date column found after cleaning")
            print(f"   📅 Date column sample: {cleaned_df['Date'].head(3).tolist()}")
        else:
            print(f"   ❌ Date column still missing after cleaning")
        print()
        
        # Step 4: Test analyzer method
        print("🔧 STEP 4: Testing Analyzer Method")
        print("-" * 30)
        
        try:
            result = analyzer.analyze_operative_metrics(node_path, start_date)
            print(f"   ✅ Analyzer method executed successfully")
            print(f"   📊 Result type: {type(result)}")
            print(f"   📋 Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
            
            if isinstance(result, dict) and 'error' in result:
                print(f"   ❌ Analyzer returned error: {result['error']}")
            else:
                print(f"   ✅ Analyzer returned valid result")
                
        except Exception as e:
            print(f"   ❌ Analyzer method failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 5: Test causal explanation agent method
        print("🔧 STEP 5: Testing Causal Explanation Agent")
        print("-" * 30)
        
        try:
            from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
            from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType, get_default_llm_type
            
            agent = CausalExplanationAgent(
                llm_type=get_default_llm_type(),
                config_path="dashboard_analyzer/anomaly_explanation/config/prompts/causal_explanation.yaml",
                logger=logging.getLogger("debug_causal"),
                causal_filter="vs L7d",
                comparison_start_date=None,
                comparison_end_date=None
            )
            
            agent.pbi_collector = pbi_collector
            
            # Test the tool method
            result = await agent._operative_data_tool(node_path, start_date, end_date)
            print(f"   ✅ Agent tool executed")
            print(f"   📊 Result length: {len(result) if isinstance(result, str) else 'Not a string'}")
            print(f"   📋 Result preview: {result[:200]}..." if isinstance(result, str) else f"Result: {result}")
            
        except Exception as e:
            print(f"   ❌ Agent tool failed: {e}")
            import traceback
            traceback.print_exc()
    
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_operative_data_tool()) 