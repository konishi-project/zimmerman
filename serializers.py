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
    'status': fields.String(required=True, enum=['LOCKED', 'NORMAL'], default='NORMAL'),
    'modified': fields.DateTime(default=datetime.now),
    'created': fields.DateTime(default=datetime.now),
    'likes': fields.Integer(default=0),
})