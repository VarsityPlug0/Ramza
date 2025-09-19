#!/usr/bin/env python
import os
import sys
import time

print("=== EXECUTION TEST ===")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Working directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Environment variables:")
for key in sorted(os.environ.keys()):
    if 'PATH' in key or 'PYTHON' in key or 'DATABASE' in key or 'DJANGO' in key:
        print(f"  {key}: {os.environ[key]}")

# Create a test file to see if this script runs
with open('execution_test.txt', 'w') as f:
    f.write(f"Execution test ran at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Working directory: {os.getcwd()}\n")

print("Execution test completed - file created")
print("=== END EXECUTION TEST ===")