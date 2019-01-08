from uuid import uuid4
from datetime import datetime

from zimmerman.main import db
from zimmerman.main.model.user import User

from flask_jwt_extended import create_access_token

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def register_new_user(data):
    # Assign the variables
    email = data['email']
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    entry_key = data['entry_key']

    # Check if the email is used
    if User.query.filter_by(email=email).first() is not None:
        return {'message': 'Email is being used in another account!', 'reason': 'email'}, 403

    # Check if the username exists
    if User.query.filter_by(username=username).first() is not None:
        return {'message': 'Username has already been taken!', 'reason': 'username'}, 403
    elif not 4 <= len(username) <= 15:
        return {'message': 'Username length is invalid!', 'reason': 'usernameLength'}, 403
    elif not username.isalnum():
        return {'message': 'Username is not alpha numeric!', 'reason': 'usernameNotAlphaNumeric'}, 403

    if not first_name.isalpha() or not last_name.isalpha():
        return {'message': 'Name is not alphabetical', 'reason': 'nonAlphaName'}, 403
    elif not 2 <= len(first_name) <= 50 or not 2 <= len(last_name) <= 50:
        return {'message': 'Name length is invalid', 'reason': 'nameLength'}, 403

    # Check if entry key is right
    # Change during production
    if entry_key != "KonishiTesting":
        return {'message': 'Entry key is invalid!', 'reason': 'key'}, 403

    new_user = User(
        public_id = str(uuid4()),
        email = email,
        username = username,
        first_name = first_name,
        last_name = last_name,
        password = password,
        joined_date = datetime.now()
    )

    save_changes(new_user)
    # Return success response
    return create_token(new_user)

def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()

def create_token(user):
    try:
        # Generate token
        access_token = create_access_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered',
            'Authorization': access_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occured. Please try again.'
        }
        return response_object, 401