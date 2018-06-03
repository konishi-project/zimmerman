from app import app, api, db
from flask_security import current_user
from functools import wraps

def is_admin():
    if current_user.has_role('admin'):
        return True
    else:
        api.abort(403)

def authenticated():
    if current_user.is_authenticated:
        return True
    else:
        api.abort(401)