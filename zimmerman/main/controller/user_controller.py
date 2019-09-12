from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import UserDto
from ..service.user_service import UserFn

api = UserDto.api
_user = UserDto.user

@api.route('/register')
class UserRegister(Resource):

    @api.expect(_user, validate=True)
    @api.doc('Register a new user.', 
      responses = {
        403: 'Requirements were not fulfilled',
        201: 'Successfully registered'
    })
    def post(self):
        """ Registers new user """
        data = request.get_json()
        return UserFn.register(data)

@api.route('/get')
class UserGet(Resource):

    @api.doc('Get a specific user', 
        responses = {
            200: 'User data has been sent',
            404: 'User not found!'
        }
    )
    @jwt_required
    def get(self):
        """ Get a specific user using its public id """
        # Check for arguments
        current_user = load_user(get_jwt_identity())
        current_public_id = current_user.public_id

        user_public_id = request.args.get("user_public_id", default=current_public_id)
        return UserFn.get_by_public_id(user_public_id)