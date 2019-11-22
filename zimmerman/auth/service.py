import re

from flask import current_app
from flask_jwt_extended import create_access_token
from datetime import datetime
from uuid import uuid4

from zimmerman.main import db
from zimmerman.main.service.upload_service import get_image
from zimmerman.main.service.user_service import private_info


from zimmerman.main.model.main import User
from zimmerman.main.model.schemas import UserSchema

# Basic email regex check.
EMAIl_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class Auth:
    @staticmethod
    def login_user(data):
        # Assign variables
        email = data["email"]
        password = data["password"]

        try:
            # Check if email or password was provided
            if not email or not password:
                response_object = {
                    "success": False,
                    "message": "Credentials not fully provided",
                    "error_reason": "no_credentials",
                }
                return response_object, 403

            # Fetch the user data
            user = User.query.filter_by(email=email).first()
            if not user:
                response_object = {
                    "success": False,
                    "message": "The email you have entered does not match any account.",
                    "error_reason": "email_404",
                }
                return response_object, 404

            elif user and user.check_password(password):
                user_schema = UserSchema()
                user_info = user_schema.dump(user)

                # Remove sensitive information
                for info in private_info:
                    del user_info[info]

                # Check if the user has an avatar
                if user_info["profile_picture"]:
                    user_info["avatar"] = get_image(
                        user_info["profile_picture"], "avatars"
                    )

                access_token = create_access_token(identity=user.id)

                if access_token:
                    response_object = {
                        "success": True,
                        "message": "Successfully logged in.",
                        "Authorization": access_token,
                        "user": user_info,
                    }
                    return response_object, 200

            # Return incorrect password if others fail
            response_object = {
                "success": False,
                "message": "Failed to log in, password may be incorrect.",
                "error_reason": "incorrect_password",
            }
            return response_object, 403

        except Exception as error:
            current_app.logger.error(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_issues",
            }
            return response_object, 500

    @staticmethod
    def register(data):
        try:
            # Assign the vars
            email = data["email"]
            username = data["username"]
            full_name = data["full_name"]
            password = data["password"]
            entry_key = data["entry_key"]
            orientation = data["orientation"]

            # Check if email exists
            if len(email) == 0 or email is None:
                response_object = {
                    "success": False,
                    "message": "Email is required!",
                    "error_reason": "no_email",
                }
                return response_object, 403

            # Check if the email is being used
            if User.query.filter_by(email=email).first() is not None:
                response_object = {
                    "success": False,
                    "message": "Email is being used in another account.",
                    "error_reason": "email_used",
                }
                return response_object, 403

            # Check if the email is valid
            elif not EMAIl_REGEX.match(email):
                response_object = {
                    "success": False,
                    "message": "Invalid email!",
                    "error_reason": "email_invalid",
                }
                return response_object, 403

            # Check if the username is empty
            if len(username) == 0 or username is None:
                response_object = {
                    "success": False,
                    "message": "Username is required!",
                    "error_reason": "no_username",
                }
                return response_object, 403

            # Check if the username is being used
            elif User.query.filter_by(username=username.lower()).first() is not None:
                response_object = {
                    "success": False,
                    "message": "Username is already taken!",
                    "error_reason": "username_taken",
                }
                return response_object, 403

            # Check if the username is equal to or between 4 and 15
            elif not 4 <= len(username) <= 15:
                response_object = {
                    "success": False,
                    "message": "Username length is invalid!",
                    "error_reason": "username_invalid",
                }
                return response_object, 403

            # Check if the username is alpha numeric
            elif not username.isalnum():
                response_object = {
                    "success": False,
                    "message": "Username is not alpha numeric",
                    "error_reason": "username_not_alpha_numeric",
                }
                return response_object, 403
            
            # Check if the orientation is alphabetical and 1-30
            if len(orientation) == 0 or orientation is None:
                orientation = None

            elif not 1 <= len(orientation) <= 30 or not orientation.isalpha():
                response_object = {
                    "success": False,
                    "message": "Orientation is not alphabetical or between 1-30.",
                    "error_reason": "invalid_orientation",
                }
                return response_object


                
            # Verify the full name and if it exists
            if len(full_name) == 0 or full_name is None:
                full_name = None

            else:
                # Validate the full name
                # Remove any spaces so that it properly checks.
                if not full_name.replace(" ", "").isalpha():
                    response_object = {
                        "success": False,
                        "message": "Name is not alphabetical!",
                        "error_reason": "fullname_notalpha",
                    }
                    return response_object, 403

                # Check if the full name is equal to or between 2 and 50
                elif not 2 <= len(full_name) <= 50:
                    response_object = {
                        "success": False,
                        "message": "Name is length is invalid!",
                        "error_reason": "fullname_invalid!",
                    }
                    return response_object, 403

                # Replace multiple spaces with one.
                # 'firstName    lastName' -> 'firstName lastName'
                re.sub(" +", " ", full_name)

            # Check if the entry key is right
            if entry_key != current_app.config["ENTRY_KEY"]:
                response_object = {
                    "success": False,
                    "message": "Entry key is invalid!",
                    "error_reason": "entrykey_invalid",
                }
                return response_object, 403

            # Create new user object
            new_user = User(
                public_id=str(uuid4().int)[:15],
                email=email,
                username=username.lower(),
                full_name=full_name,
                orientation=orientation,
                password=password,
                joined_date=datetime.now(),
            )

            # Add and commit the user to the database
            db.session.add(new_user)
            db.session.flush()

            # Get the user's info
            user_schema = UserSchema()
            user_info = user_schema.dump(new_user)

            # Save changes
            db.session.commit()

            # Remove private information from user info
            for info in private_info:
                del user_info[info]

            # Return success response
            access_token = create_access_token(identity=new_user.id)
            response_object = {
                "success": True,
                "message": "User has successfully been registered.",
                "Authorization": access_token,
                "user": user_info,
            }
            return response_object, 201

        except Exception as error:
            current_app.logger.error(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_error",
            }
            return response_object, 500
