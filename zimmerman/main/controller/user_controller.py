from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..util.dto import UserDto
from ..service.user_service import UserService, load_user

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
        return UserService.register(data)

@api.route('/get/<string:username>')
class UserGet(Resource):

    @api.doc('Get a specific user', 
        responses = {
            200: 'User data has been sent',
            404: 'User not found!'
        }
    )
    @jwt_required
    def get(self):
        """ Get a specific user by their username """
        # Check for arguments
        current_user = load_user(get_jwt_identity())
        current_username = current_user.username

        username = request.args.get("username", default=current_username)
        return UserService.get_user_info(username)

@api.route('/update')
class UserUpdate(Resource):
    
    @api.doc('Update a user\' information', 
        responses = {
            200: 'User data has been updated.',
            404: 'User not found!'
        }
    )
    @jwt_required
    def post(self):
        """ Update a user's data """
        current_user = load_user(get_jwt_identity())
        data = request.get_json()

        return UserService.update(data, current_user)