from zimmerman import db

from ..user.utils import filter_author

# Import Schemas
from zimmerman.models.schemas import ReplySchema

# Define deserializers
from ..user.utils import user_schema

from ..like_service import check_like

reply_schema_many = ReplySchema(many=True)
reply_schema = ReplySchema()


def delete_reply(reply):
    db.session.delete(reply)
    db.session.commit()


def update_reply(reply, content):
    reply.content = content
    reply.edited = True

    db.session.commit()


def add_reply_and_flush(data, user_id):
    db.session.add(data)
    db.session.flush()

    latest_reply = load_reply(data, user_id)

    db.session.commit()

    return latest_reply


def load_reply(reply, user_id):
    reply_info = reply_schema.dump(reply)

    # Set the author
    author = user_schema.dump(reply.author)
    reply_info["author"] = filter_author(author)

    reply_info["liked"] = check_like(reply.likes, user_id)

    # Filter reply

    return reply_info
