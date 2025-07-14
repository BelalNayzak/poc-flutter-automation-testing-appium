import pytest
import time
from pom_pages.login_page_pom import LoginPagePom
from conftest import Config


class TestLogin:
    """Test cases for login functionality using the LoginPagePom."""
    
    def test_login_screen_elements_displayed(self, login_page_pom, platform):
        """Test that all login screen elements are displayed on the login page."""
        time.sleep(3)  # Wait for the app to fully load
        assert login_page_pom.is_login_screen_displayed(), "Login screen should be displayed"
        print("✅ Login screen elements are displayed correctly")

    def test_empty_email_validation(self, login_page_pom, platform):
        """Test validation for empty email field (should show error)."""
        time.sleep(2)  # wait for app to load
        login_page_pom.enter_phone_number(Config.VALID_PHONE)  # enter only valid phone & pass without enter email
        login_page_pom.enter_password(Config.VALID_PASSWORD)  # enter only valid phone & pass without enter email
        login_page_pom.click_login_button()  # Attempt login
        login_page_pom.wait_for_loading_to_complete()  # Wait for loading
        error_message = login_page_pom.get_validation_error(key='email_validation_error')  # Get error
        assert error_message is not None, "Validation error should be displayed for empty email"
        assert "Please enter your email" in error_message, f"Expected email validation message, got: {error_message}"
        print(f"✅ Empty email validation test passed: {error_message}")

    def test_empty_phone_validation(self, login_page_pom, platform):
        """Test validation for empty phone field (should show error)."""
        time.sleep(2)  # Wait for app to load
        login_page_pom.enter_password(Config.VALID_PASSWORD)  # Enter only password
        login_page_pom.click_login_button()  # Attempt login
        login_page_pom.wait_for_loading_to_complete()  # Wait for loading
        error_message = login_page_pom.get_validation_error(key='phone_validation_error')  # Get error
        assert error_message is not None, "Validation error should be displayed for empty phone"
        assert "Please enter your phone number" in error_message, f"Expected phone validation message, got: {error_message}"
        print(f"✅ Empty phone validation test passed: {error_message}")
    
    def test_empty_password_validation(self, login_page_pom, platform):
        """Test validation for empty password field (should show error)."""
        time.sleep(2)  # Wait for app to load
        login_page_pom.enter_phone_number(Config.VALID_PHONE)  # Enter only phone
        login_page_pom.click_login_button()  # Attempt login
        login_page_pom.wait_for_loading_to_complete()  # Wait for loading
        error_message = login_page_pom.get_validation_error(key='password_validation_error')  # Get error
        assert error_message is not None, "Validation error should be displayed"
        assert "Please enter" in error_message, f"Expected validation message, got: {error_message}"
        print(f"✅ Empty password validation test passed: {error_message}")
    
    def test_invalid_email_validation(self, login_page_pom, platform):
        """Test validation for invalid email (should show error)."""
        time.sleep(2)  # Wait for app to load
        login_page_pom.enter_phone_number(Config.VALID_PHONE)  # Enter valid phone
        login_page_pom.enter_password(Config.VALID_PASSWORD)  # Enter valid password
        login_page_pom.enter_email(Config.INVALID_EMAIL)  # Enter invalid email
        login_page_pom.click_login_button()  # Attempt login
        login_page_pom.wait_for_loading_to_complete()  # Wait for loading
        error_message = login_page_pom.get_validation_error(key='email_validation_error')  # Get error
        assert error_message is not None, "Validation error should be displayed for invalid email"
        assert "Invalid email" in error_message, f"Expected email validation message, got: {error_message}"
        print(f"✅ Invalid email validation test passed: {error_message}")

    def test_invalid_phone_validation(self, login_page_pom, platform):
        """Test validation for invalid phone number (should show error)."""
        time.sleep(2)  # Wait for app to load
        login_page_pom.enter_phone_number(Config.INVALID_PHONE)  # Enter invalid phone
        login_page_pom.enter_password(Config.VALID_PASSWORD)  # Enter valid password
        login_page_pom.click_login_button()  # Attempt login
        login_page_pom.wait_for_loading_to_complete()  # Wait for loading
        error_message = login_page_pom.get_validation_error(key='phone_validation_error')  # Get error
        assert error_message is not None, "Validation error should be displayed for invalid phone"
        assert "Phone number must be at least 10 digits" in error_message, f"Expected phone validation message, got: {error_message}"
        print(f"✅ Invalid phone validation test passed: {error_message}")
    
    def test_invalid_password_validation(self, login_page_pom, platform):
        """Test validation for invalid password (should show error)."""
        time.sleep(2)  # Wait for app to load
        login_page_pom.enter_phone_number(Config.VALID_PHONE)  # Enter valid phone
        login_page_pom.enter_password(Config.INVALID_PASSWORD)  # Enter invalid password
        login_page_pom.click_login_button()  # Attempt login
        login_page_pom.wait_for_loading_to_complete()  # Wait for loading
        error_message = login_page_pom.get_validation_error(key='password_validation_error')  # Get error
        assert error_message is not None, "Validation error should be displayed for invalid password"
        assert "Password must be at least 6 characters" in error_message, f"Expected validation message, got: {error_message}"
        print(f"✅ Invalid password validation test passed: {error_message}")

    def test_successful_login(self, login_page_pom, platform):
        """Test successful login with valid credentials (fields should be populated)."""
        time.sleep(2)  # Wait for app to load
        assert login_page_pom.is_login_screen_displayed(), "Login screen should be displayed"
        login_page_pom.perform_login(Config.VALID_EMAIL, Config.VALID_PHONE, Config.VALID_PASSWORD)  # Perform login
        email_text = login_page_pom.get_email_field_text()  # Get phone field value
        phone_text = login_page_pom.get_phone_field_text()  # Get phone field value
        password_text = login_page_pom.get_password_field_text()  # Get phone field value
        assert Config.VALID_EMAIL in email_text, f"Phone field should contain entered value: {email_text}"
        assert Config.VALID_PHONE in phone_text, f"Phone field should contain entered value: {phone_text}"
        assert Config.VALID_PASSWORD in password_text, f"Phone field should contain entered value: {password_text}"
        print(f"✅ Successful login test passed - fields populated correctly")
    
