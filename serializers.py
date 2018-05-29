"""
serializers.py
---
API Models
"""
from flask_restplus import fields
from flask_security import current_user
from models import *
from app import api

user_post = api.model('Post', {
    'owner_id': fields.Integer,
    'creator_name': fields.String(required=True, description='Name of the User who created this.'),
    'content': fields.String(required=True, description='Post content'),
    'status': fields.String(required=True, enum=['LOCKED', 'NORMAL']),
    'modified': fields.DateTime,
    'created': fields.DateTime,
    'likes': fields.Integer(default=0),
})