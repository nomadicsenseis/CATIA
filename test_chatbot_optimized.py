#!/usr/bin/env python3
"""
Test optimized chatbot with fast timeout
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append('/app')

from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

def test_chatbot_optimized():
    """Test optimized chatbot with fast timeout"""
    print("🚀 OPTIMIZED CHATBOT TEST")
    print("=" * 40)
    
    # Initialize collectors
    print("1️⃣ Initializing collectors...")
    pbi_collector = PBIDataCollector()
    verbatims_collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
    
    # Test status
    print("2️⃣ Testing status...")
    token_status = verbatims_collector.get_token_status()
    print(f"   Token: {token_status['status']} (expires in {token_status.get('expires_in', 'N/A')}s)")
    
    # Test asking a simple question with optimized timeout
    print("3️⃣ Testing chatbot question (OPTIMIZED MODE)...")
    
    question = "What are the main customer complaints about delays?"
    
    print(f"   Question: {question}")
    print(f"   ⏱️ Using 30-second timeout with fast polling...")
    
    try:
        answer_data = verbatims_collector.ask_chatbot_question(
            question=question,
            start_date="2025-08-15",
            end_date="2025-08-21",
            node_path="Global",
            filters={'cabin': ['Business'], 'haul': ['LH']}
        )
        
        if answer_data:
            print(f"   ✅ Got answer from chatbot!")
            print(f"   📝 Answer: {answer_data.get('answer', 'No answer')[:150]}...")
            print(f"   🎯 JobId: {answer_data.get('jobId', 'No jobId')}")
            print(f"   🔧 Tool Output: {answer_data.get('toolOutput', 'No tool output')[:100]}...")
        else:
            print(f"   ⚠️ No answer received (timeout or error)")
            
    except Exception as e:
        print(f"   ❌ Error asking chatbot question: {e}")
    
    print("\n🎉 OPTIMIZED CHATBOT TEST COMPLETED!")

if __name__ == "__main__":
    test_chatbot_optimized()
