import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from zimmerman.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("zimmerman.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config["SECRET_KEY"] == "GahNooSlaShLinUcks")
        self.assertTrue(app.config["DEBUG"])
        self.assertFalse(current_app is None)
        # self.assertTrue(
        #     app.config["SQLALCHEMY_DATABASE_URI"] == "DATABASE_URL",
        #     "sqlite:///" + os.path.join(basedir, "zimmerman.db"),
        # )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("zimmerman.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config["DEBUG"] is False)


if __name__ == "__main__":
    unittest.main()
