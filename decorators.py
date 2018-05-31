from app import app, api, db
from flask_security import current_user
from functools import wraps

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.has_role('admin'):
                return f(*args, **kwargs)
            else:
                return api.abort(403)
        else:
            return api.abort(403)
    return wrap

def authenticated():
    if current_user.is_authenticated:
        return True
    else:
        api.abort(403)