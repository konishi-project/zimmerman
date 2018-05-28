"""
Import the Flask app and the api from 'app.py'.
Encrypt Password will be used to add users without registering them with
a default password that can be changed later on, but is encrypted.
More information related to Flask-Security found here:
https://pythonhosted.org/Flask-Security/
We use Flask-Login for handling current user and sessions.
Documentation - https://flask-login.readthedocs.io/en/latest
Flask-Admin is used for managing and CRUD models, This is similar to Django Admin.
Documentation - https://flask-admin.readthedocs.io/en/latest/
Flask-RESTPlus is used for the APIs and API routings.
Documentation - https://flask-restplus.readthedocs.io/en/stable/
---
Import all the models from 'models.py' which will be used when interacting
with the API and Routes.
Flask-SQLAlchemy will be used as the ORM.
Documentation - http://flask-sqlalchemy.pocoo.org/2.3/
"""
from app import app, api, ma
from flask import jsonify, request, json
from flask_security.utils import encrypt_password
from flask_security import roles_accepted, roles_required
from flask_admin import Admin, AdminIndexView
from flask_login import login_required
from flask_restplus import Resource, SchemaModel
from models import *
from serializers import *
import os

"""
This will tell Flask-Admin which is which (admin), We pass the arguments
it needs to know what to add, and specify the MainAdminIndexView (import from models)
Bootstrap 3 comes with Flask-Admin but this isn't really a public page so it doesn't
matter. MainAdminIndexView is already protected as seen in the models.
"""
admin = Admin(app, name='Admin Area', template_mode='bootstrap3', index_view=MainAdminIndexView())

""" 
This is to create tables and models in the database.
This should be commented out when the database models are created.
@app.before_first_request will be ran first before any request and
execute whatever is in it, "before_first_request()" is also needed.
"""

@api.route('/posts')
class NewsFeed(Resource):
    def get(self):
        posts = Posts.query.order_by(Posts.created.desc())
        post_schema = PostSchema(many=True)
        output = post_schema.dump(posts).data
        return jsonify({'posts': output})

    @api.response(201, 'Post has been successfully created')
    @api.expect(user_post)
    def post(self):
        data = request.get_json()
        # Get Information from the data
        owner_id = data['owner_id']
        creator_name = data['creator_name']
        content = data['content']
        status = data['status']
        modified = data['modified']
        likes = data['likes']
        # Add to the Database
        new_post = Posts(owner_id=owner_id, creator_name=creator_name, content=content, status=status, modified=modified, likes=likes)
        # Add to DB Session
        db.session.add(new_post)
        # Commit to Database
        db.session.commit()
        return 201

@api.route('/post/<int:post_id>')
class ReadPost(Resource):
    def get(self, post_id):
        post = Posts.query.filter_by(id=post_id).first()
        post_schema = PostSchema()
        output = post_schema.dump(post).data
        return jsonify({'post': output})
    @api.response(200, 'Post has successfully been deleted')
    def delete(self, post_id):
        # Delete the post from the ID
        post = Posts.query.filter_by(id=post_id).delete()
        # Commit those changes
        db.session.commit()
        return {'result': 'Post has successfully been deleted'}

""" 
Add Admin Views,
This will add the models for Flask-Admin which will appear in the Admin
page, then we can CRUD these models and objects within it using Flask-Admin.
"""
admin.add_view(ProtectedModelView(Role, db.session))
admin.add_view(ProtectedModelView(User, db.session))
admin.add_view(ProtectedModelView(Posts, db.session))
admin.add_view(ProtectedModelView(Comments, db.session))
admin.add_view(ProtectedModelView(Reply, db.session))