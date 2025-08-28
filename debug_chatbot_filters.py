#!/usr/bin/env python3
"""
Debug chatbot filters to see what's being applied
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append('/app')

from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

def debug_chatbot_filters():
    """Debug what filters are being applied to the chatbot"""
    print("🔍 DEBUGGING CHATBOT FILTERS")
    print("=" * 50)
    
    # Initialize collectors
    print("1️⃣ Initializing collectors...")
    pbi_collector = PBIDataCollector()
    verbatims_collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
    
    # Test different filter combinations
    test_cases = [
        {
            "name": "No filters",
            "filters": None
        },
        {
            "name": "Business cabin only",
            "filters": {'cabin': ['Business']}
        },
        {
            "name": "Long Haul only",
            "filters": {'haul': ['LH']}
        },
        {
            "name": "Business + Long Haul",
            "filters": {'cabin': ['Business'], 'haul': ['LH']}
        },
        {
            "name": "Iberia fleet only",
            "filters": {'fleet': ['IB']}
        }
    ]
    
    question = "What are the main customer complaints?"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']}")
        print(f"   Filters: {test_case['filters']}")
        
        try:
            # Test with very short timeout to see if filters affect response time
            answer_data = verbatims_collector.ask_chatbot_question(
                question=question,
                start_date="2025-08-15",
                end_date="2025-08-21",
                node_path="Global",
                filters=test_case['filters']
            )
            
            if answer_data:
                print(f"   ✅ Got answer!")
                print(f"   📝 Answer: {answer_data.get('answer', 'No answer')[:100]}...")
            else:
                print(f"   ⚠️ No answer received")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Only test first case to avoid long waits
        if i == 1:
            print("   🛑 Stopping after first test to avoid long waits...")
            break
    
    print("\n🎉 FILTER DEBUG COMPLETED!")

if __name__ == "__main__":
    debug_chatbot_filters()
