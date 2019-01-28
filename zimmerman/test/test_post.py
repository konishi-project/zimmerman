import unittest
import json

from zimmerman.test.base import BaseTestCase

def get_post(self, access_token, public_id):
    return self.client.get(
        '/post/get/%s' % public_id,
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
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

def delete_post(self, access_token, public_id):
    return self.client.delete(
        '/post/delete/%s' % public_id,
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

def update_post(self, data, access_token, public_id):
    return self.client.put(
        '/post/update/%s' % public_id,
        data = json.dumps(dict (
            content = data['content']
        )),
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

    def test_create_delete_post(self):
        """ Test for post creation and deletion """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Post creation
            create_response = create_post(self, access_token)
            create_response_data = json.loads(create_response.data.decode())

            self.assertTrue(create_response_data['success'])
            self.assertEqual(create_response.status_code, 201)
        
            # Delete the post
            post_public_id = create_response_data['post']['public_id']

            delete_response = delete_post(self, access_token, post_public_id)
            delete_response_data = json.loads(delete_response.data.decode())

            self.assertTrue(delete_response_data['success'])
            self.assertEqual(delete_response.status_code, 200)
    
    def test_post_update(self):
        """ Test for post updating """

        with self.client:
            # Create a mock post and update it.
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Create a post
            create_response = create_post(self, access_token)
            create_response_data = json.loads(create_response.data.decode())

            # Update the post
            post_public_id = create_response_data['post']['public_id']
            updated_content = {
                'content': 'Updated content'
            }
            update_response = update_post(self, updated_content, access_token, post_public_id)
            update_response_data = json.loads(update_response.data.decode())

            # Compare data
            original_content = create_response_data['post']['content']

            self.assertNotEqual(original_content, updated_content)
            self.assertEqual(update_response.status_code, 200)
            self.assertTrue(update_response_data['success'])
    
    def test_post_get(self):
        """ Test for getting specific posts """

        with self.client:
            # Create a temporary user
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Create a post
            create_post_response = create_post(self, access_token)
            create_post_response_data = json.loads(create_post_response.data.decode())

            # Get that post
            post_public_id = create_post_response_data['post']['public_id']
            get_post_response = get_post(self, access_token, post_public_id)
            get_post_response_data = json.loads(get_post_response.data.decode())

            # Get content for comparison
            original_content = create_post_response_data['post']['content']
            received_content = get_post_response_data['post']['content']

            self.assertEqual(get_post_response.status_code, 200)
            self.assertTrue(get_post_response_data['success'])
            self.assertEqual(original_content, received_content)

if __name__ == '__main__':
    unittest.main()