from appium_flutter_finder.flutter_finder import FlutterFinder, FlutterElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class LoginPage:
    """Page Object Model for Login Screen (Flutter selectors)"""
    
    def __init__(self, driver):
        self.driver = driver
        self.finder = FlutterFinder()
        self.wait = WebDriverWait(driver, 10)
        
    def is_login_screen_displayed(self):
        try:
            welcome = FlutterElement(self.driver, self.finder.by_value_key('welcome_text'))
            return welcome is not None
        except Exception:
            return False





#
#
#
#
#
#     # from Zubair
#     # from Zubair
#     # from Zubair
#     def click_certification_module(self):
#         element = self.finder.by_text("Certifications")
#         self.driver.execute_script("flutter:assertTappable", element)
#         self.driver.execute_script("flutter:clickElement", element)
#
#     self.driver.execute_script("flutter:enterText", feedback_text)
#
#
#     def click_backtolearnings(self):
#         element = self.finder.by_value_key("result_screen_back_to_learning_button")
#         self.driver.execute_script("flutter:waitFor", element, 3000)
#         self.driver.execute_script("flutter:clickElement", element)
#
#
#
#
#
#



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
            return loading is not None
        except Exception:
            return False
    
    def wait_for_loading_to_complete(self, timeout=15):
        end_time = time.time() + timeout
        while time.time() < end_time:
            if not self.is_loading_indicator_visible():
                return True
            time.sleep(0.5)
        return False
    
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
    
    def get_validation_error(self):
        # Return the text of the first widget with Key('validation_error'), or None if not found
        try:
            error_widget = FlutterElement(self.driver, self.finder.by_value_key('validation_error'))
            return error_widget.text
        except Exception:
            return None
    
    def is_success_message_displayed(self):
        return self.get_success_message_text() is not None
    
    def perform_login(self, phone_number, password):
        self.enter_phone_number(phone_number)
        self.enter_password(password)
        self.click_login_button()
        return self
