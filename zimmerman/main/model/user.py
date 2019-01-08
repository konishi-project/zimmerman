from flask_login import UserMixin
from datetime import datetime

from .. import db, ma, bcrypt

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(UserMixin, db.Model):
  """ User Model for storing user related details """

  # Basic details
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(36), unique=True)
  email = db.Column(db.String(255), unique=True, nullable=False)
  username = db.Column(db.String(20), unique=True)
  first_name = db.Column(db.String(50), nullable=True)
  last_name = db.Column(db.String(50), nullable=True)

  password_hash = db.Column(db.String(255))

  # Extra details
  bio = db.Column(db.Text, nullable=True)
  profile_picture = db.Column(db.String(35), nullable=True)

  # Post related
  post = db.relationship('Posts', backref='user')

  post_likes = db.relationship('PostLike', backref='user')
  comment_likes = db.relationship('CommentLike', backref='user')
  reply_like = db.relationship('ReplyLike', backref='user')

  # Status
  joined_date = db.Column(db.DateTime)
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users'), lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('Password: Write-Only field')

  @password.setter
  def password(self, password):
    self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
  
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)

  def __repr__(self):
    return "<User '{}'>".format(self.username)

class Role(db.Model):
    """ Role Model for storing role related details """
    __tablename__ = "role"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(50))

    def __repr__(self):
        return '{} - {}'.format(self.name, self.id)

class Posts(db.Model):
    """ Post Model for storing post related details """
    
    # Basic details
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_public_id = db.Column(db.String(36))

    # Post content and details
    content = db.Column(db.Text)
    image_file = db.Column(db.String(35), default=None, nullable=True)
    status = db.Column(db.String(10))

    created = db.Column(db.DateTime, default=datetime.now())
    edited = db.Column(db.Boolean, default=False)

    likes = db.relationship('PostLike', backref='posts')
    comments = db.relationship('Comments', backref='posts')

    def __repr__(self):
      return "<Post '{}'>".format(self.id)

class Comments(db.Model):
    """ Comment Model for storing comment related details """

    # Basic details
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    commenter = db.Column(db.String(20))

    # Comment content and details
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    edited = db.Column(db.Boolean, default=False)

    likes = db.relationship('CommentLike', backref='comments')

    def __repr__(self):
      return "<Comment '{}'>".format(self.id)

class Reply(db.Model):
    """ Reply Model for storing reply related details """

    # Basic details
    id = db.Column(db.Integer, primary_key=True)
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replier = db.Column(db.String(20))

    # Reply content and details
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    edited = db.Column(db.Boolean, default=False)

    likes = db.relationship('ReplyLike', backref='reply')

    def __repr__(self):
      return "<Reply '{}'>".format(self.id)

class PostLike(db.Model):
    """ PostLike Model for storing post like related details """

    # Details
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
      return "<PostLike on Post '{}'>".format(self.on_post)

class CommentLike(db.Model):
    """ CommentLike Model for storing comment like related details """

    # Details
    id = db.Column(db.Integer, primary_key=True)
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
      return "<CommentLike on Comment '{}'>".format(self.on_comment)

class ReplyLike(db.Model):
    """ ReplyLike Model for storing reply like related details """

    # Details
    id = db.Column(db.Integer, primary_key=True)
    on_reply = db.Column(db.Integer, db.ForeignKey('reply.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
      return "<ReplyLike on Reply '{}'>".format(self.on_comment)

# Model Schemas
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Posts

class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comments

class ReplySchema(ma.ModelSchema):
    class Meta:
        model = Reply

class PostLikeSchema(ma.ModelSchema):
    class Meta:
        model = PostLike