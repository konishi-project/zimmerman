from datetime import datetime

from zimmerman.main import db, ma, bcrypt

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model

roles_users = db.Table(
    "roles_users",
    Column("user_id", db.Integer, db.ForeignKey("user.id")),
    Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class User(Model):
    """ User Model for storing user related details """

    # Basic details
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15), unique=True)
    email = Column(db.String(255), unique=True, nullable=False)
    username = Column(db.String(15), unique=True)
    full_name = Column(db.String(50), nullable=True)
    password_hash = Column(db.String(255))
    bio = Column(db.String(150), nullable=True)

    # Media
    profile_picture = Column(db.String(40), nullable=True)
    background_cover = Column(db.String(40), nullable=True)

    # Relationships
    notifications = db.relationship("Notification", backref="user")

    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    replies = db.relationship("Reply", backref="author", lazy=True)

    post_likes = db.relationship("PostLike", backref="user")
    comment_likes = db.relationship("CommentLike", backref="user")
    reply_likes = db.relationship("ReplyLike", backref="user")

    # Status
    joined_date = Column(db.DateTime)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users"), lazy="dynamic"
    )

    @property
    def password(self):
        raise AttributeError("Password: Write-Only field")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User '{self.username}'>"


class Role(Model):
    """ Role Model for storing role related details """

    __tablename__ = "role"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), unique=True)
    description = Column(db.String(50))

    def __repr__(self):
        return f"{self.name} - {self.id}"


class Notification(Model):
    id = Column(db.Integer, primary_key=True)
    # The user that committed the action, takes public_id.
    actor = Column(db.String(15))
    # Target owner is the user receiving the notification.
    target_owner = Column(db.Integer, db.ForeignKey("user.id"))
    # Example actions: 'liked', 'replied', 'commented', etc.
    action = Column(db.String(10))

    timestamp = Column(db.DateTime)
    read = Column(db.Boolean, default=False)

    # Object type: post, comment, reply ...
    object_type = Column(db.String(20))
    object_public_id = Column(db.String(15))

    def is_read(self, read):
        self.read = True


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
    status = Column(db.String(10))

    created = Column(db.DateTime, default=datetime.utcnow)
    edited = Column(db.Boolean, default=False)

    likes = db.relationship(
        "PostLike", backref="post", cascade="all, delete-orphan", lazy=True
    )
    comments = db.relationship(
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

    likes = db.relationship(
        "CommentLike", backref="comment", cascade="all, delete-orphan", lazy=True
    )
    replies = db.relationship("Reply", backref="comment", cascade="all, delete-orphan")

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

    likes = db.relationship("ReplyLike", backref="reply", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reply '{self.id}'>"


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


# Model Schemas
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
