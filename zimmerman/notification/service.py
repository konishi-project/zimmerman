from flask import current_app

from zimmerman.util import Message, InternalErrResp

from zimmerman.main.model.notification import Notification

from ..main.service.feed.utils import uniq
from ..main.service.user.utils import load_user, user_schema, filter_author

from .util.main import notifications_schema
from .util.main import notification_schema

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


class NotificationService:
    @staticmethod
    def get_notification_ids(current_user):
        try:
            notifs = (
                Notification.query.filter_by(target_owner=current_user.id)
                .with_entities(Notification.id, Notification.timestamp)
                .all()
            )
            notification_info = notifications_schema.dump(notifs)

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
            return InternalErrResp()

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
            return InternalErrResp()

    @staticmethod
    def read_notifications():
        try:
            pass
        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()
