from flask_restx import Namespace, fields


class NotificationDto:
    api = Namespace("notifications", description="Notification related operations.")
    notification = api.model(
        "notification",
        {
            "notification_ids": fields.List(
                fields.Integer, description="Array of Notification IDs"
            )
        },
    )
