build:
	docker-compose build --build-arg USER_ID=$$(id -u) --build-arg GROUP_ID=$$(id -g)

dev:
	docker-compose run app chalice local

test: migrate
	docker-compose run app pytest 

test_watch: migrate
	docker-compose run app ptw -- --testmon

run:
	docker-compose run app /bin/bash  

migration_generate:
	docker-compose run app alembic revision --autogenerate -m "$(message)"

migrate:
	docker-compose run app alembic upgrade head
