#!/usr/bin/env python3
"""
Example usage of ChatbotVerbatimsCollector with automatic token refresh
Demonstrates both token-based API mode and PBI fallback mode
"""

import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector


def example_token_based_mode():
    """
    Example using token-based authentication with automatic refresh
    """
    print("🔐 Example: Token-based Chatbot API Mode")
    print("=" * 50)
    
    # Initialize with token and base URL
    # The collector will automatically handle token refresh
    collector = ChatbotVerbatimsCollector(
        token="your_jwt_token_here",  # Will be loaded from temp_aws_credentials.env
        base_url="https://b8fktdca38.execute-api.eu-west-1.amazonaws.com/api/transformation/api/nps-chatbot"
    )
    
    # Test connection
    success, message = collector.test_connection()
    print(f"Connection test: {message}")
    
    if success:
        # Define date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        date_range = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        # Collect verbatims
        print(f"\n📊 Collecting verbatims for period: {date_range[0]} to {date_range[1]}")
        
        verbatims_df = collector.collect_verbatims_for_period(
            date_range=date_range,
            node_path="ALL",  # All nodes
            filters={
                'sentiment_type': 'negative',
                'min_nps': 0
            }
        )
        
        if not verbatims_df.empty:
            print(f"✅ Collected {len(verbatims_df)} verbatims")
            
            # Get summary
            summary = collector.get_verbatims_summary(verbatims_df)
            print(f"\n📈 Summary: {summary['summary']}")
        else:
            print("❌ No verbatims collected")
    else:
        print("❌ Cannot proceed without valid connection")


def example_pbi_fallback_mode():
    """
    Example using PBI collector as fallback
    """
    print("\n\n📊 Example: PBI Collector Fallback Mode")
    print("=" * 50)
    
    # Initialize with PBI collector only
    # This simulates the original behavior
    collector = ChatbotVerbatimsCollector(
        pbi_collector="mock_pbi_collector"  # Replace with actual PBI collector
    )
    
    # Test connection
    success, message = collector.test_connection()
    print(f"Connection test: {message}")
    
    if success:
        print("✅ PBI collector mode ready")
    else:
        print("❌ PBI collector not available")


def example_hybrid_mode():
    """
    Example using both token and PBI collector for maximum reliability
    """
    print("\n\n🔄 Example: Hybrid Mode (Token + PBI Fallback)")
    print("=" * 50)
    
    # Initialize with both token and PBI collector
    collector = ChatbotVerbatimsCollector(
        token="your_jwt_token_here",
        base_url="https://b8fktdca38.execute-api.eu-west-1.amazonaws.com/api/transformation/api/nps-chatbot",
        pbi_collector="mock_pbi_collector"  # Replace with actual PBI collector
    )
    
    # Test connection
    success, message = collector.test_connection()
    print(f"Connection test: {message}")
    
    if success:
        print("✅ Hybrid mode ready - will try API first, fallback to PBI if needed")
        
        # The collector will automatically:
        # 1. Try to get data from chatbot API
        # 2. If API fails, fallback to PBI collector
        # 3. Handle token refresh automatically
        # 4. Provide seamless data collection
    else:
        print("❌ Neither data source available")


def main():
    """
    Main function to run examples
    """
    print("🚀 ChatbotVerbatimsCollector Examples")
    print("=" * 60)
    
    # Example 1: Token-based mode
    example_token_based_mode()
    
    # Example 2: PBI fallback mode
    example_pbi_fallback_mode()
    
    # Example 3: Hybrid mode
    example_hybrid_mode()
    
    print("\n\n💡 Key Benefits of the New Implementation:")
    print("• Automatic JWT token refresh from temp_aws_credentials.env")
    print("• Seamless fallback from chatbot API to PBI collector")
    print("• Token validation and expiry checking")
    print("• Retry logic with fresh tokens")
    print("• Backward compatibility with existing code")
    
    print("\n📝 Usage Notes:")
    print("• Place your JWT token in dashboard_analyzer/temp_aws_credentials.env")
    print("• Format: chatbot_jwt_token = your_token_here")
    print("• Token will be automatically refreshed when needed")
    print("• No manual intervention required")


if __name__ == "__main__":
    main()
