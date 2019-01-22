from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import CommentDto
from ..service.comment_service import create_new_comment, delete_comment
from ..service.user_service import load_user

api = CommentDto.api
_comment = CommentDto.comment

@api.route('/create/<string:post_public_id>')
class CommentCreate(Resource):

    @api.doc('Comment on a specific post',
        responses = {
            201: 'Successfully commented on the post',
            403: 'Comment content exceeds limit',
            401: 'Post status is locked!'
        }
    )
    @jwt_required
    def post(self, post_public_id):
        """ Create a new comment on a post """
        # Get the post's id
        data = request.json
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return create_new_comment(post_public_id, data, current_user)

@api.route('/delete/<int:comment_id>')
class CommentDelete(Resource):

    @api.doc('Delete a comment',
        responses = {
            200: 'Comment has been deleted',
            403: 'This comment does not belong to the current user',
            404: 'Comment not found!'
        }
    )
    @jwt_required
    def delete(self, comment_id):
        """ Deletes a comment using its id """
        current_user = load_user(get_jwt_identity())
        return delete_comment(comment_id, current_user)