from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from ..util.dto import CommentDto

# from ..service.comment_service import create_new_comment, delete_comment, update_comment, get_comment
from ..service.comment_service import Comment
from ..service.user_service import load_user

api = CommentDto.api
_comment = CommentDto.comment


@api.route("/get/<int:comment_id>")
class CommentGet(Resource):
    @api.doc(
        "Get a specific comment.",
        responses={
            200: "Commment has successfully been sent",
            404: "Comment not found!",
        },
    )
    @jwt_required
    def get(self, comment_id):
        """ Get a specific comment using its id """
        return Comment.get(comment_id)


@api.route("/create/<string:post_public_id>")
class CommentCreate(Resource):
    @api.expect(_comment, validate=True)
    @api.doc(
        "Comment on a post",
        responses={
            201: "Successfully commented on the post",
            403: "Comment content exceeds limit",
            401: "Post status is locked!",
        },
    )
    @jwt_required
    def post(self, post_public_id):
        """ Create a new comment on a post """
        # Get the comment's content
        data = request.get_json()
        # Get the current user
        current_user = load_user(get_jwt_identity())
        return Comment.create(post_public_id, data, current_user)


@api.route("/update/<int:comment_id>")
class CommentUpdate(Resource):
    @api.expect(_comment, validate=True)
    @api.doc(
        "Update a comment",
        responses={
            200: "Comment has been updated.",
            403: "User does not have permissions.",
            404: "Comment or comment data not found.",
        },
    )
    @jwt_required
    def put(self, comment_id):
        """ Updates a comment using its id and new content """
        current_user = load_user(get_jwt_identity())
        data = request.get_json()
        return Comment.update(comment_id, data, current_user)


@api.route("/delete/<int:comment_id>")
class CommentDelete(Resource):
    @api.doc(
        "Delete a comment",
        responses={
            200: "Comment has been deleted",
            403: "This comment does not belong to the current user",
            404: "Comment not found!",
        },
    )
    @jwt_required
    def delete(self, comment_id):
        """ Deletes a comment using its id """
        current_user = load_user(get_jwt_identity())
        return Comment.delete(comment_id, current_user)
