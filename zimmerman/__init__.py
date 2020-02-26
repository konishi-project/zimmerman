""" Top level module for zimmerman

This module

- Contains create_app()
- Registers extensions
"""
from flask import Flask

# Import extensions
from .extensions import bcrypt, cors, db, jwt, limiter, ma

# Import configuration
from config import config_by_name


def create_app(config_name):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_by_name[config_name])

    register_extensions(app)

    # Register blueprint
    from .api import main_bp
    app.register_blueprint(main_bp)

    return app


def register_extensions(app):
    # Registers flask extensions.
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    # talisman.init_app(app)
