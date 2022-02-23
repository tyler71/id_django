# ======== Development
FROM python:3.8-buster as dev

EXPOSE 8000

RUN apt-get update \
 && apt-get install -y sqlite3 \
 && rm -r /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

USER 1000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ======== Production
FROM python:3.8-slim-buster as prod

EXPOSE 8000


COPY --from=caddy /usr/bin/caddy /usr/bin/caddy

COPY requirements.txt /
RUN pip install --no-cache-dir numpy==1.19.4    \
                               pillow==8.0.1    \
                               gunicorn==20.0.4 \
 && pip install --no-cache-dir -r /requirements.txt

COPY ./entrypoint.sh /
COPY ./Caddyfile /etc/caddy/Caddyfile

USER 1000
COPY --chown=1000:1000 ./app/ /app/

WORKDIR /app
CMD ["/entrypoint.sh"]

# ======== Quality Assurance
FROM prod as qa

USER root
RUN apt-get update \
 && apt-get install -y sqlite3 curl procps \
 && rm -r /var/lib/apt/lists/*

USER 1000

WORKDIR /app
CMD ["/entrypoint.sh"]
