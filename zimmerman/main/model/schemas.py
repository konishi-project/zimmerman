from .user import User, Posts, Comments, Reply, PostLike
from .. import db, ma

# Model Schemas
# class UserSchema(ma.ModelSchema):
#     class Meta:
#         model = User

# class PostSchema(ma.ModelSchema):
#     class Meta:
#         model = Posts

# class CommentSchema(ma.ModelSchema):
#     class Meta:
#         model = Comments

# class ReplySchema(ma.ModelSchema):
#     class Meta:
#         model = Reply

# class PostLikeSchema(ma.ModelSchema):
#     class Meta:
#         model = PostLike