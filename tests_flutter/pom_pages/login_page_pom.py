from appium_flutter_finder.flutter_finder import FlutterFinder
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time


class FlutterElement(WebElement):
    """Custom wrapper for Flutter elements compatible with Selenium/WebDriver."""
    
    def __init__(self, driver, element_id):
        """Initialize a FlutterElement with driver and element ID."""
        super(FlutterElement, self).__init__(driver, element_id)


class LoginPagePom:
    """Page Object Model for the Flutter Login Screen, using Flutter selectors. (acts as an actuator class)"""
    
    def __init__(self, driver):
        """Initialize with Appium driver and FlutterFinder instance."""
        self.driver = driver  # Appium driver instance
        self.finder = FlutterFinder()  # FlutterFinder for locating widgets
        
    def _find_element_with_retry(self, finder_method, max_retries=3):
        """Find an element with retry logic to handle stale references.
        Args:
            finder_method: The finder method to locate the element.
            max_retries: Number of retry attempts for stale elements.
        Returns:
            FlutterElement if found, else raises last exception.
        """
        for attempt in range(max_retries):
            try:
                element = FlutterElement(self.driver, finder_method)
                return element
            except (StaleElementReferenceException, Exception) as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(0.5)  # Wait before retry
        return None
        
    def is_login_screen_displayed(self):
        """Check if the login screen is displayed by finding the welcome text widget."""
        try:
            time.sleep(3)  # Wait for the app to load
            welcome = self._find_element_with_retry(self.finder.by_value_key('welcome_text'))
            return welcome is not None
        except Exception as e:
            print(f"Error checking login screen: {e}")
            return False

    def enter_email(self, email):
        """Enter the email into the email field"""
        try:
            email_field = self._find_element_with_retry(self.finder.by_value_key('email_field'))
            email_field.clear()
            email_field.send_keys(email)
        except Exception as e:
            print(f"Error entering email: {e}")
            raise
        return self

    def enter_phone_number(self, phone_number):
        """Enter a phone number into the phone field."""
        try:
            phone_field = self._find_element_with_retry(self.finder.by_value_key('phone_field'))
            phone_field.clear()
            phone_field.send_keys(phone_number)
        except Exception as e:
            print(f"Error entering phone number: {e}")
            raise
        return self
    
    def enter_password(self, password):
        """Enter a password into the password field."""
        try:
            password_field = self._find_element_with_retry(self.finder.by_value_key('password_field'))
            password_field.clear()
            password_field.send_keys(password)
        except Exception as e:
            print(f"Error entering password: {e}")
            raise
        return self
    
    def click_login_button(self):
        try:
            login_button = self._find_element_with_retry(self.finder.by_value_key('login_button'))
            login_button.click()
        except Exception as e:
            print(f"Error clicking login button: {e}")
            raise
        return self
    
    def is_loading_indicator_visible(self):
        try:
            loading = self._find_element_with_retry(self.finder.by_value_key('loading_indicator'))
            # Just check if element exists, don't call is_displayed()
            return loading is not None
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
            success = self._find_element_with_retry(self.finder.by_value_key('success_text'))
            return success.text
        except Exception:
            return None
    
    def get_email_field_text(self):
        try:
            email_field = self._find_element_with_retry(self.finder.by_value_key('email_field'))
            return email_field.text
        except Exception as e:
            print(f"Error getting email field text: {e}")
            return ""

    def get_phone_field_text(self):
        try:
            phone_field = self._find_element_with_retry(self.finder.by_value_key('phone_field'))
            return phone_field.text
        except Exception as e:
            print(f"Error getting phone field text: {e}")
            return ""

    def get_password_field_text(self):
        try:
            password_field = self._find_element_with_retry(self.finder.by_value_key('password_field'))
            return password_field.text
        except Exception as e:
            print(f"Error getting password field text: {e}")
            return ""

    def get_validation_error(self, key, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                error_widget = self._find_element_with_retry(self.finder.by_value_key(key))
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
    
    def perform_login(self, email, phone_number, password):
        self.enter_email(email)
        self.enter_phone_number(phone_number)
        self.enter_password(password)
        self.click_login_button()
        self.wait_for_loading_to_complete()
        return self
