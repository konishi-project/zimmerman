from datetime import datetime
from flask import current_app

from zimmerman.main import db
from zimmerman.util import Message, InternalErrResp
from zimmerman.notification.util.main import notify
from zimmerman.main.model.main import (
    Post,
    Comment,
    Reply,
)

# Import like models
from zimmerman.main.model.likes import PostLike, CommentLike, ReplyLike


def check_like(item_likes, user_id):
    for like in item_likes:
        if user_id == like.owner_id:
            return True

        return False


def remove_like(like):
    db.session.delete(like)
    db.session.commit()


def add_like(like):
    db.session.add(like)
    db.session.commit()


class Like:
    @staticmethod
    def post(post_public_id, current_user):
        # Query for the post using its public id
        post = Post.query.filter_by(public_id=post_public_id).first()

        # Check if the post exists
        if not post:
            resp = Message(False, "Post not found!")
            return resp, 404

        if check_like(post.likes, current_user.id):
            resp = Message(False, "User already liked.")
            return resp, 403

        # Create a new like obj.
        post_like = PostLike(
            on_post=post.id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        # Commit the changes
        try:
            # Notify post owner
            if current_user.public_id != post.creator_public_id:
                notify("liked", "post", post.public_id, post.creator_public_id)

            add_like(post_like)
            return "", 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def comment(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        # Check if the comment exists
        if not comment:
            return "", 404

        # Check if the user already liked
        if check_like(comment.likes, current_user.id):
            return "", 403

        # Create a new like obj.
        comment_like = CommentLike(
            on_comment=comment_id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        try:
            # Notify comment owner
            if current_user.public_id != comment.creator_public_id:
                notify("liked", "comment", comment.public_id, comment.creator_public_id)

            add_like(comment_like)

            resp = Message(True, "User has liked the comment.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def reply(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()

        # Check if the reply exists
        if not reply:
            return "", 404

        # Check if the user already liked
        if check_like(reply.likes, current_user.id):
            return "", 403

        # Create a new like obj.
        like_reply = ReplyLike(
            on_reply=reply_id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        try:
            # Notify reply owner
            if current_user.public_id != reply.creator_public_id:
                notify("liked", "reply", reply.public_id, reply.creator_public_id)

            db.session.add(like_reply)
            db.session.commit()

            return "", 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()


class Unlike:
    @staticmethod
    def post(post_public_id, current_user):
        # Query for the post
        post = Post.query.filter_by(public_id=post_public_id).first()

        for like in post.likes:
            if like.owner_id == current_user.id:
                try:
                    remove_like(like)
                    return "", 200

                except Exception as error:
                    current_app.logger.error(error)
                    return InternalErrResp()

            # Return 404 if item isn't found
            return "", 404

    @staticmethod
    def comment(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        for like in comment.likes:
            if like.owner_id == current_user.id:
                try:
                    remove_like(like)
                    return "", 200

                except Exception as error:
                    current_app.logger.error(error)
                    return InternalErrResp()

            # Return 404 if item isn't found
            return "", 404

    @staticmethod
    def reply(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        for like in reply.likes:
            if like.owner_id == current_user.id:
                try:
                    remove_like(like)
                    return "", 204

                except Exception as error:
                    current_app.logger.error(error)
                    return InternalErrResp()

            return "", 404
