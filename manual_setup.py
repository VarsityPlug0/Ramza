#!/usr/bin/env python
import os
import sys
import django
import traceback

print("=== RUNNING MANUAL SETUP ===")
print(f"Working directory: {os.getcwd()}")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

try:
    print("Setting up Django...")
    django.setup()
    print("Django setup completed successfully")
except Exception as e:
    print(f"Error during Django setup: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Importing Django modules...")
try:
    from django.core.management import execute_from_command_line
    print("Django modules imported successfully")
except Exception as e:
    print(f"Error importing Django modules: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Running Django migrations...")
try:
    # Show current migrations status
    print("Current migration status:")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    # Run migrations
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations completed successfully")
except Exception as e:
    print(f"Error running migrations: {e}")
    traceback.print_exc()
    sys.exit(1)

print("=== MANUAL SETUP COMPLETED SUCCESSFULLY ===")
sys.exit(0)