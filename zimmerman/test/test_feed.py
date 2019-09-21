import unittest
import json

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

def get_post_ids(self, access_token):
    return self.client.get(
        '/feed/get',
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

def get_post_information(self, access_token, id_array):
    return self.client.post(
        '/feed/get',
        data = json.dumps(dict (
            post_ids = id_array
        )),
        headers = {
          'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

class TestFeedBlueprint(BaseTestCase):

    def test_get_ids(self):
        """ Test for feed getting IDs """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Post creation
            create_post(self, access_token)

            # Get the posts
            get_response = get_post_ids(self, access_token)
            get_response_data = json.loads(get_response.data.decode())

            self.assertTrue(get_response_data['success'])
            self.assertFalse(get_response_data['post_ids'] is None)
            self.assertEqual(get_response.status_code, 200)

    def test_get_info(self):
        """ Test for getting feed information """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Post creation
            create_post(self, access_token)

            # Get the posts
            get_response = get_post_ids(self, access_token)
            get_response_data = json.loads(get_response.data.decode())

            id_array = get_response_data['post_ids']

            # Get post information
            get_post_response = get_post_information(self, access_token, id_array)
            get_post_response_data = json.loads(get_post_response.data.decode())

            info_array = get_post_response_data['posts']

            self.assertTrue(get_post_response_data['success'])
            self.assertFalse(info_array[0] is None)
            self.assertEqual(get_post_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()