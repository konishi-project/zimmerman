from uuid import uuid4
from datetime import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.main.model.user import User, UserSchema

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def register_new_user(data):
    # Assign the variables
    email = data['email']
    username = data['username']
    password = data['password']
    entry_key = data['entry_key']

    # Check if the email is used
    if User.query.filter_by(email=email).first() is not None:
        response_object = {
            'success': False,
            'message': 'Email is being used in another account!',
            'error_reason': 'email_taken'
        }
        return response_object, 403

    # Check if the username exists
    if User.query.filter_by(username=username).first() is not None:
        response_object = {
            'success': False,
            'message': 'Username has already been taken!',
            'error_reason': 'username_taken'
        }
        return response_object, 403

    # Check if the username is equal to or between 4 and 15
    elif not 4 <= len(username) <= 15:
        response_object = {
            'success': False,
            'message': 'Username length is invalid!',
            'error_reason': 'username_length'
        }
        return response_object, 403

    # Check if the username is alpha numeric
    elif not username.isalnum():
        response_object = {
            'success': False,
            'message': 'Username is not alpha numeric!',
            'error_reason': 'username_not_alpha_numeric'
        }
        return response_object, 403

    # Check if there are first name or last name and verify if they exist
    # Verify first name
    if not data['first_name']:
        first_name = ''

    elif 'first_name' in data:
        first_name = data['first_name']

        # Check if the first name is alphabetical
        if not first_name.isalpha():
            response_object = {
                'success': False,
                'message': 'First name is not alphabetical',
                'error_reason': 'first_name_nonalpha'
            }
            return response_object, 403

        if not 2 <= len(first_name) <= 50:
            response_object = {
                'success': False,
                'message': 'First name length is invalid',
                'error_reason': 'first_name_length'
            }
            return response_object, 403
    else:
        response_object = {
            'success': False,
            'message': 'Something went wrong while verifying the first name'
        }
        return response_object, 500

    # Verify last name
    if not data['last_name']:
        last_name = ''

    elif 'last_name' in data:
        last_name = data['last_name']

        if not last_name.isalpha():
            response_object = {
                'success': False,
                'message': 'Last name is not alphabetical',
                'error_reason': 'name_not_alphabetical'
            }
            return response_object, 403

        if not 2 <= len(last_name) <= 50:
            response_object = {
                'success': False,
                'message': 'Last name length is invalid',
                'error_reason': 'last_name_length'
            }
            return response_object, 403
    else:
        response_object = {
            'success': False,
            'message': 'Something went wrong while verifying the last name'
        }
        return response_object, 500

    # Check if entry key is right
    # Change during production
    if entry_key != "KonishiTesting":
        return {'message': 'Entry key is invalid!', 'error_reason': 'key'}, 403

    new_user = User(
        public_id = str(uuid4().int)[:15],
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

# Loads user using public ID
def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()

# Loads user using ID
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

def create_token(user):
    try:
        # Generate token
        access_token = create_access_token(user.id)
        response_object = {
            'success': True,
            'message': 'Successfully registered',
            'Authorization': access_token
        }
        return response_object, 201

    except Exception as e:
        response_object = {
            'success': False,
            'message': 'Some error occured. Please try again.'
        }
        return response_object, 401

def get_user_info(user_public_id):

    user = get_a_user(user_public_id)
    if not user:
        response_object = {
            'success': False,
            'message': 'User not found!'
        }
        return response_object, 404
    
    # Get the user's information
    user_schema = UserSchema()
    user_info = user_schema.dump(user)
    # Remove hashed password
    del user_info['password_hash']

    response_object = {
        'success': True,
        'message': 'User info sent',
        'user': user_info
    }
    return response_object, 200

def update_user(user_public_id, data, current_user):
    # Query the user
    user = get_user_info(user_public_id)
    if not user:
        response_object = {
            'success': False,
            'message': 'User not found!'
        }
        return response_object, 404

    # WIP, add more stuff here.