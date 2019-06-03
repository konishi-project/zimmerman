from datetime import datetime

from zimmerman.main import db
from zimmerman.main.model.user import Reply, Comments

# Import Schema
from zimmerman.main.model.user import ReplySchema

def add_reply_and_flush(data):
    db.session.add(data)
    db.session.flush()

    reply_schema = ReplySchema()
    latest_reply = reply_schema.dump(data).data

    db.session.commit()

    return latest_reply

def create_new_reply(comment_id, data, current_user):
    # Get the comment
    comment = Comments.query.filter_by(id=comment_id).first()
    # Assign the variables
    content = data['content']

    # Validations
    limit = 500
    if len(content) > limit:
        respnse_onject = {
          'success': False,
          'message': 'Reply content exceeds limit (%s)' % limit
        }
        return response_object, 403

    new_reply = Reply(
      creator_public_id = current_user.public_id,
      on_comment = comment.id,
      content = content,
      created = datetime.utcnow()
    )

    latest_reply = add_reply_and_flush(new_reply)

    response_object = {
        'success': True,
        'message': 'Successfully replied on comment',
        'reply': latest_reply
    }
    return response_object, 201

def delete_reply(reply_id, current_user):
    # Query for the reply
    reply = Reply.query.filter_by(id=reply_id).first()
    if not reply:
        response_object = {
            'success': False,
            'message': 'Reply not found!'
        }
        return response_object, 404

    # Check reply owner
    elif current_user.public_id == reply.creator_public_id: # or is admin(current_user)
        reply = Reply.query.filter_by(id=reply_id).first()

        # Get the likes for the replies and delete them

        db.session.delete(reply)
        db.session.commit()
        response_object = {
            'success': True,
            'message': 'Reply has been deleted'
        }
        return response_object, 200

    elif current_user.public_id != reply.creator_public_id:
        response_object = {
            'success': False,
            'message': 'This reply does not belong to you'
        }
        return response_object, 403

    response_object = {
        'success': False,
        'message': 'Uh oh! Something went wrong during the process'
    }
    return response_object, 500

def update_reply(reply_id, data, current_user):
    # Query for the reply
    reply = Reply.query.filter_by(id=reply_id).first()
    if not reply:
        response_object = {
            'success': False,
            'message': 'Reply not found!'
        }
        return response_object, 404

    # Check reply owner
    elif current_user.public_id == reply.creator_public_id:
        # Get the new data
        if not data['content']:
            response_object = {
                'success': False,
                'message': 'Content data not found!',
                'error_reason': 'noData'
            },
            return response_object, 404

    elif current_user.public_id != reply.creator_public_id:
        response_object = {
            'success': False,
            'message': 'You do not own this reply',
            'error_reason': 'permission'
        }
        return response_object, 403

    response_object = {
        'success': False,
        'message': 'Something went wrong during the process'
    }
    return response_object, 500

def get_reply(reply_id):
    # Get the specific reply using its id
    reply = Reply.query.filter_by(id=reply_id).first()
    if not reply:
        response_object = {
            'success': False,
            'message': 'Reply not found!'
        }
        return response_object, 404
    
    reply_schema = ReplySchema()
    reply_info = reply_schema.dump(reply).data

    response_object = {
        'success': True,
        'reply': reply_info
    }
    return response_object, 200