import unittest
from uuid import uuid4
from datetime import datetime
from flask_jwt_extended import create_access_token

from zimmerman.main import db
from zimmerman.main.model.user import User
from zimmerman.test.base import BaseTestCase

class TestUserModel(BaseTestCase):

      def test_create_access_token(self):
          user = User(
              public_id = str(uuid4().int)[:15],
              email = 'email@test.com',
              username = 'testUser',
              first_name = 'Test',
              last_name = 'User',
              password = 'test1234',
              joined_date = datetime.now()
          )

          db.session.add(user)
          db.session.commit()

          access_token = create_access_token(user.public_id)
          self.assertTrue(isinstance(access_token, str))
          self.assertEqual(len(user.public_id), 15)

if __name__ == '__main__':
    unittest.main()