#!/usr/bin/env python3
"""
Debug script for the FlexibleAnomalyInterpreter.

This script automatically finds all causal explanation JSON reports from the
`agent_conversations/causal_explanation` directory. It intelligently groups
these reports by their analysis period (e.g., a single day or a full week)
by parsing the filenames.

For each period, it constructs the complete hierarchical data tree that the
interpreter expects, mirroring the production logic. It then runs the
interpreter on each complete tree and saves the rich, contextual output
to the `agent_conversations/interpreter_outputs` directory.

This allows for batch processing of all analysis outputs, preparing them
for the summary agent debugging step.

Usage:
    python dashboard_analyzer/debug_interpreter.py
"""

import asyncio
import sys
import os
import json
import logging
from pathlib import Path
from collections import defaultdict
import re
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The agent that creates the final summary from the causal agent's output
from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_interpreter_agent import AnomalyInterpreterAgent
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
# The class that defines the structural hierarchy
from dashboard_analyzer.anomaly_detection.anomaly_tree import AnomalyTree

def parse_filename(filename: str):
    """Parses the filename to extract dates and segment path."""
    match = re.match(r"causal_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_(.*?)_\d{8}_\d{6}\.json", filename)
    if match:
        start_date = match.group(1)
        end_date = match.group(2)
        return f"{start_date}_to_{end_date}", start_date
    return None, None

async def main():
    """
    This script replicates the logic of main.py for interpreting causal explanations.
    It reads existing causal agent outputs, builds the hierarchical text prompt for each
    analysis period, runs the AnomalyInterpreterAgent on it, and saves the final,
    clean summaries.
    """
    print("🚀 Running Final Interpreter Step on Causal Explanations (Correct Flow) 🚀")
    print("=" * 70)
    
    base_dir = Path(__file__).parent
    causal_dir = base_dir / "agent_conversations" / "causal_explanation"
    output_dir = base_dir / "agent_conversations" / "interpreter_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    report_paths = sorted(list(causal_dir.glob("*.json")))

    if not report_paths:
        print(f"⚠️ No causal reports (.json files) found in '{causal_dir}'.")
        return

    # 1. Group reports by analysis period
    grouped_reports = defaultdict(list)
    for path in report_paths:
        period_key, _ = parse_filename(path.name)
        if period_key:
            grouped_reports[period_key].append(path)

    print(f"📂 Found {len(report_paths)} reports, grouped into {len(grouped_reports)} analysis periods.")
    print("-" * 70)
    
    # Configure logging ONCE at the application entry point.
    # The agent will reuse this configuration.
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

    # 2. Process each period group
    for period_key, paths_in_group in grouped_reports.items():
        print(f"🔄 Processing period: {period_key} ({len(paths_in_group)} reports)")

        try:
            # 2a. Load all explanations for the period into a dictionary
            loaded_explanations = {}
            has_global_report = False
            for path in paths_in_group:
                with open(path, 'r', encoding='utf-8') as f_in:
                    causal_data = json.load(f_in)
                
                # Check for "Global" in the filename to determine the segment for the whole period
                if "_Global_" in path.name:
                    has_global_report = True

                node_path = causal_data.get("metadata", {}).get("node_path")
                clean_explanations = causal_data.get("clean_explanations")

                if node_path and clean_explanations:
                    loaded_explanations[node_path] = "\n\n---\n\n".join(clean_explanations)

            if not loaded_explanations:
                print(f"   ⚠️ Warning: No valid explanations found for period {period_key}. Skipping.")
                continue

            # 2b. Build the hierarchical text prompt
            structural_tree = AnomalyTree()
            structural_tree.build_tree_structure()
            
            hierarchical_prompt_parts = []
            # Iterate through the DEFINED structure to maintain order
            for node_path in structural_tree.nodes.keys():
                if node_path in loaded_explanations:
                    hierarchical_prompt_parts.append(f"NODO: {node_path}\n{loaded_explanations[node_path]}")

            hierarchical_prompt_text = "\n\n".join(hierarchical_prompt_parts)

            # 2c. Instantiate and run the interpreter agent
            _, start_date_str = parse_filename(paths_in_group[0].name)
            start_str, end_str = period_key.split('_to_')
            study_mode = "single" if start_str == end_str else "comparative"
            
            # Determine segment based on whether a Global report was found
            period_segment = "Global" if has_global_report else None

            interpreter_agent = AnomalyInterpreterAgent(
                llm_type=get_default_llm_type(),
                study_mode=study_mode
            )

            final_summary = await interpreter_agent.interpret_anomaly_tree_hierarchical(
                tree_data=hierarchical_prompt_text,
                date=start_date_str,
                segment=period_segment  # Pass the determined segment to the agent
            )
            
            # 2d. Save the final summary for the period
            output_filename = f"interpreter_summary_{period_key}.json"
            output_path = output_dir / output_filename
            
            # The summary agent expects the same format we were creating before
            output_data = {
                "period": period_key,
                "ai_interpretation": final_summary
            }

            with open(output_path, 'w', encoding='utf-8') as f_out:
                json.dump(output_data, f_out, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Successfully generated and saved summary for period {period_key}.")

        except Exception as e:
            print(f"❌ An error occurred while processing period '{period_key}': {e}.")
            import traceback
            traceback.print_exc()

    print("-" * 70)
    print("🎉 Interpretation complete!")
    print(f"📄 All period summaries have been saved to '{output_dir}'.")
    print("👉 You can now run 'debug_summary_agent.py'.")


if __name__ == "__main__":
    asyncio.run(main()) 