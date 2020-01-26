from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from ..util.dto import FeedDto

from ..service.feed.service import FeedService
from ..service.user.utils import load_user

api = FeedDto.api
_feed = FeedDto.feed


@api.route("/get")
class FeedGet(Resource):
    decorators = [
        limiter.limit(
            "10/minute", error_message="Too many posts requests (10 per minute)."
        )
    ]

    @api.doc("Get Posts IDs", responses={200: "Post IDs successfully sent to client."})
    @jwt_required
    def get(self):
        """ Return posts IDs from the Database. """
        # Args
        limit = request.args.get("limit", default=500, type=int)

        return FeedService.get_activity(limit)

    decorators = [
        limiter.limit(
            "25/minute", error_message="Too many posts requests (25 per minute)."
        )
    ]

    @api.expect(_feed, validate=True)
    @api.doc(
        "Get the posts data",
        responses={200: "Post data successfully sent to the client."},
    )
    @jwt_required
    def post(self):
        """ Get the posts data from the Database. """
        # Get the id array
        data = request.get_json()
        id_array = data["post_ids"]
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return FeedService.get_posts_info(id_array, current_user)
