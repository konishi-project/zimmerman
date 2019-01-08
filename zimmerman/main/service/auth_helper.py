from zimmerman.main.model.user import User
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
            if user and user.check_password(password):
                access_token = create_access_token(identity=user.id)
                if access_token:
                  return {
                    'message': 'Successfully logged in',
                    'success': True,
                    'Authorization': access_token
                  }, 200
            else:
                return {
                  'message': 'Failed to log in',
                  'success': False,
                }, 403

        except Exception as e:
          print(e)
          return {
            'message': 'Something failed!',
            'success': False
          }, 500