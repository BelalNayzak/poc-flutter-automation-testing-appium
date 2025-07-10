from appium_flutter_finder.flutter_finder import FlutterFinder, FlutterElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


class LoginPage:
    """Page Object Model for Login Screen (Flutter selectors)"""
    
    def __init__(self, driver):
        self.driver = driver
        self.finder = FlutterFinder()
        
    def _wait_for_element_to_be_interactable(self, locator, timeout=20):
        try:
            # Use the supported Appium Flutter Driver command
            self.driver.execute_script('flutter:waitFor', locator, timeout * 1000)
            element = FlutterElement(self.driver, locator)
            return element
        except Exception as e:
            raise TimeoutException(f"Element with locator {locator} not interactable after {timeout} seconds: {e}")

    def is_login_screen_displayed(self):
        try:
            self.driver.execute_script('flutter:waitFor', self.finder.by_value_key('welcome_text'), 5000)
            return True
        except Exception:
            return False

    def enter_phone_number(self, phone_number):
        phone_field = self._wait_for_element_to_be_interactable(self.finder.by_value_key('phone_field'))
        phone_field.clear()
        phone_field.send_keys(phone_number)
        return self
    
    def enter_password(self, password):
        password_field = self._wait_for_element_to_be_interactable(self.finder.by_value_key('password_field'))
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login_button(self):
        login_button = self._wait_for_element_to_be_interactable(self.finder.by_value_key('login_button'))
        login_button.click()
        return self
    
    def is_loading_indicator_visible(self):
        try:
            self.driver.execute_script('flutter:waitFor', self.finder.by_value_key('loading_indicator'), 1000)
            return True
        except Exception:
            return False
    
    def wait_for_loading_to_complete(self, timeout=20):
        start_time = time.time()
        # First, wait for the loading indicator to appear
        appeared = False
        while time.time() - start_time < timeout:
            if self.is_loading_indicator_visible():
                appeared = True
                break
            time.sleep(0.5)
        
        # Then, wait for the loading indicator to disappear if it appeared
        if appeared:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if not self.is_loading_indicator_visible():
                    return True
                time.sleep(0.5)
            return False # Timeout: loading indicator did not disappear
        else:
            # If loading indicator never appeared, assume loading is complete.
            return True
    
    def get_success_message_text(self):
        try:
            self.driver.execute_script('flutter:waitFor', self.finder.by_value_key('success_text'), 2000)
            success = FlutterElement(self.driver, self.finder.by_value_key('success_text'))
            return success.text
        except Exception:
            return None
    
    def get_phone_field_text(self):
        phone_field = FlutterElement(self.driver, self.finder.by_value_key('phone_field'))
        return phone_field.text
    
    def get_validation_error(self, key, timeout=20):
        try:
            self.driver.execute_script('flutter:waitFor', self.finder.by_value_key(key), timeout * 1000)
            error_widget = FlutterElement(self.driver, self.finder.by_value_key(key))
            return error_widget.text
        except Exception:
            return None

    def get_phone_validation_error(self):
        return self.get_validation_error(key='phone_validation_error')
    
    def get_password_validation_error(self):
        return self.get_validation_error(key='password_validation_error')
    
    def is_success_message_displayed(self):
        return self.get_success_message_text() is not None
    
    def perform_login(self, phone_number, password):
        self.enter_phone_number(phone_number)
        self.enter_password(password)
        self.click_login_button()
        self.wait_for_loading_to_complete()
        return self
