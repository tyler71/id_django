FROM python as dev

EXPOSE 8000

RUN apt-get update \
 && apt-get install -y sqlite3 \
 && rm -r /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /
RUN pip install --no-cache-dir numpy==1.19.4 \
                               pillow==8.0.1 \
    && pip install --no-cache-dir -r /requirements.txt

USER 1000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:slim as prod
ENV DEBUG=False

EXPOSE 8000

COPY requirements.txt /
RUN pip install --no-cache-dir numpy==1.19.4    \
                               pillow==8.0.1    \
                               gunicorn==20.0.4 \
    && pip install --no-cache-dir -r /requirements.txt


USER 1000
COPY --chown=1000:1000 ./app/ /app/

WORKDIR /app
RUN ./manage.py makemigrations \
 && ./manage.py migrate        \
 && ./manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "image_difference.wsgi"]
