from app import app, jwt
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models import *
from functools import wraps

def is_admin(current_user):
    # Get admin role
    for role in current_user.roles:
        if role.name == 'admin':
            return True
        else:
            return False

def check_like(likes, current_user):
    for like in likes:
        if like.owner_id == current_user.id:
            return True
        else:
            pass

def load_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'message': 'User does not exist!'}, 404
    else:
        return user

def uniq(a_list):
    encountered = set()
    result = []
    for elem in a_list:
        if elem not in encountered:
            result.append(elem)
        encountered.add(elem)
    return result

def delete_replies(commentid):
    comment = Comments.query.filter_by(id=commentid).first()
    # Check if there are replies
    if comment.replies != None:
        for reply in comment.replies:
            db.session.delete(reply)
        db.session.commit()

def delete_comments(postid):
    post = Posts.query.filter_by(id=postid).first()
    # Check if there are comments
    if post.comments != None:
        for comment in post.comments:
            db.session.delete(comment)
        db.session.commit()
