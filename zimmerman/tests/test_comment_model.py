import unittest
from uuid import uuid4
from datetime import datetime

from api.main import db
from models.main import Comment, Post, User
from tests.base import BaseTestCase


class TestCommentModel(BaseTestCase):
    def test_create_comment(self):
        """ Test for comment model """
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
            creator_public_id=user.public_id,
            on_post=post.id,
            content="Test comment",
            owner_id=user.id,
        )

        db.session.add(comment)
        db.session.commit()

        self.assertTrue(isinstance(comment, Comment))


if __name__ == "__main__":
    unittest.main()
