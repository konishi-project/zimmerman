from zimmerman.main.model.user import User, UserSchema
from flask_jwt_extended import create_access_token

from .upload_service import get_image

class Auth:
    @staticmethod
    def login_user(data):
        # Assign variables
        email = data['email']
        password = data['password']
        try:
            # Check if email or password was provided
            if not email or not password:
              response_object = {
                'success': False,
                'message': 'Credentials not fully provided!'
              }
              return response_object, 403

            # Fetch the user data
            user = User.query.filter_by(email=email).first()
            if not user:
              response_object = {
                'success': False,
                'message': 'The email you have entered does not match any account.',
              }
              return response_object, 404

            elif user and user.check_password(password):
                user_schema = UserSchema()
                user_info = user_schema.dump(user)

                # Remove sensitive information
                del user_info['password_hash']
                del user_info['id']

                # Check if the user has an avatar
                if user_info['profile_picture']:
                    user_info['avatar'] = get_image(user_info['profile_picture'], 'avatars')

                access_token = create_access_token(identity=user.id)
                if access_token:
                  return {
                    'message': 'Successfully logged in',
                    'success': True,
                    'user': user_info,
                    'Authorization': access_token
                  }, 200
              # Return Incorrect pass if the others fail
            else:
                return {
                  'message': 'Failed to log in, password may be incorrect.',
                  'success': False,
                }, 403

        except Exception as error:
          response_object = {
            'success': False,
            'message': 'Something went wrong during the process! \
            \nPlease report this issue and the output! \
            \nOutput: "%s"' % error
          }
          return response_object, 500
