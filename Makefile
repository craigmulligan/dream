build:
	docker-compose build	

dev:
	docker-compose run app chalice local

test:
	docker-compose run app pytest 

test_watch:
	docker-compose run app ptw

run:
	docker-compose  run app /bin/bash  
