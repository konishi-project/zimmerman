from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.feed_controller import api as feed_ns
from .main.controller.post_controller import api as post_ns
from .main.controller.comment_controller import api as comment_ns
from .main.controller.reply_controller import api as reply_ns
from .main.controller.like_controller import api as like_ns
from .main.controller.upload_controller import api as upload_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Zimmerman API",
    version="0.69",
    description="Zimmerman, backend API for Konishi",
)

api.add_namespace(user_ns, path="/user")
api.add_namespace(auth_ns)
api.add_namespace(feed_ns)
api.add_namespace(post_ns)
api.add_namespace(comment_ns)
api.add_namespace(reply_ns)
api.add_namespace(like_ns)
api.add_namespace(upload_ns)
