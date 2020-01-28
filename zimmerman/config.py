import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Change secret keys in production run!
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    DEBUG = False
    # Change the entry key in production
    ENTRY_KEY = os.getenv("ENTRY_KEY", "KonishiTesting")

    # JWT Extended configs
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "4cRK'[pGI%28blJ6$?/Oy+')uG=Txx")
    # Set token to expire every month.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgres://postgres:password@localhost:5432/konishitesting"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgres://postgres:password@localhost:5432/konishi"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
