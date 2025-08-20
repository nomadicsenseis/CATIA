#!/usr/bin/env python3
"""
JWT Token Extractor for Iberia NPS Chatbot
Extracts JWT tokens from Chrome network logs, focusing on Authorization Bearer tokens in verbatim requests
"""

import json
import time
import logging
import re
from typing import Optional, Dict, Any, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class TokenExtractor:
    """
    Extracts JWT tokens from Chrome browser network logs
    Focuses on Authorization Bearer tokens from verbatim-related requests
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Token Extractor
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.extraction_timeout = config.get('extraction_timeout', 10)
        self.verbatim_keywords = ['verbatim', 'nps', 'chatbot', 'api']
        
        logger.info("🔍 TokenExtractor initialized")
    
    def extract_token(self, driver: webdriver.Chrome) -> Optional[str]:
        """
        Main method to extract JWT token from the browser
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            str: JWT token if found, None otherwise
        """
        logger.info("🎯 Starting token extraction process...")
        
        # Try multiple extraction strategies
        strategies = [
            self._extract_from_network_logs,
            self._extract_from_storage,
            self._extract_from_page_interaction,
            self._extract_from_dom_inspection
        ]
        
        for strategy in strategies:
            try:
                token = strategy(driver)
                if token and self._validate_jwt_format(token):
                    logger.info(f"✅ Token extracted successfully using {strategy.__name__}")
                    return token
                else:
                    logger.debug(f"❌ Strategy {strategy.__name__} failed or returned invalid token")
            except Exception as e:
                logger.error(f"❌ Error in strategy {strategy.__name__}: {e}")
        
        logger.error("❌ All token extraction strategies failed")
        return None
    
    def _extract_from_network_logs(self, driver: webdriver.Chrome) -> Optional[str]:
        """
        Extract token from Chrome network logs (performance logs)
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            str: JWT token if found, None otherwise
        """
        logger.info("📡 Extracting token from network logs...")
        
        try:
            # Wait a bit for network activity
            time.sleep(3)
            
            # Get performance logs
            logs = driver.get_log('performance')
            
            for log_entry in logs:
                try:
                    log_message = json.loads(log_entry['message'])
                    message = log_message.get('message', {})
                    
                    # Look for network request messages
                    if message.get('method') == 'Network.responseReceived':
                        response = message.get('params', {}).get('response', {})
                        url = response.get('url', '')
                        
                        # Check if this is a verbatim-related request
                        if self._is_verbatim_request(url):
                            logger.info(f"🎯 Found verbatim request: {url}")
                            
                            # Get request details
                            request_id = message.get('params', {}).get('requestId')
                            if request_id:
                                token = self._get_request_headers_token(driver, request_id)
                                if token:
                                    return token
                    
                    # Also check for request headers in sent requests
                    elif message.get('method') == 'Network.requestWillBeSent':
                        request = message.get('params', {}).get('request', {})
                        url = request.get('url', '')
                        headers = request.get('headers', {})
                        
                        if self._is_verbatim_request(url):
                            logger.info(f"🎯 Found outgoing verbatim request: {url}")
                            token = self._extract_token_from_headers(headers)
                            if token:
                                return token
                
                except (json.JSONDecodeError, KeyError) as e:
                    continue
            
            logger.warning("⚠️ No token found in network logs")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting from network logs: {e}")
            return None
    
    def _extract_from_storage(self, driver: webdriver.Chrome) -> Optional[str]:
        """
        Extract token from browser storage (localStorage, sessionStorage, cookies)
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            str: JWT token if found, None otherwise
        """
        logger.info("💾 Extracting token from browser storage...")
        
        try:
            # Check localStorage
            storage_keys = [
                'token', 'jwt', 'auth_token', 'authorization', 'bearer_token',
                'access_token', 'chatbot_token', 'nps_token', 'iberia_token'
            ]
            
            for key in storage_keys:
                try:
                    value = driver.execute_script(f"return localStorage.getItem('{key}');")
                    if value and self._validate_jwt_format(value):
                        logger.info(f"✅ Token found in localStorage['{key}']")
                        return value
                except Exception:
                    continue
            
            # Check sessionStorage
            for key in storage_keys:
                try:
                    value = driver.execute_script(f"return sessionStorage.getItem('{key}');")
                    if value and self._validate_jwt_format(value):
                        logger.info(f"✅ Token found in sessionStorage['{key}']")
                        return value
                except Exception:
                    continue
            
            # Check cookies
            cookies = driver.get_cookies()
            for cookie in cookies:
                if any(keyword in cookie.get('name', '').lower() for keyword in ['token', 'jwt', 'auth']):
                    value = cookie.get('value', '')
                    if self._validate_jwt_format(value):
                        logger.info(f"✅ Token found in cookie '{cookie['name']}'")
                        return value
            
            logger.warning("⚠️ No token found in browser storage")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting from storage: {e}")
            return None
    
    def _extract_from_page_interaction(self, driver: webdriver.Chrome) -> Optional[str]:
        """
        Extract token by interacting with the page to trigger network requests
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            str: JWT token if found, None otherwise
        """
        logger.info("🖱️ Extracting token through page interaction...")
        
        try:
            # Clear existing logs
            driver.get_log('performance')
            
            # Try to trigger verbatim-related requests
            interactions = [
                self._click_verbatim_elements,
                self._trigger_data_refresh,
                self._navigate_verbatim_sections
            ]
            
            for interaction in interactions:
                try:
                    interaction(driver)
                    time.sleep(2)  # Wait for network requests
                    
                    # Check for new network activity
                    token = self._extract_from_network_logs(driver)
                    if token:
                        return token
                        
                except Exception as e:
                    logger.debug(f"Interaction failed: {e}")
                    continue
            
            logger.warning("⚠️ No token found through page interaction")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error in page interaction extraction: {e}")
            return None
    
    def _extract_from_dom_inspection(self, driver: webdriver.Chrome) -> Optional[str]:
        """
        Extract token by inspecting DOM elements and JavaScript variables
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            str: JWT token if found, None otherwise
        """
        logger.info("🔍 Extracting token from DOM inspection...")
        
        try:
            # Check common JavaScript global variables
            js_variables = [
                'window.token', 'window.jwt', 'window.authToken', 'window.bearerToken',
                'window.accessToken', 'window.authorization', 'window.chatbotToken',
                'window.npsToken', 'window.iberiaToken'
            ]
            
            for var in js_variables:
                try:
                    value = driver.execute_script(f"return {var};")
                    if value and self._validate_jwt_format(value):
                        logger.info(f"✅ Token found in {var}")
                        return value
                except Exception:
                    continue
            
            # Check for meta tags with tokens
            meta_tags = driver.find_elements(By.XPATH, "//meta[contains(@name, 'token') or contains(@name, 'jwt') or contains(@name, 'auth')]")
            for meta in meta_tags:
                try:
                    content = meta.get_attribute('content')
                    if content and self._validate_jwt_format(content):
                        logger.info(f"✅ Token found in meta tag")
                        return content
                except Exception:
                    continue
            
            # Check for data attributes with tokens
            elements_with_data = driver.find_elements(By.XPATH, "//*[@data-token or @data-jwt or @data-auth]")
            for element in elements_with_data:
                try:
                    for attr in ['data-token', 'data-jwt', 'data-auth']:
                        value = element.get_attribute(attr)
                        if value and self._validate_jwt_format(value):
                            logger.info(f"✅ Token found in {attr} attribute")
                            return value
                except Exception:
                    continue
            
            logger.warning("⚠️ No token found in DOM inspection")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error in DOM inspection: {e}")
            return None
    
    def _is_verbatim_request(self, url: str) -> bool:
        """
        Check if a URL is related to verbatim requests
        
        Args:
            url: URL to check
            
        Returns:
            bool: True if verbatim-related, False otherwise
        """
        if not url:
            return False
        
        url_lower = url.lower()
        return any(keyword in url_lower for keyword in self.verbatim_keywords)
    
    def _extract_token_from_headers(self, headers: Dict[str, str]) -> Optional[str]:
        """
        Extract JWT token from HTTP headers
        
        Args:
            headers: Dictionary of HTTP headers
            
        Returns:
            str: JWT token if found, None otherwise
        """
        auth_header = headers.get('Authorization') or headers.get('authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            if self._validate_jwt_format(token):
                return token
        return None
    
    def _get_request_headers_token(self, driver: webdriver.Chrome, request_id: str) -> Optional[str]:
        """
        Get request headers for a specific request ID and extract token
        
        Args:
            driver: Chrome driver instance
            request_id: Network request ID
            
        Returns:
            str: JWT token if found, None otherwise
        """
        try:
            # This is a simplified approach since getting request details via CDP is complex
            # For now, we'll rely on the logs we already have
            return None
        except Exception:
            return None
    
    def _click_verbatim_elements(self, driver: webdriver.Chrome) -> None:
        """
        Click on elements that might trigger verbatim requests
        
        Args:
            driver: Chrome driver instance
        """
        try:
            # Look for buttons or links related to verbatims
            selectors = [
                "//button[contains(text(), 'verbatim') or contains(text(), 'Verbatim')]",
                "//a[contains(text(), 'verbatim') or contains(text(), 'Verbatim')]",
                "//button[contains(@class, 'verbatim')]",
                "//div[contains(@class, 'verbatim')]//button",
                "//button[contains(text(), 'Load') or contains(text(), 'Cargar')]",
                "//button[contains(text(), 'Refresh') or contains(text(), 'Actualizar')]"
            ]
            
            for selector in selectors:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    logger.info(f"🖱️ Clicking verbatim element: {selector}")
                    elements[0].click()
                    time.sleep(1)
                    break
                    
        except Exception as e:
            logger.debug(f"Error clicking verbatim elements: {e}")
    
    def _trigger_data_refresh(self, driver: webdriver.Chrome) -> None:
        """
        Trigger data refresh actions
        
        Args:
            driver: Chrome driver instance
        """
        try:
            # Try common refresh actions
            driver.execute_script("location.reload();")
            time.sleep(3)
        except Exception as e:
            logger.debug(f"Error triggering data refresh: {e}")
    
    def _navigate_verbatim_sections(self, driver: webdriver.Chrome) -> None:
        """
        Navigate to different verbatim sections
        
        Args:
            driver: Chrome driver instance
        """
        try:
            # Look for navigation elements
            nav_selectors = [
                "//nav//a[contains(text(), 'verbatim')]",
                "//ul//li//a[contains(text(), 'verbatim')]",
                "//div[contains(@class, 'nav')]//a"
            ]
            
            for selector in nav_selectors:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    logger.info(f"🧭 Navigating to verbatim section: {selector}")
                    elements[0].click()
                    time.sleep(2)
                    break
                    
        except Exception as e:
            logger.debug(f"Error navigating verbatim sections: {e}")
    
    def _validate_jwt_format(self, token: str) -> bool:
        """
        Validate if a string has JWT format (3 base64 parts separated by dots)
        
        Args:
            token: String to validate
            
        Returns:
            bool: True if valid JWT format, False otherwise
        """
        if not token or not isinstance(token, str):
            return False
        
        # Remove any 'Bearer ' prefix
        if token.startswith('Bearer '):
            token = token[7:]
        
        # JWT should have 3 parts separated by dots
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        # Each part should be base64-like (alphanumeric + - and _)
        jwt_pattern = re.compile(r'^[A-Za-z0-9_-]+$')
        for part in parts:
            if not jwt_pattern.match(part):
                return False
        
        # Additional length check (JWTs are typically quite long)
        if len(token) < 100:
            return False
        
        return True
    
    def debug_network_activity(self, driver: webdriver.Chrome) -> List[Dict[str, Any]]:
        """
        Debug method to inspect all network activity
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            list: List of network activity details
        """
        try:
            logs = driver.get_log('performance')
            network_activity = []
            
            for log_entry in logs:
                try:
                    log_message = json.loads(log_entry['message'])
                    message = log_message.get('message', {})
                    
                    if message.get('method') in ['Network.requestWillBeSent', 'Network.responseReceived']:
                        network_activity.append({
                            'method': message.get('method'),
                            'timestamp': log_entry.get('timestamp'),
                            'url': message.get('params', {}).get('request', {}).get('url') or 
                                   message.get('params', {}).get('response', {}).get('url'),
                            'headers': message.get('params', {}).get('request', {}).get('headers') or
                                      message.get('params', {}).get('response', {}).get('headers')
                        })
                except:
                    continue
            
            return network_activity
            
        except Exception as e:
            logger.error(f"❌ Error debugging network activity: {e}")
            return []
