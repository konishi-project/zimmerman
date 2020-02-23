import json

from flask import current_app


def register_user(self):
    return self.client.post(
        "/auth/register",
        data=json.dumps(
            dict(
                email="test@user.com",
                username="testUser",
                full_name="Test User",
                password="12345678",
                entry_key=current_app.config["ENTRY_KEY"],
            )
        ),
        content_type="application/json",
    )


def login_user(self):
    return self.client.post(
        "/auth/login",
        data=json.dumps(dict(email="test@user.com", password="12345678")),
        content_type="application/json",
    )
