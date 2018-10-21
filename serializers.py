"""
serializers.py
---
API Models
"""
from flask_restplus import fields
from app import api
from wtforms import Form, StringField, PasswordField, validators

user_post = api.model('User Post', {
    'content': fields.String(required=True, description='Post content'),
    'image_id': fields.String(required=False, description='Uploaded Image ID for the post.'),
})

user_comment = api.model('Comment', {
    'content': fields.String(required=True, description='Comment content'),
})

user_reply = api.model('Reply', {
    'content': fields.String(required=True, description='Reply content'),
})

user_login = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

user_registration = api.model('Register', {
    'email': fields.String(required=True), 
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'confirm_password': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=False)
})

id_array = api.model('IdArray', {
    "post_ids": fields.List(fields.Integer)
})

comment_id_array = api.model('CommentIdArray', {
    "comment_ids": fields.List(fields.Integer)
})

reply_id_array = api.model('ReplyIdArray', {
"reply_ids": fields.List(fields.Integer)
})

user_post_method = api.model('PostMethod', {
    "method": fields.String(required=True)
})

class AdminLoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=15), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(max=255), validators.DataRequired()])
