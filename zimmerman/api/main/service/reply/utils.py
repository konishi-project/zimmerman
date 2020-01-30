from api.main import db

from ..like_service import check_like
from ..user.utils import filter_author

# Import Schemas
from models.schemas import ReplySchema, UserSchema

# Define deserializers
from ..user.utils import user_schema

reply_schema_many = ReplySchema(many=True)
reply_schema = ReplySchema()

## TODO - Notify


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

    # TODO - Check like, Filter Reply

    return reply_info
