.PHONY: install dev test lint clean build up down

install:
	cd api && pip install -r requirements.txt
	cd web && npm install

dev:
	docker-compose up --build

test:
	cd api && pytest tests/ -v --cov=.
	cd web && npm test

lint:
	cd api && black . && flake8 . && mypy .
	cd web && npm run lint

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

seed:
	docker-compose exec api python scripts/seed_database.py
