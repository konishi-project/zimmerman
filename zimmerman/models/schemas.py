## Schemas
from zimmerman import ma

from .user import User
from .notification import Notification
from .post import Post, Comment, Reply
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
