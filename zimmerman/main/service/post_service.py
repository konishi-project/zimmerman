from datetime import datetime
from uuid import uuid4
from glob import glob
from os import path

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from zimmerman.main import db
from zimmerman.main.model.user import Posts
from .user_service import load_user

# Import Schema
from zimmerman.main.model.user import PostSchema

POST_UPLOAD_PATH = '../static/postimages/'

def add_post_and_flush(data):
    db.session.add(data)
    db.session.flush()

    post_schema = PostSchema()
    latest_post = post_schema.dump(data).data

    check_image(latest_post)


def check_image(post):
    if post['image_file']:
        # Get the image_id
        image_id = post['image_file']
        # Search for the image in the static file
        image_url = glob(path.join(POST_UPLOAD_PATH, '{}.*'.format(image_id)))
        # Attach it to the latest post
        post['image_url'] = image_url[0]

def create_new_post(data, user):
    # Get the current user
    current_user = user
    # Assign the variables
    content = data['content']
    image_id = data['image_id']

    # Check if the content doesn't exceed limit
    # This limit can be changed, but for testing - it is set to 2000
    if len(content) >= 2000:
        return {'message': 'Content exceeds limit', 'success': False}, 403
    
    new_post = Posts(
        public_id = str(uuid4()),
        owner_id = current_user.id,
        creator_public_id = current_user.public_id,
        content = content,
        image_file = image_id,
        status = "normal"
    )

    add_post_and_flush(new_post)

    # Collect the data of the flushed post.
    post_schema = PostSchema()
    latest_post = post_schema.dump(new_post).data

    db.session.commit()

    # Check if the latest posts has an image
    check_image(latest_post)
    # Return success response
    response_object = {
        'success': True,
        'message': 'Post has successfully been created',
        'post': latest_post
    }
    return response_object, 201

def delete_post(post_public_id, user):
    # Get the current user
    current_user = user

    # Query for the post
    post = Posts.query.filter_by(public_id=post_public_id).first()
    if not post:
        response_object = {
            'success': False,
            'message': 'Post not found!'
        }
        return response_object, 404

    # Check post owner
    elif current_user.public_id == post.creator_public_id: # or is_admin(current_user)::
        post = Posts.query.filter_by(public_id=post_public_id).first()

        # Get the likes for the post and delete them too
        # Get comments for the post and delete them

        db.session.delete(post)
        db.session.commit()
        response_object = {
            'success': True,
            'message': 'Post has successfully been deleted'
        }
        return response_object, 200

def update_post(post_public_id, data, user):
    # Get the current user
    current_user = user

    # Query for the post
    post = Posts.query.filter_by(public_id=post_public_id).first()
    if not post:
        response_object = {
            'success': False,
            'message': 'Post not found!'
        }
        return response_object, 404

    # Check post owner
    elif current_user.public_id == post.creator_public_id and post.status == 'normal': # or is_admin(current_user)
        # Get the new data
        if data['content'] is not None:
            # Update the post
            post.content = data['content']
            post.edited = True
            # Commit changes
            db.session.commit()

            response_object = {
                'success': True,
                'message': 'Post has successfully been updated.'
            }
            return response_object, 200
    
    elif post.status.lower() == 'locked':
        response_object = {
            'success': False,
            'message': 'Post is locked!',
            'reason': 'locked'
        }
        return response_object, 403
    else:
        response_object = {
            'success': False,
            'message': 'You do not own this post!',
            'reason': 'permission'
        }
        return response_object, 403

def get_post(post_public_id):
    # Get the specific post using its public id
    post = Posts.query.filter_by(public_id=post_public_id).first()
    if not post:
        response_object = {
            'success': False,
            'message': 'Post not found!'
        }
        return response_object, 404

    post_schema = PostSchema()
    post_info = post_schema.dump(post).data

    # Check for an image file and add it if it has any.
    if post.image_file:
        # Get the image id
        image_id = post.image_file
        # Search for the image in the static/postimages directory
        image_url = glob(path.join(POST_UPLOAD_PATH), '%s' % image_id)
        # Attach it to the post and jsonify.
        post_info['image_url'] = image_url[0]
        response_object = {
            'success': True,
            'message': 'Post info successfully been sent.',
            'post': post_info
        }
        return jsonify(response_object)

    response_object = {
        'success': True,
        'message': 'Post info successfully been sent.',
        'post': post_info
    }
    return jsonify(response_object)