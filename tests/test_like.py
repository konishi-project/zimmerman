import json

from tests.base import BaseTestCase
from tests.common_functions import register_user, login_user


def create_post(self, access_token):
    return self.client.post(
        "/post/create",
        data=json.dumps(dict(content="Sample content", image_id="")),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def like_post(self, access_token, post_public_id):
    return self.client.post(
        f"/like/post/{post_public_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def unlike_post(self, access_token, post_public_id):
    return self.client.delete(
        f"/like/post/{post_public_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


class TestLikeBlueprint(BaseTestCase):
    def test_post_like_unlike(self):
        """ Test for post liking and unliking """

        with self.client:
            # Create a mock user and login
            register_user(self)
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            access_token = data["access_token"]

            # Post creation
            create_response = create_post(self, access_token)
            create_response_data = json.loads(create_response.data.decode())

            post = create_response_data["post"]
            post_public_id = post["public_id"]

            # Like the post
            like_response = like_post(self, access_token, post_public_id)
            json.loads(like_response.data.decode())

            self.assertEqual(like_response.status_code, 201)

            # Unlike the post
            unlike_response = unlike_post(self, access_token, post_public_id)
            json.loads(unlike_response.data.decode())

            self.assertEqual(unlike_response.status_code, 200)
