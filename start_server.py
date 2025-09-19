#!/usr/bin/env python
import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

print("=== START SERVER SCRIPT ===")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

try:
    print("Setting up Django...")
    django.setup()
    print("Django setup completed successfully")
except Exception as e:
    print(f"Error during Django setup: {e}")
    sys.exit(1)

# Run migrations
print("Running Django migrations...")
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations completed successfully")
except Exception as e:
    print(f"Error running migrations: {e}")
    sys.exit(1)

# Create superuser if needed
print("Creating superuser if needed...")
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating new superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f"Error creating superuser: {e}")

# Start Gunicorn server
print("Starting Gunicorn server...")
port = os.environ.get('PORT', '8000')
try:
    os.execvp('gunicorn', [
        'gunicorn', 
        'fastfood_restaurant.wsgi:application', 
        '--bind', f'0.0.0.0:{port}'
    ])
except Exception as e:
    print(f"Error starting Gunicorn: {e}")
    sys.exit(1)