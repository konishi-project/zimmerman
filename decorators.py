from app import app, jwt
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from models import *
from functools import wraps

# Removed old functions related to Flask-Security, will be adding items here soon.
def is_authenticated():
    if current_user.is_authenticated:
        return True

def is_admin(current_user):
    if current_user.status == 'admin':
        return True

def check_like(likes, current_user):
    for like in likes:
        if like.owner_id == current_user.id:
            return True
        else:
            pass

def something_went_wrong():
    return jsonify({'message': 'Uh oh! Something went wrong.'}), 500