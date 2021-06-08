build:
	docker-compose build --build-arg USER_ID=$$(id -u) --build-arg GROUP_ID=$$(id -g)

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

local:
	docker-compose run app chalice-local deploy

invoke:
	awslocal lambda invoke --function-name dream-dev --payload "{}" out.txt

setup:
	awslocal sns create-topic --name MyDemoTopic

package:
	chalice-local package --pkg-format terraform infrastructure

terraform_apply: package
	docker-compose run app terraform apply
