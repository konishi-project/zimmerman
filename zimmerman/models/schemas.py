## Schemas
from zimmerman import ma

from .user import User
from .notification import Notification
from .content import Post, Comment, Reply
from .likes import PostLike


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

        # Fields to expose
        fields = (
            "email",
            "public_id",
            "username",
            "private",
            "full_name",
            "bio",
            "orientation",
            "profile_picture",
            "background_cover",
            "notifications",
            "posts",
            "comments",
            "replies",
            "post_likes",
            "joined_date",
            "roles",
        )


class NotificationSchema(ma.ModelSchema):
    class Meta:
        model = Notification


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

        # Fields to expose
        fields = (
            "public_id",
            "owner_id",
            "creator_public_id",
            "content",
            "image_file",
            "status",
            "created",
            "edited",
            "likes",
            "comments"
        )


class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment


class ReplySchema(ma.ModelSchema):
    class Meta:
        model = Reply


class PostLikeSchema(ma.ModelSchema):
    class Meta:
        model = PostLike
