from datetime import datetime
from uuid import uuid4

from flask import current_app
from flask_jwt_extended import get_jwt_identity

from zimmerman.main import db
from zimmerman.util import Message, ErrResp
from zimmerman.main.model.main import Post, User

from .user_service import filter_author
from .comment_service import load_comment
from .reply_service import load_reply

from .like_service import check_like
from .upload_service import get_image

# Import Schemas
from zimmerman.main.model.schemas import PostSchema, UserSchema

# Define the schemas
post_schema = PostSchema()
user_schema = UserSchema()

# Add more if possible.
sensitive_info = "image_file"


def add_post_and_flush(data, user_id):
    db.session.add(data)
    db.session.flush()

    latest_post = load_post(data, user_id)

    db.session.commit()

    return latest_post


def get_initial_comments(comment_array, user_id):
    comments = []

    for comment in comment_array:
        comment_info = load_comment(comment, user_id)
        comments.append(comment_info)

    return comments


def filter_post(post_info):
    # Remove sensitive information
    # Add more if possible
    del post_info["image_file"]

    # for i in sensitive_info:
    #     del post_info[i]


def load_post(post, user_id):
    post_info = post_schema.dump(post)

    # Set the author
    author = user_schema.dump(post.author)
    post_info["author"] = filter_author(author)

    # Get the first 5 comments
    post_info["initial_comments"] = (
        get_initial_comments(
            sorted(post.comments, key=lambda x: x.created)[:5], user_id
        )
        if post.comments
        else None
    )

    # Returns boolean
    post_info["liked"] = check_like(post.likes, user_id)

    # Returns static path.
    post_info["image_url"] = (
        get_image(post.image_file, "postimages") if post.image_file else None
    )

    # Remove post sensitive data
    filter_post(post_info)

    return post_info


class PostService:
    def create(data, current_user):
        # Assign the vars
        content = data["content"]
        image_id = data["image_id"]

        # Check if the content doesn't exceed limit
        # This limit can be changed, 2000 - just for testing.
        limit = 2000
        if len(content) > limit:
            resp = Message(False, "Content exceeds limit (%s)" % limit)
            return resp, 403

        if not content:
            resp = Message(False, "Content can't be empty!")
            return resp, 403

        # Create new post obj.
        new_post = Post(
            public_id=str(uuid4().int)[:15],
            owner_id=current_user.id,
            creator_public_id=current_user.public_id,
            content=content,
            image_file=image_id,
            status="normal",
            created=datetime.utcnow(),
        )

        latest_post = add_post_and_flush(new_post, current_user.id)

        resp = Message(True, "Post created.")
        resp["post"] = latest_post
        return resp, 201

    def delete(post_public_id, current_user):
        # Query for the post
        post = Post.query.filter_by(public_id=post_public_id).first()
        if not post:
            resp = Message(False, "Post not found!")
            return resp, 404

        # Check post owner
        elif (
            current_user.public_id == post.creator_public_id
        ):  # or is_admin(current_user)
            try:
                db.session.delete(post)
                db.session.commit()

                resp = Message(True, "Post deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                ErrResp()

        # Return a 403 response if the current is not the owner or the admin
        resp = Message(False, "Insufficient permissions!")
        return resp, 403

    def update(post_public_id, data, current_user):
        post = Post.query.filter_by(public_id=post_public_id).first()
        if not post:
            resp = Message(False, "Post not found!")
            resp["error_reason"] = "post_404"
            return resp, 404

        # Check the post owner
        elif (
            current_user.public_id == post.creator_public_id and post.status == "normal"
        ):
            # Get the new data
            if not data["content"]:
                resp = Message(False, "Content not found!")
                resp["error_reason"] = "content_invalid"
                return resp, 404

            try:
                # Update the post
                post.content = data["content"]
                post.edited = True
                # Commit the changes
                db.session.commit()

                resp = Message(True, "Post updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                ErrResp()

        # Check if the post is locked
        elif post.status.lower() == "locked":
            resp = Message(False, "Post is locked!")
            resp["error_reason"] = "post_locked"
            return resp, 403

        resp = Message(False, "Insufficient permissions!")
        resp["error_reason"] = "permission_insufficient"
        return resp, 403

    def get(post_public_id, current_user):
        # Get the specific post using its public id
        post = Post.query.filter_by(public_id=post_public_id).first()
        if not post:
            resp = Message(False, "Post not found!")
            return resp, 404

        # Load the post
        post_info = load_post(post, current_user.id)

        resp = Message(True, "Post info sent.")
        resp["post"] = post_info
        return resp, 200
