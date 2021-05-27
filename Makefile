build:
	docker build . -t dream

dev:
	docker run -p 8000:8000 -v "$$(pwd)":/app dream

test:
	docker run -p 8000:8000 -v "$$(pwd)":/app dream pytest
