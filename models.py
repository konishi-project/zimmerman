import datetime
from peewee import *
from app import db



class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
    username = CharField(unique=True)
    name = CharField()
    bio = TextField(null=True)


class Note(BaseModel):
	creator = ForeignKeyField(User, backref='notes')
	content = TextField()
	created = DateTimeField(default=datetime.datetime.now)
	modified = DateTimeField(default=datetime.datetime.now)
	likes = IntegerField(default=0)
	image = CharField(default='')


class Post(Note):
	pass


class Comment(Note):
	parent = ForeignKeyField(Post, backref='comments')


class Reply(Note):
	parent = ForeignKeyField(Comment, backref='replies')
