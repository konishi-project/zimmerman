from datetime import datetime
from flask import current_app
from flask_jwt_extended import get_jwt_identity

from zimmerman import db
from zimmerman.utils import Message, InternalErrResp
from zimmerman.api.main.service.user.utils import load_user

# Import model/schemas
from zimmerman.models.user import User
from zimmerman.models.notification import Notification
from zimmerman.models.schemas import UserSchema, NotificationSchema

# Define deserializers
notifications_schema = NotificationSchema(many=True)
notification_schema = NotificationSchema()
user_schema = UserSchema()

allowed_types = ("post", "comment", "reply")
# Add more if needed
valid_actions = ("replied", "liked", "commented")


def notify(action, object_type, object_public_id, target_owner_public_id):
    notif_data = dict(
        action=action, object_type=object_type, object_public_id=object_public_id
    )
    send_notification(notif_data, target_owner_public_id)


def send_notification(data, target_user_public_id):

    actor = load_user(get_jwt_identity())
    action = data["action"]

    # Post, Comment, Reply, etc.
    object_type = data["object_type"]
    object_public_id = data["object_public_id"]

    # Get the target user
    target_user = User.query.filter_by(public_id=target_user_public_id).first()

    if action not in valid_actions:
        resp = Message(False, "Invalid action!")
        resp["error_reason"] = "action_invalid"
        return resp, 403

    # Validate
    if object_type not in allowed_types:
        resp = Message(False, "Object type is invalid!")
        resp["error_reason"] = "object_invalid"
        return resp, 403

    notification = Notification.query.filter_by(
        object_type=object_type, object_public_id=object_public_id
    ).first()

    if notification is not None:
        return None, 204

    try:
        new_notification = Notification(
            target_owner=target_user.id,
            actor=actor.public_id,
            action=action,
            timestamp=datetime.utcnow(),
            object_type=object_type,
            object_public_id=object_public_id,
        )

        db.session.add(new_notification)
        db.session.commit()

        resp = Message(True, "Notification has been created.")
        return resp, 201

    except Exception as error:
        current_app.logger.error(error)
        return InternalErrResp()
