from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="Auth related operations.")
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
            "full_name": fields.String(
                description="Full name for identifying users."
            ),
            "password": fields.String(
                description="Password for securing user accounts."
            ),
            "entry_key": fields.String(
                required=True,
                description="Entry key for filtering out unwanted members.",
            ),
        },
    )
