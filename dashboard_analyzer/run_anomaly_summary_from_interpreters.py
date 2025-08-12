import argparse
import asyncio
import json
import os
from datetime import datetime
from glob import glob
from typing import List, Dict, Any
import re

from dashboard_analyzer.anomaly_explanation.genai_core.agents.anomaly_summary_agent import AnomalySummaryAgent


def load_weekly_synthesis(weekly_file_path: str) -> str:
    with open(weekly_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # The weekly synthesis is stored in 'final_interpretation'
    weekly_text = data.get('final_interpretation', '').strip()
    if not weekly_text:
        raise ValueError(f"Weekly synthesis not found in {weekly_file_path}")
    return weekly_text


def _condense_text(text: str, max_chars: int = 1400) -> str:
    """Condense daily text: keep executive intro and key cabin sections within a char budget."""
    if not text:
        return ""
    t = text.strip()
    if len(t) <= max_chars:
        return t

    # Try to keep the executive intro (first paragraph)
    parts = re.split(r"\n\n+", t)
    intro = parts[0] if parts else t[:400]

    # Extract key cabin/radio sections (first paragraph each)
    sections = []
    section_headers = [
        r"\*\*ECONOMY SH\*\*", r"\*\*BUSINESS SH\*\*",
        r"\*\*ECONOMY LH\*\*", r"\*\*BUSINESS LH\*\*",
        r"\*\*PREMIUM LH\*\*"
    ]
    for header in section_headers:
        m = re.search(header + r"\s*\n([\s\S]*?)(\n\n|$)", t, re.IGNORECASE)
        if m:
            sect = m.group(0).strip()
            sections.append(sect)

    condensed = intro
    for s in sections:
        if len(condensed) + 2 + len(s) > max_chars:
            break
        condensed += "\n\n" + s

    # If still short, append the next paragraph(s) from intro tail
    if len(condensed) < max_chars and len(parts) > 1:
        for p in parts[1:]:
            if len(condensed) + 2 + len(p) > max_chars:
                break
            condensed += "\n\n" + p

    # Hard cap
    return condensed[:max_chars]


def load_daily_single_analyses(daily_folder_path: str, max_chars_per_day: int = 1400) -> List[Dict[str, Any]]:
    files = sorted(glob(os.path.join(daily_folder_path, 'interpreter_output_*.json')))
    daily_list: List[Dict[str, Any]] = []
    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            meta = data.get('metadata', {})
            date = meta.get('date') or meta.get('start_date')
            analysis = str(data.get('final_interpretation', '')).strip()
            if not analysis:
                continue
            daily_list.append({
                'date': date or 'Unknown',
                'analysis': analysis,
                'anomalies': []  # not used for filtering
            })
        except Exception:
            continue
    # Sort by date when possible
    def sort_key(item: Dict[str, Any]):
        try:
            return item.get('date') or ''
        except Exception:
            return ''
    daily_list.sort(key=sort_key)
    return daily_list


async def main(weekly_file: str, daily_folder: str, out_dir: str, max_chars_per_day: int) -> None:
    weekly_text = load_weekly_synthesis(weekly_file)
    daily_items = load_daily_single_analyses(daily_folder, max_chars_per_day=max_chars_per_day)

    agent = AnomalySummaryAgent()
    summary = await agent.generate_comprehensive_summary(
        weekly_comparative_analysis=weekly_text,
        daily_single_analyses=daily_items,
        date_flight_local=datetime.now().strftime('%Y%m%d_%H%M%S')
    )

    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = os.path.join(out_dir, f"summary_from_interpreters_{ts}.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n✅ Summary generated and saved to: {out_path}\n")
    print(summary)


if __name__ == '__main__':
    default_weekly = 'dashboard_analyzer/agent_conversations/interpreter/interpreter_2025-07-28_2025-07-28_Global_20250807_134327.json'
    default_daily = 'dashboard_analyzer/agent_conversations/interpreter_outputs'
    default_out = 'dashboard_analyzer/summary_reports'

    parser = argparse.ArgumentParser(description='Run AnomalySummaryAgent from interpreter outputs')
    parser.add_argument('--weekly-file', type=str, default=default_weekly, help='Path to weekly interpreter JSON with final_interpretation')
    parser.add_argument('--daily-folder', type=str, default=default_daily, help='Folder with interpreter_output_*.json daily files')
    parser.add_argument('--out-dir', type=str, default=default_out, help='Output directory for the consolidated summary')
    parser.add_argument('--max-day-chars', type=int, default=1400, help='Max characters to include per daily analysis')
    args = parser.parse_args()

    asyncio.run(main(args.weekly_file, args.daily_folder, args.out_dir, args.max_day_chars)) 