.PHONY: install run test docker-up docker-down

install:
	poetry install

run:
	poetry run uvicorn main:app --reload

test:
	poetry run pytest -v

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down