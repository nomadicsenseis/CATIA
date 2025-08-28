#!/usr/bin/env python3
"""
Fast test of the chatbot with short timeout
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append('/app')

from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

def test_chatbot_fast():
    """Fast test of the chatbot with short timeout"""
    print("🚀 FAST CHATBOT TEST")
    print("=" * 40)
    
    # Initialize collectors
    print("1️⃣ Initializing collectors...")
    pbi_collector = PBIDataCollector()
    verbatims_collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
    
    # Test status
    print("2️⃣ Testing status...")
    token_status = verbatims_collector.get_token_status()
    print(f"   Token: {token_status['status']} (expires in {token_status.get('expires_in', 'N/A')}s)")
    
    # Test asking a simple question with short timeout
    print("3️⃣ Testing chatbot question (FAST MODE)...")
    
    question = "What are the main customer complaints?"
    
    print(f"   Question: {question}")
    print(f"   ⏱️ Using 30-second timeout for fast response...")
    
    try:
        # Override the timeout for this test
        original_method = verbatims_collector._wait_for_chatbot_answer_working
        
        def fast_wait(job_id, headers, max_wait_time=30):
            print(f"   🚀 Using FAST timeout: {max_wait_time}s")
            return original_method(job_id, headers, max_wait_time)
        
        verbatims_collector._wait_for_chatbot_answer_working = fast_wait
        
        answer_data = verbatims_collector.ask_chatbot_question(
            question=question,
            start_date="2025-08-15",
            end_date="2025-08-21",
            node_path="Global",
            filters={'cabin': ['Business']}
        )
        
        if answer_data:
            print(f"   ✅ Got answer from chatbot!")
            print(f"   📝 Answer: {answer_data.get('answer', 'No answer')[:100]}...")
            print(f"   🎯 JobId: {answer_data.get('jobId', 'No jobId')}")
        else:
            print(f"   ⚠️ No answer received (timeout or error)")
            
    except Exception as e:
        print(f"   ❌ Error asking chatbot question: {e}")
    
    print("\n🎉 FAST CHATBOT TEST COMPLETED!")

if __name__ == "__main__":
    test_chatbot_fast()
