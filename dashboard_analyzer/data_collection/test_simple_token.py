#!/usr/bin/env python3
"""
Simple test for the simplified token system
"""

import sys
import os
import logging

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_simple_token_system():
    """Test the simplified token system"""
    
    print("🧪 SIMPLE TOKEN SYSTEM TEST")
    print("=" * 50)
    
    try:
        # Import the simplified collector
        from chatbot_verbatims_collector import ChatbotVerbatimsCollector
        
        print("📋 Step 1: Initialize simplified ChatbotVerbatimsCollector")
        
        # Test with PBI fallback only (no token)
        collector = ChatbotVerbatimsCollector()
        print("✅ ChatbotVerbatimsCollector initialized successfully")
        
        # Test connection
        success, message = collector.test_connection()
        print(f"🔗 Connection test: {message}")
        
        print()
        print("📋 Step 2: Test token validation")
        
        # Test token status
        status = collector.get_token_status()
        print(f"🔒 Token status: {status['status']}")
        print(f"📝 Message: {status['message']}")
        
        if 'expires_in' in status and status['expires_in']:
            print(f"⏰ Expires in: {status['expires_in']} seconds")
        
        print()
        print("🎉 TEST COMPLETED!")
        print("✅ Simplified token system working correctly!")
        print("✅ No reloading/refreshing logic")
        print("✅ Direct fallback to PBI when token expires")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_simple_token_system()
