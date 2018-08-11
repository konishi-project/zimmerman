"""
serializers.py
---
API Models
"""
from flask_restplus import fields
from datetime import datetime
from app import api

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