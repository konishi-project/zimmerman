from datetime import datetime
from zimmerman.main import db

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Notification(Model):
    id = Column(db.Integer, primary_key=True)
    # The user that committed the action, takes public_id.
    actor = Column(db.String(15))
    # Target owner is the user receiving the notification.
    target_owner = Column(db.Integer, db.ForeignKey("user.id"))
    # Example actions: 'liked', 'replied', 'commented', etc.
    action = Column(db.String(10))

    timestamp = Column(db.DateTime, default=datetime.utcnow)
    read = Column(db.Boolean, default=False)

    # Object type: post, comment, reply ...
    object_type = Column(db.String(20))
    object_public_id = Column(db.String(15))

    def is_read(self, read):
        self.read = True
