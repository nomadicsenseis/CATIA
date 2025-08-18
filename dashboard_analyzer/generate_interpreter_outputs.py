#!/usr/bin/env python3
"""
Script to generate interpreter outputs from interpreter conversation files.
This script extracts the final interpretations from the conversation files
and generates the interpreter outputs in the format expected by the summary agent.
"""

import json
import os
import glob
from pathlib import Path
from datetime import datetime
import re

def extract_final_interpretation(conversation_file_path):
    """
    Extract the final interpretation from a conversation file.
    
    Args:
        conversation_file_path (str): Path to the conversation file
        
    Returns:
        dict: Dictionary with metadata and final interpretation
    """
    try:
        with open(conversation_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract metadata
        metadata = data.get('metadata', {})
        final_interpretation = data.get('final_interpretation', '')
        
        if not final_interpretation:
            print(f"⚠️ No final interpretation found in {conversation_file_path}")
            return None
        
        # Extract date from filename or metadata
        filename = os.path.basename(conversation_file_path)
        
        # Try to extract date range first (for weekly analysis)
        date_range_match = re.search(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', filename)
        if date_range_match:
            start_date = date_range_match.group(1)
            end_date = date_range_match.group(2)
            date = f"{start_date}_to_{end_date}"  # Use range format for weekly
        else:
            # Try single date (for daily analysis)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
            if date_match:
                date = date_match.group(1)
            else:
                date = metadata.get('start_date', 'Unknown')
        
        return {
            'date': date,
            'node_path': metadata.get('node_path', 'Global'),
            'start_date': metadata.get('start_date', ''),
            'end_date': metadata.get('end_date', ''),
            'study_mode': metadata.get('study_mode', ''),
            'final_interpretation': final_interpretation,
            'source_file': conversation_file_path
        }
        
    except Exception as e:
        print(f"❌ Error processing {conversation_file_path}: {str(e)}")
        return None

def generate_interpreter_outputs():
    """
    Generate interpreter outputs from conversation files.
    """
    # Define paths
    interpreter_dir = Path("dashboard_analyzer/agent_conversations/interpreter")
    outputs_dir = Path("dashboard_analyzer/agent_conversations/interpreter_outputs")
    
    # Create outputs directory if it doesn't exist
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all conversation files
    conversation_files = glob.glob(str(interpreter_dir / "interpreter_*.json"))
    
    if not conversation_files:
        print(f"❌ No conversation files found in {interpreter_dir}")
        return
    
    print(f"🔍 Found {len(conversation_files)} conversation files")
    
    # Process each conversation file
    successful_extractions = 0
    failed_extractions = 0
    
    for conversation_file in conversation_files:
        print(f"📄 Processing {os.path.basename(conversation_file)}...")
        
        result = extract_final_interpretation(conversation_file)
        
        if result:
            # Generate output filename
            date = result['date']
            node_path = result['node_path'].replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            output_filename = f"interpreter_output_{date}_{node_path}_{timestamp}.json"
            output_path = outputs_dir / output_filename
            
            # Create output data structure
            output_data = {
                "metadata": {
                    "source_file": result['source_file'],
                    "extraction_timestamp": datetime.now().isoformat(),
                    "date": result['date'],
                    "node_path": result['node_path'],
                    "start_date": result['start_date'],
                    "end_date": result['end_date'],
                    "study_mode": result['study_mode']
                },
                "final_interpretation": result['final_interpretation']
            }
            
            # Save output file
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Generated {output_filename}")
                successful_extractions += 1
                
            except Exception as e:
                print(f"❌ Error saving {output_filename}: {str(e)}")
                failed_extractions += 1
        else:
            failed_extractions += 1
    
    print(f"\n🎯 SUMMARY:")
    print(f"   ✅ Successful extractions: {successful_extractions}")
    print(f"   ❌ Failed extractions: {failed_extractions}")
    print(f"   📁 Output directory: {outputs_dir}")
    
    if successful_extractions > 0:
        print(f"\n🚀 Interpreter outputs generated successfully!")
        print(f"   You can now run the debug_summary_agent.py script.")
    else:
        print(f"\n⚠️ No interpreter outputs were generated.")

def main():
    """Main function."""
    print("🚀 Generating Interpreter Outputs")
    print("=" * 50)
    
    generate_interpreter_outputs()
    
    print("\n🏁 Process completed!")

if __name__ == "__main__":
    main() 