#!/usr/bin/env python
import os
import sys
import django

print("=== DEBUG SETUP ===")
print(f"Working directory: {os.getcwd()}")
print(f"Environment variables:")
for key, value in os.environ.items():
    if 'DATABASE' in key or 'DJANGO' in key:
        print(f"  {key}: {value}")

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

# Check database configuration
try:
    from django.conf import settings
    print("Database configuration:")
    db_config = settings.DATABASES['default']
    for key, value in db_config.items():
        if key == 'PASSWORD':
            print(f"  {key}: {'*' * len(str(value)) if value else 'None'}")
        else:
            print(f"  {key}: {value}")
except Exception as e:
    print(f"Error getting database configuration: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try to run a simple database query
try:
    from django.db import connection
    print("Testing database connection...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"Database version: {version}")
except Exception as e:
    print(f"Error testing database connection: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check if tables exist
try:
    print("Checking for existing tables...")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
except Exception as e:
    print(f"Error checking tables: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=== DEBUG SETUP COMPLETED ===")