# Chatbot JWT Token Management Guide

## Overview

The `ChatbotVerbatimsCollector` has been enhanced to support automatic JWT token management with seamless fallback to Power BI collector. This eliminates the need for manual token updates and provides a robust data collection system.

## Architecture

### Dual Mode Operation
1. **Primary Mode**: Chatbot API with JWT authentication
2. **Fallback Mode**: Power BI collector (existing functionality)
3. **Hybrid Mode**: Both sources for maximum reliability

### Token Management Features
- ✅ **Automatic token validation** - Checks expiry before each request
- ✅ **Proactive refresh** - Refreshes token 5 minutes before expiry
- ✅ **File-based storage** - Reads from `temp_aws_credentials.env`
- ✅ **Retry logic** - Automatically retries failed requests with fresh tokens
- ✅ **Seamless fallback** - Falls back to PBI collector if API fails

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Token File
Create or update `dashboard_analyzer/temp_aws_credentials.env`:
```env
chatbot_jwt_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9...
```

### 3. Initialize Collector

#### Token-Only Mode (Recommended)
```python
from data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector

collector = ChatbotVerbatimsCollector(
    token="your_jwt_token_here",
    base_url="https://b8fktdca38.execute-api.eu-west-1.amazonaws.com/api/transformation/api/nps-chatbot"
)
```

#### Hybrid Mode (Maximum Reliability)
```python
collector = ChatbotVerbatimsCollector(
    token="your_jwt_token_here",
    base_url="https://b8fktdca38.execute-api.eu-west-1.amazonaws.com/api/transformation/api/nps-chatbot",
    pbi_collector=your_pbi_collector_instance
)
```

#### PBI Fallback Mode (Legacy)
```python
collector = ChatbotVerbatimsCollector(
    pbi_collector=your_pbi_collector_instance
)
```

## How It Works

### Token Lifecycle
1. **Initialization**: Token loaded from file or constructor
2. **Validation**: Before each API request, token expiry is checked
3. **Proactive Refresh**: If token expires within 5 minutes, it's refreshed
4. **Automatic Retry**: Failed requests due to expired tokens are retried
5. **Fallback**: If token refresh fails, falls back to PBI collector

### Token Refresh Process
```
API Request → Check Token Expiry → Valid? → Use Token
                    ↓
                Expires Soon? → Refresh from File → Success? → Update Token
                    ↓
                Failed Refresh → Fallback to PBI Collector
```

## Usage Examples

### Basic Data Collection
```python
# The collector handles token management automatically
verbatims_df = collector.collect_verbatims_for_period(
    date_range=('2024-01-01', '2024-01-31'),
    node_path='ALL',
    filters={'sentiment_type': 'negative'}
)
```

### Connection Testing
```python
success, message = collector.test_connection()
if success:
    print("✅ Ready to collect data")
else:
    print(f"❌ Connection failed: {message}")
```

### Manual Token Update
Simply update the token in `temp_aws_credentials.env`:
```env
# Old token (expired)
# chatbot_jwt_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9...

# New token (fresh)
chatbot_jwt_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9...
```

The collector will automatically detect and use the new token on the next request.

## Configuration Options

### Environment Variables
```bash
# Optional: Override token file path
export CHATBOT_TOKEN_FILE="/path/to/your/credentials.env"

# Optional: Override base URL
export CHATBOT_BASE_URL="https://your-api-endpoint.com/api"
```

### Constructor Parameters
```python
collector = ChatbotVerbatimsCollector(
    token="your_token",
    base_url="your_api_url",
    pbi_collector=your_pbi_collector,
    # Optional: Customize token management
    token_file="custom/path/to/credentials.env",
    token_refresh_threshold=600  # 10 minutes before expiry
)
```

## Troubleshooting

### Common Issues

#### 1. Token Expired
**Symptoms**: 401 Unauthorized errors
**Solution**: Update token in `temp_aws_credentials.env`

#### 2. File Not Found
**Symptoms**: "Token file not found" warnings
**Solution**: Ensure `temp_aws_credentials.env` exists in correct location

#### 3. Invalid Token Format
**Symptoms**: "Invalid token format" errors
**Solution**: Check token format in file (no extra quotes/spaces)

#### 4. API Endpoint Unreachable
**Symptoms**: Connection timeout errors
**Solution**: Verify base URL and network connectivity

### Debug Mode
Enable detailed logging to troubleshoot token issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Best Practices

### 1. Token Security
- Store tokens in environment-specific files
- Use `.env` files (not committed to git)
- Rotate tokens regularly

### 2. Error Handling
- Always check connection status before data collection
- Implement proper fallback logic in your application
- Monitor token refresh logs

### 3. Performance
- Token validation adds minimal overhead
- File I/O only occurs during refresh
- API requests use persistent sessions

## Migration from Old Version

### Before (Old Version)
```python
# Only supported PBI collector
collector = ChatbotVerbatimsCollector(pbi_collector)
```

### After (New Version)
```python
# Supports both modes, backward compatible
collector = ChatbotVerbatimsCollector(
    token="your_token",  # New: JWT authentication
    base_url="your_api", # New: API endpoint
    pbi_collector=pbi_collector  # Existing: Fallback support
)
```

## API Endpoints

The collector expects the following API structure:
- `GET /health` - Health check endpoint
- `GET /verbatims` - Main verbatims endpoint with query parameters

### Query Parameters
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `node_path`: Node path for filtering
- `sentiment`: Sentiment filter (optional)
- `theme`: Theme filter (optional)
- `min_nps_score`: Minimum NPS score (optional)

## Support

For issues or questions:
1. Check the logs for detailed error messages
2. Verify token format and expiry
3. Test API connectivity manually
4. Review this documentation

---

**Note**: This implementation provides a robust, production-ready solution for managing JWT tokens in the ChatbotVerbatimsCollector while maintaining full backward compatibility.
