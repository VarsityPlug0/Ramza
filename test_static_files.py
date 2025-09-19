#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

try:
    print("Setting up Django...")
    django.setup()
    print("Django setup completed successfully")
    
    # Check if staticfiles directory exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_root = os.path.join(current_dir, 'staticfiles')
    print(f"Static root directory: {static_root}")
    print(f"Static root exists: {os.path.exists(static_root)}")
    
    if os.path.exists(static_root):
        # Count files in staticfiles directory
        file_count = 0
        for root, dirs, files in os.walk(static_root):
            file_count += len(files)
        print(f"Files in staticfiles directory: {file_count}")
        
        # List some files
        print("Sample files in staticfiles:")
        for root, dirs, files in os.walk(static_root):
            for file in files[:10]:  # Show first 10 files
                print(f"  {os.path.join(root, file)}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")
            break
    
    # Try to collect static files
    print("Attempting to collect static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=2'])
    print("Static files collection completed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)