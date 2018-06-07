"""
models.py
---
Database models, Security models, and Model Schemas.
"""
from app import app, ma
from app import db
from flask import redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.ext.declarative import declarative_base
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_restplus import SchemaModel
from datetime import datetime

""" 
Defining the Models
---
Some of the items is directly from Flask-Security but modified to fit our needs.
Documentation - https://pythonhosted.org/Flask-Security/ 
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Posts', backref='user')
    # Likes 
    post_likes = db.relationship('PostLike', backref='user')
    comment_likes = db.relationship('CommentLike', backref='user')
    reply_like = db.relationship('ReplyLike', backref='user')
    ##
    member = db.Column(db.Boolean(), default=False)
    status = db.Column(db.String(10))

    def __repr__(self):
        return '{}'.format(self.username)

"""
Used One to Many relationship for Posts.
Posts to Comments, Comments to Replies.
"""
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_name = db.Column(db.String(20))
    content = db.Column(db.Text)
    status = db.Column(db.String(10))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.relationship('PostLike', backref='posts')
    comments = db.relationship('Comments', backref='posts')
    def __repr__(self):
        return 'Post ID - {}'.format(self.id)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    commenter = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.relationship('CommentLike', backref='comments')
    replies = db.relationship('Reply', backref='comments')
    def __repr__(self):
        return 'Comment ID - {}'.format(self.id)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Where this Reply belongs to which comment.
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replier = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime,default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    likes = db.relationship('ReplyLike', backref='reply')
    def __repr__(self):
        return 'Reply ID - {}'.format(self.id)

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, default=datetime.now)

class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, default=datetime.now)

class ReplyLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_reply = db.Column(db.Integer, db.ForeignKey('reply.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, default=datetime.now)

## Model Schemas
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Posts

class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comments

class ReplySchema(ma.ModelSchema):
    class Meta:
        model = Reply

# Admin Index View is the Main Index, not the ModelView
class MainAdminIndexView(AdminIndexView):
    @jwt_required
    def is_accessible(self):
        return True
        # current_user = User.query.filter_by(username=get_jwt_identity()).first()
        # return current_user.status == 'admin'
    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        else:
            return jsonify({'error': 'Forbidden!'}), 403

# This is exactly similar to above Model but for ModelViews not Admin Index View.
class ProtectedModelView(ModelView):
    @jwt_required
    def is_accessible(self):
        return True
        # current_user = User.query.filter_by(username=get_jwt_identity()).first()
        # return current_user.status == 'admin'
    def inaccessible_callback(self, name, **kwargs):
        return jsonify({'message': 'Forbidden!'}), 403