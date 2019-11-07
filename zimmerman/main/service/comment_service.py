from datetime import datetime
from uuid import uuid4

from zimmerman.main import db
from zimmerman.main.model.main import Comment, Post

from .user_service import load_author
from zimmerman.notification.service import send_notification

# Import Schema
from zimmerman.main.model.main import CommentLike, CommentSchema


def add_comment_and_flush(data):
    db.session.add(data)
    db.session.flush()

    comment_schema = CommentSchema()
    latest_comment = comment_schema.dump(data)

    db.session.commit()

    return latest_comment

def notify(object_public_id, target_owner_public_id):
    notif_data = dict(
        action="commented",
        object_type="comment",
        object_public_id=object_public_id,
    )
    send_notification(notif_data, target_owner_public_id)


class CommentService:
    def create(post_public_id, data, current_user):
        # Get the post
        post = Post.query.filter_by(public_id=post_public_id).first()

        # Assign the vars
        content = data["content"]

        # Validations
        limit = 1500
        if not content:
            response_object = {
                "success": False,
                "message": "Comment content not found!",
            }
            return response_object, 404

        elif len(content) > limit:
            response_object = {
                "success": False,
                "message": "Comment content exceeds limit (%s)" % limit,
            }
            return response_object, 403

        try:
            # Create new comment obj.
            new_comment = Comment(
                public_id=str(uuid4().int)[:15],
                creator_public_id=current_user.public_id,
                on_post=post.id,
                content=content,
                created=datetime.utcnow(),
            )

            latest_comment = add_comment_and_flush(new_comment)

            # Add the author's info
            latest_comment["author"] = load_author(latest_comment["creator_public_id"])

            # Send a notification to the post owner
            if current_user.public_id != post.creator_public_id:
                notify(latest_comment['public_id'], post.creator_public_id)

            response_object = {
                "success": True,
                "message": "Successfully commented on the post.",
                "comment": latest_comment,
            }
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500

    def delete(comment_id, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()
        if not comment:
            response_object = {"success": False, "message": "Comment not found!"}
            return response_object, 404

        # Check comment owner
        elif (
            current_user.public_id == comment.creator_public_id
        ):  # or is_admin(current_user)
            comment = Comment.query.filter_by(id=comment_id).first()

            try:
                db.session.delete(comment)
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": "Comment has successfully been deleted.",
                }
                return response_object, 200

            except Exception as error:
                print(error)
                response_object = {
                    "success": False,
                    "message": "Something went wrong during the process!",
                }
                return response_object, 500

        response_object = {"success": False, "message": "Insufficient permissions!"}
        return response_object, 403

    def update(comment_id, data, current_user):
        # Query for the comment
        comment = Comment.query.filter_by(id=comment_id).first()
        if not comment:
            response_object = {
                "success": False,
                "message": "Comment not found!",
                "error_reason": "commentNotFound",
            }
            return response_object, 404

        # Check comment owner
        elif current_user.public_id == comment.creator_public_id:
            # Get the new data:
            if not data["content"]:
                response_object = {
                    "success": False,
                    "message": "Content data not found!",
                    "error_reason": "noData",
                }
                return response_object, 404

            try:
                # Update the comment
                comment.content = data["content"]
                comment.edited = True
                # Commit the changes
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": "Comment has successfully been updated.",
                }
                return response_object, 200

            except Exception as error:
                print(error)
                response_object = {
                    "success": False,
                    "message": "Something went wrong during the process!",
                }
                return response_object, 500

        response_object = {
            "success": False,
            "message": "Insufficient permissions!",
            "error_reason": "permission",
        }
        return response_object, 403

    def get(comment_id):
        # Get the specific comment using its id
        comment = Comment.query.filter_by(id=comment_id).first()
        if not comment:
            response_object = {"success": False, "message": "Comment not found!"}
            return response_object, 404

        comment_schema = CommentSchema()
        comment_info = comment_schema.dump(comment)

        # Add the comment's author
        comment_info["author"] = load_author(comment_info["creator_public_id"])

        response_object = {
            "success": True,
            "message": "Comment info successfully sent.",
            "comment": comment_info,
        }
        return response_object, 200
