from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from zimmerman.main import limiter
from .service import NotificationService
from .util.dto import NotificationDto

api = NotificationDto.api
notification = NotificationDto.notification

@api.route('/notifications')
class NotificationGet(Resource):
    """ Get user notifications endpoint
    Hit the endpoint with the user's public id.
    """
    @jwt_required
    def get(self, user_public_id):
        pass

@api.route('/notifications/read')

    """ Set notifications as read
    The client sends an array of notification IDs.
    Then the backend will set them as read.
    """
    @jwt_required
    def put(self):
        data = request.get_json()
        pass