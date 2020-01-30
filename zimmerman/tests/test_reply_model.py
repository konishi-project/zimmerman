import unittest
from uuid import uuid4
from datetime import datetime


from zimmerman import db
from zimmerman.models.user import User
from zimmerman.models.post import Post, Comment, Reply

from zimmerman.tests.base import BaseTestCase


class TestReplyModel(BaseTestCase):
    def test_create_reply(self):
        """ Test for reply model """
        # Create test user
        user = User(
            public_id=str(uuid4().int)[:15],
            email="email@test.com",
            username="testUser",
            full_name="Test User",
            password="test1234",
            joined_date=datetime.utcnow(),
        )

        db.session.add(user)
        db.session.commit()

        # Create test post
        post = Post(
            owner_id=user.id,
            creator_public_id=user.public_id,
            content="Test content",
            image_file="",
            status="normal",
        )

        db.session.add(post)
        db.session.commit()

        # Create comment
        comment = Comment(
            owner_id=user.id,
            creator_public_id=user.public_id,
            on_post=post.id,
            content="Test comment",
        )

        db.session.add(comment)
        db.session.commit()

        # Create reply
        reply = Reply(
            owner_id=user.id,
            creator_public_id=user.public_id,
            on_comment=comment.id,
            content="Test reply",
        )

        db.session.add(reply)
        db.session.commit()

        self.assertTrue(isinstance(reply, Reply))


if __name__ == "__main__":
    unittest.main()
