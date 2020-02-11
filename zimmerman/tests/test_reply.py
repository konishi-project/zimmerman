import unittest
import json

from zimmerman.tests.base import BaseTestCase
from zimmerman.tests.common_functions import register_user, login_user


def get_reply(self, reply_public_id, access_token):
    return self.client.get(
        f"/reply/get/{reply_public_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def create_reply(self, access_token, comment_id):
    return self.client.post(
        f"/reply/create/{comment_id}",
        data=json.dumps(dict(content="Sample content")),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def delete_reply(self, access_token, reply_public_id):
    return self.client.delete(
        f"/reply/delete/{reply_public_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def create_post(self, access_token):
    return self.client.post(
        "/post/create",
        data=json.dumps(dict(content="Sample content", image_id="")),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def create_comment(self, access_token, post_public_id):
    return self.client.post(
        f"/comment/create/{post_public_id}",
        data=json.dumps(dict(content="Sample content")),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def update_reply(self, access_token, reply_public_id, data):
    return self.client.put(
        f"/reply/update/{reply_public_id}",
        data=json.dumps(dict(content=data["content"])),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


class TestReplyBlueprint(BaseTestCase):
    def test_create_delete_reply(self):
        """ Test for reply creation and deletion """

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

            comment_id = create_comment_resp_data["comment"]["public_id"]

            # Create a reply
            create_reply_resp = create_reply(self, access_token, comment_id)
            create_reply_resp_data = json.loads(create_reply_resp.data.decode())

            self.assertTrue(create_reply_resp_data["success"])
            self.assertEqual(create_post_resp.status_code, 201)

            # Delete the reply
            reply_public_id = create_reply_resp_data["reply"]["public_id"]

            delete_response = delete_reply(self, access_token, reply_public_id)
            delete_response_data = json.loads(delete_response.data.decode())

            self.assertTrue(delete_response_data["success"])
            self.assertEqual(delete_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
