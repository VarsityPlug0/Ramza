#!/usr/bin/env python
import os
import sys
import django

print("=== RUNNING MIGRATIONS ===")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

try:
    print("Setting up Django...")
    django.setup()
    print("Django setup completed")
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Run migrations
try:
    from django.core.management import execute_from_command_line
    print("Showing current migration status...")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    print("Migration process completed")
except Exception as e:
    print(f"Error running migrations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=== MIGRATIONS COMPLETED ===")