web: gunicorn --threads 4 manage:app
release: python manage.py db init; python manage.py db migrate; python manage.py db upgrade