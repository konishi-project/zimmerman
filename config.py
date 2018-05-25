from app import app
import os

DEBUG = True
""" Secret Key to Encrypt Sessions, Change this in Production """
SECRET_KEY = 'SomeSecretKeyThisIsJustAnExample'

"""
DATABASE_URL is meant for PostgreSQL, When adding the Postgres Addon
it will have a DATABASE_URL, this is to connect it.

SQLAlchemy URI format is 'postgresql://username:password@localhost:5432/mydatabase'
What you see here is an example of my Postgres and Sample Password with postgres as username.
"""
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres://username:password@localhost:5432/konishidb')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Flask-Security Configuration
SECURITY_PASSWORD_SALT = 'SomeRandomTextToEncryptPassword'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
# User Can Register, Set to [ON] at the moment.
SECURITY_REGISTERABLE = True
# User Account Needs to be confirmed to Login.
SECURITY_CONFIRMABLE = True