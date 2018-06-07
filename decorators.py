from app import app, jwt
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models import *
from functools import wraps

def is_admin(current_user):
    if current_user.status == 'admin':
        return True

def check_like(likes, current_user):
    for like in likes:
        if like.owner_id == current_user.id:
            return True
        else:
            pass

def member_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if the current user is a member.
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        # current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.member == True:
            pass
        else:
            return {'message': 'You are not a member!'}, 401
        return f(*args, **kwargs)
    return decorated