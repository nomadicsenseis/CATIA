#!/usr/bin/env python3
"""
Test script for JWT Token Automation System
Tests the automatic token refresh functionality for Iberia NPS Chatbot
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_verbatims_collector import ChatbotVerbatimsCollector
from token_manager import TokenManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_token_manager():
    """Test TokenManager functionality"""
    print("🧪 Testing TokenManager...")
    print("=" * 50)
    
    try:
        # Initialize TokenManager
        token_manager = TokenManager()
        
        # Test current token status
        token_info = token_manager.get_token_info()
        print(f"📊 Token Status: {token_info['status']}")
        print(f"⏰ Expires in: {token_info.get('expires_in', 'N/A')} seconds")
        print(f"📅 Expires at: {token_info.get('expires_at', 'N/A')}")
        
        # Test token validation
        is_valid = token_manager.ensure_valid_token()
        print(f"✅ Token validation: {'PASSED' if is_valid else 'FAILED'}")
        
        if not is_valid:
            print("🔄 Testing forced token refresh...")
            refresh_success = token_manager.force_refresh()
            print(f"🔄 Forced refresh: {'SUCCESS' if refresh_success else 'FAILED'}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ TokenManager test failed: {e}")
        return False


def test_chrome_automation():
    """Test Chrome automation (browser setup test only)"""
    print("\n🌐 Testing Chrome Automation...")
    print("=" * 50)
    
    try:
        from chrome_automation import ChromeAutomation
        
        config = {
            'verbatims_url': 'https://nps.chatbot.iberia.es/home',
            'headless': False,  # Visible for testing
            'wait_timeout': 10
        }
        
        chrome_automation = ChromeAutomation(config)
        
        # Test browser setup
        browser_test = chrome_automation.test_browser_setup()
        print(f"🌐 Browser setup test: {'PASSED' if browser_test else 'FAILED'}")
        
        return browser_test
        
    except Exception as e:
        logger.error(f"❌ Chrome automation test failed: {e}")
        return False


def test_chatbot_collector_integration():
    """Test ChatbotVerbatimsCollector with automatic token refresh"""
    print("\n🤖 Testing ChatbotVerbatimsCollector Integration...")
    print("=" * 50)
    
    try:
        # Test with automatic token refresh enabled
        collector_auto = ChatbotVerbatimsCollector(
            auto_refresh_tokens=True
        )
        
        # Test connection
        success, message = collector_auto.test_connection()
        print(f"🔗 Auto-refresh connection: {message}")
        
        # Test with automatic token refresh disabled (manual mode)
        collector_manual = ChatbotVerbatimsCollector(
            auto_refresh_tokens=False
        )
        
        success_manual, message_manual = collector_manual.test_connection()
        print(f"🔗 Manual mode connection: {message_manual}")
        
        return success or success_manual
        
    except Exception as e:
        logger.error(f"❌ ChatbotVerbatimsCollector test failed: {e}")
        return False


def test_token_extraction_simulation():
    """Simulate token extraction without actually opening browser"""
    print("\n🔍 Testing Token Extraction (Simulation)...")
    print("=" * 50)
    
    try:
        from token_extractor import TokenExtractor
        
        config = {
            'extraction_timeout': 5
        }
        
        token_extractor = TokenExtractor(config)
        
        # Test JWT validation function
        test_tokens = [
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJ0ZXN0IiwiaXNzIjoidGVzdCIsImV4cCI6OTk5OTk5OTk5OX0.test",  # Valid format
            "invalid.token",  # Invalid format
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJ0ZXN0IiwiaXNzIjoidGVzdCIsImV4cCI6OTk5OTk5OTk5OX0.test",  # With Bearer prefix
            ""  # Empty
        ]
        
        for i, token in enumerate(test_tokens):
            is_valid = token_extractor._validate_jwt_format(token)
            print(f"🧪 Token {i+1} validation: {'VALID' if is_valid else 'INVALID'}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Token extraction test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 JWT Token Automation System Tests")
    print("=" * 60)
    
    test_results = []
    
    # Run tests
    tests = [
        ("TokenManager", test_token_manager),
        ("Chrome Automation", test_chrome_automation),
        ("ChatbotCollector Integration", test_chatbot_collector_integration),
        ("Token Extraction Simulation", test_token_extraction_simulation)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{len(test_results)} tests passed")
    
    if passed == len(test_results):
        print("🎉 All tests passed! The token automation system is ready.")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    print("\n💡 Next Steps:")
    print("1. Ensure Chrome is installed and accessible")
    print("2. Update your JWT token in temp_aws_credentials.env")
    print("3. Run the ChatbotVerbatimsCollector with auto_refresh_tokens=True")
    print("4. Monitor logs for automatic token refresh events")


if __name__ == "__main__":
    main()
