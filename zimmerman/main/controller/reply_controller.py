from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import ReplyDto
from ..service.reply_service import create_new_reply, delete_reply, update_reply, get_reply
from ..service.user_service import load_user

api = ReplyDto.api
_reply = ReplyDto.reply

@api.route('/get/<int:reply_id>')
class ReplyGet(Resource):

    @api.doc('Get a specific reply.',
        reponses = {
            200: 'Reply has successfully been received by client.',
            404: 'Reply not found!'
        }
    )
    @jwt_required
    def get(self, reply_id):
        """ Get a specific reply using its id """
        return get_reply(reply_id)

@api.route('/create/<int:comment_id>')
class ReplyCreate(Resource):

    @api.doc('Reply on a comment',
        responses = {
            201: 'Successfully replied on the comment.',
            403: 'Reply content exceeds limit'
        }
    )
    @jwt_required
    def post(self, comment_id):
        """ Create a new reply on a comment """
        # Get the content
        data = request.get_json()
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return create_new_reply(comment_id, data, current_user)

@api.route('/update/<int:reply_id>')
class ReplyUpdate(Resource):

    @api.expect(_reply, validate=True)
    @api.doc('Update a reply',
        responses = {
            200: 'Reply has been updated.',
            403: 'User does not have permissions.',
            404: 'Reply or reply data not found.'
        }
    )
    @jwt_required
    def put(self, reply_id):
        """ Updates a reply using its id and new content """
        # Get the new content
        data = request.get_json()
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return update_reply(reply_id, data, current_user)

@api.route('/delete/<int:reply_id>')
class ReplyDelete(Resource):

    @api.doc('Delete a reply',
        responses = {
            200: 'Reply has been deleted.',
            403: 'User does not have permissions.',
            404: 'Reply not found!'
        }
    )
    @jwt_required
    def delete(self, reply_id):
        """ Deletes a reply using its id """
        current_user = load_user(get_jwt_identity())
        return delete_reply(reply_id, current_user)