USER_ID  := $(shell id -u)
GROUP_ID := $(shell id -g)

build:
	docker-compose build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)

dev:
	docker-compose run --service-ports --publish app

test: migrate
	docker-compose run app pytest 

test_watch: migrate
	docker-compose run app ptw -- --testmon

run:
	docker-compose run app /bin/bash

migrate_generate:
	docker-compose run app alembic revision --autogenerate -m "$(message)"

migrate:
	docker-compose run app alembic upgrade head

fmt:
	docker-compose run app black .

fmt_check:
	docker-compose run app black . --check

package:
	chalice-local package --pkg-format terraform infrastructure
