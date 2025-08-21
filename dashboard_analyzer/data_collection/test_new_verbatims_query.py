#!/usr/bin/env python3
"""
Test script to test the new verbatims query with verbatims_sentiment table
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pbi_collector import PBIDataCollector
import pandas as pd

async def test_new_verbatims_query():
    """Test the new verbatims query"""
    print("🔍 Testing new verbatims query with verbatims_sentiment table...")
    
    try:
        # Initialize PBI collector
        collector = PBIDataCollector()
        print("✅ PBI collector initialized")
        
        # Read the new query from file
        query_file = "queries/Verbatims.txt"
        if os.path.exists(query_file):
            with open(query_file, 'r', encoding='utf-8') as f:
                query = f.read()
            print(f"📄 Loaded query from {query_file}")
        else:
            print(f"❌ Query file {query_file} not found")
            return
        
        print("📊 Executing new verbatims query...")
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
                        unique_vals = result[col].dropna().unique()
                        print(f"   {col}: {len(unique_vals)} unique values")
                        if len(unique_vals) <= 10:
                            print(f"      Values: {unique_vals}")
                
                # Test sentiment distribution
                if 'sentiment_score' in result.columns:
                    print(f"\n📊 Sentiment Score Distribution:")
                    print(f"   Min: {result['sentiment_score'].min()}")
                    print(f"   Max: {result['sentiment_score'].max()}")
                    print(f"   Mean: {result['sentiment_score'].mean():.3f}")
                    print(f"   Negative (< 0): {len(result[result['sentiment_score'] < 0])}")
                    print(f"   Positive (> 0): {len(result[result['sentiment_score'] > 0])}")
                    print(f"   Neutral (= 0): {len(result[result['sentiment_score'] == 0])}")
                
                # Test theme detection
                theme_columns = [col for col in result.columns if col.startswith('Theme_')]
                if theme_columns:
                    print(f"\n🎭 Theme Detection Results:")
                    for theme_col in theme_columns:
                        theme_name = theme_col.replace('Theme_', '')
                        theme_count = result[theme_col].sum()
                        print(f"   {theme_name}: {theme_count} mentions")
                
                # Test route extraction
                if 'Route' in result.columns:
                    routes = result['Route'].dropna().unique()
                    print(f"\n🛫 Routes found: {len(routes)}")
                    if len(routes) <= 10:
                        print(f"   Sample routes: {list(routes)}")
                
            else:
                print("⚠️  Query returned 0 rows - check filters")
        else:
            print("❌ Query failed - no result returned")
            
    except Exception as e:
        print(f"❌ Error testing new verbatims query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_new_verbatims_query())
