from uuid import uuid4
from datetime import datetime

from flask import jsonify, current_app
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.main.model.user import User, UserSchema

from .upload_service import get_image

private_info = (
    "password_hash",
    "id",
    "post_likes",
    "comment_likes",
    "reply_likes",
    "posts",
)


def load_author(user_public_id):
    # Add the author's essential details.
    user_schema = UserSchema()
    user = load_by_public_id(user_public_id)
    author = user_schema.dump(user)

    # Remove sensitive information
    for info in private_info:
        del author[info]

    # Add avatar if there are any
    if author["profile_picture"]:
        author["avatar"] = get_image(author["profile_picture"], "avatars")

    return author


def load_by_public_id(user_public_id):
    return User.query.filter_by(public_id=user_public_id).first()


def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class UserService:
    # Get user INFO by its username
    def get_user_info(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            response_object = {"success": False, "message": "User not found!"}
            return response_object, 404

        user_schema = UserSchema()
        user_info = user_schema.dump(user)

        unnecessary_info = ("password_hash", "id", "comment_likes", "reply_likes")
        # Remove unnecessary info
        for info in unnecessary_info:
            del user_info[info]

        # Add avatar if there are any
        if user_info["profile_picture"]:
            user_info["avatar"] = get_image(user_info["profile_picture"], "avatars")

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
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }

            return response_object, 500
