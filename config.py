"""
config.py
---
Configuration for the Flask Application
"""
from app import app
import os

# Debug mode
DEBUG = True
# Flask Secret Key for encrypting sessions, change in production to something very secret.
SECRET_KEY = 'SomeSecretKeyThisIsJustAnExample'
# Secret key for JWT, change in production to something no one knows.
JWT_SECRET_KEY = 'SuperSecreto'

"""
Check out documentation for Flask-SQLAlchemy Here
---
http://flask-sqlalchemy.pocoo.org/2.3/
"""
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres://postgres:password@localhost:5432/konishidb')
SQLALCHEMY_TRACK_MODIFICATIONS = True