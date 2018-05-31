"""
views.py
---
Import the Flask app, ma, and the api from 'app.py'.
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
from flask import jsonify, request
from flask_security.utils import encrypt_password
from flask_security import roles_accepted, roles_required
from flask_admin import Admin, AdminIndexView
from flask_login import login_required
from flask_restplus import Resource, SchemaModel
from models import *
from serializers import *
from decorators import *
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

@api.route('/feed')
class IdFeed(Resource):
    def get(self):
        """ Get IDs from Database
        ---
        This queries the database and grabs the latest IDs,
        the 'limit' query string limits how many IDs are quried
        from the database.
        """
        limit = request.args.get('limit', default=1000)
        # Query Posts
        posts_ids = Posts.query.order_by(Posts.created.desc()).limit(limit).with_entities(Posts.id)
        post_schema = PostSchema(many=True)
        output = [i["id"] for i in post_schema.dump(posts_ids).data]
        return jsonify({'posts_ids': output})

@api.route('/posts')
class NewsFeed(Resource):
    def get(self):
        """
        Read all the posts
        ---
        1. Flask-SQLAlchemy queries all the posts in the Database and orders
        them by their descending dates (Newest to Oldest).
        2. Then the Model Schema for Post is requested so that we can turn
        it into a JSON formatted object.
        3. Then the object's data is dumped from the object and uses the schema
        to understand the model and make it into JSON 
        """
        posts = Posts.query.order_by(Posts.created.desc())
        post_schema = PostSchema(many=True)
        output = post_schema.dump(posts).data
        return jsonify({'posts': output})

    @api.response(201, 'Post has successfully been created')
    @api.expect(user_post)
    def post(self):
        """ Create a new post.
        ---
        The 'data' variable requests for the incoming JSON and then
        we pass those data to the new variables that will be used later
        on as another argument and commit it to the database.
        """
        if authenticated():
            data = request.get_json()
            # Pass the information to the variables
            content = data['content']
            status = data['status']
            modified = data['modified']
            likes = data['likes']
            """
            Create a new variable called 'new_post' and pass the collected data
            from the requested JSON, then 'new_post' is added to the current DB
            session and the changes are commited.
            """
            new_post = Posts(owner_id=current_user.id, creator_name=current_user.username, content=content, status=status, modified=modified, likes=likes)
            db.session.add(new_post)
            db.session.commit()
            return {'message': 'Post has successfully been created'}, 201

@api.route('/post/<int:post_id>')
@api.doc(params={'post_id': 'The unique identifier for the post'})
class InteractPost(Resource):
    @api.response(404, 'Post not found!')
    def get(self, post_id):
        """
        Interact with a specific post
        ---
        1. Flask-SQLAlchemy looks for the Post with the corresponding ID provided by the client side,
        and it checks if it exists, if it doesn't then it will raise a 404 error.
        2. It gets the first Post it finds with that ID.
        3. Then it gets the Model Schema from 'models.py' so that it can be turned into JSON format.
        4. The Post Schema is then used to dump the data about the Post into JSON and then returns
        a JSON formatted output for Flask-RESTPlus 
        """
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return api.abort(404)
        else:
            post_schema = PostSchema()
            output = post_schema.dump(post).data
            return jsonify({'post': output})

    @api.expect(user_post)
    @api.doc(responses={
        404: 'Post not found!',
        403: 'Forbidden',
        200: 'Post successfully been updated'
    })
    def put(self, post_id):
        """
        Update or Edit a specific post
        ---
        1. Flask-SQLAlchemy will query for the post and filters it by provided id, and tries
        to get the first result of the matched unique id.
        2. If it the post is not found it will raise a 404 error, else it will
        update the post with the user provided API Payload, then it commits to the Database.
        """
        if authenticated():
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return api.abort(404)
            # Similar to the get method for specific post but updates instead.
            # Check if the Post belongs to the current user or the current user is an admin.
            elif post.id == current_user.id or is_admin():
                Posts.query.filter_by(id=post_id).update(api.payload)
                db.session.commit()
                return {'result': 'Post has been updated'}, 200
            # If the Post does not belong to the User, return 403.
            elif post.id != current_user.id:
                # Raise 403 error if the current user doesn't match the Post owner id
                return api.abort(403)
            else:
                return {'message': 'Uh oh! Something went wrong.'}

    @api.doc(responses={
        200: 'Post has successfully been deleted',
        403: 'Forbidden',
        404: 'Post not found!'
    })
    def delete(self, post_id):
        """ Delete a specific post by id
        ---
        1. Flask-SQLAlchemy queries the Database and filters the result with the ID provided by the
        client side application. It first checks if the post exist and raises 404 if not.
        2. Once SQLAlchemy finds that specific post, it is then deleted during the session, then
        commits the changes to the Database.
        3. Then Flask-RESTPlus returns the result
        """
        if authenticated():
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return api.abort(404)
            # Check if the Post belongs to the User or the user is an Admin
            elif post.owner_id == current_user.id or is_admin():
                delete_post = Posts.query.filter_by(id=post_id).delete()
                # Commit those changes
                db.session.commit()
                return {'result': 'Post has successfully been deleted'}, 200
            # If the Post does not belong to the User, return 403.
            elif post.owner_id != current_user.id:
                # Raise 403 error if the current user doesn't match the Post owner id
                return api.abort(403)
            else:
                return {'message': 'Uh oh! something went wrong'}

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