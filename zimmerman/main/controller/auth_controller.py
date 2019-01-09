from flask import request
from flask_restplus import Resource

from zimmerman.main.service.auth_helper import Auth
from  ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth

@api.route('/login')
class UserLogin(Resource):

  """ User login, get an access token """
  @api.doc('User login route')
  @api.expect(user_auth, validate=True)
  def post(self):
    # Grab the post data
    login_data = request.json
    return Auth.login_user(data=login_data)