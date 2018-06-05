"""
serializers.py
---
API Models
"""
from flask_restplus import fields
from flask_security import current_user
from models import *
from datetime import datetime
from app import api

user_post = api.model('Post', {
    'content': fields.String(required=True, description='Post content'),
    'status': fields.String(required=True, enum=['NORMAL', 'LOCKED']),
    'modified': fields.DateTime(default=datetime.now),
})

user_comment = api.model('Comment', {
    'content': fields.String(required=True, description='Comment content'),
    'modified': fields.DateTime(default=datetime.now),
})

user_reply = api.model('Reply', {
    'content': fields.String(required=True, description='Reply content'),
    'modified': fields.DateTime(default=datetime.now),
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

user_token = api.model('Token', {
    'token': fields.String(required=True)
})