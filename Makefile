.PHONY: clean install tests run all migrate

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	pip install -r requirements.txt

migrate:
	python manage.py db migrate
	python manage.py db upgrade

tests:
	python manage.py test

run:
	python manage.py run

all:
	clean install migrate tests run