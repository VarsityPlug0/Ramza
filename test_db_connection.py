#!/usr/bin/env python
import os
import sys
import django
import traceback

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

print("=== Testing Database Connection ===")
print(f"Python path: {sys.path}")
print(f"Current working directory: {os.getcwd()}")
print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    django.setup()
    print("Django setup completed successfully")
except Exception as e:
    print(f"Error during Django setup: {e}")
    traceback.print_exc()
    sys.exit(1)

from django.conf import settings
from django.db import connection

def test_connection():
    """Test database connection and show settings"""
    print("Testing database connection...")
    print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"Database name: {settings.DATABASES['default']['NAME']}")
    print(f"Database host: {settings.DATABASES['default']['HOST']}")
    print(f"Database user: {settings.DATABASES['default']['USER']}")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"Database version: {version}")
            
            # List all tables
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            print("Existing tables:")
            for table in tables:
                print(f"  - {table[0]}")
                
        print("Database connection successful!")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        success = test_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)