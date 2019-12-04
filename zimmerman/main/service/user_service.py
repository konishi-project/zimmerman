from uuid import uuid4
from datetime import datetime

from flask import current_app
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.util import Message, ErrResp

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
        resp = Message(False, "Current user does not exist!")
        resp["error_reason"] = "user_404"
        return resp, 404

    return user


class UserService:
    # Get user INFO by its username
    def get_user_info(username):
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            resp = Message(False, "User not found!")
            return resp, 404

        user_schema = UserSchema()
        user_info = user_schema.dump(user)

        # Remove unnecessary info
        for info in unnecessary_info:
            del user_info[info]

        # Add avatar
        user_info["avatar"] = (
            get_image(user.profile_picture, "avatars")
            if user.profile_picture is not None
            else None
        )


        resp = Message(True, "User data sent.")
        resp["user"] = user_info
        return resp, 200

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
            ErrResp()
