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

def create_new_reply(comment_id, data, user):
    # Get the current user
    current_user = user
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
      on_comment = comment.id
      content = content
    )

    latest_reply = add_reply_and_flush(new_reply)

    response_object = {
        'success': True,
        'message': 'Successfully replied on comment',
        'reply': latest_reply
    }
    return response_object, 201