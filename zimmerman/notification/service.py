from flask import current_app
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from zimmerman.main import db
from zimmerman.util import Message, InternalErrResp
from zimmerman.main.model.main import Notification, User

from zimmerman.main.service.user.utils import load_user, filter_author

# Import schemas
from zimmerman.main.model.schemas import UserSchema, NotificationSchema

"""
Notification flow:
When the actor commits an action, it'll create a notification
and add it to the target owner's notifications.

If the target object has the same owner, then no need to create
a notification. All of this must be handled by the backend.

Example:
User *likes* a post -> Create a notification to the post's owner
(if User == Post owner) then ignore notification creation.
"""

# Define schema
notification_schema = NotificationSchema()
user_schema = UserSchema()

allowed_types = ("post", "comment", "reply")
# Add more if needed
valid_actions = ("replied", "liked", "commented")


def uniq(a_list):
    encountered = set()
    result = []
    for elem in a_list:
        if elem not in encountered:
            result.append(elem)
        encountered.add(elem)
    return result


def add_notification_and_flush(data):
    db.session.add(data)
    db.session.flush()

    latest_notification = notification_schema.dump(data)

    db.session.commit()

    return latest_notification


# Creates and sends the notification to the user.
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

    # Check if notification exists.
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

        latest_notification = add_notification_and_flush(new_notification)

        resp = Message(True, "Notification has been created.")
        resp["notification"] = latest_notification
        return resp, 201

    except Exception as error:
        current_app.logger.error(error)
        InternalErrResp()


class NotificationService:
    @staticmethod
    def get_notification_ids(current_user):
        try:
            notifs = (
                Notification.query.filter_by(target_owner=current_user.id)
                .with_entities(Notification.id, Notification.timestamp)
                .all()
            )
            notification_schema = NotificationSchema(many=True)
            notification_info = notification_schema.dump(notifs)

            ids = uniq(
                x["id"]
                for x in sorted(
                    notification_info, key=lambda x: x["timestamp"], reverse=True
                )
            )

            resp = Message(True, "Sent notification IDs.")
            resp["notif_ids"] = ids
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()

    @staticmethod
    def get_notifs_info(id_array, current_user):
        # Check if the array is empty
        if len(id_array) == 0 or id_array is None:
            return None, 204

        notifs = []

        notif_query = Notification.query.filter(Notification.id.in_(id_array)).all()

        try:
            for notification in notif_query:
                notif_info = notification_schema.dump(notification)

                # Load the actor as user
                actor = load_user(notif_info["actor"])
                actor_info = user_schema.dump(actor)
                notif_info["actor_info"] = filter_author(actor_info)

                notifs.append(notif_info)

            # Re-sort it back to the original array
            res = [notif for id in id_array for notif in notifs if notif["id"] == id]

            resp = Message(True, "Notifications sent.")
            resp["notifications"] = res
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()

    @staticmethod
    def read_notifications():
        try:
            pass
        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()
