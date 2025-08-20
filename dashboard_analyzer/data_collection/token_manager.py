#!/usr/bin/env python3
"""
JWT Token Manager for Chatbot Verbatims Collection
Manages automatic token refresh using Chrome automation to extract fresh tokens from Iberia NPS Chatbot
"""

import os
import jwt
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

try:
    from .chrome_automation import ChromeAutomation
    from .token_extractor import TokenExtractor
except ImportError:
    # Fallback for direct execution
    from chrome_automation import ChromeAutomation
    from token_extractor import TokenExtractor

logger = logging.getLogger(__name__)


class TokenManager:
    """
    Manages JWT token lifecycle for Iberia NPS Chatbot authentication
    Automatically refreshes tokens when they expire using Chrome automation
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Token Manager
        
        Args:
            config: Configuration dictionary with settings
        """
        self.config = config or self._get_default_config()
        
        # Initialize components
        self.chrome_automation = ChromeAutomation(self.config)
        self.token_extractor = TokenExtractor(self.config)
        
        # Token management settings - use absolute path
        self.token_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'temp_aws_credentials.env'
        ))
        self.refresh_threshold = self.config.get('refresh_threshold', 300)  # 5 minutes
        self.max_retries = self.config.get('max_retries', 3)
        
        # State tracking
        self.current_token = None
        self.last_refresh_time = None
        self.refresh_in_progress = False
        
        logger.info("🚀 TokenManager initialized")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for Token Manager"""
        return {
            'verbatims_url': 'https://nps.chatbot.iberia.es/home',
            'token_file': 'dashboard_analyzer/temp_aws_credentials.env',
            'refresh_threshold': 300,  # 5 minutes before expiry
            'max_retries': 3,
            'headless': False,  # Set to True for production
            'chrome_profile_dir': None,  # Will auto-detect default Chrome profile
            'wait_timeout': 30,  # seconds to wait for page loads
            'extraction_timeout': 10,  # seconds to wait for token extraction
        }
    
    def ensure_valid_token(self) -> bool:
        """
        Ensures the current token is valid, refreshes if needed
        
        Returns:
            bool: True if valid token is available, False otherwise
        """
        try:
            # Load current token from file
            self.current_token = self._load_token_from_file()
            
            if not self.current_token:
                logger.warning("⚠️ No token found in file, attempting fresh extraction")
                return self._refresh_token()
            
            # Check token validity
            token_status = self._get_token_status(self.current_token)
            
            if token_status['expired']:
                logger.warning("⚠️ Token has expired, refreshing...")
                return self._refresh_token()
            
            if token_status['expires_in'] <= self.refresh_threshold:
                logger.warning(f"⚠️ Token expires in {token_status['expires_in']}s, refreshing proactively...")
                return self._refresh_token()
            
            logger.info(f"✅ Token is valid, expires in {token_status['expires_in']}s")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error ensuring valid token: {e}")
            return False
    
    def _refresh_token(self) -> bool:
        """
        Refreshes the JWT token using Chrome automation
        
        Returns:
            bool: True if refresh successful, False otherwise
        """
        if self.refresh_in_progress:
            logger.info("🔄 Token refresh already in progress, waiting...")
            return self._wait_for_refresh_completion()
        
        self.refresh_in_progress = True
        
        try:
            logger.info("🔄 Starting token refresh process...")
            
            for attempt in range(1, self.max_retries + 1):
                logger.info(f"🔄 Refresh attempt {attempt}/{self.max_retries}")
                
                try:
                    # Start Chrome automation
                    driver = self.chrome_automation.start_browser()
                    
                    if not driver:
                        logger.error(f"❌ Failed to start Chrome browser (attempt {attempt})")
                        continue
                    
                    # Navigate to verbatims page
                    if not self.chrome_automation.navigate_to_verbatims(driver):
                        logger.error(f"❌ Failed to navigate to verbatims page (attempt {attempt})")
                        self.chrome_automation.cleanup(driver)
                        continue
                    
                    # Extract token from network requests
                    new_token = self.token_extractor.extract_token(driver)
                    
                    # Cleanup browser
                    self.chrome_automation.cleanup(driver)
                    
                    if new_token:
                        # Validate the new token
                        if self._is_valid_token(new_token):
                            # Save to file
                            if self._save_token_to_file(new_token):
                                self.current_token = new_token
                                self.last_refresh_time = datetime.now()
                                logger.info("✅ Token refresh successful!")
                                return True
                            else:
                                logger.error(f"❌ Failed to save token to file (attempt {attempt})")
                        else:
                            logger.error(f"❌ Extracted token is invalid (attempt {attempt})")
                    else:
                        logger.error(f"❌ Failed to extract token (attempt {attempt})")
                
                except Exception as e:
                    logger.error(f"❌ Error during refresh attempt {attempt}: {e}")
                    # Ensure cleanup in case of exception
                    try:
                        if 'driver' in locals():
                            self.chrome_automation.cleanup(driver)
                    except:
                        pass
                
                # Wait before retry
                if attempt < self.max_retries:
                    wait_time = attempt * 2  # Exponential backoff
                    logger.info(f"⏱️ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
            
            logger.error("❌ All token refresh attempts failed")
            return False
            
        finally:
            self.refresh_in_progress = False
    
    def _load_token_from_file(self) -> Optional[str]:
        """
        Loads JWT token from the credentials file
        
        Returns:
            str: JWT token if found, None otherwise
        """
        try:
            if not os.path.exists(self.token_file):
                logger.warning(f"⚠️ Token file not found: {self.token_file}")
                return None
            
            with open(self.token_file, 'r') as f:
                for line in f:
                    if line.startswith('chatbot_jwt_token ='):
                        token = line.split('=', 1)[1].strip().strip('"\'')
                        if token:
                            logger.debug("📄 Token loaded from file")
                            return token
            
            logger.warning("⚠️ No token found in credentials file")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error loading token from file: {e}")
            return None
    
    def _save_token_to_file(self, token: str) -> bool:
        """
        Saves JWT token to the credentials file
        
        Args:
            token: JWT token to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read existing content
            lines = []
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    lines = f.readlines()
            
            # Update or add token line
            token_line = f"chatbot_jwt_token = {token}\n"
            token_updated = False
            
            for i, line in enumerate(lines):
                if line.startswith('chatbot_jwt_token ='):
                    lines[i] = token_line
                    token_updated = True
                    break
            
            if not token_updated:
                lines.append(token_line)
            
            # Write back to file
            with open(self.token_file, 'w') as f:
                f.writelines(lines)
            
            logger.info("💾 Token saved to file successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving token to file: {e}")
            return False
    
    def _get_token_status(self, token: str) -> Dict[str, Any]:
        """
        Gets status information for a JWT token
        
        Args:
            token: JWT token to analyze
            
        Returns:
            dict: Token status information
        """
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = decoded.get('exp')
            
            if not exp_timestamp:
                return {
                    'expired': True,
                    'expires_in': 0,
                    'expires_at': None,
                    'valid': False
                }
            
            current_time = datetime.utcnow().timestamp()
            time_until_expiry = exp_timestamp - current_time
            
            return {
                'expired': time_until_expiry <= 0,
                'expires_in': max(0, int(time_until_expiry)),
                'expires_at': datetime.fromtimestamp(exp_timestamp).isoformat(),
                'valid': time_until_expiry > 0
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting token status: {e}")
            return {
                'expired': True,
                'expires_in': 0,
                'expires_at': None,
                'valid': False
            }
    
    def _is_valid_token(self, token: str) -> bool:
        """
        Checks if a token is valid and not expired
        
        Args:
            token: JWT token to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        status = self._get_token_status(token)
        return status['valid'] and not status['expired']
    
    def _wait_for_refresh_completion(self) -> bool:
        """
        Waits for an in-progress refresh to complete
        
        Returns:
            bool: True if refresh completed successfully
        """
        max_wait_time = 120  # 2 minutes max wait
        check_interval = 2   # Check every 2 seconds
        
        start_time = time.time()
        
        while self.refresh_in_progress:
            if time.time() - start_time > max_wait_time:
                logger.error("⏰ Timeout waiting for refresh completion")
                return False
            
            time.sleep(check_interval)
        
        # Check if we now have a valid token
        return self.current_token is not None and self._is_valid_token(self.current_token)
    
    def get_current_token(self) -> Optional[str]:
        """
        Gets the current valid token, refreshing if needed
        
        Returns:
            str: Current valid JWT token, None if unavailable
        """
        if self.ensure_valid_token():
            return self.current_token
        return None
    
    def get_token_info(self) -> Dict[str, Any]:
        """
        Gets comprehensive information about the current token
        
        Returns:
            dict: Token information and status
        """
        token = self._load_token_from_file()
        
        if not token:
            return {
                'status': 'no_token',
                'message': 'No token available',
                'token_present': False
            }
        
        status = self._get_token_status(token)
        
        return {
            'status': 'expired' if status['expired'] else 'valid',
            'message': f"Token {'expired' if status['expired'] else 'valid'}",
            'token_present': True,
            'expires_in': status['expires_in'],
            'expires_at': status['expires_at'],
            'needs_refresh': status['expires_in'] <= self.refresh_threshold,
            'last_refresh': self.last_refresh_time.isoformat() if self.last_refresh_time else None
        }
    
    def force_refresh(self) -> bool:
        """
        Forces an immediate token refresh regardless of expiration
        
        Returns:
            bool: True if refresh successful
        """
        logger.info("🔄 Forcing token refresh...")
        return self._refresh_token()
