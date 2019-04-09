import unittest
from uuid import uuid4
from datetime import datetime

from zimmerman.main import db
from zimmerman.main.model.user import Comments, User, Posts
from zimmerman.test.base import BaseTestCase

class TestCommentModel(BaseTestCase):
    
    def test_create_comment(self):
        """ Test for comment model """
        # Create test user
        user = User(
          public_id = str(uuid4().int)[:15],
          email = 'email@test.com',
          username = 'testUser',
          first_name = 'Test',
          last_name = 'User',
          password = 'test1234',
          joined_date = datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()

        # Create test post
        post = Posts(
            owner_id = user.id,
            creator_public_id = user.public_id,
            content = "Test content",
            image_file = "",
            status = "normal",
        )

        db.session.add(post)
        db.session.commit()

        # Create comment
        comment = Comments(
          creator_public_id = user.public_id,
          on_post = post.id,
          content = "Test comment"
        )
        
        db.session.add(comment)
        db.session.commit()

        self.assertTrue(isinstance(comment, Comments))

if __name__ == '__main__':
    unittest.main()