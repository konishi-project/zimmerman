## Schemas
from zimmerman.main import ma

from .main import Column, Model, relationship

from .main import Notification, Post, Comment, Reply, User
from .likes import PostLike


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class NotificationSchema(ma.ModelSchema):
    class Meta:
        model = Notification


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post


class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment


class ReplySchema(ma.ModelSchema):
    class Meta:
        model = Reply


class PostLikeSchema(ma.ModelSchema):
    class Meta:
        model = PostLike
