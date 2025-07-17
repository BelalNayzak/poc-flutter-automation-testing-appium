# Login App POC with Appium Testing

---

🚀 **Documentation & Step-by-Step Guide** 🚀

> **🟢 I've made a clear step-by-step guide for this project (Flutter + Appium + Automation Testing) and hosted it in the below link for a complete setup, troubleshooting, and cross-platform (Android & iOS) test instructions:**
> 
> **https://belalnayzak.github.io/poc-flutter-automation-testing-appium/**

---

> **📊 Gap Analysis: Flutter Test Suite vs. Appium**
>
> For a detailed comparison and gap analysis between Flutter's built-in test suite and Appium-based testing (strengths, limitations, and when to use each), see:
>
> **https://belalnayzak.github.io/gap-analysis-flutter-vs-appium/**

---

This is a Flutter application with a simple login screen that includes automated testing using Appium and Python.

## App Features

- Simple login screen with email, phone number, and password fields
- Form validation for empty fields and minimum length requirements
- Loading indicator during login process
- Success message display after login

## Project Structure

```
appium_testing_poc/
  ├── lib/
  │   └── main.dart
  ├── test/
  │   ├── flutter/
  │   │   ├── widget_test.dart
  │   │   └── login_screen_test.dart
  │   └── appium/
  │       ├── docs/...
  │       ├── reports/...
  │       ├── venv/...
  │       ├── pom_pages/
  │       │   └── login_page_pom.py
  │       ├── conftest.py
  │       ├── test_login.py
  │       ├── run_tests.py
  │       └── requirements.txt
  └── README.md
```

## Prerequisites

### Flutter Setup
- Flutter SDK (latest stable version)
- Android Studio / Xcode for emulators
- Android emulator or iOS simulator running

### Python Setup
- Python 3.8 or higher
- pip package manager

### Appium Setup
- Node.js and npm
- Appium server
- Android SDK (for Android testing)
- Xcode (for iOS testing on macOS)

## Installation

### 1. Install Appium

```bash
# Install Appium globally
npm install -g appium

# Install Appium drivers
appium driver install uiautomator2  # For Android
appium driver install xcuitest      # For iOS
```

### 2. Install Python Dependencies

```bash
cd test/appium
pip install -r requirements.txt
```

### 3. Verify Flutter Setup

```bash
flutter doctor
```

## Running the App

### Start the Flutter App

```bash
# From project root
flutter run
```

This will start the app on your connected device/emulator.

## Running Tests

### 1. Start Appium Server

```bash
appium
```

The server should start on `http://localhost:4723`

### 2. Update Configuration

Edit `test/appium/conftest.py` to match your device configuration:

For Android:
```python
ANDROID_DEVICE_NAME = "your-device-name"  # e.g., "emulator-5554"
ANDROID_APP_PACKAGE = "com.example.appium_testing_poc"
```

For iOS:
```python
IOS_DEVICE_NAME = "your-simulator-name"  # e.g., "iPhone 15"
IOS_BUNDLE_ID = "com.example.appiumTestingPoc"
```

### 3. Run Tests

#### Using the test runner (recommended):

```bash
cd test/appium

# Run all tests on Android
python run_tests.py --platform android --verbose

# Run all tests on iOS  
python run_tests.py --platform ios --verbose

# Run specific test file
python run_tests.py --test test_login.py --verbose
```

#### Using pytest directly:

```bash
cd test/appium

# Run all tests
pytest test_login.py -v -s --platform=android

# Run specific test
pytest test_login.py::TestLogin::test_successful_login -v -s --platform=android
```

## Test Cases

The test suite includes the following test cases:

1. **test_login_screen_elements_displayed** - Verifies all UI elements (welcome text, email, phone, password fields, login button) are visible
2. **test_successful_login** - Tests login with valid credentials (email, phone, password)
3. **test_empty_email_validation** - Tests validation for empty email field
4. **test_invalid_email_validation** - Tests validation for invalid email format
5. **test_empty_phone_validation** - Tests validation for empty phone field
6. **test_invalid_phone_validation** - Tests validation for invalid phone number
7. **test_empty_password_validation** - Tests validation for empty password field
8. **test_invalid_password_validation** - Tests validation for invalid password
9. **test_field_input_functionality** - Tests input field functionality for all fields
10. **test_multiple_login_attempts** - Tests multiple login attempts and error resets

## Test Data

Default test data is configured in `conftest.py`:

```python
VALID_EMAIL = "test@example.com"
INVALID_EMAIL = "invalid-email"
VALID_PHONE = "1234567890"
INVALID_PHONE = "123"
VALID_PASSWORD = "password123"
INVALID_PASSWORD = "123"
```

## Troubleshooting

### Common Issues

1. **Appium server not running**
   ```bash
   appium
   ```

2. **Device not found**
   - Check device name in conftest.py
   - Ensure emulator/simulator is running
   - For Android: `adb devices`
   - For iOS: `xcrun simctl list`

3. **App not found**
   - Make sure Flutter app is running
   - Check package name/bundle ID in conftest.py

4. **Element not found**
   - Elements may have different locators on different platforms
   - Use Appium Inspector to find correct element locators

### Getting Device Information

#### Android:
```bash
# List connected devices
adb devices

# Get package name of running app
adb shell dumpsys window windows | grep -E 'mCurrentFocus'
```

#### iOS:
```bash
# List simulators
xcrun simctl list

# Get bundle ID
xcrun simctl list apps booted
```

## Reports

Test reports are generated in `test/appium/reports/report.html` after running tests.

## Extending Tests

To add new test cases:

1. Add new test methods to `test_login.py`
2. Use the `LoginPagePom` class methods for interaction
3. Follow the existing test pattern with assertions
4. Add new page objects if testing additional screens

## Key Features for Testing

The Flutter app includes special keys for testing:

- `Key('welcome_text')` - Welcome text
- `Key('email_field')` - Email input field
- `Key('email_validation_error')` - Email validation error text
- `Key('phone_field')` - Phone input field
- `Key('phone_validation_error')` - Phone validation error text
- `Key('password_field')` - Password input field
- `Key('password_validation_error')` - Password validation error text
- `Key('login_button')` - Login button
- `Key('loading_indicator')` - Loading spinner
- `Key('login_success_snackbar')` - Success message

These keys make it easier to locate elements consistently across platforms.
