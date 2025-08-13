#!/usr/bin/env python3
"""
Debug script for routes_tool - Comprehensive Analysis
Tests the complete flow from routes data collection to top 5 selection per driver
"""

import asyncio
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the dashboard_analyzer to the path
sys.path.append('/app')
sys.path.append('/app/dashboard_analyzer')

from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

async def debug_routes_comprehensive():
    print("🔧 DEBUGGING ROUTES_TOOL - COMPREHENSIVE ANALYSIS")
    print("=" * 80)
    
    # Test parameters - simulate causal scenario with known drivers
    node_path = "Global/LH/Business"
    start_date = "2025-08-01"
    end_date = "2025-08-07"
    comparison_filter = "vs L7d"
    
    # Simulate main drivers from explanatory_drivers_tool
    main_drivers = ["Punctuality", "Cabin Crew", "IB Plus loyalty program"]
    driver_shaps = {
        "Punctuality": -7.572,  # Negative SHAP
        "Cabin Crew": 3.091,    # Positive SHAP  
        "IB Plus loyalty program": -2.582  # Negative SHAP
    }
    
    print(f"📅 PERIOD: {start_date} to {end_date}")
    print(f"🎯 SEGMENT: {node_path}")
    print(f"📊 COMPARISON: {comparison_filter}")
    print(f"🎯 MAIN DRIVERS: {main_drivers}")
    print(f"📈 SHAP VALUES: {driver_shaps}")
    print()
    
    try:
        # Initialize PBI Collector
        pbi_collector = PBIDataCollector()
        print("✅ PBI Collector initialized")
        
        # Test 1: Get routes data with comparison
        print("\n" + "="*50)
        print("🧪 TEST 1: COLLECT ROUTES DATA WITH COMPARISON")
        print("="*50)
        
        # Calculate comparison dates
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        period_days = (end_dt - start_dt).days + 1
        
        comparison_end_dt = start_dt - timedelta(days=1)
        comparison_start_dt = comparison_end_dt - timedelta(days=period_days-1)
        
        routes_data = await pbi_collector.collect_routes_for_date_range(
            node_path=node_path,
            start_date=start_dt,
            end_date=end_dt,
            comparison_filter=comparison_filter,
            comparison_start_date=comparison_start_dt,
            comparison_end_date=comparison_end_dt
        )
        
        print(f"📊 Routes data shape: {routes_data.shape}")
        print(f"📊 Routes data columns: {list(routes_data.columns)}")
        if not routes_data.empty:
            print(f"📊 Routes data sample (first 3 rows):")
            print(routes_data.head(3))
        else:
            print("⚠️ No routes data found")
            return
        
        # Clean column names
        routes_data.columns = [col.replace('[', '').replace(']', '') for col in routes_data.columns]
        
        # Test 2: Identify key columns
        print("\n" + "="*50)
        print("🧪 TEST 2: IDENTIFY KEY COLUMNS")
        print("="*50)
        
        def find_column(df, possible_names):
            for name in possible_names:
                for col in df.columns:
                    if name.lower() in col.lower():
                        return col
            return None
        
        route_col = find_column(routes_data, ['route', 'Route', 'ROUTE'])
        nps_col = find_column(routes_data, ['nps', 'NPS', 'Nps'])
        nps_diff_col = find_column(routes_data, ['NPS diff', 'nps diff', 'nps_diff', 'vs'])
        pax_col = find_column(routes_data, ['pax', 'n (route)', 'Pax', 'PAX'])
        
        print(f"🔍 Route column: {route_col}")
        print(f"🔍 NPS column: {nps_col}")
        print(f"🔍 NPS diff column: {nps_diff_col}")
        print(f"🔍 Pax column: {pax_col}")
        
        # Find touchpoint columns for each driver
        touchpoint_mapping = {
            'punctuality': 'Operative',
            'cabin crew': 'Crew',
            'ib plus loyalty program': 'Loyalty',
            'arrivals experience': 'Arrivals',
            'journey preparation support': 'Journey',
            'boarding': 'Boarding',
            'in flight food and beverage': 'Food',
            'ease of contact by phone': 'Contact',
            'check-in': 'Check-in',
            'ife': 'IFE',
            'lounge': 'Lounge'
        }
        
        touchpoint_cols = {}
        for driver in main_drivers:
            touchpoint_name = touchpoint_mapping.get(driver.lower(), driver)
            touchpoint_col = find_column(routes_data, [touchpoint_name])
            touchpoint_cols[driver] = touchpoint_col
            print(f"🎯 {driver} -> {touchpoint_name} -> Column: {touchpoint_col}")
        
        # Test 3: Filter by minimum surveys
        print("\n" + "="*50)
        print("🧪 TEST 3: FILTER BY MINIMUM SURVEYS")
        print("="*50)
        
        min_surveys = 2  # Reduced to get more routes per driver
        original_count = len(routes_data)
        
        if pax_col:
            routes_data = routes_data[routes_data[pax_col].fillna(0) >= min_surveys]
            filtered_count = len(routes_data)
            print(f"📊 Original routes: {original_count}")
            print(f"📊 After min_surveys filter (>={min_surveys}): {filtered_count}")
        else:
            print(f"⚠️ No pax column found - cannot filter by min_surveys")
        
        # Test 4: Analyze each driver's routes
        print("\n" + "="*50)
        print("🧪 TEST 4: ANALYZE ROUTES PER DRIVER")
        print("="*50)
        
        for driver in main_drivers:
            print(f"\n🎯 ANALYZING DRIVER: {driver}")
            print(f"   SHAP: {driver_shaps[driver]}")
            
            touchpoint_col = touchpoint_cols[driver]
            if not touchpoint_col:
                print(f"   ❌ No touchpoint column found for {driver}")
                continue
            
            # Determine sorting logic based on SHAP
            shap_value = driver_shaps[driver]
            if shap_value < 0:
                # Negative SHAP: sort by worst CSAT first (ascending)
                sort_ascending = True
                sort_logic = "worst CSAT first (ascending)"
            else:
                # Positive SHAP: sort by best CSAT first (descending)
                sort_ascending = False
                sort_logic = "best CSAT first (descending)"
            
            print(f"   📈 Sorting logic: {sort_logic}")
            
            # Filter routes with valid touchpoint data
            valid_routes = routes_data[routes_data[touchpoint_col].notna()]
            print(f"   📊 Routes with valid {touchpoint_col} data: {len(valid_routes)}")
            
            if valid_routes.empty:
                print(f"   ⚠️ No routes with valid touchpoint data")
                continue
            
            # Sort by touchpoint CSAT
            sorted_routes = valid_routes.sort_values(touchpoint_col, ascending=sort_ascending)
            top_5_routes = sorted_routes.head(5)
            
            print(f"   🏆 TOP 5 ROUTES FOR {driver}:")
            for idx, (_, route) in enumerate(top_5_routes.iterrows(), 1):
                route_name = route.get(route_col, 'Unknown')
                nps_value = route.get(nps_col, 'N/A')
                nps_diff_value = route.get(nps_diff_col, 'N/A')
                pax_value = route.get(pax_col, 'N/A')
                csat_value = route.get(touchpoint_col, 'N/A')
                
                print(f"      {idx}. {route_name}: CSAT={csat_value}, NPS={nps_value}, NPS_diff={nps_diff_value}, Pax={pax_value}")
        
        # Test 5: Test NCS routes integration
        print("\n" + "="*50)
        print("🧪 TEST 5: NCS ROUTES INTEGRATION")
        print("="*50)
        
        print("🔍 EXPECTED BEHAVIOR:")
        print("   • Get routes from NCS incidents for the same period")
        print("   • Filter by segment (Global/LH/Business)")
        print("   • Combine with explanatory drivers routes")
        print("   • Provide NPS data for NCS routes if available")
        
        # Test 6: Consolidation logic
        print("\n" + "="*50)
        print("🧪 TEST 6: CONSOLIDATION ANALYSIS")
        print("="*50)
        
        print("🔍 CURRENT ISSUE:")
        print("   • Only getting 1 route total (MAD-MEX) in actual analysis")
        print("   • Should get up to 5 routes PER DRIVER")
        print("   • Should combine routes from explanatory drivers + NCS + verbatims")
        
        print(f"\n🔍 EXPECTED TOTAL ROUTES:")
        print(f"   • {len(main_drivers)} drivers × 5 routes each = up to {len(main_drivers) * 5} routes")
        print(f"   • Plus routes from NCS incidents")
        print(f"   • Plus routes from verbatims")
        print(f"   • Deduplicated final list with data from all sources")
        
        # Test 7: Sample size analysis
        print("\n" + "="*50)
        print("🧪 TEST 7: SAMPLE SIZE ANALYSIS")
        print("="*50)
        
        if not routes_data.empty and pax_col:
            print("📊 SAMPLE SIZE DISTRIBUTION:")
            sample_sizes = routes_data[pax_col].fillna(0)
            print(f"   Total routes: {len(sample_sizes)}")
            print(f"   Routes with ≥4 surveys: {sum(sample_sizes >= 4)}")
            print(f"   Routes with ≥10 surveys: {sum(sample_sizes >= 10)}")
            print(f"   Routes with ≥20 surveys: {sum(sample_sizes >= 20)}")
            print(f"   Max sample size: {sample_sizes.max()}")
            print(f"   Median sample size: {sample_sizes.median()}")
        
        print("\n" + "="*80)
        print("✅ DEBUGGING COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error during debugging: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_routes_comprehensive()) 