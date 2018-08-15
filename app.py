"""
Import Flask and SQLAlchemy to instantiate the app
aswell as the Database.
---
Import the RESTPlus API and instantiate it from the app.
Documentation for RESTPlus - https://flask-restplus.readthedocs.io/en/stable/
--- 
Resources:
Flask-Marshmallow - http://flask-marshmallow.readthedocs.io/en/latest/
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api
from flask_jwt_extended import JWTManager 
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Init Flask App
app = Flask(__name__)
# Get configurations
app.config.from_pyfile('config.py')
# Init the Database
db = SQLAlchemy(app)
# Init CORS
CORS(app)
# Init RESTPlus
api = Api(app)
# Init Marshmallow
ma = Marshmallow(app)
# Init Migrate
migrate = Migrate(app, db)
# Init JWT
jwt = JWTManager(app)
# Init Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "500 per hour"]
    )
"""
Import everything from 'views.py'.
---
This is positioned after instantiating the App, Api, etc.
If it was imported above then it will cause errors.
"""
from views import *

if __name__ == '__main__':
    app.run(port=4000)
