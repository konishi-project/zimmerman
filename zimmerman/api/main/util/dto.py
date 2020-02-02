from flask_restx import Namespace, fields


class UserDto:
    api = Namespace("user", description="User related operations.")
    user = api.model(
        "user",
        {
            "email": fields.String(required=True, description="User's email address"),
            "username": fields.String(required=True, description="User's username"),
            "first_name": fields.String(description="User's first name"),
            "last_name": fields.String(description="User's last name"),
            "password": fields.String(required=True, description="User's password"),
            "entry_key": fields.String(description="Entry Key for registration"),
            "public_id": fields.String(description="User identifier"),
        },
    )
    user_update = api.model(
        "user_update",
        {
            "bio": fields.String(description="Update user's bio"),
            "avatar": fields.String(description="Update user's avatar"),
        },
    )


class PostDto:
    api = Namespace("post", description="Post related operations.")
    post = api.model(
        "post",
        {
            "content": fields.String(required=True, description="Post content."),
            "image_id": fields.String(description="Attached image"),
        },
    )


class CommentDto:
    api = Namespace("comment", description="Comment related operations.")
    comment = api.model(
        "comment",
        {
            "content": fields.String(required=True, description="Comment content."),
            "image_id": fields.String(description="Attached image"),
        },
    )


class ReplyDto:
    api = Namespace("reply", description="Reply related operations.")
    reply = api.model(
        "reply",
        {
            "content": fields.String(required=True, description="Reply content.",),
            "image_id": fields.String(description="Attached image"),
        },
    )


class FeedDto:
    api = Namespace("feed", description="Feed related operations.")
    posts = api.model(
        "post_ids",
        {"post_ids": fields.List(fields.Integer, description="Array of Post IDs")},
    )

    comments = api.model(
        "comment_ids",
        {
            "comment_ids": fields.List(
                fields.Integer, description="Array of Comment IDs"
            )
        },
    )

    replies = api.model(
        "reply_ids",
        {"reply_ids": fields.List(fields.Integer, description="Array of Reply IDs")},
    )


class LikeDto:
    api = Namespace("like", description="Like related operations.")
    like = api.model(
        "like",
        {
            "object_id": fields.String(
                required=True, description="The ID of the object being liked."
            )
        },
    )


class UploadDto:
    api = Namespace("upload", description="Upload related operations")
