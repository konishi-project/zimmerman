from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('user', description='User related operations.')
    user = api.model("user", {
        "email": fields.String(required=True, description="User's email address"),
        "username": fields.String(required=True, description="User's username"),
        "first_name": fields.String(description="User's first name"),
        "last_name": fields.String(description="User's last name"),

        "password": fields.String(required=True, description="User's password"),
        "entry_key": fields.String(description="Entry Key for registration"),
        "public_id": fields.String(description="User identifier")
    })

class AuthDto:
    api = Namespace('auth', description='Authentication related operations.')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='User password')
    })

class PostDto:
    api = Namespace('post', description='Post related operations.')
    post = api.model("post", {
        "content": fields.String(required=True, description="Post content."),
        "image_id": fields.String(description="Attached image"),
    })

class CommentDto:
    api = Namespace('comment', description='Comment related operations.')
    comment = api.model("comment", {
        "content": fields.String(required=True, description="Comment content."),
        "image_id": fields.String(description="Attached image"),
    })

class ReplyDto:
    api = Namespace('reply', description='Reply related operations.')
    comment = api.model("comment", {
        "content": fields.String(required=True, description="Reply content."),
    })

class FeedDto:
    api = Namespace('feed', description='Feed related operations.')
    feed = api.model('feed', {
        'item_ids': fields.List(fields.Integer, description='Array of IDs')
    })