#!/usr/bin/env python3
"""
Test the updated verbatims_tool in the causal explanation agent
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append('/app')

from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector

async def test_verbatims_tool_agent():
    """Test the updated verbatims_tool in the causal explanation agent"""
    print("🤖 TESTING VERBATIMS TOOL IN CAUSAL EXPLANATION AGENT")
    print("=" * 60)
    
    # Initialize the agent
    print("1️⃣ Initializing causal explanation agent...")
    agent = CausalExplanationAgent()
    
    # Test the verbatims_tool directly
    print("2️⃣ Testing verbatims_tool directly...")
    
    try:
        # Test single period verbatims tool
        result = await agent._verbatims_tool_single_period(
            node_path="Global/LH/Business",
            start_date="2025-08-15",
            end_date="2025-08-21"
        )
        
        print(f"   ✅ Verbatims tool result:")
        print(f"   📝 {result[:200]}...")
        
    except Exception as e:
        print(f"   ❌ Error testing verbatims tool: {e}")
        import traceback
        traceback.print_exc()
    
    # Test the chatbot conversation method
    print("3️⃣ Testing chatbot conversation method...")
    
    try:
        conversation = await agent._conduct_chatbot_conversation(
            verbatim_type="nps",
            node_path="Global/LH/Business",
            start_date="2025-08-15",
            end_date="2025-08-21"
        )
        
        if conversation:
            print(f"   ✅ Chatbot conversation completed!")
            print(f"   📊 Conversation rounds: {len(conversation)}")
            for i, round_data in enumerate(conversation):
                print(f"   🔄 Round {i+1}: {round_data.get('purpose', 'Unknown purpose')}")
        else:
            print(f"   ⚠️ No conversation data received")
            
    except Exception as e:
        print(f"   ❌ Error testing chatbot conversation: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 VERBATIMS TOOL AGENT TEST COMPLETED!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_verbatims_tool_agent())
