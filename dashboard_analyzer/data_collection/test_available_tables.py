#!/usr/bin/env python3
"""
Test script to explore ALL available tables in Power BI
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pbi_collector import PBIDataCollector
import pandas as pd

async def test_all_available_tables():
    """Test what tables are available in Power BI"""
    print("🔍 Testing ALL available tables in Power BI...")
    
    try:
        # Initialize PBI collector
        collector = PBIDataCollector()
        print("✅ PBI collector initialized")
        
        # List of common table names to test
        common_tables = [
            'NPS_Data',
            'Route_Master', 
            'Customer_Data',
            'Survey_Data',
            'Feedback_Data',
            'Comments_Data',
            'Text_Responses',
            'Open_Ended',
            'Qualitative_Data',
            'Customer_Feedback',
            'Route_Performance',
            'Operational_Data',
            'Incident_Data',
            'NCS_Data',
            'Quality_Data',
            'Service_Data',
            'Flight_Data',
            'Booking_Data',
            'Reservation_Data',
            'Passenger_Data'
        ]
        
        print(f"\n📊 Testing {len(common_tables)} common table names...")
        
        available_tables = []
        for table_name in common_tables:
            try:
                # Simple query to test table existence
                test_query = f"EVALUATE TOPN(1, '{table_name}')"
                result = await collector._execute_query_async(test_query)
                
                if result is not None and len(result) > 0:
                    print(f"✅ Table '{table_name}' found: {len(result)} rows")
                    available_tables.append(table_name)
                    
                    # Show sample data structure
                    if len(result) > 0:
                        print(f"   📋 Columns: {list(result.columns)}")
                        print(f"   📄 Sample row: {result.iloc[0].to_dict()}")
                        print()
                else:
                    print(f"❌ Table '{table_name}' not found or empty")
                    
            except Exception as e:
                print(f"❌ Table '{table_name}' error: {str(e)[:100]}...")
        
        print(f"\n🎯 SUMMARY: Found {len(available_tables)} available tables:")
        for table in available_tables:
            print(f"   - {table}")
            
        if len(available_tables) == 0:
            print("\n⚠️  No tables found! This suggests a connection issue.")
        else:
            print(f"\n💡 SUGGESTION: Use these available tables to find verbatims data")
            
    except Exception as e:
        print(f"❌ Error testing tables: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_all_available_tables())
