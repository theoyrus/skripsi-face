SHELL := /bin/bash
.POSIX:
.PHONY: help

## @egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
help: ## Show this help
	@grep -E '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

env:
	pip install --user pipenv

prod-env: ## Read Production Env
	@cat .prod.env

prod-run: ## Run production app inside docker
	docker-compose --env-file=.prod.env up -d

prod-stop: ## Stop production app inside docker
	docker-compose --env-file=.prod.env down

shell: ## Enter the virtual environment
	pipenv shell

install: ## Install or update dependencies
	pipenv install --dev

runserver: ## Run the local development server
	python manage.py runserver

makemigrations: ## Generate migrations
	python manage.py makemigrations

migrate: ## Run migrations
	python manage.py migrate

collectstatic: ## Generate staticfiles
	python manage.py collectstatic

serve: migrate collectstatic runserver ## Run the production server
	make migrate \
	&& make collectstatic \
	&& make runserver

dev: migrate runserver ## Jalankan shell dan jalankan development server
	make migrate \
	&& make runserver

initial: env install ## Install tool
	make env && make install

app: ## Generate Django App | Usage : `make app name=theappname`
ifdef name
	@mkdir -p ./apps/$(name)
	@django-admin startapp $(name) ./apps/$(name)
	@sed -i 's|$(name)|apps.$(name)|g' ./apps/$(name)/apps.py
	@echo Successfuly create apps $(name), add to LOCAL_APPS with
	@echo 'apps.$(name)'
endif
