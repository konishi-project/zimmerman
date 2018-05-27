from app import app
from app import db
from flask import redirect, url_for, abort
from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import SQLAlchemy
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from datetime import datetime

""" 
Defining the Models
---
Some of the items is directly from Flask-Security but modified to fit our needs.
Documentation - https://pythonhosted.org/Flask-Security/ 
"""

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
    username = db.Column(db.String(20), unique=True)
    full_name = db.Column(db.String(50))
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Posts', backref='user')
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return '{}'.format(self.username)

"""
Used One to Many relationship for Posts.
Posts to Comments, Comments to Replies.
"""
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_name = db.Column(db.String(50))
    content = db.Column(db.Text)
    status = db.Column(db.String(10))
    created = db.Column(db.DateTime,default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comments', backref='posts')

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    commenter = db.Column(db.String(50))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime,default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    replies = db.relationship('Reply', backref='comments')
    def __repr__(self):
        return 'Comment ID - {}'.format(self.id)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Where this Reply belongs to which comment.
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replier = db.Column(db.String(50))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime,default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    def __repr__(self):
        return 'Reply ID - {}'.format(self.id)

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