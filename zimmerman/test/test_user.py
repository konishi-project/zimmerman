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

def get_user(self, access_token):
    return self.client.get(
        '/user/get',
        headers = {
            'Authorization': 'Bearer %s' % access_token
        },
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

class TestAuthBlueprint(BaseTestCase):

    def test_registered_user_login(self):
        ''' Test for login of registered-user login '''

        with self.client:
            # User registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())

            self.assertEqual(user_response.status_code, 201)

            # Registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())

            self.assertTrue(data['Authorization'])
            self.assertEqual(login_response.status_code, 200)

    def test_get_user(self):
        ''' Get a specific user using its public id '''

        with self.client:
            # User registration
            register_user(self)
            login_response = login_user(self)
            login_response_data = json.loads(login_response.data.decode())
            access_token = login_response_data['Authorization']

            # Get the user data
            get_response = get_user(self, access_token)

            self.assertEqual(get_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()