import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
import os
import time


class Config:
    # Android configuration
    ANDROID_PLATFORM_NAME = "Android"
    ANDROID_DEVICE_NAME = "emulator-5554"  # Change this to your device name
    ANDROID_APP_PACKAGE = "com.example.appium_testing_poc"
    ANDROID_APP_ACTIVITY = ".MainActivity"
    
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


@pytest.fixture(scope="session")
def driver_android():
    """Setup Android driver for testing"""
    options = UiAutomator2Options()
    options.platform_name = Config.ANDROID_PLATFORM_NAME
    options.device_name = Config.ANDROID_DEVICE_NAME
    options.app_package = Config.ANDROID_APP_PACKAGE
    options.app_activity = Config.ANDROID_APP_ACTIVITY
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    
    driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="session")
def driver_ios():
    """Setup iOS driver for testing"""
    options = XCUITestOptions()
    options.platform_name = Config.IOS_PLATFORM_NAME
    options.device_name = Config.IOS_DEVICE_NAME
    options.bundle_id = Config.IOS_BUNDLE_ID
    options.automation_name = "XCUITest"
    options.no_reset = True
    
    driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(10)
    
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
    
    from pages.login_page import LoginPagePom
    return LoginPagePom(driver)


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
