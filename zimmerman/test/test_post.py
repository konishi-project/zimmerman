import unittest
import json

from zimmerman.test.base import BaseTestCase

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

def delete_post(self, access_token, post_id):
    return self.client.delete(
      '/post/delete/%s' % post_id,
      headers = {
        'Authorization': 'Bearer %s' % access_token
      },
      content_type = 'application/json'
    )

def register_user(self):
    return self.client.post(
      '/user/register',
      data = json.dumps(dict (
          email = 'test@Email.com',
          username = 'testUser',
          first_name = 'test',
          last_name = 'user',
          password = '123456',
          entry_key = 'KonishiTesting'
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

class TestPostBlueprint(BaseTestCase):

    def test_create_post(self):
      ''' Test for post creation and deletion '''

      with self.client:
        # Create a mock user and login
        register_user(self)
        login_response = login_user(self)
        data = json.loads(login_response.data.decode())
        access_token = data['Authorization']

        # Post creation
        user_response = create_post(self, access_token)
        response_data = json.loads(user_response.data.decode())

        self.assertTrue(response_data['success'])
        self.assertEqual(user_response.status_code, 201)
    
        # Delete the post
        post_id = response_data['post']['id']

        delete_response = delete_post(self, access_token, post_id)
        delete_response_data = json.loads(delete_response.data.decode())

        self.assertTrue(delete_response_data['success'])
        self.assertEqual(delete_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()