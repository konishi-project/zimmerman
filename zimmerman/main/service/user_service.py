from uuid import uuid4
from datetime import datetime

from flask import jsonify, current_app
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.main.model.user import User, UserSchema

def load_author(user_public_id):
    # Add the author's essential details.
    user_schema = UserSchema()
    user = load_by_public_id(user_public_id)
    author = user_schema.dump(user)

    # Remove sensitive information
    unnecessary_info = (
        'password_hash',
        'id',
        'post_likes',
        'comment_likes',
        'reply_likes',
        'posts'
    )
    for info in unnecessary_info:
        del author[info]

    return author

def load_by_public_id(user_public_id):
    return User.query.filter_by(public_id=user_public_id).first()

def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class UserService:
    def register(data):
        try:
            # Assign the vars
            email = data['email']
            username = data['username']
            password = data['password']
            entry_key = data['entry_key']

            first_name = data['first_name']
            last_name = data['last_name']

            # Check if the email is used
            if User.query.filter_by(email=email).first() is not None:
                response_object = {
                    'success': False,
                    'message': 'Email is being used in another account!',
                    'error_reason': 'email_taken'
                }
                return response_object, 403
            
            # Check if the username is equal to or between 4 and 15
            elif not 4 <= len(username) <= 15:
                response_object = {
                    'success': False,
                    'message': 'User name length is invalid!',
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
            
            # Verify the first name if it exists
            if first_name is not None:
                # Check if the first name is alphabetical
                if not first_name.isalpha():
                    response_object = {
                        'success': False,
                        'message': 'First name is not alphabetical.',
                        'error_reason': 'first_name_nonalpha'
                    }
                    return response_object, 403

                # Check if the first name is equal to or between 2 and 50
                if not 2 <= len(first_name) <= 50:
                    response_object = {
                        'success': False,
                        'message': 'First name length is invalid!',
                        'error_reason': 'first_name_length'
                    }
                    return response_object, 403

            # Verify last name
            if last_name is not None:
                # Check if the last name is alphabetical
                if not last_name.isalpha():
                    response_object = {
                        'success': False,
                        'message': 'Last name is not alphabetical.',
                        'error_reason': 'name_not alphabetical'
                    }
                    return response_object, 403

                # Check if the last name is equal to or between 2 and 50
                if not 2 <= len(last_name) <= 50:
                    response_object = {
                        'success': False,
                        'message': 'Last name length is invalid',
                        'error_reason': 'last_name_length'
                    }
                    return response_object, 403
            
            # Check if the entry key is right
            if entry_key != current_app.config['ENTRY_KEY']:
                response_object = {
                    'success': False,
                    'message': 'Entry key is invalid!',
                    'error_reason': 'entry_key'
                }
                return response_object, 403

            new_user = User(
                public_id = str(uuid4().int)[:15],
                email = email,
                username = username,
                first_name = first_name,
                last_name = last_name,
                password = password,
                joined_date = datetime.now()
            )

            # Add and commit the user to the database
            db.session.add(new_user)
            db.session.commit()

            # Return success response
            response_object = {
                'success': True,
                'message': 'User has successfully been registered',
            }
            return response_object, 201

        except Exception as error:
            response_object = {
                'success': False,
                'message': 'Something went wrong during the process!\nOutput: "%s"' % error
            }
            return response_object, 500

    # Query user INFO by its public id
    def get_user_info(user_public_id):
        user = User.query.filter_by(public_id=user_public_id).first()
        if not user:
            response_object = {
                'success': False,
                'message': 'User not found!'
            }
            return response_object, 404

        user_schema = UserSchema()
        user_info = user_schema.dump(user)

        unnecessary_info = (
            'password_hash',
            'id',
            'comment_likes',
            'reply_likes',
        )
        # Remove unnecessary info
        for info in unnecessary_info:
            del user_info[info]

        response_object = {
            'success': True,
            'message': 'User data sent.'
        }
        return response_object, 200
    
    def update(user_public_id, data, current_user):
        # Assign the vars
        bio = data['bio']
        avatar = data['avatar']
        # Get the user
        user = User.query.filter_by(id=user_public_id).first()

        if not user:
            response_object = {
                'success': False,
                'message': 'User not found!'
            }
            return response_object, 404

        # Check if the current user is the same as the one being updated.
        elif not current_user.public_id == user.publid_id:
            try:
                # Update the user's data
                user.bio = bio
                user.profile_picture = avatar
                # Commit the changes
                db.session.commit()

                response_object = {
                    'success': False,
                    'message': 'User data has successfully been updated.'
                }
                return response_object, 200
            except Exception as error:
                response_object = {
                    'success': False,
                }
            # Commit the changes
            db.session.commit()
            response_object = {
                'success': True,
                'message': 'User data successfully updated'
            }
            return response_object, 200
        
        response_object = {
            'success': True,
            'message': 'Currently work in progress.'
        }
        return response_object, 200