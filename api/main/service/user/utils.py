from api.util import Message

from api.main.model.user import User
from api.main.model.schemas import UserSchema

from ..upload_service import get_image

user_schema = UserSchema()

private_info = (
    "password_hash",
    "id",
    "post_likes",
    "comment_likes",
    "reply_likes",
    "posts",
    "comments",
    "replies",
    "notifications",
)

unnecessary_info = ("password_hash", "id", "comment_likes", "reply_likes")


def filter_author(user):
    # Remove sensitive information
    for info in private_info:
        del user[info]

    # Add the avatar
    user["avatar"] = (
        get_image(user["profile_picture"], "avatars")
        if user["profile_picture"] is not None
        else None
    )

    return user


def load_info(user_obj):
    info = user_schema.dump(user_obj)
    for i in unnecessary_info:
        del info[i]

    # Add avatar
    info["avatar"] = (
        get_image(user_obj.profile_picture, "avatars")
        if user_obj.profile_picture is not None
        else None
    )

    return info


# Special fn
def load_user(identififer):
    # If the user_id is an int then use id
    if type(identififer) == int:
        user = User.query.filter_by(id=identififer).first()

    # Use public id
    else:
        user = User.query.filter_by(public_id=identififer).first()

    if not user:
        resp = Message(False, "Current user does not exist!")
        resp["error_reason"] = "user_404"
        return resp, 404

    return user
