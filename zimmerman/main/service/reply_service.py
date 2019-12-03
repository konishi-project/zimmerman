from datetime import datetime
from uuid import uuid4
from flask import current_app

from zimmerman.main import db
from zimmerman.util import Message, ErrResp
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
            resp = Message(False, "Reply content not found!")
            return resp, 404

        elif len(content) > limit:
            resp = Message(False, "Reply content exceeds limit (%s)" % limit)
            return resp, 403

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

            resp = Message(True, "Replied on comment.")
            resp["reply"] = latest_reply
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            ErrResp()

    def delete(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            resp = Message(False, "Reply not found!")
            return resp, 404

        # Check reply owner
        elif (
            current_user.public_id == reply.creator_public_id
        ):  # or is_admin(current_user)
            try:
                # Delete the reply and commit
                db.session.delete(reply)
                db.session.commit()

                resp = Message(True, "Reply deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                ErrResp()

        resp = Message(False, "Insufficient permissions!")
        return resp, 403

    def update(reply_id, data, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            resp = Message(False, "Reply not found!")
            resp["error_reason"] = "reply_404"
            return resp, 404

        # Check reply owner
        elif current_user.public_id == reply.creator_public_id:
            # Get the new data
            if not data["content"]:
                resp = Message(False, "Content data not found!")
                resp["error_reason"] = "content_404"
                return resp, 404

            try:
                # Update the reply
                reply.content = data["content"]
                reply.edited = True
                # Commit the changes
                db.session.commit()

                resp = Message(True, "Reply updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                ErrResp()

        resp = Message(False, "Insufficient permissions!")
        resp["error_reason"] = "permission"
        return resp, 403

    def get(reply_id, current_user):
        # Get the specific reply using its id
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            resp = Message(False, "Reply not found!")
            return resp, 404

        reply_info = load_reply(reply, current_user.id)

        resp = Message(True, "Reply info sent.")
        resp["reply"] = reply_info
        return resp, 200
