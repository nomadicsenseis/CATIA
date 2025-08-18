#!/usr/bin/env python3
"""
Debug script for AnomalySummaryAgent.
This script loads interpreter outputs and generates a consolidated summary.
"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_summary_agent import AnomalySummaryAgent
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type

async def main():
    """
    Main function to debug the AnomalySummaryAgent.
    """
    print("🚀 Debugging AnomalySummaryAgent 🚀")
    print("=" * 50)

    # Define the reports directory
    base_dir = Path(__file__).parent
    reports_dir = base_dir / "agent_conversations" / "interpreter_outputs"

    if not reports_dir.exists():
        print(f"❌ Reports directory not found at '{reports_dir}'")
        print("💡 Please run the 'generate_interpreter_outputs.py' script first to generate interpreter outputs.")
        return

    # Gather all JSON file paths from the directory
    reports_content = []
    report_paths = list(reports_dir.glob("*.json"))

    if not report_paths:
        print(f"⚠️ No JSON reports found in '{reports_dir}'. Nothing to summarize.")
        return

    print(f"📂 Found {len(report_paths)} interpreter reports to summarize.")
    
    # Load all reports
    for path in report_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                reports_content.append(content)
        except json.JSONDecodeError:
            print(f"⚠️ WARNING: Could not decode JSON from '{path}'. Skipping this file.")
            continue
    
    if not reports_content:
        print(f"❌ ERROR: No valid JSON reports could be loaded. Cannot summarize.")
        return

    # Initialize the agent
    try:
        print("\n🤖 Initializing AnomalySummaryAgent...")
        # Setup a basic logger to see agent's output
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger("summary_debug")
        
        summary_agent = AnomalySummaryAgent(
            llm_type=get_default_llm_type(),
            logger=logger
        )
        print("✅ Agent initialized successfully.")

        print("\n📝 Generating consolidated summary from interpreter outputs...")
        try:
            # Process the reports to separate weekly and daily analyses
            weekly_report = None
            daily_reports = []

            # Sort reports by date
            sorted_reports = sorted(reports_content, key=lambda x: x.get('metadata', {}).get('date', ''))
            
            for report in sorted_reports:
                metadata = report.get("metadata", {})
                final_interpretation = report.get("final_interpretation", "")
                
                if not final_interpretation:
                    continue
                
                # Extract date information
                date = metadata.get("date", "")
                start_date = metadata.get("start_date", "")
                end_date = metadata.get("end_date", "")
                study_mode = metadata.get("study_mode", "")
                
                # Convert the final_interpretation to the format expected by summary agent
                # The summary agent expects 'ai_interpretation' field
                report_for_agent = {
                    "date": date,
                    "analysis": final_interpretation,
                    "anomalies": ["daily_analysis"]  # Placeholder for anomalies
                }
                
                # Classify reports based on date range (more reliable than date string format)
                start_date = metadata.get("start_date", "")
                end_date = metadata.get("end_date", "")
                
                if start_date and end_date and start_date != end_date:
                    # This is a weekly/comparative report (different start and end dates)
                    if weekly_report is None:
                        weekly_report = final_interpretation
                        print(f"📊 Found weekly report: {date} (study_mode: {study_mode}) [{start_date} to {end_date}]")
                    else:
                        print(f"⚠️ Multiple weekly reports found, using first one: {date}")
                else:
                    # This is a daily/single report (same start and end date)
                    daily_reports.append(report_for_agent)
                    print(f"📅 Found daily report: {date} (study_mode: {study_mode}) [{start_date} to {end_date}]")

            # Verify we have the required reports
            if not weekly_report:
                print("⚠️ No weekly comparative report found. Cannot generate a comprehensive summary.")
                return

            if not daily_reports:
                print("⚠️ No daily reports found. Summary may be incomplete.")

            print(f"📊 Processing {len(daily_reports)} daily reports and 1 weekly report...")

            # Call the correct method for a comprehensive summary
            final_summary = await summary_agent.generate_comprehensive_summary(
                weekly_comparative_analysis=weekly_report,
                daily_single_analyses=daily_reports
            )

            if final_summary:
                # Save the final summary to a file
                summary_output_dir = base_dir / "summary_reports"
                summary_output_dir.mkdir(parents=True, exist_ok=True)
                summary_file_path = summary_output_dir / "consolidated_summary.json"
                
                # Create a structured output
                output_data = {
                    "metadata": {
                        "generation_timestamp": datetime.now().isoformat(),
                        "weekly_reports_processed": 1,
                        "daily_reports_processed": len(daily_reports),
                        "total_reports": len(reports_content)
                    },
                    "consolidated_summary": final_summary
                }
                
                with open(summary_file_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=4, ensure_ascii=False)
                
                print(f"✅ Consolidated summary saved to '{summary_file_path}'")
                print(f"\n📄 SUMMARY PREVIEW:")
                print("=" * 50)
                print(final_summary[:500] + "..." if len(final_summary) > 500 else final_summary)
                print("=" * 50)

        except Exception as e:
            print(f"\n❌ An error occurred during summary generation: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"\n❌ An error occurred during summary generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 