from uuid import uuid4
from flask import current_app

from zimmerman.utils import Message, InternalErrResp
from zimmerman.api.notification.util.main import notify

# Import models
from zimmerman.models.content import Comment, Post

from .utils import add_comment_and_flush, delete_comment, update_comment, load_comment


class CommentService:
    @staticmethod
    def create(post_public_id, data, current_user):
        # Get the post
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            resp = Message(False, "Post not found!")
            resp["error_reason"] = "post_404"
            return resp, 404

        # Assign the vars
        content = data["content"]

        # Validations
        limit = 1500
        if not content:
            resp = Message(False, "Comment content not found!")
            resp["error_reason"] = "comment_404"
            return resp, 404

        elif len(content) > limit:
            resp = Message(False, f"Comment content exceeds limits ({ limit })")
            return resp, 403

        try:
            # Create a new comment obj.
            new_comment = Comment(
                public_id=str(uuid4().int)[:15],
                owner_id=current_user.id,
                creator_public_id=current_user.public_id,
                on_post=post.id,
                content=content,
            )

            latest_comment = add_comment_and_flush(new_comment, current_user.id)

            # Notify post owner
            notify(
                "commented",
                "comment",
                latest_comment["public_id"],
                latest_comment["creator_public_id"],
            )

            resp = Message(True, "Successfully commented.")
            resp["comment"] = latest_comment
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def delete(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        if not comment:
            resp = Message(False, "Comment not found!")
            return resp, 204

        # Check comment owner
        elif current_user.public_id == comment.creator_public_id:
            try:
                delete_comment(comment)

                resp = Message(True, "Comment has been deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        resp = Message(False, "Insufficient permissions!")
        return resp, 403

    @staticmethod
    def update(comment_id, data, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        if not comment:
            resp = Message(False, "Comment not found!")
            resp["error_reason"] = "comment_404"
            return resp, 404

        # Check coment owner
        elif current_user.public_id == comment.creator_public_id:
            if not data["content"]:
                resp = Message(False, "Content data not found!")
                resp["error_reason"] = "data_404"
                return resp, 404

            try:
                update_comment(comment, data["content"])

                resp = Message(True, "Comment updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        resp = Message(False, "Insufficient permissions!")
        resp["error_reason"] = "insufficient_permissions"
        return resp, 403

    @staticmethod
    def get(comment_id, current_user):
        # Get the specific comment using its id
        comment = Comment.query.filter_by(id=comment_id).first()

        if not comment:
            resp = Message(False, "Comment not found!")
            return resp, 404

        comment_info = load_comment(comment, current_user.id)

        resp = Message(True, "Comment info sent.")
        resp["comment"] = comment_info
        return resp, 200
