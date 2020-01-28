from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="Auth related operations.")

    user_obj = api.model(
        "user",
        {
            "orientation": fields.String,
            "email": fields.String,

            "username": fields.String,
            "full_name": fields.String,

            "profile_picture": fields.String,
            "public_id": fields.String,

            "roles": fields.List(fields.Integer),
            "background_cover": fields.String,

            "joined_date": fields.String,
            "bio": fields.String,
        },
    )

    auth_login = api.model(
        "auth_details",
        {
            "email": fields.String(required=True, description="User's email."),
            "password": fields.String(required=True, description="User's password."),
        },
    )

    auth_register = api.model(
        "register_details",
        {
            "email": fields.String(
                required=True, description="Email address for logging in."
            ),
            "username": fields.String(
                required=True, description="Username for tagging users."
            ),
            "full_name": fields.String(description="Full name for identifying users."),
            "password": fields.String(
                description="Password for securing user accounts."
            ),
            "entry_key": fields.String(
                required=True,
                description="Entry key for filtering out unwanted members.",
            ),
        },
    )

    auth_success = api.model(
        "Response",
        {
            "success": fields.Boolean,
            "message": fields.String,
            "access_token": fields.String,
            "user": fields.Nested(user_obj)
        },
    )
