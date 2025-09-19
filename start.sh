#!/bin/bash
echo "Running Django migrations..."
python manage.py migrate --noinput
echo "Creating superuser if needed..."
python create_superuser.py
echo "Starting Gunicorn server..."
exec gunicorn fastfood_restaurant.wsgi:application --bind 0.0.0.0:$PORT