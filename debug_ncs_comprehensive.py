#!/usr/bin/env python3
"""
Debug script for ncs_tool - Comprehensive Analysis
Tests the complete flow from NCS data collection to temporal comparison matrix
"""

import asyncio
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the dashboard_analyzer to the path
sys.path.append('/app')
sys.path.append('/app/dashboard_analyzer')

from dashboard_analyzer.data_collection.ncs_collector import NCSDataCollector
from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent

async def debug_ncs_comprehensive():
    print("🔧 DEBUGGING NCS_TOOL - COMPREHENSIVE ANALYSIS")
    print("=" * 80)
    
    # Test parameters - simulate causal scenario
    node_path = "Global/LH/Business"  # LH + Business cabin - test new filtering logic
    current_start = "2025-08-01"
    current_end = "2025-08-07"
    
    # Calculate comparison period (previous week)
    current_start_dt = datetime.strptime(current_start, '%Y-%m-%d')
    current_end_dt = datetime.strptime(current_end, '%Y-%m-%d')
    period_days = (current_end_dt - current_start_dt).days + 1
    
    comparison_end_dt = current_start_dt - timedelta(days=1)
    comparison_start_dt = comparison_end_dt - timedelta(days=period_days-1)
    
    comparison_start = comparison_start_dt.strftime('%Y-%m-%d')
    comparison_end = comparison_end_dt.strftime('%Y-%m-%d')
    
    print(f"📅 CURRENT PERIOD: {current_start} to {current_end} ({period_days} days)")
    print(f"📅 COMPARISON PERIOD: {comparison_start} to {comparison_end} ({period_days} days)")
    print()
    
    try:
        # Initialize NCS Collector with temp credentials
        temp_creds_file = "dashboard_analyzer/temp_aws_credentials.env"
        ncs_collector = NCSDataCollector(temp_env_file=temp_creds_file)
        print("✅ NCS Collector initialized with temp AWS credentials")
        
        # Test 1: Get NCS data for current period (all days)
        print("\n" + "="*50)
        print("🧪 TEST 1: COLLECT CURRENT PERIOD NCS DATA")
        print("="*50)
        
        current_data = ncs_collector.collect_ncs_data_for_date_range(
            start_date=current_start_dt,
            end_date=current_end_dt
        )
        
        print(f"📊 Current period data shape: {current_data.shape}")
        print(f"📊 Current period columns: {list(current_data.columns)}")
        if not current_data.empty:
            print(f"📊 Current period sample (first 3 rows):")
            print(current_data.head(3))
        else:
            print("⚠️ No current period data found")
        
        # Test 2: Get NCS data for comparison period (all days)
        print("\n" + "="*50)
        print("🧪 TEST 2: COLLECT COMPARISON PERIOD NCS DATA")
        print("="*50)
        
        comparison_data = ncs_collector.collect_ncs_data_for_date_range(
            start_date=comparison_start_dt,
            end_date=comparison_end_dt
        )
        
        print(f"📊 Comparison period data shape: {comparison_data.shape}")
        print(f"📊 Comparison period columns: {list(comparison_data.columns)}")
        if not comparison_data.empty:
            print(f"📊 Comparison period sample (first 3 rows):")
            print(comparison_data.head(3))
        else:
            print("⚠️ No comparison period data found")
        
        # Test 3: Test segment filtering
        print("\n" + "="*50)
        print("🧪 TEST 3: SEGMENT FILTERING")
        print("="*50)
        
        # Create a mock causal agent to test filtering logic (skip if complex)
        # agent = CausalExplanationAgent(
        #     llm_type="aws",
        #     pbi_collector=None,
        #     config={
        #         "comparison_mode": "vslast",
        #         "comparison_days": 7,
        #         "causal_filter": "vs L7d"
        #     }
        # )
        
        print("🔍 Skipping segment filtering test for now - focusing on raw data analysis")
        
        print(f"🔍 Testing segment filtering for: {node_path}")
        
        # Apply segment filtering to match the actual NCS tool behavior
        print(f"🔍 Applying segment filtering for: {node_path}")
        
        # Create a mock agent to use the filtering method
        from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        
        mock_agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(), 
            silent_mode=True, 
            detection_mode='vslast', 
            causal_filter='vs L7d', 
            study_mode='comparative'
        )
        
        # Apply segment filtering
        filtered_current = await mock_agent._filter_ncs_by_segment(current_data, node_path)
        filtered_comparison = await mock_agent._filter_ncs_by_segment(comparison_data, node_path)
        
        print(f"📊 After segment filtering:")
        print(f"   Current period: {len(filtered_current)}/{len(current_data)} incidents")
        print(f"   Comparison period: {len(filtered_comparison)}/{len(comparison_data)} incidents")
        
        # Test 4: Test temporal comparison analysis
        print("\n" + "="*50)
        print("🧪 TEST 4: TEMPORAL COMPARISON ANALYSIS")
        print("="*50)
        
        if not filtered_current.empty and not filtered_comparison.empty:
            temporal_analysis = ncs_collector.create_temporal_comparison_analysis(
                current_data=filtered_current,
                comparison_data=filtered_comparison,
                current_period=f"{current_start} to {current_end}",
                comparison_period=f"{comparison_start} to {comparison_end}",
                node_path=node_path
            )
            
            print("📊 TEMPORAL ANALYSIS RESULT:")
            print(f"Analysis keys: {list(temporal_analysis.keys())}")
            
            if 'error' in temporal_analysis:
                print(f"❌ ERROR: {temporal_analysis['error']}")
            else:
                # Show route × incident matrix
                if 'route_incident_matrix' in temporal_analysis:
                    matrix = temporal_analysis['route_incident_matrix']
                    print(f"\n🗺️ ROUTE × INCIDENT MATRIX:")
                    print(f"Matrix keys: {list(matrix.keys()) if matrix else 'Empty'}")
                    
                    for route, incidents in (matrix.items() if matrix else []):
                        print(f"   Route: {route}")
                        for incident_type, data in incidents.items():
                            print(f"      {incident_type}: {data}")
                
                # Show incident type deltas
                if 'incident_type_deltas' in temporal_analysis:
                    deltas = temporal_analysis['incident_type_deltas']
                    print(f"\n📈 INCIDENT TYPE DELTAS:")
                    for incident_type, delta_data in deltas.items():
                        print(f"   {incident_type}: {delta_data}")
                
                # Show analysis summary
                if 'analysis_summary' in temporal_analysis:
                    print(f"\n📋 ANALYSIS SUMMARY:")
                    print(temporal_analysis['analysis_summary'])
        else:
            print("⚠️ Insufficient data for temporal comparison")
        
        # Test 5: Test route aggregation
        print("\n" + "="*50)
        print("🧪 TEST 5: ROUTE AGGREGATION ANALYSIS")
        print("="*50)
        
        print("🔍 EXPECTED BEHAVIOR:")
        print("   • Sum incidents for EACH ROUTE across ALL DAYS in period")
        print("   • Create table: Route × IncidentType × Count for each period")
        print("   • Calculate differences: Current - Comparison for each cell")
        print("   • Handle missing routes (treat as 0)")
        
        if not filtered_current.empty:
            print(f"\n📊 CURRENT PERIOD ROUTES:")
            # Extract route information from current data
            route_analysis_current = ncs_collector._extract_route_analysis_from_data(filtered_current)
            print(f"Routes found: {route_analysis_current}")
            
        if not filtered_comparison.empty:
            print(f"\n📊 COMPARISON PERIOD ROUTES:")
            # Extract route information from comparison data  
            route_analysis_comparison = ncs_collector._extract_route_analysis_from_data(filtered_comparison)
            print(f"Routes found: {route_analysis_comparison}")
        
        # Test 6: Test incident type aggregation
        print("\n" + "="*50)
        print("🧪 TEST 6: INCIDENT TYPE AGGREGATION")
        print("="*50)
        
        if not filtered_current.empty:
            print(f"\n📊 CURRENT PERIOD INCIDENT COUNTS:")
            incident_counts_current = ncs_collector._extract_incident_counts_from_data(filtered_current)
            print(f"Incident counts: {incident_counts_current}")
            
        if not filtered_comparison.empty:
            print(f"\n📊 COMPARISON PERIOD INCIDENT COUNTS:")
            incident_counts_comparison = ncs_collector._extract_incident_counts_from_data(filtered_comparison)
            print(f"Incident counts: {incident_counts_comparison}")
        
        print("\n" + "="*80)
        print("✅ DEBUGGING COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error during debugging: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ncs_comprehensive()) 