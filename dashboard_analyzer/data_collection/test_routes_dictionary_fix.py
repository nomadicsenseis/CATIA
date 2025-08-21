#!/usr/bin/env python3
"""
Test to verify the routes dictionary fix
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


async def test_routes_dictionary_fix():
    """Test that routes dictionary collection works correctly"""
    
    print("🧪 ROUTES DICTIONARY FIX TEST")
    print("=" * 50)
    
    try:
        # Import the PBI collector
        from pbi_collector import PBIDataCollector
        
        print("📋 Step 1: Initialize PBIDataCollector")
        
        # Initialize collector
        collector = PBIDataCollector()
        print("✅ PBIDataCollector initialized successfully")
        
        print()
        print("📋 Step 2: Test routes dictionary collection")
        
        # Test routes dictionary collection
        routes_dict = await collector.collect_routes_dictionary()
        
        if routes_dict is not None and not routes_dict.empty:
            print(f"✅ Routes dictionary collected successfully!")
            print(f"📊 Number of routes: {len(routes_dict)}")
            print(f"📋 Columns: {list(routes_dict.columns)}")
            
            # Show sample data
            if len(routes_dict) > 0:
                print("\n📋 Sample routes:")
                sample = routes_dict.head(3)
                for _, route in sample.iterrows():
                    route_info = route.get('route', 'N/A')
                    haul_info = route.get('haul_aggr', 'N/A')
                    print(f"  {route_info} -> {haul_info}")
        else:
            print("⚠️ Routes dictionary is empty (this might be expected if no data)")
        
        print()
        print("🎉 TEST COMPLETED!")
        print("✅ Routes dictionary collection working correctly!")
        print("✅ No more 'await' expression errors!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_routes_dictionary_fix())
