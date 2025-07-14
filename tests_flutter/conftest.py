import pytest
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.options.common import AppiumOptions
from selenium.common.exceptions import WebDriverException


class Config:
    """Configuration class for test settings, device info, and test data."""

    # Appium server URL
    APPIUM_SERVER_URL = "http://localhost:4723"

    # Appium Flutter Driver name (used for automationName capability)
    FLUTTER_DRIVER_NAME = "Flutter"    # Equivalent to XCUItest for native iOS and UIAutomator2 for native Android
    
    # Android configuration
    ANDROID_PLATFORM_NAME = "Android"  # Platform name for Android
    ANDROID_DEVICE_NAME = "emulator-5554"  # Android device name (change to your device name)
    ANDROID_APP_PACKAGE = "com.example.appium_testing_poc"  # Android app package name
    ANDROID_APK_PATH = "/Users/mazeed/StudioProjects/appium_testing_poc/build/app/outputs/flutter-apk/app-debug.apk"  # Path to built APK
    ANDROID_APP_ACTIVITY = ".MainActivity"  # Main activity for the app

    # iOS configuration  
    IOS_PLATFORM_NAME = "iOS"  # Platform name for iOS
    IOS_DEVICE_NAME = "iPhone 16 Plus" # iOS device/simulator name
    # IOS_BUNDLE_ID = "com.example.appiumTestingPoc"  # (Unused, for reference)
    IOS_APP_PATH = "/Users/mazeed/StudioProjects/appium_testing_poc/build/ios/iphonesimulator/Runner.app"  # Path to built iOS app

    # Test data for login
    VALID_PHONE = "1234567890"
    VALID_PASSWORD = "password123"
    INVALID_PHONE = "123"
    INVALID_PASSWORD = "123"

    # Retry configuration for driver setup
    MAX_RETRIES = 20
    RETRY_DELAY = 5


# @pytest.fixture(scope="session") # uncomment if need to disable app reset
@pytest.fixture(scope="function")
def driver_android(request):
    """Fixture to set up and yield an Appium driver for Android tests."""
    options = AppiumOptions()
    options.set_capability("platformName", Config.ANDROID_PLATFORM_NAME)
    options.set_capability("deviceName", Config.ANDROID_DEVICE_NAME)
    options.set_capability("automationName", Config.FLUTTER_DRIVER_NAME)
    options.set_capability("app", Config.ANDROID_APK_PATH)
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("fastReset", True)
    options.set_capability("skipUninstall", True)
    # options.set_capability("noReset", True) # Uncomment to disable app reset between tests

    attempt = 0  # Track retry attempts
    driver = None  # Appium driver instance
    while attempt < Config.MAX_RETRIES:
        try:
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            driver.implicitly_wait(10)  # Wait for app to load
            time.sleep(3)  # Additional wait for Flutter app to initialize
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


# @pytest.fixture(scope="session") # uncomment if need to disable app reset
@pytest.fixture(scope="function")
def driver_ios():
    """Fixture to set up and yield an Appium driver for iOS tests."""
    options = AppiumOptions()
    options.set_capability("platformName", Config.IOS_PLATFORM_NAME)
    options.set_capability("deviceName", Config.IOS_DEVICE_NAME)
    options.set_capability("automationName", Config.FLUTTER_DRIVER_NAME)  # Use Flutter for Flutter apps
    options.set_capability("app", Config.IOS_APP_PATH)
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("fastReset", True)
    options.set_capability("skipUninstall", True)
    # options.set_capability("noReset", True) # Uncomment to disable app reset between tests

    attempt = 0  # Track retry attempts
    driver = None  # Appium driver instance
    while attempt < Config.MAX_RETRIES:
        try:
            driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
            driver.implicitly_wait(10)  # Wait for app to load
            time.sleep(3)  # Additional wait for Flutter app to initialize
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
def login_page(request, platform):
    """Fixture to provide a LoginPagePom instance for the current platform."""
    if platform == "android":
        driver = request.getfixturevalue('driver_android')
    else:
        driver = request.getfixturevalue('driver_ios')
    from pom_pages.login_page_pom import LoginPagePom
    return LoginPagePom(driver)


def pytest_addoption(parser):
    """Pytest hook to add custom command-line options (e.g., --platform)."""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Platform to test: android or ios"
    )


@pytest.fixture
def platform(request):
    """Fixture to get the selected platform from the command line (android or ios)."""
    return request.config.getoption("--platform")
