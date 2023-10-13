COMPOSE = docker-compose
SERVICE = web


up:
	$(COMPOSE) up

up-build:
	$(COMPOSE) up --build

build:
	$(COMPOSE) build

up-b:
	$(COMPOSE) up -b

enter:
	$(COMPOSE) exec $(SERVICE) bash

createsuperuser:
	$(COMPOSE) exec $(SERVICE) python manage.py createsuperuser

pre-commit:
	pre-commit run --all-files

populate-history:
	$(COMPOSE) exec $(SERVICE) python manage.py populate_history --auto

shell:
	$(COMPOSE) exec $(SERVICE) python manage.py shell

test:
	pytest

down:
	$(COMPOSE) down

collectstatic:
	$(COMPOSE) exec $(SERVICE) python manage.py collectstatic

migrate:
	$(COMPOSE) exec $(SERVICE) python manage.py migrate

dbbackup:
	$(COMPOSE) exec $(SERVICE) python manage.py dbbackup

dbrestore:
	$(COMPOSE) exec $(SERVICE) python manage.py dbrestore

migrations:
	$(COMPOSE) exec $(SERVICE) python manage.py makemigrations

showmigrations:
	$(COMPOSE) exec $(SERVICE) python manage.py showmigrations
