from appium_flutter_finder.flutter_finder import FlutterFinder, FlutterElement
from selenium.common.exceptions import NoSuchElementException
import time


class LoginPage:
    """Page Object Model for Login Screen (Flutter selectors)"""
    
    def __init__(self, driver):
        self.driver = driver
        self.finder = FlutterFinder()
        
    def is_login_screen_displayed(self):
        try:
            welcome = FlutterElement(self.driver, self.finder.by_value_key('welcome_text'))
            return welcome is not None
        except Exception:
            return False

    def enter_phone_number(self, phone_number):
        phone_field = FlutterElement(self.driver, self.finder.by_value_key('phone_field'))
        phone_field.clear()
        phone_field.send_keys(phone_number)
        return self
    
    def enter_password(self, password):
        password_field = FlutterElement(self.driver, self.finder.by_value_key('password_field'))
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login_button(self):
        login_button = FlutterElement(self.driver, self.finder.by_value_key('login_button'))
        login_button.click()
        return self
    
    def is_loading_indicator_visible(self):
        try:
            loading = FlutterElement(self.driver, self.finder.by_value_key('loading_indicator'))
            return loading.is_displayed()
        except Exception:
            return False
    
    def wait_for_loading_to_complete(self, timeout=10):
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
        # On navigation, check for SuccessScreen text
        try:
            success = FlutterElement(self.driver, self.finder.by_value_key('success_text'))
            return success.text
        except Exception:
            return None
    
    def get_phone_field_text(self):
        phone_field = FlutterElement(self.driver, self.finder.by_value_key('phone_field'))
        return phone_field.text
    
    def get_validation_error(self, key, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                error_widget = FlutterElement(self.driver, self.finder.by_value_key(key))
                return error_widget.text
            except NoSuchElementException:
                pass  # Element not found yet, keep trying
            except Exception:
                pass # Catch other exceptions during element interaction
            time.sleep(0.2) # Small delay to avoid busy-waiting
        return None # Timeout, element never became visible or found

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
