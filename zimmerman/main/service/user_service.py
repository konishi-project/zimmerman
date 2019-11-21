from uuid import uuid4
from datetime import datetime

from flask import current_app
from flask_jwt_extended import create_access_token

from zimmerman.main import db

from zimmerman.main.model.main import User
from zimmerman.main.model.schemas import UserSchema

from .upload_service import get_image

private_info = (
    "password_hash",
    "id",
    "post_likes",
    "comment_likes",
    "reply_likes",
    "posts",
    "comments",
    "replies",
    "notifications",
)

unnecessary_info = ("password_hash", "id", "comment_likes", "reply_likes")


def filter_author(user):
    # Remove sensitive information
    for info in private_info:
        del user[info]

    # Add the avatar
    user["avatar"] = (
        get_image(user["profile_picture"], "avatars")
        if user["profile_picture"] is not None
        else None
    )

    return user


def load_user(identififer):
    # If the user_id is an int then use id
    if type(identififer) == int:
        user = User.query.filter_by(id=identififer).first()

    # Use public id
    else:
        user = User.query.filter_by(public_id=identififer).first()

    if not user:
        response_object = {
            "success": False,
            "message": "Current user does not exist!",
            "error_reason": "non_existent",
        }
        return response_object, 403

    return user


class UserService:
    # Get user INFO by its username
    def get_user_info(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            response_object = {"success": False, "message": "User not found!"}
            return response_object, 404

        user_schema = UserSchema()
        user_info = user_schema.dump(user)

        # Remove unnecessary info
        for info in unnecessary_info:
            del user_info[info]

        # Add avatar
        user["avatar"] = (
            get_image(user["profile_picture"], "avatars")
            if user["profile_picture"] is not None
            else None
        )

        response_object = {
            "success": True,
            "message": "User data sent.",
            "user": user_info,
        }
        return response_object, 200

    def update(data, current_user):
        # Get the user
        user = User.query.filter_by(id=current_user.id).first()

        if not user:
            response_object = {"success": False, "message": "User not found!"}
            return response_object, 404

        # Check if the current user is the same as the one being updated.
        try:
            if data["bio"] is not None and len(data["bio"]) > 0:
                # Check if the bio does not exceed limits
                if 1 <= len(data["bio"]) <= 150:
                    user.bio = data["bio"]

                else:
                    response_object = {
                        "success": False,
                        "message": "Bio content is invalid!",
                    }
                    return response_object, 403

            if data["avatar"] is not None:
                user.profile_picture = data["avatar"]

            # Commit the changes
            db.session.commit()
            response_object = {
                "success": True,
                "message": "User data has successfully been updated.",
            }
            return response_object, 200

        except Exception as error:
            current_app.logger.error(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }

            return response_object, 500
