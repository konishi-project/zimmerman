from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from ..util.dto import LikeDto
from ..service.like_service import Like, Unlike
from ..service.user_service import load_user

api = LikeDto.api
_like = LikeDto.like

@api.route('/post/<string:post_public_id>')
class LikePost(Resource):

    @api.doc('Like a post.',
        responses = {
            201: 'Successfully liked the post.',
            403: 'User has already liked the post.',
            404: 'Post not found!',
            500: 'Something went wrong during the process!'
        }
    )
    @jwt_required
    def post(self, post_public_id):
        """ Like a post using its specific id """
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Like.post(post_public_id, current_user)

    @api.doc('Unlike a post.',
        responses = {
            200: 'Successfully unliked the post.',
            500: 'Something went wrong during the process!'
        }
    )
    @jwt_required
    def delete(self, post_public_id):
        """ Unlike a specific post using its specific id """
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Unlike.post(post_public_id, current_user)

@api.route('/comment/<int:comment_id>')
class LikeComment(Resource):

    @api.doc('Like a comment.', 
        responses = {
            201: 'Successfully liked the comment.',
            403: 'User has already liked the comment.',
            404: 'Comment not found!',
            500: 'Something went wrong during the process!'
        }
    )
    @jwt_required
    def post(self, comment_id):
        """ Like a comment using its specific id """
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Like.comment(comment_id, current_user)

    @api.doc('Unlike a comment.',
        responses = {
            200: 'Successfully unliked the comment.',
            500: 'Something went wrong during the process!'
        }
    )
    @jwt_required
    def delete(self, comment_id):
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Unlike.comment(comment_id, current_user)

@api.route('/reply/<int:reply_id>')
class LikeComment(Resource):

    @api.doc('Like a reply.', 
        responses = {
            201: 'Successfully liked the reply.',
            403: 'User has already liked the reply.',
            404: 'Comment not found!',
            500: 'Something went wrong during the process!'
        }
    )
    @jwt_required
    def post(self, reply_id):
        """ Like a reply using its specific id """
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Like.reply(reply_id, current_user)

    @api.doc('Unlike a reply.',
        responses = {
            200: 'Successfully unliked the reply.',
            500: 'Something went wrong during the process!'
        }
    )
    @jwt_required
    def delete(self, reply_id):
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Unlike.reply(reply_id, current_user)