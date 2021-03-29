#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate
cd /app/cars_api
python manage.py migrate
gunicorn --bind 0.0.0.0:$PORT core.wsgi:application
# You can put other setup logic here

# Evaluating passed command:
exec "$@"