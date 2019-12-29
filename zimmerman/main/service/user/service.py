from uuid import uuid4
from datetime import datetime

from flask import current_app
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.util import Message, InternalErrResp

from zimmerman.main.model.main import User

from .utils import load_info

from ..upload_service import get_image


class UserService:
    # Get user INFO by its username
    @staticmethod
    def get_user_info(username):
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            resp = Message(False, "User not found!")
            return resp, 404

        user_info = load_info(user)

        resp = Message(True, "User data sent.")
        resp["user"] = user_info
        return resp, 200

    # Update this method
    @staticmethod
    def update(data, current_user):
        # Get the user
        user = User.query.filter_by(id=current_user.id).first()

        if not user:
            resp = Message(False, "User not found!")
            return resp, 404

        # Check if the current user is the same as the one being updated.
        try:
            if data["bio"] is not None and len(data["bio"]) > 0:
                # Check if the bio does not exceed limits
                if 1 <= len(data["bio"]) <= 150:
                    user.bio = data["bio"]

                else:
                    resp = Message(False, "Bio content is invalid!")
                    return resp, 403

            if data["avatar"] is not None:
                user.profile_picture = data["avatar"]

            # Commit the changes
            db.session.commit()

            resp = Message(True, "User data updated.")
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()

    # Add user deletion
