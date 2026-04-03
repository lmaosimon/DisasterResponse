.PHONY: install test api docker-build docker-run

install:
	python3 -m pip install -r requirements.txt

test:
	python3 -m unittest discover -s Test -t . -v

api:
	python3 -m flask --app api.app:create_app run --host 0.0.0.0 --port 8000

docker-build:
	docker build -t disaster-response .

docker-run:
	docker run --rm -p 8000:8000 disaster-response
