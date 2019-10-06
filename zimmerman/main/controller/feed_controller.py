from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from ..util.dto import FeedDto
from ..service.feed_service import Feed
from ..service.user_service import load_user

api = FeedDto.api
_feed = FeedDto.feed

@api.route('/get')
class FeedGet(Resource):

    @api.doc('Get Posts IDs', 
        responses = {
            200: 'Post IDs successfully sent to client.'
        }
    )
    @jwt_required
    def get(self):
        """ Return posts IDs from the Database. """
        return Feed.get_activity()

    @api.expect(_feed, validate=True)
    @api.doc('Get the posts data',
        responses = {
            200: 'Post data successfully sent to the client.'
        }
    )
    @jwt_required
    def post(self):
        """ Get the posts data from the Database. """
        # Get the id array
        data = request.get_json()
        id_array = data['post_ids']
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Feed.get_posts_info(id_array, current_user)