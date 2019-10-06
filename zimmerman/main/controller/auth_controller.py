from flask import request
from flask_restplus import Resource

from zimmerman.main import limiter
from ..service.auth_helper import Auth
from  ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth

@api.route('/login')
class UserLogin(Resource):

  """ User login, get an access token """
  decorators = [
      limiter.limit(
          '5/minute', 
          error_message='You have exceeded login attempts (5/minute).')
  ]
  @api.doc('User login route')
  @api.expect(user_auth, validate=True)
  def post(self):
    """ Login user using email and password and receive an access_token """
    # Grab the post data
    login_data = request.get_json()
    return Auth.login_user(data=login_data)