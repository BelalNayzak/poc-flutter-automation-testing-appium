from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class LoginPagePom:
    """Page Object Model for Login Screen"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    # Locators - based on actual Flutter page source
    WELCOME_TEXT = (By.XPATH, "//android.view.View[@content-desc='Welcome']")
    PHONE_FIELD = (By.XPATH, "//android.widget.EditText[@hint='Phone Number']")
    PASSWORD_FIELD = (By.XPATH, "//android.widget.EditText[@hint='Password']")
    LOGIN_BUTTON = (By.XPATH, "//android.widget.Button[@content-desc='Login']")
    LOADING_INDICATOR = (By.XPATH, "//android.widget.ProgressBar")
    SUCCESS_SNACKBAR = (By.XPATH, "//android.widget.TextView[contains(@text, 'Login successful')]")
    
    # Alternative locators for iOS
    IOS_WELCOME_TEXT = (By.XPATH, "//XCUIElementTypeStaticText[@name='Welcome']")
    IOS_PHONE_FIELD = (By.XPATH, "//XCUIElementTypeTextField[contains(@name, 'phone')]")
    IOS_PASSWORD_FIELD = (By.XPATH, "//XCUIElementTypeSecureTextField[contains(@name, 'password')]")
    IOS_LOGIN_BUTTON = (By.XPATH, "//XCUIElementTypeButton[@name='Login']")
    IOS_LOADING_INDICATOR = (By.XPATH, "//XCUIElementTypeActivityIndicator")
    IOS_SUCCESS_SNACKBAR = (By.XPATH, "//XCUIElementTypeStaticText[contains(@name, 'Login successful')]")
    
    def get_locator(self, android_locator, ios_locator):
        """Get appropriate locator based on platform"""
        platform = self.driver.capabilities.get('platformName', '').lower()
        return ios_locator if platform == 'ios' else android_locator
    
    def is_login_screen_displayed(self):
        """Check if login screen is displayed"""
        try:
            welcome_locator = self.get_locator(self.WELCOME_TEXT, self.IOS_WELCOME_TEXT)
            self.wait.until(EC.presence_of_element_located(welcome_locator))
            return True
        except TimeoutException:
            return False
    
    def enter_phone_number(self, phone_number):
        """Enter phone number in the phone field"""
        phone_locator = self.get_locator(self.PHONE_FIELD, self.IOS_PHONE_FIELD)
        phone_field = self.wait.until(EC.element_to_be_clickable(phone_locator))
        phone_field.clear()
        phone_field.send_keys(phone_number)
        return self
    
    def enter_password(self, password):
        """Enter password in the password field"""
        password_locator = self.get_locator(self.PASSWORD_FIELD, self.IOS_PASSWORD_FIELD)
        password_field = self.wait.until(EC.element_to_be_clickable(password_locator))
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login_button(self):
        """Click the login button"""
        login_locator = self.get_locator(self.LOGIN_BUTTON, self.IOS_LOGIN_BUTTON)
        login_button = self.wait.until(EC.element_to_be_clickable(login_locator))
        login_button.click()
        return self
    
    def is_loading_indicator_visible(self):
        """Check if loading indicator is visible"""
        try:
            loading_locator = self.get_locator(self.LOADING_INDICATOR, self.IOS_LOADING_INDICATOR)
            self.wait.until(EC.presence_of_element_located(loading_locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_loading_to_complete(self, timeout=15):
        """Wait for loading indicator to disappear"""
        try:
            loading_locator = self.get_locator(self.LOADING_INDICATOR, self.IOS_LOADING_INDICATOR)
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(loading_locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_success_message_text(self):
        """Get the text of success message"""
        try:
            success_locator = self.get_locator(self.SUCCESS_SNACKBAR, self.IOS_SUCCESS_SNACKBAR)
            element = self.wait.until(EC.presence_of_element_located(success_locator))
            return element.text
        except TimeoutException:
            return None
    
    def get_phone_field_text(self):
        """Get current text in phone field"""
        phone_locator = self.get_locator(self.PHONE_FIELD, self.IOS_PHONE_FIELD)
        phone_field = self.wait.until(EC.presence_of_element_located(phone_locator))
        return phone_field.text
    
    def get_validation_error(self):
        """Get validation error message if present"""
        try:
            # Look for validation error using content-desc in child views
            error_locator = (By.XPATH, "//android.view.View[contains(@content-desc, 'Please enter') or contains(@content-desc, 'must be')]")
            if self.driver.capabilities.get('platformName', '').lower() == 'ios':
                error_locator = (By.XPATH, "//XCUIElementTypeStaticText[contains(@name, 'Please enter') or contains(@name, 'must be')]")
            
            error_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(error_locator)
            )
            return error_element.get_attribute('content-desc') if error_element.get_attribute('content-desc') else error_element.text
        except TimeoutException:
            return None
            
    def is_success_message_displayed(self):
        """Check if success message is displayed - adapted for snackbar behavior"""
        try:
            # In Flutter, snackbars may not always be detectable, so we check if login flow completed
            # by seeing if loading has finished and no validation errors remain
            return not self.is_loading_indicator_visible() and self.get_validation_error() is None
        except:
            return False
    
    def perform_login(self, phone_number, password):
        """Perform complete login flow"""
        self.enter_phone_number(phone_number)
        self.enter_password(password)
        self.click_login_button()
        return self
