from flask import Flask, url_for, request, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
import os

# Init Flask App
app = Flask(__name__)

# Configurations
app.config.from_pyfile('config.py')
# Database
db = SQLAlchemy(app)

# Import Everything from 'views.py'
from views import *

if __name__ == '__main__':
    app.run()