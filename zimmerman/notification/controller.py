from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from zimmerman.main.service.user_service import load_user
from .service import NotificationService
from .util.dto import NotificationDto

api = NotificationDto.api
notification = NotificationDto.notification


@api.route("/get")
class NotificationGet(Resource):
    """ 
    Get user notifications IDs
    """

    @jwt_required
    def get(self):
        current_user = load_user(get_jwt_identity())
        return NotificationService.get_notification_ids(current_user)


@api.route("/get")
class NotificationGetInfo(Resource):
    """ Get user notifications' info
    User hits the endpoint with array of IDs
    and returns the information.
    """

    @jwt_required
    def post(self):
        data = request.get_json()
        notif_ids = data["notif_ids"]
        return NotificationService.get_notification_info(notif_ids)


@api.route("/read")
class NotificationRead(Resource):
    """ Set notifications as read
    The client sends an array of notification IDs.
    Then the backend will set them as read.
    """

    @jwt_required
    def put(self):
        data = request.get_json()
        notif_ids = data["notif_ids"]
        current_user = load_user(get_jwt_identity())
        return NotificationService.read_notifications()
