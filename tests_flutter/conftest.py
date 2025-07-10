import pytest
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.options.common import AppiumOptions
from selenium.common.exceptions import WebDriverException


class Config:

    # Appium server
    APPIUM_SERVER_URL = "http://localhost:4723"
    
    # Android configuration
    ANDROID_PLATFORM_NAME = "Android"
    ANDROID_DEVICE_NAME = "emulator-5554"  # Change this to your device name
    ANDROID_APP_PACKAGE = "com.example.appium_testing_poc"
    ANDROID_APK_PATH = "/Users/mazeed/StudioProjects/appium_testing_poc/build/app/outputs/flutter-apk/app-debug.apk"
    ANDROID_APP_ACTIVITY = ".MainActivity"

    # iOS configuration  
    IOS_PLATFORM_NAME = "iOS"
    IOS_DEVICE_NAME = "iPhone 16 Plus" # Changed back to device type name
    # IOS_BUNDLE_ID = "com.example.appiumTestingPoc"
    IOS_APP_PATH = "/Users/mazeed/StudioProjects/appium_testing_poc/build/ios/iphonesimulator/Runner.app"

    # Test data
    VALID_PHONE = "1234567890"
    VALID_PASSWORD = "password123"
    INVALID_PHONE = "123"
    INVALID_PASSWORD = "123"

    # Retry configuration
    MAX_RETRIES = 20
    RETRY_DELAY = 5


# @pytest.fixture(scope="session") # uncomment if need to disable app reset
@pytest.fixture(scope="function")
def driver_android(request):
    """Setup Android driver for testing"""

    options = AppiumOptions()
    options.set_capability("platformName", Config.ANDROID_PLATFORM_NAME)
    options.set_capability("deviceName", Config.ANDROID_DEVICE_NAME)
    options.set_capability("automationName", "Flutter")
    options.set_capability("app", Config.ANDROID_APK_PATH)
    options.set_capability("autoGrantPermissions", True)
    # options.set_capability("noReset", True) # uncomment if need to disable app reset

    attempt = 0
    driver = None # Initialize driver to None
    while attempt < Config.MAX_RETRIES:
        try:
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            yield driver
            break
        except WebDriverException as e:
            attempt += 1
            if attempt >= Config.MAX_RETRIES:
                raise
            time.sleep(Config.RETRY_DELAY)
        finally:
            if driver:
                driver.quit()


@pytest.fixture(scope="function")
def driver_ios():
    """Setup iOS driver for testing"""

    options = AppiumOptions()
    options.set_capability("platformName", Config.IOS_PLATFORM_NAME)
    options.set_capability("deviceName", Config.IOS_DEVICE_NAME)
    options.set_capability("automationName", "XCUITest") # You must use XCUITest for automationName on iOS not Flutter
    options.set_capability("app", Config.IOS_APP_PATH)
    options.set_capability("autoGrantPermissions", True)
    # options.set_capability("noReset", True) # uncomment if need to disable app reset

    attempt = 0
    driver = None # Initialize driver to None
    while attempt < Config.MAX_RETRIES:
        try:
            driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
            driver.implicitly_wait(30)
            yield driver
            break
        except WebDriverException as e:
            attempt += 1
            if attempt >= Config.MAX_RETRIES:
                raise
            time.sleep(Config.RETRY_DELAY)
        finally:
            if driver:
                driver.quit()


@pytest.fixture
def login_page(request, platform): # Inject the platform fixture here
    """Fixture to provide login page object"""
    # The 'platform' parameter now directly gets the value from the 'platform' fixture
    # if hasattr(request, 'param'): # This block is no longer needed
    #     current_platform = request.param
    # else:
    #     current_platform = "android"  # This default is now handled by the 'platform' fixture's default

    if platform == "android":
        driver = request.getfixturevalue('driver_android')
    else:
        driver = request.getfixturevalue('driver_ios')

    from pages.login_page import LoginPage
    return LoginPage(driver)


def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Platform to test: android or ios"
    )


@pytest.fixture
def platform(request):
    """Get platform from command line"""
    return request.config.getoption("--platform")
