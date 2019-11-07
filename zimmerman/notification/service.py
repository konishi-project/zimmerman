from flask import jsonify
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from zimmerman.main import db
from zimmerman.main.model.main import Notification, NotificationSchema, User
from zimmerman.main.service.user_service import load_user, load_author

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

    notification_schema = NotificationSchema()
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
        response_object = {
            "success": False,
            "message": "Invalid action!",
            "error_reason": "action_invalid",
        }
        return response_object, 403

    # Validate
    if object_type not in allowed_types:
        response_object = {
            "success": False,
            "message": "Object type is invalid!",
            "error_reason": "object_invalid",
        }
        return response_object, 403

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

        response_object = {
            "success": True,
            "message": "Notification has been created.",
            "notification": latest_notification,
        }
        return response_object, 201

    except Exception as error:
        print(error)
        response_object = {
            "success": False,
            "message": "Something went wrong during the process!",
            "error_reason": "server_error",
        }
        return response_object, 500


class NotificationService:
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

            response_object = {
                "success": True,
                "message": "Sent notification IDs",
                "notif_ids": ids,
            }
            return response_object

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_error",
            }
            return response_object, 500

    def get_notifs_info(id_array, current_user):
        notif_schema = NotificationSchema()
        notifs = []

        # Check if the array is empty
        if len(id_array) == 0 or id_array is None:
            return None, 204

        try:
            for notif_id in id_array:
                # Get the notif and dump
                notif = Notification.query.get(notif_id)
                # Dump the data and append it to notifs
                notif_info = notif_schema.dump(notif)
                # Load the actor as user
                notif_info["user"] = load_author(notif_info['actor'])

                notifs.append(notif_info)

            response_object = {
                "success": True,
                "message": "Notifications successfully sent.",
                "notifications": notifs,
            }
            return response_object, 200

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_error",
            }
            return response_object, 500

    def read_notifications():
        try:
            pass
        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_error",
            }
            return response_object, 500
