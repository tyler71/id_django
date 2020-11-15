#!/usr/bin/env sh

./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic --noinput

/usr/local/bin/gunicorn --bind 0.0.0.0:8000 --access-logfile '-' image_difference.wsgi

