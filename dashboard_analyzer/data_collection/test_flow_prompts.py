#!/usr/bin/env python3
"""
Test script to verify that flow-specific helper prompts work correctly.
This tests the new structure where each tool has prompts for different flows.
"""

import sys
import os
import yaml
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_flow_specific_prompts():
    """Test that flow-specific helper prompts are properly structured."""
    
    # Load the YAML configuration
    yaml_path = project_root / "dashboard_analyzer" / "anomaly_explanation" / "config" / "prompts" / "causal_explanation.yaml"
    
    with open(yaml_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    print("🔍 Testing flow-specific helper prompts structure...")
    
    # Check that tools_prompts section exists
    if 'tools_prompts' not in config:
        print("❌ ERROR: 'tools_prompts' section not found in YAML")
        return False
    
    tools_prompts = config['tools_prompts']
    
    # Test each tool has the expected structure
    expected_tools = [
        'explanatory_drivers_tool',
        'operative_data_tool', 
        'ncs_tool',
        'verbatims_tool',
        'routes_tool',
        'customer_profile_tool'
    ]
    
    for tool_name in expected_tools:
        if tool_name not in tools_prompts:
            print(f"❌ ERROR: {tool_name} not found in tools_prompts")
            continue
            
        tool_config = tools_prompts[tool_name]
        
        # Check comparative mode exists
        if 'comparative' not in tool_config:
            print(f"❌ ERROR: {tool_name} missing 'comparative' section")
            continue
            
        comparative_config = tool_config['comparative']
        
        # Check if it's a dictionary (flow-specific) or string (general)
        if isinstance(comparative_config, dict):
            print(f"✅ {tool_name}: Flow-specific prompts found")
            
            # Check specific flows
            if 'operative' in comparative_config:
                print(f"   - Operative flow: ✅")
            if 'product' in comparative_config:
                print(f"   - Product flow: ✅")
            if 'mixed' in comparative_config:
                print(f"   - Mixed flow: ✅")
                
            # Check for special mixed flow variants
            if 'mixed_operative' in comparative_config:
                print(f"   - Mixed operative branch: ✅")
            if 'mixed_product' in comparative_config:
                print(f"   - Mixed product branch: ✅")
            if 'product_validation' in comparative_config:
                print(f"   - Product validation (2nd execution): ✅")
                
        else:
            print(f"✅ {tool_name}: General comparative prompt (string)")
    
    print("\n🎯 Testing specific flow sequences...")
    
    # Test operative flow sequence
    print("\n📋 OPERATIVE FLOW SEQUENCE:")
    operative_sequence = [
        ('explanatory_drivers_tool', 'operative'),
        ('operative_data_tool', 'operative'),
        ('ncs_tool', 'operative'),
        ('verbatims_tool', 'operative'),
        ('routes_tool', 'operative'),
        ('customer_profile_tool', 'operative')
    ]
    
    for tool_name, flow_type in operative_sequence:
        if tool_name in tools_prompts:
            tool_config = tools_prompts[tool_name]
            if 'comparative' in tool_config:
                comparative_config = tool_config['comparative']
                if isinstance(comparative_config, dict) and flow_type in comparative_config:
                    prompt = comparative_config[flow_type]
                    # Check if it mentions the next tool
                    if 'SIGUIENTE PASO OBLIGATORIO' in prompt:
                        next_tool = extract_next_tool(prompt)
                        print(f"   ✅ {tool_name} ({flow_type}) → {next_tool}")
                    else:
                        print(f"   ⚠️ {tool_name} ({flow_type}) → No next tool specified")
                else:
                    print(f"   ❌ {tool_name} ({flow_type}) → Flow not found")
    
    # Test product flow sequence
    print("\n📋 PRODUCT FLOW SEQUENCE:")
    product_sequence = [
        ('explanatory_drivers_tool', 'product'),
        ('operative_data_tool', 'product'),
        ('verbatims_tool', 'product'),
        ('ncs_tool', 'product'),
        ('verbatims_tool', 'product_validation'),
        ('routes_tool', 'product'),
        ('customer_profile_tool', 'product')
    ]
    
    for tool_name, flow_type in product_sequence:
        if tool_name in tools_prompts:
            tool_config = tools_prompts[tool_name]
            if 'comparative' in tool_config:
                comparative_config = tool_config['comparative']
                if isinstance(comparative_config, dict) and flow_type in comparative_config:
                    prompt = comparative_config[flow_type]
                    # Check if it mentions the next tool
                    if 'SIGUIENTE PASO OBLIGATORIO' in prompt:
                        next_tool = extract_next_tool(prompt)
                        print(f"   ✅ {tool_name} ({flow_type}) → {next_tool}")
                    else:
                        print(f"   ⚠️ {tool_name} ({flow_type}) → No next tool specified")
                else:
                    print(f"   ❌ {tool_name} ({flow_type}) → Flow not found")
    
    print("\n🎉 Flow-specific helper prompts test completed!")
    return True

def extract_next_tool(prompt):
    """Extract the next tool mentioned in the prompt."""
    import re
    
    # Look for patterns like "Ejecuta `tool_name`" or "SIGUIENTE PASO OBLIGATORIO"
    tool_patterns = [
        r'Ejecuta `([^`]+)`',
        r'Ejecuta ([a-zA-Z_]+)',
        r'`([a-zA-Z_]+)`',
        r'([a-zA-Z_]+)_tool'
    ]
    
    for pattern in tool_patterns:
        match = re.search(pattern, prompt)
        if match:
            return match.group(1)
    
    return "Unknown"

if __name__ == "__main__":
    try:
        success = test_flow_specific_prompts()
        if success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)
