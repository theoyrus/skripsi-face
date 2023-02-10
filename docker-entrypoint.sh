#!/bin/sh
cd /app
python manage.py collectstatic --no-input
python manage.py migrate
exec gunicorn --bind '0.0.0.0:8000' --worker-tmp-dir /dev/shm --workers "${GUNICORN_WORKERS:-3}" core.wsgi:application
