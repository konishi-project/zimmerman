import unittest
import json

from flask import current_app
from zimmerman.tests.base import BaseTestCase
from zimmerman.tests.common_functions import register_user, login_user


def get_user(self, access_token, username):
    return self.client.get(
        "/user/get/%s" % username,
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


def update_user(self, data, access_token):
    return self.client.put(
        "/user/update",
        data=json.dumps(dict(bio=data["bio"], avatar=data["avatar"])),
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """

        with self.client:
            # User registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())

            self.assertEqual(user_response.status_code, 201)

            # Registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())

            self.assertTrue(data["access_token"])
            self.assertEqual(login_response.status_code, 200)

    def test_get_user(self):
        """ Get a specific user using its public id """

        with self.client:
            # User registration
            register_user(self)
            login_response = login_user(self)
            login_response_data = json.loads(login_response.data.decode())
            access_token = login_response_data["access_token"]

            # Get the user data
            username = login_response_data["user"]["username"]
            get_response = get_user(self, access_token, username)
            get_response_data = json.loads(get_response.data.decode())

            self.assertEqual(get_response.status_code, 200)

    def test_update_user(self):
        """ Test for updating the user """

        with self.client:
            # User registration
            register_user(self)
            login_response = login_user(self)
            login_response_data = json.loads(login_response.data.decode())
            access_token = login_response_data["access_token"]

            # Update the user data
            updated_user = {"bio": "reEeeeEEEEEeEeeeee", "avatar": "test.png"}
            update_response = update_user(self, updated_user, access_token)
            update_response_data = json.loads(update_response.data.decode())

            self.assertTrue(update_response_data["success"])


if __name__ == "__main__":
    unittest.main()
