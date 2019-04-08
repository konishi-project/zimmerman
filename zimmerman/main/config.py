import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "4cRK'[pGI%28blJ6$?/Oy+')uG=Txx")
    # Set token to never expire.
    JWT_ACCESS_TOKEN_EXPIRES = False
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://postgres:password@localhost:5432/konishidb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://postgres:password@localhost:5432/konishidb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_by_name = dict(
            dev = DevelopmentConfig,
            test = TestingConfig,
            prod = ProductionConfig
        )

key = Config.SECRET_KEY
