#!/usr/bin/env python3
"""
Test runner script for Appium tests
"""

import subprocess
import sys
import os
import argparse
import time

def check_appium_server():
    """Check if Appium server is running"""
    try:
        import requests
        response = requests.get("http://localhost:4723/status", timeout=5)
        if response.status_code == 200:
            print("✅ Appium server is running")
            return True
    except:
        pass
    
    print("❌ Appium server is not running")
    print("Please start Appium server with: appium")
    return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import appium
        import selenium
        import pytest
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def run_flutter_app():
    """Start Flutter app"""
    print("Starting Flutter app...")
    os.chdir("..")  # Go to project root
    subprocess.run(["flutter", "run"], check=False)

def run_tests(platform="android", test_file=None, verbose=False):
    """Run the tests"""
    if not check_dependencies():
        return False
    
    if not check_appium_server():
        return False
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    if test_file:
        cmd.append(test_file)
    else:
        cmd.append("test_login.py")
    
    if verbose:
        cmd.extend(["-v", "-s"])
    
    cmd.extend([
        f"--platform={platform}",
        "--html=reports/report.html",
        "--self-contained-html"
    ])
    
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    
    print(f"Running tests on {platform} platform...")
    print(f"Command: {' '.join(cmd)}")
    
    # Run tests
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Run Appium tests for Login App")
    parser.add_argument("--platform", choices=["android", "ios"], default="android",
                       help="Platform to test (default: android)")
    parser.add_argument("--test", help="Specific test file to run")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--start-app", action="store_true",
                       help="Start Flutter app before running tests")
    
    args = parser.parse_args()
    
    if args.start_app:
        print("Starting Flutter app in separate process...")
        print("Make sure to run the app and then run tests separately")
        run_flutter_app()
        return
    
    success = run_tests(args.platform, args.test, args.verbose)
    
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
