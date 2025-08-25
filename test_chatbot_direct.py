#!/usr/bin/env python3
"""
Test script to directly ask questions to the chatbot
"""

import asyncio
import os
import sys
import logging
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append('/app')

from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_chatbot_direct():
    """Test the chatbot directly with a question"""
    
    print("🤖 TESTING CHATBOT DIRECTLY")
    print("=" * 50)
    
    try:
        # Initialize collectors
        print("\n1️⃣ Initializing collectors...")
        pbi_collector = PBIDataCollector()
        chatbot_collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
        
        print("✅ Collectors initialized successfully")
        
        # Test chatbot status
        print("\n2️⃣ Chatbot status...")
        status = chatbot_collector.get_chatbot_status()
        print(f"📊 Status: {status}")
        
        # Test connection
        print("\n3️⃣ Testing connection...")
        connection_success, connection_message = chatbot_collector.test_chatbot_connection()
        print(f"🔗 Connection: {connection_message}")
        
        # Test with a specific question
        print("\n4️⃣ Testing with specific question...")
        start_date = "2025-08-15"
        end_date = "2025-08-21"
        node_path = "Global/LH"
        
        print(f"📅 Period: {start_date} to {end_date}")
        print(f"🎯 Node: {node_path}")
        
        # Test the chatbot conversation
        print("\n5️⃣ Testing chatbot conversation...")
        
        # Simulate the conversation flow that the agent uses
        conversation = await chatbot_collector._conduct_chatbot_conversation(
            verbatim_type="boarding",
            node_path=node_path,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"💬 Conversation completed: {len(conversation)} rounds")
        
        for i, round_data in enumerate(conversation):
            print(f"\n--- ROUND {i+1} ---")
            print(f"Purpose: {round_data.get('purpose', 'Unknown')}")
            print(f"Question: {round_data.get('question', 'No question')[:100]}...")
            print(f"Response: {round_data.get('response', 'No response')[:200]}...")
            print(f"Status: {round_data.get('status', 'Unknown')}")
        
        print("\n✅ Chatbot test completed!")
        
    except Exception as e:
        print(f"❌ Error testing chatbot: {e}")
        logger.exception("Test failed")

async def test_simple_question():
    """Test with a simple, direct question"""
    
    print("\n🎯 TESTING SIMPLE QUESTION")
    print("=" * 50)
    
    try:
        # Initialize collector
        pbi_collector = PBIDataCollector()
        chatbot_collector = ChatbotVerbatimsCollector(pbi_collector=pbi_collector)
        
        # Simple question
        question = "¿Cuáles son las rutas con más comentarios negativos en Global/LH?"
        
        print(f"❓ Question: {question}")
        
        # Try to get a direct response
        # This would simulate what the agent does
        response = await chatbot_collector._collect_from_chatbot_api(
            date_range=("2025-08-15", "2025-08-21"),
            node_path="Global/LH",
            filters={"verbatim_type": "boarding"}
        )
        
        if not response.empty:
            print(f"✅ Got response with {len(response)} records")
            print(f"📊 Columns: {list(response.columns)}")
            print(f"📋 Sample data:")
            print(response.head(2))
        else:
            print("⚠️ No response data")
            
    except Exception as e:
        print(f"❌ Error in simple question: {e}")
        logger.exception("Simple question failed")

async def main():
    """Main test function"""
    
    print("🚀 STARTING DIRECT CHATBOT TESTS")
    print("=" * 60)
    
    # Test 1: Full conversation flow
    await test_chatbot_direct()
    
    # Test 2: Simple question
    await test_simple_question()
    
    print("\n🎉 ALL TESTS COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
