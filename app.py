import os
from flask import Flask
from peewee import SqliteDatabase



app = Flask(__name__)

DATABASE = 'zimmerman.db'
app.config.from_object(__name__)

db = SqliteDatabase(app.config['DATABASE'])
