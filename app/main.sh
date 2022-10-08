#!/usr/bin/env sh

./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic --noinput

#/usr/bin/caddy start -config /etc/caddy/Caddyfile
/usr/local/bin/gunicorn --bind 127.0.0.1:35252 --access-logfile '-' image_difference.wsgi
