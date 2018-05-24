from app import app
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from datetime import datetime

# Define models
""" This is from Flask-Security which can be found here
    https://pythonhosted.org/Flask-Security/ """

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(50), unique=True)
    bio = db.Column(db.Text)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

"""
class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel):
    username = CharField(unique=True)
    name = CharField()
    bio = TextField(null=True)
"""
""" Using One to Many Relationship for Notes, One owner but many different types of Notes.
    Relationship is not implemented yet as seen below.
 """
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column('Creator', db.String(50)) 
    created = db.Column(db.DateTime,default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    # image = db.Column(**args)
	
""" Commented out for now 
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
"""

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)