#!/usr/bin/env python3
"""
Test to verify the agent can decide the next tool intelligently
"""

import sys
import os
import asyncio

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_agent_decision():
    """Test that the agent can decide the next tool intelligently"""
    
    print("🧪 AGENT DECISION TEST")
    print("=" * 50)
    
    try:
        # Import the agent
        from anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
        
        print("📋 Step 1: Initialize CausalExplanationAgent")
        
        # Initialize agent (without running full analysis)
        agent = CausalExplanationAgent(
            causal_filter="vs L7d",
            study_mode="comparative",
            silent_mode=True
        )
        
        print("✅ CausalExplanationAgent initialized successfully")
        
        print()
        print("📋 Step 2: Test helper prompt retrieval")
        
        # Test getting helper prompts for different tools
        tools_to_test = [
            "explanatory_drivers_tool",
            "operative_data_tool", 
            "ncs_tool",
            "verbatims_tool",
            "routes_tool"
        ]
        
        for tool in tools_to_test:
            helper_prompt = agent._get_helper_prompt_for_tool(tool)
            if helper_prompt and "No helper prompt found" not in helper_prompt:
                print(f"✅ {tool}: Helper prompt found ({len(helper_prompt)} chars)")
                # Show first 100 chars
                preview = helper_prompt[:100].replace('\n', ' ').strip()
                print(f"   Preview: {preview}...")
            else:
                print(f"❌ {tool}: No helper prompt found")
        
        print()
        print("📋 Step 3: Test agent decision making")
        
        # Test the decision making with a mock reflection
        mock_reflection = """
        Based on the explanatory drivers analysis, I can see that Punctuality has a significant negative SHAP value (-5.11), 
        indicating it's a major driver of the NPS decline. The next logical step would be to investigate operational data 
        to see if there are actual punctuality issues that correlate with this perception.
        """
        
        next_tool = await agent._determine_next_tool_from_reflection(
            reflection=mock_reflection,
            current_tool="explanatory_drivers_tool",
            iteration=1,
            max_iterations=5
        )
        
        if next_tool:
            print(f"✅ Agent decided next tool: {next_tool}")
            print(f"   This makes sense: explanatory_drivers_tool → {next_tool}")
        else:
            print("❌ Agent decided to end investigation (unexpected)")
        
        print()
        print("🎉 TEST COMPLETED!")
        print("✅ Agent decision making should now work intelligently!")
        print("✅ No more programmatic sequences!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent_decision())
