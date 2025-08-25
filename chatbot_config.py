"""
Chatbot Configuration
Configuration file for chatbot API endpoints and settings
"""

import os
from typing import Dict, Any

# Chatbot API Configuration
CHATBOT_CONFIG = {
    # API Endpoints
    "api_endpoints": {
        "verbatims": os.getenv('CHATBOT_API_ENDPOINT', 'https://nps.chatbot.iberia.es/api/verbatims'),
        "conversation": os.getenv('CHATBOT_CONVERSATION_ENDPOINT', 'https://nps.chatbot.iberia.es/api/conversation'),
        "analysis": os.getenv('CHATBOT_ANALYSIS_ENDPOINT', 'https://nps.chatbot.iberia.es/api/analysis'),
        "health": os.getenv('CHATBOT_HEALTH_ENDPOINT', 'https://nps.chatbot.iberia.es/api/health')
    },
    
    # Authentication
    "auth": {
        "token_header": "Authorization",
        "token_prefix": "Bearer",
        "timeout_seconds": 30,
        "retry_attempts": 3,
        "retry_delay_seconds": 2
    },
    
    # Request Configuration
    "requests": {
        "user_agent": "CausalExplanationAgent/1.0",
        "content_type": "application/json",
        "accept": "application/json",
        "max_payload_size_mb": 10
    },
    
    # Response Handling
    "response": {
        "expected_fields": ["verbatims", "status", "message", "metadata"],
        "max_verbatims_per_request": 1000,
        "default_page_size": 100
    },
    
    # Error Handling
    "errors": {
        "retryable_status_codes": [408, 429, 500, 502, 503, 504],
        "max_retry_attempts": 3,
        "exponential_backoff": True
    },
    
    # Development/Testing
    "development": {
        "mock_api": os.getenv('CHATBOT_MOCK_API', 'false').lower() == 'true',
        "log_requests": os.getenv('CHATBOT_LOG_REQUESTS', 'true').lower() == 'true',
        "log_responses": os.getenv('CHATBOT_LOG_RESPONSES', 'false').lower() == 'true'
    }
}

def get_chatbot_config() -> Dict[str, Any]:
    """Get the chatbot configuration"""
    return CHATBOT_CONFIG

def get_api_endpoint(endpoint_name: str) -> str:
    """Get a specific API endpoint URL"""
    return CHATBOT_CONFIG["api_endpoints"].get(endpoint_name, "")

def get_auth_config() -> Dict[str, Any]:
    """Get authentication configuration"""
    return CHATBOT_CONFIG["auth"]

def is_development_mode() -> bool:
    """Check if we're in development mode"""
    return CHATBOT_CONFIG["development"]["mock_api"]

def should_log_requests() -> bool:
    """Check if requests should be logged"""
    return CHATBOT_CONFIG["development"]["log_requests"]

def should_log_responses() -> bool:
    """Check if responses should be logged"""
    return CHATBOT_CONFIG["development"]["log_responses"]

# Environment variable overrides
def update_config_from_env():
    """Update configuration from environment variables"""
    global CHATBOT_CONFIG
    
    # Update API endpoints from environment
    for endpoint_name in CHATBOT_CONFIG["api_endpoints"]:
        env_var = f"CHATBOT_{endpoint_name.upper()}_ENDPOINT"
        if os.getenv(env_var):
            CHATBOT_CONFIG["api_endpoints"][endpoint_name] = os.getenv(env_var)
    
    # Update other settings from environment
    if os.getenv('CHATBOT_TIMEOUT'):
        try:
            CHATBOT_CONFIG["auth"]["timeout_seconds"] = int(os.getenv('CHATBOT_TIMEOUT'))
        except ValueError:
            pass
    
    if os.getenv('CHATBOT_MAX_RETRIES'):
        try:
            CHATBOT_CONFIG["errors"]["max_retry_attempts"] = int(os.getenv('CHATBOT_MAX_RETRIES'))
        except ValueError:
            pass

# Initialize configuration
update_config_from_env()
