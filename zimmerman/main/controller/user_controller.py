from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import register_new_user

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
        data = request.json
        return register_new_user(data=data)