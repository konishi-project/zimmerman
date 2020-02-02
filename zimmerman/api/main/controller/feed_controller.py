from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman import limiter
from ..util.dto import FeedDto

from ..service.feed.service import FeedService
from ..service.user.utils import load_user

api = FeedDto.api
_posts = FeedDto.posts
_comments = FeedDto.comments
_replies = FeedDto.replies


@api.route("/posts")
class FeedPost(Resource):
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

    @api.expect(_posts, validate=True)
    @api.doc(
        "Get the posts data",
        responses={200: "Posts data successfully sent to the client."},
    )
    @jwt_required
    def post(self):
        """ Get the posts data from the DB. """
        # Get the id array
        data = request.get_json()
        id_array = data["post_ids"]

        # Get the current user
        current_user = load_user(get_jwt_identity())
        return FeedService.get_posts_data(id_array, current_user)


@api.route("/comments")
class FeedComment(Resource):
    @api.expect(_comments, validate=True)
    @api.doc(
        "Get the comments data",
        responses={200: "Comments data successfully sent to the client."},
    )
    @jwt_required
    def post(self):
        """ Get the comments data from the DB. """
        # Get the id array
        data = request.get_json()
        id_array = data["comment_ids"]

        # Get the current user
        current_user = load_user(get_jwt_identity())
        return FeedService.get_comments_data(id_array, current_user)


@api.route("/replies")
class FeedReplies(Resource):
    @api.expect(_replies, validate=True)
    @jwt_required
    def post(self):
        """ Nothing yet """
        return "To be implemented.", 200
