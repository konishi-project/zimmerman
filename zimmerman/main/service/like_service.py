from datetime import datetime

from zimmerman.main import db
from zimmerman.notification.service import send_notification
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


def notify(object_type, object_public_id, target_owner_public_id):
    notif_data = dict(
        action="liked", object_type=object_type, object_public_id=object_public_id
    )
    send_notification(notif_data, target_owner_public_id)


class Like:
    def post(post_public_id, current_user):
        # Query for the post using its public id
        post = Post.query.filter_by(public_id=post_public_id).first()

        # Check if the post exists
        if not post:
            response_object = {"success": False, "message": "Post not found!"}
            return response_object, 404

        if check_like(post.likes, current_user.id):
            response_object = {
                "success": False,
                "message": "User has already liked the post.",
            }
            return response_object, 403

        # Create a new like obj.
        post_like = PostLike(
            on_post=post.id, owner_id=current_user.id, liked_on=datetime.utcnow()
        )

        # Commit the changes
        try:
            # Notify post owner
            if current_user.public_id != post.creator_public_id:
                notify("post", post.public_id, post.creator_public_id)

            add_like(post_like)
            return "", 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something failed during the process!",
            }
            return response_object, 500

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
                notify("comment", comment.public_id, comment.creator_public_id)

            add_like(comment_like)

            response_object = {
                "success": True,
                "message": "User has liked the comment.",
            }
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500

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
                notify("reply", reply.public_id, reply.creator_public_id)

            db.session.add(like_reply)
            db.session.commit()

            return "", 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500


class Unlike:
    def post(post_public_id, current_user):
        # Query for the post
        post = Post.query.filter_by(public_id=post_public_id).first()

        for like in post.likes:
            if like.owner_id == current_user.id:
                try:
                    remove_like(like)
                    return "", 200

                except Exception as error:
                    print(error)
                    response_object = {
                        "success": False,
                        "message": "Something went wrong during the process!",
                    }
                    return response_object, 500

            # Return 404 if item isn't found
            return "", 404

    def comment(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        for like in comment.likes:
            if like.owner_id == current_user.id:
                try:
                    remove_like(like)
                    return "", 200

                except Exception as error:
                    print(error)
                    response_object = {
                        "success": False,
                        "message": "Something went wrong during the process!",
                    }
                    return response_object, 500

            # Return 404 if item isn't found
            return "", 404

    def reply(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        for like in reply.likes:
            if like.owner_id == current_user.id:
                try:
                    remove_like(like)
                    return "", 204

                except Exception as error:
                    print(error)
                    response_object = {
                        "success": False,
                        "message": "Something went wrong during the process!",
                    }
                    return response_object, 500

            return "", 404
