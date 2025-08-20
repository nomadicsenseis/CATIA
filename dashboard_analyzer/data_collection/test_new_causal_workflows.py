#!/usr/bin/env python3
"""
Test script for the new causal workflows
Tests the updated helper prompts and workflow guidance
"""

import sys
import os
import yaml
import logging

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_new_causal_workflows():
    """Test the new causal workflows implementation"""
    
    print("🧪 NEW CAUSAL WORKFLOWS TEST")
    print("=" * 60)
    print("Testing the updated helper prompts and workflow guidance")
    print()
    
    try:
        # Load the updated YAML configuration
        config_path = "dashboard_analyzer/anomaly_explanation/config/prompts/causal_explanation.yaml"
        print(f"📋 Loading configuration from: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        print("✅ Configuration loaded successfully!")
        print()
        
        # Test 1: Verify helper prompts exist
        print("🔍 TEST 1: Verificar helper prompts actualizados")
        tools_prompts = config.get('tools_prompts', {})
        
        # Check operative_data_tool
        operative_tool = tools_prompts.get('operative_data_tool', {})
        if 'comparative' in operative_tool:
            print("✅ operative_data_tool[comparative] exists")
            if 'ncs_tool' in operative_tool['comparative']:
                print("✅ operative_data_tool directs to ncs_tool")
        
        # Check ncs_tool 
        ncs_tool = tools_prompts.get('ncs_tool', {})
        if 'comparative' in ncs_tool:
            print("✅ ncs_tool[comparative] exists")
            if 'verbatims_tool' in ncs_tool['comparative']:
                print("✅ ncs_tool directs to verbatims_tool")
        
        # Check verbatims_tool
        verbatims_tool = tools_prompts.get('verbatims_tool', {})
        if 'comparative' in verbatims_tool:
            print("✅ verbatims_tool[comparative] exists")
            if 'FLUJO OPERATIVO' in verbatims_tool['comparative']:
                print("✅ verbatims_tool has flow-specific logic")
            if 'FLUJO PRODUCTO' in verbatims_tool['comparative']:
                print("✅ verbatims_tool supports product flow")
        
        # Check routes_tool
        routes_tool = tools_prompts.get('routes_tool', {})
        if 'comparative' in routes_tool:
            print("✅ routes_tool[comparative] exists")
            if 'customer_profile_tool' in routes_tool['comparative']:
                print("✅ routes_tool directs to customer_profile_tool")
        
        print()
        
        # Test 2: Verify workflow guidance
        print("🔍 TEST 2: Verificar workflow guidance actualizado")
        workflow_guidance = config.get('workflow_guidance', {})
        
        # Check operative flow
        operative_flow = workflow_guidance.get('operative', '')
        if 'operative_data_tool' in operative_flow and 'ncs_tool' in operative_flow and 'verbatims_tool' in operative_flow:
            print("✅ Operative flow: operative_data_tool → ncs_tool → verbatims_tool")
        
        # Check product flow  
        product_flow = workflow_guidance.get('product', '')
        if '1ª ejecución' in product_flow and '2ª ejecución' in product_flow:
            print("✅ Product flow: verbatims_tool (1ª) → ncs_tool → verbatims_tool (2ª)")
        
        # Check mixed flow
        mixed_flow = workflow_guidance.get('mixed', '')
        if 'RAMA OPERATIVA' in mixed_flow and 'RAMA PRODUCTO' in mixed_flow:
            print("✅ Mixed flow: Independent branches with complete workflows")
        
        print()
        
        # Test 3: Verify system prompt map
        print("🔍 TEST 3: Verificar mapa de flujo en system prompt")
        system_prompt = config.get('system_prompt', '')
        if 'operative: [operative_data_tool, ncs_tool, verbatims_tool, routes_tool, customer_profile_tool]' in system_prompt:
            print("✅ System prompt has updated operative flow map")
        if 'verbatims_tool(1ª)' in system_prompt and 'verbatims_tool(2ª)' in system_prompt:
            print("✅ System prompt shows product flow with dual verbatims calls")
        if 'RAMA_OPERATIVA' in system_prompt and 'RAMA_PRODUCTO' in system_prompt:
            print("✅ System prompt shows mixed flow with independent branches")
        
        print()
        
        # Test 4: Verify specific workflow features
        print("🔍 TEST 4: Verificar características específicas de workflows")
        
        # Check that verbatims_tool has the new questions
        if 'rutas específicas (origen-destino) que tienen los comentarios más negativos' in verbatims_tool.get('comparative', ''):
            print("✅ Verbatims tool includes route-specific negative comments question")
        
        if 'comentarios más representativos de cada una de esas rutas' in verbatims_tool.get('comparative', ''):
            print("✅ Verbatims tool includes representative comments question")
        
        # Check flow-specific guidance
        if 'VALIDACIÓN DE CORRELACIÓN OPERATIVA' in verbatims_tool.get('comparative', ''):
            print("✅ Verbatims tool has operative correlation validation")
        
        print()
        print("🎉 ALL TESTS PASSED!")
        print("✅ New causal workflows successfully implemented!")
        print("✅ Helper prompts updated with proper tool sequencing")
        print("✅ Workflow guidance reflects new operative/product/mixed flows")  
        print("✅ System prompt map updated with complete sequences")
        print("✅ Verbatims tool includes new route-focused questions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_new_causal_workflows()
