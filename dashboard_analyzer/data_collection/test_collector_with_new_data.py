#!/usr/bin/env python3
"""
Test script to test ChatbotVerbatimsCollector with new verbatims_sentiment data structure
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_verbatims_collector import ChatbotVerbatimsCollector
from pbi_collector import PBIDataCollector
import pandas as pd

async def test_collector_with_new_data():
    """Test the collector with new verbatims_sentiment data structure"""
    print("🔍 Testing ChatbotVerbatimsCollector with new verbatims_sentiment data...")
    
    try:
        # Initialize PBI collector
        pbi_collector = PBIDataCollector()
        print("✅ PBI collector initialized")
        
        # Initialize ChatbotVerbatimsCollector with PBI fallback
        collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
        print("✅ ChatbotVerbatimsCollector initialized")
        
        # Test the intelligent query filtering with the new data structure
        print("\n📊 Testing intelligent query filtering...")
        
        # Create a sample DataFrame with the new structure
        sample_data = {
            'verbatims_sentiment[respondent_id]': ['123', '456', '789'],
            'verbatims_sentiment[verbatim_global_sentiment]': ['Positive', 'Negative', 'Neutral'],
            'verbatims_sentiment[topic]': ['Service', 'Punctuality', 'Comfort'],
            'verbatims_sentiment[sentiment]': ['Positive', 'Negative', 'Neutral'],
            '[Verbatim]': [
                'Excelente servicio, muy amable la tripulación',
                'Terrible retraso, nunca más vuelo con esta aerolínea',
                'El asiento era cómodo pero el avión estaba sucio'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        print(f"📋 Sample data created with {len(df)} rows")
        print(f"🔧 Original columns: {list(df.columns)}")
        
        # Test column cleaning
        print("\n🧹 Testing column cleaning...")
        cleaned_df = collector._clean_verbatims_columns(df)
        print(f"✅ Cleaned columns: {list(cleaned_df.columns)}")
        
        # Test negative routes filtering
        print("\n🔍 Testing negative routes filtering...")
        negative_query = "¿Cuáles son las rutas con comentarios más negativos?"
        negative_result = collector._apply_intelligent_query_filter(cleaned_df, negative_query)
        print(f"✅ Negative filtering result: {len(negative_result)} rows")
        
        if not negative_result.empty:
            print("📄 Sample negative verbatims:")
            print(negative_result[['Verbatim_Text', 'verbatim_global_sentiment']].head())
        
        # Test representative comments filtering
        print("\n🔍 Testing representative comments filtering...")
        representative_query = "¿Cuáles son los comentarios más representativos de cada ruta?"
        representative_result = collector._apply_intelligent_query_filter(cleaned_df, representative_query)
        print(f"✅ Representative filtering result: {len(representative_result)} rows")
        
        if not representative_result.empty:
            print("📄 Sample representative verbatims:")
            print(representative_result[['Verbatim_Text', 'topic']].head())
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing collector: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_collector_with_new_data())
