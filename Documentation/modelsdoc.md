# Models.py Documentation
---
This is the documentation regarding the _models.py_ file, its uses and functions.

---
## Models and Relationships
#### Models
These are the models that are currently in the file and Konishi uses.

* Role 
* User 
* Posts 
* Comments 
* Reply 

#### Relationships
These are the relationships between models and what they use. **Emphasized text are database models**.

* _Role_ has a Many to Many relationship with _User_.
* _User_ has a One to Many relationship with _Posts_.
* _Posts_ has a One to Many relationship with _Comments_.
* _Comments_ have a One to Many relationship with _Reply_.

We use PostgreSQL and SQLAlchemy to handle these models, check the Resources section for more details and information.

---
## Schemas
These are the schemas within the file and where are they used for. Format is 'Schema' - 'Model it refers to'.

* RoleSchema - Role
* UserSchema - User
* PostSchema - Posts
* CommentSchema - Comments
* ReplySchema - Reply

These schemas are used for turning models into readable dictionaries or json for our API (Flask-RESTPlus)

---
## Admin Views
These are the models and settings for Flask-Admin views, this is set up to protect the views from being accessed by normal users.

* Main Admin Index View
* Protected Model View

---
## Resources
Descriptions are taken from the website, it is not written by us.

**Flask-Admin - https://flask-admin.readthedocs.io/en/latest/**
> Is an admin interface similar to (Django Admin) that let's you
CRUD (Create, Read, Update, Delete) existing data models in your
database with very little effort and saves alot of time.

**Flask-Login - https://flask-login.readthedocs.io/en/latest/**
> Provides user session management for Flask. It handles the common
tasks of logging in, logging out, and remembering your users'
sessions over extended periods of time.

**Flask-Security - https://pythonhosted.org/Flask-Security/**
> Flask-Security allows you to quickly add common security 
mechanisms to your Flask application. 
Flask-SQLAlchemy - 

**PostgreSQL - https://www.postgresql.org/**
> PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.