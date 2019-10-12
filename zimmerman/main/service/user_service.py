from uuid import uuid4
from datetime import datetime

from flask import jsonify, current_app
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.main.model.user import User, UserSchema

from .upload_service import get_image


def load_author(user_public_id):
    # Add the author's essential details.
    user_schema = UserSchema()
    user = load_by_public_id(user_public_id)
    author = user_schema.dump(user)

    # Remove sensitive information
    unnecessary_info = (
        "password_hash",
        "id",
        "post_likes",
        "comment_likes",
        "reply_likes",
        "posts",
    )
    for info in unnecessary_info:
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
    def register(data):
        try:
            # Assign the vars
            email = data["email"]
            username = data["username"]
            password = data["password"]
            entry_key = data["entry_key"]

            first_name = data["first_name"]
            last_name = data["last_name"]

            # Check if the email is used
            if User.query.filter_by(email=email).first() is not None:
                response_object = {
                    "success": False,
                    "message": "Email is being used in another account!",
                    "error_reason": "email_taken",
                }
                return response_object, 403

            # Check if the username is equal to or between 4 and 15
            elif not 4 <= len(username) <= 15:
                response_object = {
                    "success": False,
                    "message": "User name length is invalid!",
                    "error_reason": "username_length",
                }
                return response_object, 403

            # Check if the username is alpha numeric
            elif not username.isalnum():
                response_object = {
                    "success": False,
                    "message": "Username is not alpha numeric!",
                    "error_reason": "username_not_alpha_numeric",
                }
                return response_object, 403

            # Verify the first name if it exists
            if len(first_name) == 0 or first_name is None:
                first_name = None

            else:
                # Check if the first name is alphabetical
                if not first_name.isalpha():
                    response_object = {
                        "success": False,
                        "message": "First name is not alphabetical.",
                        "error_reason": "first_name_nonalpha",
                    }
                    return response_object, 403

                # Check if the first name is equal to or between 2 and 50
                if not 2 <= len(first_name) <= 50:
                    response_object = {
                        "success": False,
                        "message": "First name length is invalid!",
                        "error_reason": "first_name_length",
                    }
                    return response_object, 403

            # Verify last name
            if len(last_name) == 0 or last_name is None:
                last_name = None

            else:
                # Check if the last name is alphabetical
                if not last_name.isalpha():
                    response_object = {
                        "success": False,
                        "message": "Last name is not alphabetical.",
                        "error_reason": "name_not alphabetical",
                    }
                    return response_object, 403

                # Check if the last name is equal to or between 2 and 50
                if not 2 <= len(last_name) <= 50:
                    response_object = {
                        "success": False,
                        "message": "Last name length is invalid",
                        "error_reason": "last_name_length",
                    }
                    return response_object, 403

            # Check if the entry key is right
            if entry_key != current_app.config["ENTRY_KEY"]:
                response_object = {
                    "success": False,
                    "message": "Entry key is invalid!",
                    "error_reason": "entry_key",
                }
                return response_object, 403

            new_user = User(
                public_id=str(uuid4().int)[:15],
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                joined_date=datetime.now(),
            )

            # Add and commit the user to the database
            db.session.add(new_user)
            db.session.commit()

            # Return success response
            response_object = {
                "success": True,
                "message": "User has successfully been registered",
            }
            return response_object, 201

        except Exception as error:
            response_object = {
                "success": False,
                "message": 'Something went wrong during the process!\nOutput: "%s"'
                % error,
            }
            return response_object, 500

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
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!\nOutput: %s"
                % error,
            }
            return response_object, 500
