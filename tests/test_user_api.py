import json

from flask_jwt_extended import create_access_token

from zimmerman import db
from zimmerman.models.user import User
from zimmerman.models.schemas import UserSchema

from tests.utils.base import BaseTestCase


def get_user_data(self, access_token, username):
    return self.client.get(
        f"/user/get/{username}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def update_user_bio(self, access_token, new_bio):
    return self.client.put(
        f"/user/update",
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps(dict(bio=new_bio)),
        content_type="application/json",
    )


class TestUserBlueprint(BaseTestCase):
    def test_user_get(self):
        """ Test getting a user from DB """

        # Create a mock user
        username = "test1234"
        user = User(username=username)

        db.session.add(user)
        db.session.flush()

        access_token = create_access_token(identity=user.id)

        user_resp = get_user_data(self, access_token, username)
        user_data = json.loads(user_resp.data.decode())

        self.assertTrue(user_resp.status)
        self.assertEquals(user_resp.status_code, 200)
        self.assertEquals(user_data["user"]["username"], username)

        # Test a 404 request
        user_404_resp = get_user_data(self, access_token, "nonexistent")
        self.assertEquals(user_404_resp.status_code, 404)

    def test_user_update(self):
        """ Test updating a user """
        bio = "I like beans"
        user = User(bio=bio)

        db.session.add(user)
        db.session.flush()

        access_token = create_access_token(identity=user.id)

        new_bio = "I love Linux"

        update_resp = update_user_bio(self, access_token, new_bio)

        self.assertTrue(update_resp.status)
        self.assertEqual(update_resp.status_code, 200)
