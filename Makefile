SHELL := /bin/bash

VENV?=venv
ENV?=dev
BIN ?= $(VENV)/bin
PYTHON ?= $(BIN)/python3

#include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(BIN)/activate && exec bash

.PHONY: install
install: ## Make venv and install requirements
	$(BIN)/pip install -r requirements.txt

create_env: ## this will create the directories for the .env files
	@if [ ! -d restaurant/envs ]; then mkdir -p restaurant/envs; fi
	touch restaurant/envs/.env.$(ENV); \
	echo -e "DJANGO_SECRET_KEY=\nDB_NAME=\nDB_USER=\nDB_PASSWORD=\nDB_HOST=\nDB_PORT=\nDEBUG=\nLOG_LEVEL=\nDEBUG_LOG_DIR=\nEMAIL_HOST_USER=\nEMAIL_HOST_PASSWORD=\nPOSTGRES_NAME=\nPOSTGRES_DB=\nPOSTGRES_USER=\nPOSTGRES_PASSWORD=\nENV=" > restaurant/envs/.env.$(ENV); \

migrate: ## Make and run migrations
	ENV=$(ENV) $(PYTHON) manage.py makemigrations
	ENV=$(ENV) $(PYTHON) manage.py migrate

createsuperuser: ## Create a superuser
	ENV=$(ENV) $(PYTHON) manage.py createsuperuser

e2e-up: ## Start the cluster of e2e containers
	ENV=$(ENV) docker-compose up -d

api-up:
	ENV=$(ENV) docker-compose up -d api

docker-down:
	ENV=$(ENV) docker-compose down

db-shell: ## Access the Postgres Docker database interactively with psql
	docker exec -it container_na me psql -d $(DBNAME)

.PHONY: test
test: ## Run tests
	ENV=$(ENV) $(PYTHON) manage.py test --verbosity=0 --parallel --failfast

coverage-report: ## Run Coverage Report
	ENV=$(ENV) coverage run manage.py test && coverage report

static-code-analysis: ## Run static code analysis
	ENV=$(ENV) pylint **/*.py;

.PHONY: run
run: ## Run the Django server
	ENV=$(ENV) $(PYTHON) manage.py runserver

start: install migrate run ## Install requirements, apply migrations, then start development server

# Create a target for kick-starting a project and setting project name, apps, settings, log-levels etc.