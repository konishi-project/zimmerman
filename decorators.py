from app import app, jwt
from flask_security import current_user
from flask import jsonify, request
from functools import wraps

# Removed old functions related to Flask-Security, will be adding items here soon.
def is_authenticated():
    if current_user.is_authenticated:
        return True

def something_went_wrong():
    return jsonify({'message': 'Uh oh! Something went wrong.'}), 500