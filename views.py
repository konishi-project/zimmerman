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

@app.route('/e')
def secretE():
    return redirect('https://e-e.herokuapp.com/')

@api.route('/feed')
class IdFeed(Resource):
    def get(self):
        """ 
        Get IDs from Database
        """
        # Limit how many posts are being queried
        limit = request.args.get('limit', default=1000)
        # Query posts, order by newest to oldest then limit the results, and get the IDs only
        posts_ids = Posts.query.order_by(Posts.created.desc()).limit(limit).with_entities(Posts.id)
        # Grab the post schema
        post_schema = PostSchema(many=True)
        # Get the value of "id" in each list and turn it into an array
        output = [i["id"] for i in post_schema.dump(posts_ids).data]
        return jsonify({'posts_ids': output})

@api.route('/posts')
class NewsFeed(Resource):
    def get(self):
        """
        Read all the posts
        """
        # Query all the posts and order them by newest to oldest
        posts = Posts.query.order_by(Posts.created.desc())
        # Grab the post schema
        post_schema = PostSchema(many=True)
        # Dump the information of the posts
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
            # Create a new post and commit to database.
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
        """
        # Query for specific post from the passed 'post_id'
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            # If does not exist, raise 404
            return api.abort(404)
        else:
            # Grab the post schema
            post_schema = PostSchema()
            # Dump the information of that post
            output = post_schema.dump(post).data
            return jsonify({'post': output})

    @api.expect(user_post)
    @api.doc(responses={
        404: 'Post not found!',
        401: 'Unauthorized',
        403: 'Forbidden',
        200: 'Post successfully been updated'
    })
    def put(self, post_id):
        """
        Update or Edit a specific post
        """
        if authenticated():
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return api.abort(404)
            # Similar to the get method for specific post but updates instead.
            # Check if the Post belongs to the current user or the current user is an admin.
            elif post.id == current_user.id or is_admin():
                # Query and update the post using the payload
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
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Post not found!'
    })
    def delete(self, post_id):
        """ 
        Delete a specific post by id
        """
        if authenticated():
            # Check if there's a post that exists with that id
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return api.abort(404)
            # Check if the Post belongs to the User or the user is an Admin
            elif post.owner_id == current_user.id or is_admin():
                # Delete the post if it exists using the given 'post_id'
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