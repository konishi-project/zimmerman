from datetime import datetime

from zimmerman import db

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Post(Model):
    """ Post Model for storing post related details """

    # Basic details
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator_public_id = Column(db.String(15))

    # Post content and details
    content = Column(db.Text)
    image_file = Column(db.String(40), default=None, nullable=True)
    status = Column(db.String(10), default="normal")

    created = Column(db.DateTime, default=datetime.utcnow)
    edited = Column(db.Boolean, default=False)

    likes = relationship(
        "PostLike", backref="post", cascade="all, delete-orphan", lazy=True
    )
    comments = relationship(
        "Comment", backref="post", cascade="all, delete-orphan", lazy=True
    )

    def __repr__(self):
        return f"<Post '{self.id}'>"


class Comment(Model):
    """ Comment Model for storing comment related details """

    # Basic details
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator_public_id = Column(db.String(15))
    on_post = Column(db.Integer, db.ForeignKey("post.id"))

    # Comment content and details
    content = Column(db.Text)
    image_file = Column(db.String(40), default=None, nullable=True)
    created = Column(db.DateTime, default=datetime.utcnow)
    edited = Column(db.Boolean, default=False)

    likes = relationship(
        "CommentLike", backref="comment", cascade="all, delete-orphan", lazy=True
    )
    replies = relationship("Reply", backref="comment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Comment '{self.id}'>"


class Reply(Model):
    """ Reply Model for storing reply related details """

    # Basic details
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    owner_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator_public_id = Column(db.String(15))
    on_comment = Column(db.Integer, db.ForeignKey("comment.id"))

    # Reply content and details
    content = Column(db.Text)
    image_file = Column(db.String(40), default=None, nullable=True)
    created = Column(db.DateTime, default=datetime.utcnow)
    edited = Column(db.Boolean, default=False)

    likes = relationship("ReplyLike", backref="reply", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Reply {self.id}>"
