#!/usr/bin/env python3
"""
Chrome Browser Automation for Token Extraction
Handles Chrome browser automation to navigate to Iberia NPS Chatbot and extract JWT tokens
"""

import os
import time
import logging
import platform
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class ChromeAutomation:
    """
    Handles Chrome browser automation for JWT token extraction from Iberia NPS Chatbot
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Chrome Automation
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.verbatims_url = config.get('verbatims_url', 'https://nps.chatbot.iberia.es/home')
        self.headless = config.get('headless', False)
        self.wait_timeout = config.get('wait_timeout', 30)
        self.chrome_profile_dir = config.get('chrome_profile_dir') or self._get_default_chrome_profile()
        
        logger.info("🌐 ChromeAutomation initialized")
        logger.info(f"📂 Chrome profile directory: {self.chrome_profile_dir}")
        logger.info(f"🎯 Target URL: {self.verbatims_url}")
    
    def _get_default_chrome_profile(self) -> str:
        """
        Get the default Chrome profile directory for the current OS
        
        Returns:
            str: Path to Chrome profile directory
        """
        system = platform.system().lower()
        username = os.getenv('USERNAME') or os.getenv('USER') or 'user'
        
        if system == 'windows':
            return os.path.expanduser(f"~\\AppData\\Local\\Google\\Chrome\\User Data")
        elif system == 'darwin':  # macOS
            return os.path.expanduser("~/Library/Application Support/Google/Chrome")
        else:  # Linux
            return os.path.expanduser("~/.config/google-chrome")
    
    def _setup_chrome_options(self) -> Options:
        """
        Setup Chrome options for automation
        
        Returns:
            Options: Configured Chrome options
        """
        options = Options()
        
        # User profile settings
        if self.chrome_profile_dir and os.path.exists(self.chrome_profile_dir):
            options.add_argument(f"--user-data-dir={self.chrome_profile_dir}")
            logger.info(f"✅ Using Chrome profile: {self.chrome_profile_dir}")
        else:
            logger.warning(f"⚠️ Chrome profile directory not found: {self.chrome_profile_dir}")
        
        # Performance and compatibility options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")  # Faster loading
        
        # Network logging for token extraction
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})
        
        # Headless mode if configured
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            logger.info("🕶️ Running in headless mode")
        else:
            logger.info("👁️ Running in visible mode")
        
        # Anti-detection measures
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        return options
    
    def start_browser(self) -> Optional[webdriver.Chrome]:
        """
        Start Chrome browser with proper configuration
        
        Returns:
            webdriver.Chrome: Chrome driver instance, None if failed
        """
        try:
            logger.info("🚀 Starting Chrome browser...")
            
            # Setup Chrome options
            options = self._setup_chrome_options()
            
            # Setup Chrome service with webdriver manager
            service = Service(ChromeDriverManager().install())
            
            # Create WebDriver instance
            driver = webdriver.Chrome(service=service, options=options)
            
            # Configure timeouts
            driver.set_page_load_timeout(self.wait_timeout)
            driver.implicitly_wait(10)
            
            # Anti-detection script
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("✅ Chrome browser started successfully")
            return driver
            
        except WebDriverException as e:
            logger.error(f"❌ Failed to start Chrome browser: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error starting browser: {e}")
            return None
    
    def navigate_to_verbatims(self, driver: webdriver.Chrome) -> bool:
        """
        Navigate to the verbatims page and wait for it to load
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            logger.info(f"🧭 Navigating to {self.verbatims_url}")
            
            # Navigate to the page
            driver.get(self.verbatims_url)
            
            # Wait for page to start loading
            time.sleep(2)
            
            # Wait for basic page elements to load
            wait = WebDriverWait(driver, self.wait_timeout)
            
            # Try to wait for common page elements that indicate successful load
            try:
                # Wait for body element
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                logger.info("✅ Page body loaded")
                
                # Additional wait for JavaScript to initialize
                time.sleep(3)
                
                # Check if we're on the correct page
                current_url = driver.current_url
                if "nps.chatbot.iberia.es" in current_url:
                    logger.info(f"✅ Successfully navigated to verbatims page: {current_url}")
                    return True
                else:
                    logger.warning(f"⚠️ Unexpected URL after navigation: {current_url}")
                    return True  # Still attempt extraction
                    
            except TimeoutException:
                logger.warning("⚠️ Timeout waiting for page elements, but continuing...")
                return True  # Still attempt to extract
            
        except TimeoutException:
            logger.error("❌ Timeout during page navigation")
            return False
        except Exception as e:
            logger.error(f"❌ Error during navigation: {e}")
            return False
    
    def wait_for_network_activity(self, driver: webdriver.Chrome, timeout: int = 10) -> bool:
        """
        Wait for network activity to settle (for token extraction)
        
        Args:
            driver: Chrome driver instance
            timeout: Maximum time to wait
            
        Returns:
            bool: True if network activity detected
        """
        try:
            logger.info("📡 Waiting for network activity...")
            
            # Wait a bit for initial network requests
            time.sleep(3)
            
            # Try to trigger some network activity by interacting with the page
            try:
                # Scroll down to trigger lazy loading
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                # Scroll back up
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
                # Try to find and click any refresh or load button
                refresh_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Refresh') or contains(text(), 'Load') or contains(text(), 'Actualizar') or contains(text(), 'Cargar')]")
                if refresh_buttons:
                    logger.info("🔄 Found refresh button, clicking...")
                    refresh_buttons[0].click()
                    time.sleep(2)
                
            except Exception as e:
                logger.debug(f"No interactive elements found: {e}")
            
            # Additional wait for network requests to complete
            time.sleep(timeout)
            
            logger.info("✅ Network activity wait completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error waiting for network activity: {e}")
            return False
    
    def take_screenshot(self, driver: webdriver.Chrome, filename: str = "debug_screenshot.png") -> bool:
        """
        Take a screenshot for debugging purposes
        
        Args:
            driver: Chrome driver instance
            filename: Screenshot filename
            
        Returns:
            bool: True if screenshot taken successfully
        """
        try:
            screenshot_path = os.path.join("dashboard_analyzer", filename)
            driver.save_screenshot(screenshot_path)
            logger.info(f"📸 Screenshot saved: {screenshot_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to take screenshot: {e}")
            return False
    
    def get_page_info(self, driver: webdriver.Chrome) -> Dict[str, Any]:
        """
        Get information about the current page for debugging
        
        Args:
            driver: Chrome driver instance
            
        Returns:
            dict: Page information
        """
        try:
            return {
                'url': driver.current_url,
                'title': driver.title,
                'ready_state': driver.execute_script("return document.readyState"),
                'user_agent': driver.execute_script("return navigator.userAgent"),
                'cookies_count': len(driver.get_cookies()),
                'local_storage_keys': driver.execute_script("return Object.keys(localStorage)"),
                'session_storage_keys': driver.execute_script("return Object.keys(sessionStorage)")
            }
        except Exception as e:
            logger.error(f"❌ Error getting page info: {e}")
            return {}
    
    def cleanup(self, driver: webdriver.Chrome) -> None:
        """
        Clean up the browser instance
        
        Args:
            driver: Chrome driver instance to cleanup
        """
        try:
            if driver:
                logger.info("🧹 Cleaning up Chrome browser...")
                driver.quit()
                logger.info("✅ Browser cleanup completed")
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
    
    def test_browser_setup(self) -> bool:
        """
        Test if the browser can be started and basic operations work
        
        Returns:
            bool: True if test successful
        """
        try:
            logger.info("🧪 Testing browser setup...")
            
            driver = self.start_browser()
            if not driver:
                return False
            
            # Test basic navigation
            driver.get("https://www.google.com")
            time.sleep(2)
            
            # Check if we can access the page
            title = driver.title
            logger.info(f"✅ Test navigation successful, page title: {title}")
            
            self.cleanup(driver)
            return True
            
        except Exception as e:
            logger.error(f"❌ Browser setup test failed: {e}")
            return False
