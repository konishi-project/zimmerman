from datetime import datetime

from zimmerman.main import db, bcrypt

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model
relationship = db.relationship

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
    password_hash = Column(db.String(255))

    # Optional
    full_name = Column(db.String(50), nullable=True)
    bio = Column(db.String(150), nullable=True)
    orientation = Column(db.String(30), nullable=True)

    ## Media
    profile_picture = Column(db.String(40), nullable=True)
    background_cover = Column(db.String(40), nullable=True)

    # Relationships
    notifications = relationship("Notification", backref="user")

    posts = relationship("Post", backref="author", lazy=True)
    comments = relationship("Comment", backref="author", lazy=True)
    replies = relationship("Reply", backref="author", lazy=True)

    post_likes = relationship("PostLike", backref="user")
    comment_likes = relationship("CommentLike", backref="user")
    reply_likes = relationship("ReplyLike", backref="user")

    # Status
    joined_date = Column(db.DateTime)
    roles = relationship(
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
        return f"<{self.name} - {self.id}>"
