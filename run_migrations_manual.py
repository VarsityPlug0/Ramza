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

def run_migrations():
    """Run Django migrations manually"""
    print("Running Django migrations...")
    try:
        # Run migrations for all apps with verbose output
        execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
        print("Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"Error running migrations: {e}")
        return False

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1)