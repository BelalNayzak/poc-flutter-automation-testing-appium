#!/bin/bash

# Exit on any error
set -e

# 1. Kill all Dart/Flutter and Appium processes
pkill -f dart || true
pkill -f appium || true

# 2. Start Flutter app in debug mode (background)
echo "[INFO] Starting Flutter app in debug mode..."
flutter run --debug --disable-service-auth-codes > flutter_run.log 2>&1 &
FLUTTER_PID=$!

# 3. Wait for Dart VM Service port to appear in flutter_run.log
echo "[INFO] Waiting for Dart VM Service port..."
PORT=""
for i in {1..30}; do
  PORT=$(grep -oE 'http://127.0.0.1:[0-9]+' flutter_run.log | tail -1 | grep -oE '[0-9]+$' || true)
  if [[ ! -z "$PORT" ]]; then
    break
  fi
  sleep 1
done
if [[ -z "$PORT" ]]; then
  echo "[ERROR] Dart VM Service port not found. Check flutter_run.log."
  kill $FLUTTER_PID
  exit 1
fi
echo "[INFO] Dart VM Service port is $PORT"

# 4. Forward the port
adb forward --remove tcp:$PORT || true
adb forward tcp:$PORT tcp:$PORT || true

# 5. Start Appium (background)
echo "[INFO] Starting Appium server..."
appium > appium.log 2>&1 &
APPIUM_PID=$!
sleep 5

# 6. Run Python tests
source tests_flutter/venv/bin/activate
cd tests_flutter
python run_tests.py
TEST_EXIT_CODE=$?
cd ..

# 7. Cleanup
# kill $APPIUM_PID || true
# kill $FLUTTER_PID || true

echo "[INFO] All done. Test exit code: $TEST_EXIT_CODE"
exit $TEST_EXIT_CODE 