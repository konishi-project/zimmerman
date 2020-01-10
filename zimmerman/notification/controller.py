from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from zimmerman.main.service.user.utils import load_user

from .service import NotificationService
from .util.dto import NotificationDto

api = NotificationDto.api
_notification = NotificationDto.notification

# Add rate limiting


@api.route("/get")
class NotificationGet(Resource):
    @api.doc(
        "Get Notification IDs",
        responses={
            200: "Notification IDs successfully sent to the client.",
            500: "Server Error",
        },
    )
    @jwt_required
    def get(self):
        """ Get user notifications IDs """
        current_user = load_user(get_jwt_identity())
        return NotificationService.get_notification_ids(current_user)

    """ Get user notifications' info
    User hits the endpoint with array of IDs
    and returns the information.
    """

    @api.expect(_notification, validate=True)
    @api.doc(
        "Get the notifications' data",
        responses={200: "Notification data successfully sent to the client."},
    )
    @jwt_required
    def post(self):
        """ Get notifications' data """
        data = request.get_json()
        notif_ids = data["notification_ids"]
        current_user = load_user(get_jwt_identity())
        return NotificationService.get_notifs_info(notif_ids, current_user)


@api.route("/read")
class NotificationRead(Resource):
    """ Set notifications as read
    The client sends an array of notification IDs.
    Then the backend will set them as read.
    """

    @jwt_required
    def put(self):
        """ Set notifications as read """
        data = request.get_json()
        notif_ids = data["notif_ids"]
        current_user = load_user(get_jwt_identity())
        return NotificationService.read_notifications()
