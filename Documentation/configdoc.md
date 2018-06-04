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
|SECURITY_PASSWORD_SALT| Specifies the HMAC salt. This is only used if the password hash type is set to something other than plain text. Defaults to None.|
|SECURITY_PASSWORD_HASH| Specifies the password hash algorithm to use when hashing passwords. Recommended values for production systems are bcrypt, sha512_crypt, or pbkdf2_sha512. Defaults to bcrypt, Konishi uses pbkdf2_sha512.|
|SECURITY_REGISTERABLE | Specifies if Flask-Security should create a user registration endpoint. The URL for this endpoint is specified by the SECURITY_REGISTER_URL configuration option. Defaults to False. |
|SECURITY_CONFIRMABLE | Specifies if users are required to confirm their email address when registering a new account. If this value is True, Flask-Security creates an endpoint to handle confirmations and requests to resend confirmation instructions. The URL for this endpoint is specified by the SECURITY_CONFIRM_URL configuration option. Defaults to False. |


These are all the settings currently being used in Konishi.

---
## Resources

**Flask-SQLAlchemy - http://flask-sqlalchemy.pocoo.org/2.3/config/#configuration-keys**
> The following configuration values exist for Flask-SQLAlchemy. Flask-SQLAlchemy loads these values from your main Flask config which can be populated in various ways. Note that some of those cannot be modified after the engine was created so make sure to configure as early as possible and to not modify them at runtime.

**Flask-Security - https://pythonhosted.org/Flask-Security/configuration.html**
> Configuration values that can be used with Flask-Security.