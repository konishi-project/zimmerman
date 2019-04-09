from datetime import datetime

from zimmerman.main import db
from zimmerman.main.model.user import Comments, Posts

# Import Schema
from zimmerman.main.model.user import CommentSchema

def add_comment_and_flush(data):
    db.session.add(data)
    db.session.flush()

    comment_schema = CommentSchema()
    latest_comment = comment_schema.dump(data).data

    db.session.commit()

    return latest_comment

def create_new_comment(post_public_id, data, current_user):
    # Get the post
    post = Posts.query.filter_by(public_id=post_public_id).first()
    # Assign the variables
    content = data['content']

    # Validations
    limit = 1500
    if len(content) > limit:
        response_object = {
          'success': False,
          'message': 'Comment content exceeds limit (%s)' % limit
        }
        return response_object, 403

    new_comment = Comments(
        creator_public_id = current_user.public_id,
        on_post = post.id,
        content = content,
        created = datetime.utcnow()
    )

    latest_comment = add_comment_and_flush(new_comment)

    response_object = {
        'success': True,
        'message': 'Successfully commented on the post',
        'comment': latest_comment
    }
    return response_object, 201

def delete_comment(comment_id, current_user):
    # Query for the comment
    comment = Comments.query.filter_by(id=comment_id).first()
    if not comment:
        response_object = {
            'success': False,
            'message': 'Comment not found!'
        }
        return response_object, 404
    
    # Check comment owner
    elif current_user.public_id == comment.creator_public_id: # or is_admin(current_user)
        comment = Comments.query.filter_by(id=comment_id).first()

        # Get the likes for the comment and delete them
        # Get the replies for the comment and delete them

        db.session.delete(comment)
        db.session.commit()
        response_object = {
            'success': True,
            'message': 'Comment has been deleted'
        }
        return response_object, 200
    
    elif current_user.public_id != comment.creator_public_id:
        response_object = {
            'success': False,
            'message': 'This comment does not belong to you'
        }
        return response_object, 403

    response_object = {
        'success': False,
        'message': 'Uh oh! Something went wrong during the process'
    }
    return response_object, 500

def update_comment(comment_id, data, current_user):
    # Query for the comment
    comment = Comments.query.filter_by(id=comment_id).first()
    if not comment:
        response_object = {
            'success': False,
            'message': 'Comment not found!',
            'error_reason': 'noComment'
        }
        return response_object, 404
    
    # Check post owner
    elif current_user.public_id == comment.creator_public_id:
        # Get the new data
        if not data['content']:
            response_object = {
                'success': False,
                'message': 'Content data not found!',
                'error_reason': 'noData'
            }
            return response_object, 404

        # Update the comment
        comment.content = data['content']
        comment.edited = True
        # Commit changes
        db.session.commit()

        response_object = {
            'success': True,
            'message': 'Comment has successfully been updated'
        }
        return response_object, 200

    elif current_user.public_id != comment.creator_public_id:
        response_object = {
            'success': False,
            'message': 'You do not own this comment',
            'error_reason': 'permission'
        }
        return response_object, 403

    response_object = {
        'success': False,
        'message': 'Something went wrong during the process!'
    }
    return response_object, 500

def get_comment(comment_id):
    # Get the specific comment using its id
    comment = Comments.query.filter_by(id=comment_id).first()
    if not comment:
        response_object = {
            'success': False,
            'message': 'Comment not found!'
        }
        return response_object, 404
    
    comment_schema = CommentSchema()
    comment_info = comment_schema.dump(comment).data

    response_object = {
        'success': True,
        'comment': comment_info
    }
    return response_object, 200