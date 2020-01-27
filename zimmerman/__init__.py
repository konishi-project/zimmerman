from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.feed_controller import api as feed_ns
from .main.controller.post_controller import api as post_ns
from .main.controller.comment_controller import api as comment_ns
from .main.controller.reply_controller import api as reply_ns
from .main.controller.like_controller import api as like_ns
from .main.controller.upload_controller import api as upload_ns

from .auth.controller import api as auth_ns

from .notification.controller import api as notif_ns

main_bp = Blueprint("main", __name__)

main = Api(main_bp, title="Main API", version="1.10.1", description="Main routes.")

# Core API
main.add_namespace(user_ns)
main.add_namespace(feed_ns)
main.add_namespace(post_ns)
main.add_namespace(comment_ns)
main.add_namespace(reply_ns)
main.add_namespace(like_ns)
main.add_namespace(upload_ns)

# Auth
main.add_namespace(auth_ns)

# Notification
main.add_namespace(notif_ns)
