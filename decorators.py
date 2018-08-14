from app import app, jwt
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models import *
from functools import wraps

def is_admin(current_user):
    # Get primary role
    if current_user.roles[0] == 1:
        return True

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
