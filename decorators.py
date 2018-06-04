from app import app, api, db
from flask_security import current_user
from functools import wraps

def is_admin():
    if current_user.has_role('admin'):
        return True
    else:
        return {'message': 'Forbidden'}

def authenticated():
    if current_user.is_authenticated:
        return True
    else:
        return {'message': 'User is not authenticated'}
