#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection

def run_migrations():
    """Run Django migrations"""
    print("Running Django migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
        print("Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"Error running migrations: {e}")
        return False

def create_superuser():
    """Create a superuser if one doesn't exist"""
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists")
        return True
    
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
        return False

def verify_tables():
    """Verify that required tables exist"""
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
            else:
                print(f"✓ Table {table} exists")
    
    if missing_tables:
        print(f"✗ Missing tables: {', '.join(missing_tables)}")
        return False
    else:
        print("✓ All required tables exist")
        return True

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
    success = main()
    sys.exit(0 if success else 1)