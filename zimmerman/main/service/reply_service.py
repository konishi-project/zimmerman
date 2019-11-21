from datetime import datetime
from uuid import uuid4

from zimmerman.main import db
from zimmerman.main.model.main import Reply, Comment
from zimmerman.notification.service import send_notification
from .user_service import filter_author
from .like_service import check_like

# Import Schema
from zimmerman.main.model.schemas import ReplySchema, UserSchema

# Define schema
reply_schema = ReplySchema()
user_schema = UserSchema()


def add_reply_and_flush(data, user_id):
    db.session.add(data)
    db.session.flush()

    latest_reply = load_reply(data, user_id)

    db.session.commit()

    return latest_reply


def notify(object_public_id, target_owner_public_id):
    notif_data = dict(
        action="replied", object_type="reply", object_public_id=object_public_id
    )
    send_notification(notif_data, target_owner_public_id)


def load_reply(reply, user_id):
    reply_info = reply_schema.dump(reply)

    # Set the author
    author = user_schema.dump(reply.author)
    reply_info["author"] = filter_author(author)

    # Return boolean
    reply_info["liked"] = check_like(reply.likes, user_id)

    # Filter reply

    return reply_info


class ReplyService:
    def create(comment_id, data, current_user):
        # Get the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        # Assign the vars
        content = data["content"]

        # Validations
        limit = 1500
        if not content:
            response_object = {"success": False, "message": "Reply content not found!"}
            return response_object, 404

        elif len(content) > limit:
            response_object = {
                "success": False,
                "message": "Reply content exceeds limit (%s)" % limit,
            }
            return response_object, 403

        try:
            # Create new reply obj.
            new_reply = Reply(
                public_id=str(uuid4().int)[:15],
                owner_id=current_user.id,
                creator_public_id=current_user.public_id,
                on_comment=comment.id,
                content=content,
                created=datetime.utcnow(),
            )

            latest_reply = add_reply_and_flush(new_reply, current_user.id)

            response_object = {
                "success": True,
                "message": "Successfully replied on the comment.",
                "reply": latest_reply,
            }
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500

    def delete(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            response_object = {"success": False, "message": "Reply not found!"}
            return response_object, 404

        # Check reply owner
        elif (
            current_user.public_id == reply.creator_public_id
        ):  # or is_admin(current_user)
            try:
                # Delete the reply and commit
                db.session.delete(reply)
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": "Reply has successfully been deleted.",
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

    def update(reply_id, data, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            response_object = {
                "success": False,
                "message": "Reply not found!",
                "error_reason": "replyNotFound",
            }
            return response_object, 404

        # Check reply owner
        elif current_user.public_id == reply.creator_public_id:
            # Get the new data
            if not data["content"]:
                response_object = {
                    "success": False,
                    "message": "Content data not found!",
                    "error_reason": "noData",
                }

            try:
                # Update the reply
                reply.content = data["content"]
                reply.edited = True
                # Commit the changes
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": "Reply has successfully been updated.",
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

    def get(reply_id, current_user):
        # Get the specific reply using its id
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            response_object = {"success": False, "message": "Reply not found!"}
            return response_object, 404

        reply_info = load_reply(reply, current_user.id)

        response_object = {
            "success": True,
            "message": "Reply info successfully sent.",
            "reply": reply_info,
        }
        return response_object, 200
