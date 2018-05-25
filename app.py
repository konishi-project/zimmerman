from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
import os

# Init Flask App
app = Flask(__name__)
# Init RESTPlus
api = Api(app)
# Configurations
app.config.from_pyfile('config.py')
# Database
db = SQLAlchemy(app)
# Import Everything from 'views.py'
from views import *

if __name__ == '__main__':
    app.run()