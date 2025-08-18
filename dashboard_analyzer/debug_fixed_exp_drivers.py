#!/usr/bin/env python3
"""
Debug script to test the corrected explanatory_drivers_tool and verify segment filtering.
"""
import asyncio
import sys
from datetime import date
import pandas as pd

sys.path.append('.')

from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent

async def test_explanatory_drivers_filter():
    """
    Tests the explanatory_drivers_tool with 'Global' and 'Global/LH' segments
    to ensure the segment filtering is now working correctly.
    """
    print("🔬 Testing Explanatory Drivers Tool Segment Filtering...")
    print("=" * 60)

    agent = CausalExplanationAgent(study_mode="comparative", causal_filter="vs L7d")

    # --- Test Case 1: Global ---
    print("\nExecuting for segment: Global")
    global_result_str = await agent._explanatory_drivers_tool(
        node_path="Global",
        start_date="2025-08-08",
        end_date="2025-08-14"
    )
    print("--- Global Result ---")
    print(global_result_str)
    global_survey_count = int(global_result_str.split("Survey Count: ")[1].split(" ")[0])

    # --- Test Case 2: Global/LH ---
    print("\nExecuting for segment: Global/LH")
    lh_result_str = await agent._explanatory_drivers_tool(
        node_path="Global/LH",
        start_date="2025-08-08",
        end_date="2025-08-14"
    )
    print("--- Global/LH Result ---")
    print(lh_result_str)
    lh_survey_count = int(lh_result_str.split("Survey Count: ")[1].split(" ")[0])
    
    # --- Verification ---
    print("\n" + "="*60)
    print("✅ Verification:")
    
    if global_result_str == lh_result_str:
        print("❌ FAILED: Results for Global and Global/LH are identical.")
    else:
        print("✅ PASSED: Results for Global and Global/LH are different.")

    if global_survey_count == lh_survey_count:
        print(f"❌ FAILED: Survey count is the same for both segments ({global_survey_count}).")
    else:
        print(f"✅ PASSED: Survey counts are different (Global: {global_survey_count}, Global/LH: {lh_survey_count}).")
        
    print("\nTest finished.")


if __name__ == "__main__":
    # To prevent SettingWithCopyWarning in pandas
    pd.options.mode.chained_assignment = None
    asyncio.run(test_explanatory_drivers_filter()) 