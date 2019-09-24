import unittest
import json
from datetime import datetime

from flask import current_app
from zimmerman.test.base import BaseTestCase

def register_user(self):
    return self.client.post(
      '/user/register',
      data = json.dumps(dict (
          email = 'test@Email.com',
          username = 'testUser',
          first_name = 'test',
          last_name = 'user',
          password = '123456',
          entry_key = current_app.config['ENTRY_KEY']
      )),
      content_type = 'application/json'
    )

def login_user(self):
    return self.client.post(
        '/auth/login',
        data = json.dumps(dict (
            email = 'test@Email.com',
            password = '123456'
        )),
        content_type = 'application/json'
    )

def create_post(self, access_token):
    return self.client.post(
      '/post/create',
      data = json.dumps(dict (
          content = 'Sample content',
          image_id = ''
      )),
      headers = {
        'Authorization': 'Bearer %s' % access_token
      },
      content_type = 'application/json'
    )

def like_post(self, access_token, post_public_id):
    return self.client.post(
        '/like/post/%s' % post_public_id,
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

def unlike_post(self, access_token, post_public_id):
    return self.client.delete(
        '/like/post/%s' % post_public_id,
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

class TestLikeBlueprint(BaseTestCase):

    def test_post_like_unlike(self):
        """ Test for post liking and unliking """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Post creation
            create_response = create_post(self, access_token)
            create_response_data = json.loads(create_response.data.decode())

            post = create_response_data['post']
            post_public_id = post['public_id']

            # Like the post
            like_response = like_post(self, access_token, post_public_id)
            like_response_data = json.loads(like_response.data.decode())

            self.assertEqual(like_response.status_code, 201)
            self.assertTrue(like_response_data['success'])

            # Unlike the post
            unlike_response = unlike_post(self, access_token, post_public_id)
            unlike_response_data = json.loads(unlike_response.data.decode())

            self.assertEqual(unlike_response.status_code, 200)
            self.assertTrue(unlike_response_data['success'])

if __name__ == '__main__':
    unittest.main()