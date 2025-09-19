#!/bin/bash
echo "Running manual setup..."
python manual_setup.py
echo "Starting Gunicorn server..."
exec gunicorn fastfood_restaurant.wsgi:application --bind 0.0.0.0:$PORT