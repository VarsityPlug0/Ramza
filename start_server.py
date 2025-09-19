#!/usr/bin/env python
import os
import sys
import subprocess
import time
import traceback

print("=== START SERVER SCRIPT ===")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Working directory: {os.getcwd()}")

# Run execution test
print("Running execution test...")
try:
    result = subprocess.run([sys.executable, 'test_execution.py'], 
                          capture_output=True, text=True, timeout=30)
    print(f"Execution test stdout: {result.stdout}")
    if result.stderr:
        print(f"Execution test stderr: {result.stderr}")
    print(f"Execution test return code: {result.returncode}")
except Exception as e:
    print(f"Error running execution test: {e}")

# Run manual setup
print("Running manual setup...")
try:
    result = subprocess.run([sys.executable, 'manual_setup.py'], 
                          capture_output=False, text=True, timeout=120)
    print(f"Manual setup completed with return code: {result.returncode}")
    if result.returncode != 0:
        print(f"Manual setup failed with return code: {result.returncode}")
        sys.exit(result.returncode)
except Exception as e:
    print(f"Error running manual setup: {e}")
    traceback.print_exc()
    sys.exit(1)

# Start Gunicorn server
print("Starting Gunicorn server...")
try:
    os.execvp('gunicorn', [
        'gunicorn', 
        'fastfood_restaurant.wsgi:application', 
        '--bind', '0.0.0.0:$PORT'
    ])
except Exception as e:
    print(f"Error starting Gunicorn: {e}")
    sys.exit(1)