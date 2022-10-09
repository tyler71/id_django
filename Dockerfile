FROM python:3.8-slim-buster as prod

EXPOSE 8000

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY --from=caddy /usr/bin/caddy /usr/bin/caddy

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt \
 && rm /requirements.txt

COPY ./init.sh /
COPY ./config/reverse_proxy/Caddyfile /etc/caddy/Caddyfile
COPY ./config/init/supervisord.conf /etc/supervisord.conf
COPY ./config/gunicorn.py /etc/gunicorn.py

COPY ./app/ /app/

CMD ["/init.sh"]


# FROM prod as dev
# USER 1000
#
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

