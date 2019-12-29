from zimmerman.main import db

from ..like_service import check_like
from ..user.utils import filter_author
from ..upload_service import get_image

from ..comment.utils import load_comment

# Import Schemas
from zimmerman.main.model.schemas import PostSchema, UserSchema

# Define deserializers
from ..user.utils import user_schema

post_schema = PostSchema()

# TODO - Add more if possible
sensitive_info = "image_file"


def update_post(post, content):
    post.content = content
    post.edited = True

    db.session.commit()


def delete_post(post):
    db.session.delete(post)
    db.session.commit()


def add_post_and_flush(data, user_id):
    db.session.add(data)
    db.session.flush()

    latest_post = load_post(data, user_id)

    db.session.commit()

    return latest_post


def load_post(post, user_id):
    info = post_schema.dump(post)

    # Set the author
    author = user_schema.dump(post.author)
    info["author"] = filter_author(author)

    # Return boolean
    info["liked"] = check_like(post.likes, user_id)

    # Loads image url
    info["image_url"] = (
        get_image(post.image_file, "postimages") if post.image_file else None
    )

    # Get the first 5 comments
    info["initial_comments"] = (
        get_initial_comments(
            sorted(post.comments, key=lambda x: x.created)[:5], user_id
        )
        if post.comments
        else None
    )

    filter_post(info)

    return info


def filter_post(post_info):
    # Remove sensitive information
    del post_info["image_file"]

    # for i in sensitive_info:
    #     del post_info[i]


def get_initial_comments(comment_array, user_id):
    comments = []

    for comment in comment_array:
        comment_info = load_comment(comment, user_id)
        comments.append(comment_info)

    return comments
