#!/usr/bin/env python3
"""
Test script to explore available tables in Power BI for verbatims data
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pbi_collector import PBIDataCollector
import pandas as pd

async def test_available_tables():
    """Test what tables are available in Power BI"""
    print("🔍 Testing Power BI table availability for verbatims...")
    
    try:
        # Initialize PBI collector
        collector = PBIDataCollector()
        
        # Test basic connection
        print("✅ PBI collector initialized")
        
        # Try to get table schema information
        print("\n📊 Testing table discovery...")
        
        # Test a simple query to see what's available
        test_query = """
        EVALUATE
        ADDCOLUMNS(
            SUMMARIZE(
                'NPS_Data',
                'NPS_Data'[Date],
                'NPS_Data'[Survey_ID],
                'NPS_Data'[Route]
            ),
            "Sample_Count", COUNTROWS('NPS_Data')
        )
        """
        
        print("🔍 Testing NPS_Data table...")
        try:
            result = await collector._execute_query_async(test_query)
            print(f"✅ NPS_Data table accessible: {len(result)} rows")
            if len(result) > 0:
                print(f"📋 Sample columns: {list(result.columns)}")
                print(f"📊 Sample data:\n{result.head(3)}")
        except Exception as e:
            print(f"❌ NPS_Data table error: {e}")
        
        # Test for verbatims-related tables
        print("\n🔍 Testing for verbatims-related tables...")
        
        # Try different possible table names
        possible_tables = [
            'Verbatims_Data',
            'Verbatims',
            'Comments',
            'Feedback',
            'Survey_Comments',
            'Customer_Feedback',
            'Text_Responses'
        ]
        
        for table_name in possible_tables:
            test_query = f"""
            EVALUATE
            ADDCOLUMNS(
                SUMMARIZE(
                    '{table_name}',
                    '{table_name}'[Date]
                ),
                "Sample_Count", COUNTROWS('{table_name}')
            )
            """
            
            try:
                result = await collector._execute_query_async(test_query)
                print(f"✅ Table '{table_name}' found: {len(result)} rows")
                if len(result) > 0:
                    print(f"📋 Columns: {list(result.columns)}")
            except Exception as e:
                print(f"❌ Table '{table_name}' not accessible: {str(e)[:100]}...")
        
        # Test for any tables with text content
        print("\n🔍 Testing for tables with text content...")
        
        # Try to find tables that might contain verbatims
        text_search_query = """
        EVALUATE
        ADDCOLUMNS(
            SUMMARIZE(
                'NPS_Data',
                'NPS_Data'[Date]
            ),
            "Has_Comments", IF(
                ISBLANK('NPS_Data'[Comments]) || ISBLANK('NPS_Data'[Feedback]) || ISBLANK('NPS_Data'[Text_Response]),
                "No",
                "Yes"
            )
        )
        """
        
        try:
            result = await collector._execute_query_async(text_search_query)
            print(f"✅ Text content test completed: {len(result)} rows")
            if len(result) > 0:
                print(f"📋 Text columns found: {list(result.columns)}")
        except Exception as e:
            print(f"❌ Text content test error: {e}")
        
        # Test for survey-related tables
        print("\n🔍 Testing for survey-related tables...")
        
        survey_tables = [
            'Survey_Data',
            'Survey_Responses',
            'Customer_Surveys',
            'Feedback_Data'
        ]
        
        for table_name in survey_tables:
            test_query = f"""
            EVALUATE
            ADDCOLUMNS(
                SUMMARIZE(
                    '{table_name}',
                    '{table_name}'[Date]
                ),
                "Sample_Count", COUNTROWS('{table_name}')
            )
            """
            
            try:
                result = await collector._execute_query_async(test_query)
                print(f"✅ Survey table '{table_name}' found: {len(result)} rows")
                if len(result) > 0:
                    print(f"📋 Columns: {list(result.columns)}")
            except Exception as e:
                print(f"❌ Survey table '{table_name}' not accessible: {str(e)[:100]}...")
        
        print("\n🎯 Summary of available tables:")
        print("Based on the tests above, we can see which tables are accessible")
        print("and adapt the verbatims query accordingly.")
        
    except Exception as e:
        print(f"❌ Error in table discovery: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_available_tables())
