import unittest
import json

from zimmerman.tests.base import BaseTestCase
from zimmerman.tests.common_functions import register_user, login_user


def get_comment(self, comment_public_id, access_token):
    return self.client.get(
        "/comment/get/%s" % comment_public_id,
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


def create_comment(self, access_token, post_public_id):
    return self.client.post(
        "/comment/create/%s" % post_public_id,
        data=json.dumps(dict(content="Sample content")),
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


def delete_comment(self, access_token, comment_public_id):
    return self.client.delete(
        "/comment/delete/%s" % comment_public_id,
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


def create_post(self, access_token):
    return self.client.post(
        "/post/create",
        data=json.dumps(dict(content="Sample content", image_id="")),
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


def update_comment(self, comment_public_id, access_token, data):
    return self.client.put(
        "/comment/update/%s" % comment_public_id,
        data=json.dumps(dict(content=data["content"])),
        headers={"Authorization": "Bearer %s" % access_token},
        content_type="application/json",
    )


class TestCommentBlueprint(BaseTestCase):
    def test_create_delete_comment(self):
        """ Test for comment creation and deletion """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data["access_token"]

            # Create a mock post
            create_post_resp = create_post(self, access_token)
            create_post_resp_data = json.loads(create_post_resp.data.decode())

            post_public_id = create_post_resp_data["post"]["public_id"]

            # Create a comment
            create_comment_resp = create_comment(self, access_token, post_public_id)
            create_comment_resp_data = json.loads(create_comment_resp.data.decode())

            self.assertTrue(create_comment_resp_data["success"])
            self.assertEqual(create_comment_resp.status_code, 201)

            # Delete the comment
            comment_public_id = create_comment_resp_data["comment"]["public_id"]

            delete_response = delete_comment(self, access_token, comment_public_id)
            delete_response_data = json.loads(delete_response.data.decode())

            self.assertTrue(delete_response_data["success"])
            self.assertEqual(delete_response.status_code, 200)

    def test_comment_update(self):
        """ Test for comment updating """

        with self.client:
            # Create a mock comment and update it
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data["access_token"]

            # Create a mock post
            create_post_resp = create_post(self, access_token)
            create_post_rest_data = json.loads(create_post_resp.data.decode())

            post_public_id = create_post_rest_data["post"]["public_id"]

            # Create a comment
            create_comment_resp = create_comment(self, access_token, post_public_id)
            create_comment_resp_data = json.loads(create_comment_resp.data.decode())

            # Update the comment
            comment_public_id = create_comment_resp_data["comment"]["public_id"]
            updated_content = {"content": "Updated content"}
            update_response = update_comment(
                self, comment_public_id, access_token, updated_content
            )
            update_response_data = json.loads(update_response.data.decode())

            self.assertTrue(update_response_data["success"])
            self.assertEqual(update_response.status_code, 200)

    def test_comment_get(self):
        """ Test for getting specific comment """

        with self.client:
            # Create a temporary user
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data["access_token"]

            # Create a mock post
            create_post_resp = create_post(self, access_token)
            create_post_rest_data = json.loads(create_post_resp.data.decode())

            post_public_id = create_post_rest_data["post"]["public_id"]

            # Create a comment
            create_comment_resp = create_comment(self, access_token, post_public_id)
            create_comment_resp_data = json.loads(create_comment_resp.data.decode())

            # Get that comment
            comment_public_id = create_comment_resp_data["comment"]["public_id"]
            get_comment_response = get_comment(self, comment_public_id, access_token)
            get_comment_response_data = json.loads(get_comment_response.data.decode())

            # Get the content for comparison
            original_content = create_comment_resp_data["comment"]["content"]
            received_content = get_comment_response_data["comment"]["content"]

            self.assertTrue(get_comment_response_data["success"])
            self.assertEqual(get_comment_response.status_code, 200)
            self.assertEqual(original_content, received_content)


if __name__ == "__main__":
    unittest.main()
