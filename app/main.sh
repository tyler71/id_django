#!/usr/bin/env sh

./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic --noinput

#/usr/bin/caddy start -config /etc/caddy/Caddyfile
/usr/local/bin/gunicorn --bind 0.0.0.0:35252 --access-logfile '-' --config /etc/gunicorn.py image_difference.wsgi
