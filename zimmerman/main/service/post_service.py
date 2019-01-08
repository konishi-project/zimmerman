from datetime import datetime
from glob import glob
from os import path

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

def create_new_post(data):
    try:
        # Get the current user
        current_user = load_user(get_jwt_identity())
        # Assign the variables
        content = data['content']
        image_id = data['image_id']

        # Check if the content doesn't exceed limit
        # This limit can be changed, but for testing - it is set to 2000
        if len(content) >= 2000:
            return {'message': 'Content exceeds limit', 'success': False}, 403
        
        new_post = Posts(
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

    except Exception as e:
        response_object = {
          'success': True,
          'message': 'Post has successfully been created'
        }
        return response_object, 401