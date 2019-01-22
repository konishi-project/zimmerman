import unittest
import json

from zimmerman.test.base import BaseTestCase

def create_comment(self, access_token, post_public_id):
    return self.client.post(
      '/comment/create/%s' % post_public_id,
      data = json.dumps(dict (
        content = 'Sample content'
      )),
      headers = {
        'Authorization': 'Bearer %s' % access_token
      },
      content_type = 'application/json'
    )

def delete_comment(self, access_token, comment_id):
    return self.client.delete(
        '/comment/delete/%s' % comment_id,
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

class TestCommentBlueprint(BaseTestCase):

    def test_create_delete_comment(self):
        """ Test for comment creation and deletion """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data['Authorization']

            # Create a mock post
            create_post_resp = create_post(self, access_token)
            create_post_resp_data = json.loads(create_post_resp.data.decode())

            post_public_id = create_post_resp_data['post']['public_id']

            # Create a comment
            create_comment_resp = create_comment(self, access_token, post_public_id)
            create_comment_resp_data = json.loads(create_comment_resp.data.decode())

            self.assertTrue(create_comment_resp_data['success'])
            self.assertEqual(create_comment_resp.status_code, 201)

            # Delete the comment
            comment_id = create_comment_resp_data['comment']['id']

            delete_response = delete_comment(self, access_token, comment_id)
            delete_response_data = json.loads(delete_response.data.decode())

            self.assertTrue(delete_response_data['success'])
            self.assertEqual(delete_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()