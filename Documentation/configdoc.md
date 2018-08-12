# Config.py Documentation
---
This is the documentation regarding the _config.py_ file, its uses and functions.

---
## Definitions
The configuration are just settings to tell Flask or the modules it uses what to use.

|   	|   	|
|---	|---	|
|DEBUG 	|built in debug mode in Flask python, this simply shows what happens in the server side, it is not meant to be used in production. It is a boolean setting so it only takes **True to turn it ON** or **False to turn it OFF** debugging mode.	|
|SECRET_KEY | A secret key is needed to sign the cookies cryptographically, this is needed in order to use _sessions_, during production this should be changed that is not known to the public, you must provide some random bytes or text. 	|
|SQLALCHEMY_DATABASE_URI   |The database URI that should be used for the connection to the database. |
|SQLALCHEMY_TRACK_MODIFICATIONS| If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None, which enables tracking but issues a warning that it will be disabled by default in the future. This requires extra memory and should be disabled if not needed. |
| JWT-SECRET_KEY| The secret key needed for symmetric based signing algorithms, such as HS*. If this is not set, we use the flask SECRET_KEY value instead.|

These are all the settings currently being used in Konishi.

---
## Resources

**Flask-SQLAlchemy - http://flask-sqlalchemy.pocoo.org/2.3/config/#configuration-keys**
> The following configuration values exist for Flask-SQLAlchemy. Flask-SQLAlchemy loads these values from your main Flask config which can be populated in various ways. Note that some of those cannot be modified after the engine was created so make sure to configure as early as possible and to not modify them at runtime.

**Flask-JWT-Extended - http://flask-jwt-extended.readthedocs.io/en/latest/**
> Configuration values that can be used with Flask-JWT-Extended.