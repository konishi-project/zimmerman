## Like Models
from datetime import datetime

from zimmerman import db

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model


class PostLike(Model):
    """ PostLike Model for storing post like related details """

    # Details
    id = Column(db.Integer, primary_key=True)
    on_post = Column(db.Integer, db.ForeignKey("post.id"))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"))
    liked_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PostLike {self.id} on Post '{self.on_post}'>"


class CommentLike(Model):
    """ CommentLike Model for storing comment like related details """

    # Details
    id = Column(db.Integer, primary_key=True)
    on_comment = Column(db.Integer, db.ForeignKey("comment.id"))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"))
    liked_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CommentLike on Comment '{self.on_comment}'>"


class ReplyLike(Model):
    """ ReplyLike Model for storing reply like related details """

    # Details
    id = Column(db.Integer, primary_key=True)
    on_reply = Column(db.Integer, db.ForeignKey("reply.id"))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"))
    liked_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ReplyLike on Reply '{self.on_comment}'>"
