#!/usr/bin/env python3
"""
Debug script for operative_data_tool - Comprehensive Analysis
Tests the complete flow from DAX query to agent response
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
from dashboard_analyzer.anomaly_explanation.data_analyzer import OperationalDataAnalyzer

# Test configuration
target_date = datetime(2025, 8, 7)
comparison_days = 7

async def debug_mishandling_segments():
    # PROBAR DIFERENTES SEGMENTOS PARA MISHANDLING
    test_segments = [
        ("Global", "SH", "Economy", "IB"),     # Short Haul Economy IB
        ("Global", "LH", "Business", "IB"),    # Original que falla
        ("Global", "", "Economy", ""),         # Solo Economy
        ("Global", "", "", ""),                # Global sin filtros
    ]

    print("🔧 DEBUGGING OPERATIVE_DATA_TOOL - MISHANDLING ANALYSIS")
    print("=" * 80)

    for segment in test_segments:
        node_path = "/".join(filter(None, segment))  # Remove empty strings
        print(f"\n🎯 TESTING SEGMENT: {node_path}")
        print("=" * 50)
        
        try:
        # Initialize PBI collector
        pbi_collector = PBIDataCollector()
        print("✅ PBI Collector initialized")
        
        # Collect current period data
        print(f"📅 COLLECTING DATA FOR: {node_path}")
        current_data = await pbi_collector.collect_operative_data_for_date(
            target_date=target_date,
            node_path=node_path,
            comparison_days=comparison_days
        )
        
        if current_data is not None and not current_data.empty:
            mishandling_col = current_data['Mishandling']
            unique_count = mishandling_col.nunique()
            min_val = mishandling_col.min()
            max_val = mishandling_col.max()
            sample_vals = mishandling_col.head(5).tolist()
            
            print(f"   📊 Data shape: {current_data.shape}")
            print(f"   🎯 Mishandling unique values: {unique_count}")
            print(f"   📈 Mishandling range: {min_val:.3f} to {max_val:.3f}")
            print(f"   📋 Sample values: {sample_vals}")
            
            if unique_count > 1:
                print(f"   🎉 SUCCESS: Found real Mishandling data!")
                break
            else:
                print(f"   ❌ FAIL: All Mishandling values are {min_val}")
        else:
            print(f"   ❌ NO DATA returned for segment")
            
    except Exception as e:
        print(f"   💥 ERROR: {str(e)}")

    print("\n" + "=" * 80)
    print("✅ MISHANDLING SEGMENT ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(debug_mishandling_segments()) 