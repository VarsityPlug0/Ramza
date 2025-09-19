#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

print("=== START SERVER SCRIPT ===")
print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

# Add current directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"Added {current_dir} to Python path")

try:
    print("Setting up Django...")
    django.setup()
    print("Django setup completed successfully")
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Collect static files
print("Collecting static files...")
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=1'])
    print("Static files collected successfully")
except Exception as e:
    print(f"Error collecting static files: {e}")
    import traceback
    traceback.print_exc()
    # Don't exit on static file error as it's not critical for the app to run

# Run migrations
print("Running Django migrations...")
try:
    execute_from_command_line(['manage.py', 'showmigrations'])
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations completed successfully")
except Exception as e:
    print(f"Error running migrations: {e}")
    import traceback
    traceback.print_exc()
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
    # Don't exit on superuser error as it's not critical for the app to run

# Start Gunicorn server
print("Starting Gunicorn server...")
port = os.environ.get('PORT', '8000')
print(f"Binding to port {port}")

try:
    os.execvp('gunicorn', [
        'gunicorn', 
        'fastfood_restaurant.wsgi:application', 
        '--bind', f'0.0.0.0:{port}',
        '--workers', '4',
        '--timeout', '120'
    ])
except Exception as e:
    print(f"Error starting Gunicorn: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)