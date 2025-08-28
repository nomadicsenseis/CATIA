#!/usr/bin/env python3
"""
Test the updated verbatims_tool with real chatbot
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append('/app')

from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

def test_verbatims_tool_updated():
    """Test the updated verbatims_tool with real chatbot"""
    print("🤖 TESTING UPDATED VERBATIMS TOOL WITH REAL CHATBOT")
    print("=" * 60)
    
    # Initialize collectors
    print("1️⃣ Initializing collectors...")
    pbi_collector = PBIDataCollector()
    verbatims_collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
    
    # Test status
    print("2️⃣ Testing status...")
    token_status = verbatims_collector.get_token_status()
    print(f"   Token: {token_status['status']} (expires in {token_status.get('expires_in', 'N/A')}s)")
    
    # Test asking a question with the chatbot
    print("3️⃣ Testing chatbot question...")
    
    question = "What are the main customer complaints about delays and cancellations?"
    filters = {
        'cabin': ['Business'],
        'haul': ['LH']
    }
    
    print(f"   Question: {question}")
    print(f"   Filters: {filters}")
    
    try:
        answer_data = verbatims_collector.ask_chatbot_question(
            question=question,
            start_date="2025-08-15",
            end_date="2025-08-21",
            node_path="Global",
            filters=filters
        )
        
        if answer_data:
            print(f"   ✅ Got answer from chatbot!")
            print(f"   📝 Answer: {answer_data.get('answer', 'No answer')}")
            print(f"   🔧 Tool Output: {answer_data.get('toolOutput', 'No tool output')}")
            print(f"   🎯 JobId: {answer_data.get('jobId', 'No jobId')}")
        else:
            print(f"   ⚠️ No answer received from chatbot")
            
    except Exception as e:
        print(f"   ❌ Error asking chatbot question: {e}")
        import traceback
        traceback.print_exc()
    
    # Test verbatims data collection (should use PBI fallback)
    print("4️⃣ Testing verbatims data collection...")
    try:
        verbatims_data = verbatims_collector.get_verbatims_data(
            start_date="2025-08-15",
            end_date="2025-08-21",
            node_path="Global"
        )
        
        print(f"   ✅ Collected {len(verbatims_data)} verbatims")
        if not verbatims_data.empty:
            print(f"   📊 Columns: {len(verbatims_data.columns)}")
            
    except Exception as e:
        print(f"   ❌ Error collecting verbatims: {e}")
    
    print("\n🎉 UPDATED VERBATIMS TOOL TEST COMPLETED!")

if __name__ == "__main__":
    test_verbatims_tool_updated()
