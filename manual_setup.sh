#!/bin/bash
echo "=== Manual Setup Script ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Listing files:"
ls -la

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "Setup complete!"