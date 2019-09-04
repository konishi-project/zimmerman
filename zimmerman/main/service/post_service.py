import os
from datetime import datetime
from uuid import uuid4
from glob import glob

from flask import request, jsonify, url_for
from flask_jwt_extended import get_jwt_identity

from zimmerman.main import db
from zimmerman.main.model.user import Posts, PostLike
from .user_service import get_a_user

# Import Schema
from zimmerman.main.model.user import PostSchema, UserSchema

from ..config import basedir
POST_UPLOAD_PATH = basedir + 'static/postimages/'

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
        image_url = url_for('static', filename='postimages/' + image_id)
        # Attach it to the latest post
        post['image_url'] = image_url

def load_author(creator_public_id):
    # Add the author's essential details.
    user_schema = UserSchema()
    user = get_a_user(creator_public_id)
    author = user_schema.dump(user).data

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

def create_new_post(data, current_user):
    # Assign the variables
    content = data['content']
    image_id = data['image_id']

    # Check if the content doesn't exceed limit
    # This limit can be changed, but for testing - it is set to 2000
    limit = 2000
    if len(content) >= limit:
        response_object = {
            'success': False,
            'message': 'Content exceeds limit (%s)' % limit
        }
        return response_object, 403

    if len(content) == 0:
        response_object = {
            'success': False,
            'message': 'Content cannot be empty!'
        },
        return response_object, 403
    
    new_post = Posts(
        public_id = str(uuid4().int)[:15],
        owner_id = current_user.id,
        creator_public_id = current_user.public_id,
        content = content,
        image_file = image_id,
        status = "normal",
        created = datetime.utcnow()
    )

    add_post_and_flush(new_post)

    # Collect the data of the flushed post.
    post_schema = PostSchema()
    latest_post = post_schema.dump(new_post).data

    db.session.commit()

    # Check if the latest posts has an image
    check_image(latest_post)
    # Return success response

    # Add the author's information
    latest_post['author'] = load_author(latest_post['creator_public_id'])

    response_object = {
        'success': True,
        'message': 'Post has successfully been created',
        'post': latest_post
    }
    return response_object, 201

def delete_post(post_public_id, current_user):
    # Query for the post
    post = Posts.query.filter_by(public_id=post_public_id).first()
    if not post:
        response_object = {
            'success': False,
            'message': 'Post not found!'
        }
        return response_object, 404

    # Check post owner
    elif current_user.public_id == post.creator_public_id: # or is_admin(current_user)
        post = Posts.query.filter_by(public_id=post_public_id).first()

        # Get the likes for the post and delete them too
        delete_likes = PostLike.__table__.delete().where(PostLike.on_post == post.id)
        db.session.execute(delete_likes)
        # # Get comments for the post and delete them

        db.session.delete(post)
        db.session.commit()
        response_object = {
            'success': True,
            'message': 'Post has successfully been deleted'
        }
        return response_object, 200

    # Return a 403 response if the current user is not the owner or the admin.
    response_object = {
        'success': False,
        'message': 'Insufficient permission!'
    }
    return response_object, 403


def update_post(post_public_id, data, current_user):
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
            'error_reason': 'locked'
        }
        return response_object, 403

    else:
        response_object = {
            'success': False,
            'message': 'You do not own this post!',
            'error_reason': 'permission'
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

    post_info['author'] = load_author(post_info['creator_public_id'])

    # Check for an image file and add it.
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