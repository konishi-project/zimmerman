from flask import request
from flask_restplus import Resource
# from flask_jwt_extended import jwt_required

from ..util.dto import PostDto
from ..service.post_service import create_new_post

api = PostDto.api
_post = PostDto.post

@api.route('/create')
# @jwt_required
class PostCreate(Resource):

    @api.expect(_post, validate=True)
    @api.doc('Create a new post.', {
      responses = {
        201: 'Post created',
        401: 'Something went wrong during the process'
      }
    })
    def post(self):
        """ Creates new post """
        data = request.get_json()
        return create_new_post(data)