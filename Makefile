.PHONY: help run migrate migrations create-superuser shell test lint install 

create-superuser:
	uv run manage.py createsuperuser

help:
	@echo "Команды make:"
	@echo "  make create-superuser   - Создать суперпользователя"
	@echo "  make install            - Установить зависимости"
	@echo "  make lint               - Запустить линтер (ruff)"
	@echo "  make migrations         - Создать миграции"
	@echo "  make migrate            - Применить миграции"
	@echo "  make run                - Запустить Django сервер"
	@echo "  make shell              - Открыть Django shell"
	@echo "  make test               - Запустить тесты"

install:
	uv sync

lint:
	uv run ruff check

migrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

run:
	uv run manage.py runserver

run-telegram:
	uv run manage.py run_listener

shell:
	uv run manage.py shell

test:
	uv run manage.py test