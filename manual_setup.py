#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

print("=== Manual Setup Script ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.executable}")

try:
    django.setup()
    print("Django setup completed")
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

print("Running Django migrations...")
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations completed")
except Exception as e:
    print(f"Error running migrations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Creating superuser...")
try:
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f"Error creating superuser: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Setup complete!")