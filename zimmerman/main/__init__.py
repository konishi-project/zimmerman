from flask import Flask

# Import extensions
from .extensions import db, ma, jwt, bcrypt, cors, limiter
# Import configuration
from .config import config_by_name

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_by_name[config_name])

    register_extensions(app)

    return app

def register_extensions(app):
    """ Registers flask extensions. """
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)