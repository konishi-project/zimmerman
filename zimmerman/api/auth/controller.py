from flask import request
from flask_restx import Resource

from zimmerman import limiter
from .service import Auth
from .util.dto import AuthDto

api = AuthDto.api
auth_login = AuthDto.auth_login
auth_register = AuthDto.auth_register

auth_success = AuthDto.auth_success


@api.route("/login")
class AuthLogin(Resource):
    """ User login endpoint
    User logins then receives an access token.
    """

    decorators = [
        limiter.limit(
            "5/minute", error_message="You have exceeded max login attempts (5/minute)."
        )
    ]

    @api.doc("Auth login endpoint")
    @api.expect(auth_login, validate=True)
    @api.response(201, "Logged in.", auth_success)
    def post(self):
        """ Login using email and password """
        # Grab the json data
        login_data = request.get_json()
        return Auth.login_user(login_data)


@api.route("/register")
class AuthRegister(Resource):
    """ User registration endpoint
    User registers then receives the user's information and access_token
    """

    decorators = [
        limiter.limit(
            "5/day", error_message="You may only use registry route 5 times a day."
        )
    ]

    @api.doc("Auth registration endpoint")
    @api.expect(auth_register, validate=True)
    @api.response(201, "Successfully registered user.", auth_success)
    def post(self):
        """ Register to Konishi """
        # Grab the json data
        register_data = request.get_json()
        return Auth.register(register_data)
