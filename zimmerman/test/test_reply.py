import unittest
import json

from flask import current_app
from zimmerman.test.base import BaseTestCase

def get_reply(self, reply_id, access_token):
    return self.client.get(
        '/reply/get/%s' % reply_id,
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

def create_reply(self, access_token, comment_id):
    return self.client.post(
        '/reply/create/%s' % comment_id,
        data = json.dumps(dict (
            content = 'Sample content'
        )),
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
        content_type = 'application/json'
    )

def delete_reply(self, access_token, reply_id):
    return self.client.delete(
        '/reply/delete/%s' % reply_id,
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

def update_reply(self, access_token, reply_id, data):
    return self.client.put(
        '/reply/update/%s' % reply_id,
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

class TestReplyBlueprint(BaseTestCase):

    def test_create_delete_reply(self):
        """ Test for reply creation and deletion """

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

            comment_id = create_comment_resp_data['comment']['id']

            # Create a reply
            create_reply_resp = create_reply(self, access_token, comment_id)
            create_reply_resp_data = json.loads(create_reply_resp.data.decode())

            self.assertTrue(create_reply_resp_data['success'])
            self.assertEqual(create_post_resp.status_code, 201)

            # Delete the reply
            reply_id = create_reply_resp_data['reply']['id']

            delete_response = delete_reply(self, access_token, reply_id)
            delete_response_data = json.loads(delete_response.data.decode())

            self.assertTrue(delete_response_data['success'])
            self.assertEqual(delete_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()