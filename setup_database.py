#!/usr/bin/env python
import os
import sys
import django
import traceback

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

print("=== Starting Django Setup ===")
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

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection

def run_migrations():
    """Run Django migrations"""
    print("Running Django migrations...")
    try:
        print("Executing showmigrations first...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        print("Executing migrate...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
        print("Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"Error running migrations: {e}")
        traceback.print_exc()
        return False

def create_superuser():
    """Create a superuser if one doesn't exist"""
    print("Creating superuser...")
    User = get_user_model()
    
    # Check if superuser already exists
    try:
        if User.objects.filter(is_superuser=True).exists():
            print("Superuser already exists")
            return True
    except Exception as e:
        print(f"Error checking for existing superuser: {e}")
        traceback.print_exc()
        return False
    
    # Create superuser
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Superuser 'admin' created successfully with password 'admin123'")
        return True
    except Exception as e:
        print(f"Error creating superuser: {e}")
        traceback.print_exc()
        return False

def verify_tables():
    """Verify that required tables exist"""
    print("Verifying tables...")
    required_tables = [
        'auth_user',
        'restaurant_sitesettings',
        'restaurant_contentsection',
        'restaurant_siteimage'
    ]
    
    missing_tables = []
    
    try:
        with connection.cursor() as cursor:
            for table in required_tables:
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", [table])
                exists = cursor.fetchone()[0]
                if not exists:
                    missing_tables.append(table)
                else:
                    print(f"✓ Table {table} exists")
        
        if missing_tables:
            print(f"✗ Missing tables: {', '.join(missing_tables)}")
            return False
        else:
            print("✓ All required tables exist")
            return True
    except Exception as e:
        print(f"Error verifying tables: {e}")
        traceback.print_exc()
        return False

def main():
    """Main setup function"""
    print("Setting up database...")
    
    # Run migrations
    if not run_migrations():
        return False
    
    # Verify tables
    if not verify_tables():
        return False
    
    # Create superuser
    if not create_superuser():
        return False
    
    print("Database setup completed successfully!")
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error in main: {e}")
        traceback.print_exc()
        sys.exit(1)