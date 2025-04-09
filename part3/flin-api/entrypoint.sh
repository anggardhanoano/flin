#!/bin/bash
set -e

python manage.py collectstatic --noinput
python manage.py migrate

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000