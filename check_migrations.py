#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from django.db import connection

def check_tables():
    """Check if required tables exist"""
    required_tables = [
        'auth_user',
        'restaurant_sitesettings',
        'restaurant_contentsection',
        'restaurant_siteimage'
    ]
    
    missing_tables = []
    
    with connection.cursor() as cursor:
        for table in required_tables:
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", [table])
            exists = cursor.fetchone()[0]
            if not exists:
                missing_tables.append(table)
    
    return missing_tables

if __name__ == '__main__':
    missing = check_tables()
    if missing:
        print(f"Missing tables: {', '.join(missing)}")
        sys.exit(1)
    else:
        print("All required tables exist")
        sys.exit(0)