from app import app
from app import db
from flask import redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
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
    def __repr__(self):
        return '{}'.format(self.name)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(50), unique=True)
    bio = db.Column(db.Text)
    password = db.Column(db.String(255))
    posts = db.relationship('Note', backref='user')
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return '{}'.format(self.username)

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
    creator = db.Column(db.Integer, db.ForeignKey('user.id')) 
    content = db.Column(db.Text)
    created = db.Column(db.DateTime,default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    #image = db.Column(**args)

# Post is not complete.
# These models below may not be fully complete, feel free to improve or add.
class Post(Note):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.relationship('Comment', backref='post')

class Comment(Note):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    comment_on_post = db.Column(db.Integer, db.ForeignKey('post.id'))
    replies = db.relationship('Reply', backref='comment')

class Reply(Note):
    __tablename__ = 'Replies'
    id = db.Column(db.Integer, primary_key=True)
    replies_on_comment = db.Column(db.Integer, db.ForeignKey('comment.id'))

# Admin Index View is the Main Index, not the ModelView
class MainAdminIndexView(AdminIndexView):
    def is_accessible(self):
        """ 
        Check if the Current Logged in User has 
        the admin role to access this page. If not it will
        redirect to security Login page and checks if the 
        user has the admin role again. If not, it will
        raise a 403 error.
        """
        return current_user.has_role('admin')
    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        else:
            abort(403)

# This is exactly similar to above Model but for ModelViews not Admin Index View.
class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')
    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        else:
            abort(403)
	
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)