#!/usr/bin/env python
import os
import sys
import django
import traceback

print("=== STARTING MANUAL SETUP ===")
print(f"Working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
print(f"Added to Python path: {project_dir}")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

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
    from django.contrib.auth import get_user_model
    print("Django modules imported successfully")
except Exception as e:
    print(f"Error importing Django modules: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Running Django migrations...")
try:
    execute_from_command_line(['manage.py', 'showmigrations'])
    execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
    print("Migrations completed successfully")
except Exception as e:
    print(f"Error running migrations: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Creating superuser...")
try:
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating new superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f"Error creating superuser: {e}")
    traceback.print_exc()
    sys.exit(1)

print("=== MANUAL SETUP COMPLETED SUCCESSFULLY ===")