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
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_marshmallow import Marshmallow
import os

# Init Flask App
app = Flask(__name__)
# Get configurations
app.config.from_pyfile('config.py')
# Init the Database
db = SQLAlchemy(app)
# Init RESTPlus
api = Api(app)
# Init Marshmallow
ma = Marshmallow(app)
"""
Import everything from 'views.py'.
---
This is positioned after instantiating the App, Api, etc.
If it was imported above then it will cause errors.
"""
from views import *

if __name__ == '__main__':
    app.run()