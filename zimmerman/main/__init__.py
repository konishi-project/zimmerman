# Entry point
import logging
from flask import Flask

# Import extensions
from .extensions import db, ma, jwt, bcrypt, cors, limiter, talisman

# Import configuration
from zimmerman.config import config_by_name, basedir


def create_app(config_name):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_by_name[config_name])
    logging.basicConfig(
        filename="zimmerman.log",
        level=logging.NOTSET,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )

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
    # talisman.init_app(app)
