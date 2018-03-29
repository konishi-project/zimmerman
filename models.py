from peewee import *
from app import db


class User(Model):
    username = CharField(unique=True)
