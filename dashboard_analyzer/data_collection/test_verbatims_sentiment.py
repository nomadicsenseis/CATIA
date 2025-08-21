#!/usr/bin/env python3
"""
Test script to test the verbatims_sentiment query
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pbi_collector import PBIDataCollector
import pandas as pd

async def test_verbatims_sentiment():
    """Test the verbatims_sentiment query"""
    print("🔍 Testing verbatims_sentiment query...")
    
    try:
        # Initialize PBI collector
        collector = PBIDataCollector()
        print("✅ PBI collector initialized")
        
        # The query provided by the user
        query = """
DEFINE  
    VAR __DS0FilterTable =
        TREATAS({"Business", "Economy", "Premium EC"}, 'Cabin_Master'[Cabin_Show])
 
    VAR __DS0FilterTable2 =
        TREATAS({"IB","YW"}, 'Company_Master'[Company])
 
    VAR __DS0FilterTable3 =
        TREATAS({"SH","LH"}, 'Haul_Master'[Haul_Aggr])
 
    VAR __DS0FilterTable4 =
        FILTER(
            KEEPFILTERS(VALUES('Date_Master'[Date])),
            'Date_Master'[Date] =date(2025,05,12)
        )
 
    var __DS0Core= 
ADDCOLUMNS(
    CALCULATETABLE(verbatims_sentiment,
            __DS0FilterTable,
            __DS0FilterTable2,
            __DS0FilterTable3,
            __DS0FilterTable4), "Verbatim", 
CALCULATE(min(surveys_maritz[nps_all_t])))
 
EVALUATE
    __DS0Core
"""
        
        print("📊 Executing verbatims_sentiment query...")
        result = await collector._execute_query_async(query)
        
        if result is not None:
            print(f"✅ Query successful! Result: {len(result)} rows")
            print(f"📋 Columns: {list(result.columns)}")
            
            if len(result) > 0:
                print(f"\n📄 First few rows:")
                print(result.head().to_string())
                
                # Show data types
                print(f"\n🔍 Data types:")
                print(result.dtypes)
                
                # Show unique values in key columns
                print(f"\n🎯 Unique values in key columns:")
                for col in result.columns:
                    if result[col].dtype == 'object':  # String columns
                        unique_vals = result[col].unique()
                        print(f"   {col}: {len(unique_vals)} unique values")
                        if len(unique_vals) <= 10:
                            print(f"      Values: {unique_vals}")
            else:
                print("⚠️  Query returned 0 rows - check filters")
        else:
            print("❌ Query failed - no result returned")
            
    except Exception as e:
        print(f"❌ Error testing verbatims_sentiment: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_verbatims_sentiment())
