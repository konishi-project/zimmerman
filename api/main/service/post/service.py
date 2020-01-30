from uuid import uuid4
from flask import current_app

from zimmerman.util import Message, InternalErrResp

# Import models
from zimmerman.main.model.post import Post

from .utils import add_post_and_flush, delete_post, update_post, load_post


class PostService:
    @staticmethod
    def create(data, current_user):
        # Assign the vars
        content = data["content"]
        image_id = data["image_id"]

        # Check if the content doesn't exceed limit
        # This limit is temporary and can be changed, 2000 is just for testing
        limit = 2000
        if not content:
            resp = Message(False, "Content can't be empty!")
            return resp, 403

        elif len(content) > limit:
            resp = Message(False, f"Content exceeds limits ({ limit })")
            return resp, 403

        try:
            new_post = Post(
                public_id=str(uuid4().int)[:15],
                owner_id=current_user.id,
                creator_public_id=current_user.public_id,
                content=content,
                image_file=image_id,
            )

            latest_post = add_post_and_flush(new_post, current_user.id)

            resp = Message(True, "Post created.")
            resp["post"] = latest_post
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def delete(post_public_id, current_user):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            resp = Message(False, "Post not found!")
            resp["error_reason"] = "post_404"
            return resp, 404

        # Check post owner
        elif (
            current_user.public_id == post.creator_public_id
        ):  # or is_admin(current_user)
            try:
                delete_post(post)

                resp = Message(True, "Post has been deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        resp = Message(False, "Insufficient permissions!")
        return resp, 403

    @staticmethod
    def update(post_public_id, data, current_user):
        # Query for the post
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            resp = Message(False, "Post not found!")
            resp["error_reason"] = "post_404"
            return resp, 404

        # Check post owner
        elif current_user.public_id == post.creator_public_id:
            if not data["content"]:
                resp = Message(False, "Content data not found!")
                resp["error_reason"] = "data_404"
                return resp, 404

            try:
                update_post(post, data["content"])

                resp = Message(True, "Post updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        # Check if post is locked
        elif post.status.lower() == "locked":
            resp = Message(False, "Post is locked!")
            resp["error_reason"] = "post_locked"
            return resp, 403

        resp = Message(False, "Insufficient permissions!")
        resp["error_reason"] = "insufficient_permissions"
        return resp, 403

    @staticmethod
    def get(post_public_id, current_user):
        # Get the specific post using its public id
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            resp = Message(False, "Post not found!")
            resp["error_reason"] = "data_404"
            return resp, 404

        post_info = load_post(post, current_user.id)

        resp = Message(True, "Post info sent.")
        resp["post"] = post_info
        return resp, 200
