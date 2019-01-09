from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import PostDto
from ..service.post_service import create_new_post, delete_post
from ..service.user_service import load_user


api = PostDto.api
_post = PostDto.post

@api.route('/create')
class PostCreate(Resource):

    @api.expect(_post, validate=True)
    @api.doc('Create a new post.', 
      responses = {
        201: 'Post created',
        401: 'Something went wrong during the process'
      }
    )
    @jwt_required
    def post(self):
        """ Creates new post """
        data = request.get_json()
        current_user = load_user(get_jwt_identity())
        return create_new_post(data, current_user)
  
@api.route('/delete/<int:post_id>')
class PostDelete(Resource):

    @api.doc('Delete a post',
      responses = {
        200: 'Post has successfully been deleted',
        403: 'You do not have permission to delete the post',
        404: 'Post not found!'
      }
    )
    @jwt_required
    def delete(self, post_id):
        """ Deletes a post by id """
        current_user = load_user(get_jwt_identity())
        return delete_post(post_id, current_user)