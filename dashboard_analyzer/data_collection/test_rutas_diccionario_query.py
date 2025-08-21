#!/usr/bin/env python3
"""
Test to see exactly what the Rutas Diccionario query returns
"""

import sys
import os
import asyncio
import logging

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_rutas_diccionario_query():
    """Test the Rutas Diccionario query to see what it returns"""
    
    print("🧪 RUTAS DICCIONARIO QUERY TEST")
    print("=" * 50)
    
    try:
        # Import the PBI collector
        from pbi_collector import PBIDataCollector
        
        print("📋 Step 1: Initialize PBIDataCollector")
        
        # Initialize collector
        collector = PBIDataCollector()
        print("✅ PBIDataCollector initialized successfully")
        
        print()
        print("📋 Step 2: Load and display the query")
        
        # Load the query template
        template = collector._load_query_template("Rutas Diccionario.txt")
        print("📄 Query content:")
        print("-" * 30)
        print(template)
        print("-" * 30)
        
        print()
        print("📋 Step 3: Execute query and analyze response")
        
        # Execute the query
        result = await collector._execute_query_async(template)
        
        print(f"📊 Query result type: {type(result)}")
        print(f"📊 Result shape: {result.shape if hasattr(result, 'shape') else 'N/A'}")
        print(f"📊 Is empty: {result.empty if hasattr(result, 'empty') else 'N/A'}")
        
        if hasattr(result, 'columns'):
            print(f"📋 Raw column names: {list(result.columns)}")
            print(f"📋 Column types: {[type(col) for col in result.columns]}")
        
        if not result.empty and len(result) > 0:
            print()
            print("📋 First 5 rows (raw data):")
            print(result.head().to_string())
            
            print()
            print("📋 Sample data analysis:")
            for i, (_, row) in enumerate(result.head(3).iterrows()):
                print(f"  Row {i+1}:")
                for col_name in result.columns:
                    value = row[col_name] if col_name in row else "NOT_FOUND"
                    print(f"    {col_name}: {value} ({type(value)})")
                print()
        
        print()
        print("📋 Step 4: Test new routes dictionary column cleaning")
        
        # Test the new cleaning method
        cleaned_result = collector._clean_routes_dictionary_columns(result.copy()) if not result.empty else result
        
        if not cleaned_result.empty:
            print(f"📋 Cleaned column names: {list(cleaned_result.columns)}")
            
            print()
            print("📋 Sample cleaned data:")
            for i, (_, row) in enumerate(cleaned_result.head(3).iterrows()):
                print(f"  Row {i+1}:")
                for col_name in cleaned_result.columns:
                    value = row[col_name] if col_name in row else "NOT_FOUND"
                    print(f"    {col_name}: {value}")
                print()
        
        print()
        print("📋 Step 5: Test the actual collect_routes_dictionary method")
        
        # Test the actual method that will be used
        routes_dict = await collector.collect_routes_dictionary()
        
        if routes_dict is not None and not routes_dict.empty:
            print(f"📋 Final routes dictionary columns: {list(routes_dict.columns)}")
            print(f"📊 Number of routes: {len(routes_dict)}")
            
            print()
            print("📋 Sample final data:")
            for i, (_, route) in enumerate(routes_dict.head(3).iterrows()):
                route_info = route.get('route', 'N/A')
                haul_info = route.get('haul_aggr', 'N/A')
                print(f"  {route_info} -> {haul_info}")
        else:
            print("⚠️ Routes dictionary is empty")
        
        print()
        print("🎉 TEST COMPLETED!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_rutas_diccionario_query())
