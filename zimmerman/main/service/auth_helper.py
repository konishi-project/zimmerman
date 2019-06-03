from zimmerman.main.model.user import User, UserSchema
from flask_jwt_extended import create_access_token

class Auth:
    @staticmethod
    def login_user(data):
        # Assign variables
        email = data['email']
        password = data['password']
        try:
            # Fetch the user data
            user = User.query.filter_by(email=email).first()
            if not user:
              return {
                'message': 'The email you have entered does not match any account.',
                'success': False,
              }, 404
            elif user and user.check_password(password):
                user_schema = UserSchema()
                user_info = user_schema.dump(user).data

                # Remove sensitive information
                del user_info['password_hash']
                del user_info['id']

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

        except Exception as e:
          print(e)
          return {
            'message': 'Something went wrong during the process! (500)',
            'success': False
          }, 500