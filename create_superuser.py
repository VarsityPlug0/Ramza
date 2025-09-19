#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from django.contrib.auth import get_user_model

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

if __name__ == '__main__':
    success = create_superuser()
    sys.exit(0 if success else 1)