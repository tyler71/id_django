FROM python as dev

RUN apt-get update \
 && apt-get install -y sqlite3 \
 && rm -r /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /
RUN pip install --no-cache-dir numpy pillow \
    && pip install --no-cache-dir -r /requirements.txt

USER 1000

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python as prod

COPY requirements.txt /
RUN pip install --no-cache-dir numpy pillow \
    && pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

USER 1000
WORKDIR /app
COPY ./app /app

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
