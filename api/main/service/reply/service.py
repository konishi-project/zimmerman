from uuid import uuid4
from flask import current_app

from api.util import Message, InternalErrResp
from api.notification.util.main import notify

# Import models
from api.main.model.post import Reply, Comment

from .utils import add_reply_and_flush, delete_reply, update_reply, load_reply


class ReplyService:
    @staticmethod
    def create(comment_id, data, current_user):
        # Get the comment
        comment = Comment.query.filter_by(id=comment_id).first()

        if not comment:
            resp = Message(False, "Comment not found!")
            resp["error_reason"] = "comment_404"
            return resp, 404

        # Assign the vars
        content = data["content"]
        limit = 1500

        if not content:
            resp = Message(False, "Reply content not found!")
            return resp, 404

        elif len(content) > limit:
            resp = Message(False, f"Reply content exceeds limits ({ limit })")
            return resp, 403

        try:
            # Create new reply obj.
            new_reply = Reply(
                public_id=str(uuid4().int)[:15],
                owner_id=current_user.id,
                creator_public_id=current_user.public_id,
                on_comment=comment.id,
                content=content,
            )

            latest_reply = add_reply_and_flush(new_reply, current_user.id)

            # Notify commenter
            notify(
                "replied",
                "reply",
                latest_reply["public_id"],
                latest_reply["creator_public_id"],
            )

            resp = Message(True, "Replied on comment.")
            resp["reply"] = latest_reply
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def delete(reply_id, current_user):
        # Query for the reply
        reply = Reply.query.filter_by(id=reply_id).first()

        if not reply:
            resp = Message(False, "Reply not found!")
            return resp, 404

        # Check reply owner
        elif current_user.public_id == reply.creator_public_id:
            try:
                delete_reply(reply)

                resp = Message(True, "Reply has been deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        resp = Message(False, "Insufficient permissions!")
        resp["error_reason"] = "insufficient_permissions"
        return resp, 403

    @staticmethod
    def update(reply_id, data, current_user):
        reply = Reply.query.filter_by(id=reply_id).first()

        if not reply:
            resp = Message(False, "Reply not found!")
            resp["error_reason"] = "reply_404"
            return resp, 404

            try:
                update_reply(reply, data["content"])

                resp = Message(True, "Reply updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        resp = Message(False, "Insufficient permissions!")
        resp["error_reason"] = "insufficient_permissions"
        return resp, 403

    @staticmethod
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
