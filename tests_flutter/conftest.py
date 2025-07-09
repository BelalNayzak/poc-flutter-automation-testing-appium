import pytest
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.options.common import AppiumOptions
from selenium.common.exceptions import WebDriverException


class Config:
    # Android configuration
    ANDROID_PLATFORM_NAME = "Android"
    ANDROID_DEVICE_NAME = "emulator-5554"  # Change this to your device name
    ANDROID_APP_PACKAGE = "com.example.appium_testing_poc"
    ANDROID_APP_ACTIVITY = ".MainActivity"
    ANDROID_APK_PATH = "/Users/mazeed/StudioProjects/appium_testing_poc/build/app/outputs/flutter-apk/app-debug.apk"

    # iOS configuration  
    IOS_PLATFORM_NAME = "iOS"
    IOS_DEVICE_NAME = "iPhone 15"  # Change this to your simulator name
    IOS_BUNDLE_ID = "com.example.appiumTestingPoc"
    
    # Appium server
    APPIUM_SERVER_URL = "http://localhost:4723"
    
    # Test data
    VALID_PHONE = "1234567890"
    VALID_PASSWORD = "password123"
    INVALID_PHONE = "123"
    INVALID_PASSWORD = "123"

    # Retry configuration
    MAX_RETRIES = 20
    RETRY_DELAY = 5


# @pytest.fixture(scope="function")
@pytest.fixture(scope="session")
def driver_android(request):
    options = AppiumOptions()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", Config.ANDROID_DEVICE_NAME)
    options.set_capability("automationName", "Flutter")
    options.set_capability("app", Config.ANDROID_APK_PATH)
    options.set_capability("autoGrantPermissions", True)
    # options.set_capability("noReset", True) # uncomment if need to disable app reset

    attempt = 0
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

    driver.quit()


@pytest.fixture(scope="session")
def driver_ios():
    """Setup iOS driver for testing"""
    options = XCUITestOptions()
    options.platform_name = Config.IOS_PLATFORM_NAME
    options.device_name = Config.IOS_DEVICE_NAME
    options.bundle_id = Config.IOS_BUNDLE_ID
    options.automation_name = "Flutter"
    options.no_reset = True

    driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(30)

    yield driver

    driver.quit()


@pytest.fixture
def login_page(request):
    """Fixture to provide login page object"""
    if hasattr(request, 'param'):
        platform = request.param
    else:
        platform = "android"  # default

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
