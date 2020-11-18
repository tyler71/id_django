appname := "django_app"

stop:
    docker-compose stop
remove:
    docker-compose down
enter:
    #!/usr/bin/env bash
    DB="$(docker inspect -f '{{ "{{" }} .Name {{ "}}" }}' $(docker-compose ps -q {{appname}}) | cut -c2-)"
    docker container exec -it "$DB" bash
logs:
    docker-compose logs -f
sql:
    #!/usr/bin/env bash
    DB="$(docker inspect -f '{{ "{{" }} .Name {{ "}}" }}' $(docker-compose ps -q {{appname}}) | cut -c2-)"
    docker container exec -it "$DB" sqlite3 db.sqlite3
shell:
    #!/usr/bin/env bash
    DB="$(docker inspect -f '{{ "{{" }} .Name {{ "}}" }}' $(docker-compose ps -q {{appname}}) | cut -c2-)"
    docker container exec -it "$DB" ./manage.py shell

build:
    docker image build -t tyler71/image_difference --target prod .
    docker image push tyler71/image_difference:latest
dev:
    docker-compose -f docker-compose.yml build
    docker-compose -f docker-compose.yml up -d
qa:
    docker-compose -f docker-compose.qa.yml build
    docker-compose -f docker-compose.qa.yml up -d
prod:
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up -d
