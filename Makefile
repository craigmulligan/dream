build:
	docker build . -t dream

dev:
	docker run -p 8000:8000 -v "$$(pwd)":/app dream

test:
	docker run -p 8000:8000 -v "$$(pwd)":/app dream pytest

test_watch:
	docker run -it -p 8000:8000 -v "$$(pwd)":/app dream ptw -- --testmon

run:
	docker run -it --entrypoint /bin/bash -p 8000:8000  -v "$$(pwd)":/app dream
