#!/usr/bin/env python3
"""
Test rápido para verificar la presentación mejorada del operative_data_tool
"""

import asyncio
import sys
import os

# Add the dashboard_analyzer to the path
sys.path.append('/app')
sys.path.append('/app/dashboard_analyzer')

from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
from dashboard_analyzer.anomaly_explanation.data_analyzer import OperationalDataAnalyzer
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType

async def test_operative_presentation():
    print("🧪 TESTING OPERATIVE_DATA_TOOL PRESENTATION")
    print("=" * 60)
    
    # Initialize PBI Collector and Analyzer
    pbi_collector = PBIDataCollector()
    
    # Simulate causal agent call to operative_data_tool
    node_path = "Global/LH/Business"
    start_date = "2025-08-01"
    end_date = "2025-08-07"
    
    try:
        # Create causal agent
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        agent = CausalExplanationAgent(
            llm_type=get_default_llm_type(), 
            silent_mode=True, 
            detection_mode="vslast", 
            causal_filter="vs L7d", 
            study_mode="comparative"
        )
        
        # Initialize the PBI collector manually (usually done in investigate methods)
        agent.pbi_collector = pbi_collector
        
        # Set the anomaly type for proper correlation analysis
        agent.current_anomaly_type = "negative"
        
        # Call the operative data tool
        print(f"📅 Testing: {node_path} from {start_date} to {end_date}")
        print(f"🎯 Anomaly type: negative (NPS decreased)")
        print()
        
        result = await agent._operative_data_tool(node_path, start_date, end_date)
        
        print("📊 OPERATIVE_DATA_TOOL RESULT:")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_operative_presentation()) 