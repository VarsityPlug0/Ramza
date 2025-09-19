#!/usr/bin/env python
import os
import sys
import django

print("=== SETUP TEST ===")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

try:
    django.setup()
    print("Django setup successful")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

# Test database connection
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"Database connection test: {result}")
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)

# Test if auth tables exist
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'auth_user')")
        exists = cursor.fetchone()[0]
        print(f"auth_user table exists: {exists}")
        
        if not exists:
            print("ERROR: auth_user table does not exist!")
            sys.exit(1)
            
    print("Required tables exist")
except Exception as e:
    print(f"Table existence check failed: {e}")
    sys.exit(1)

print("=== SETUP TEST PASSED ===")