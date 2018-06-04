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

# Get an array of post feeds
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
            # Create a new post and commit to database.
            new_post = Posts(owner_id=current_user.id, creator_name=current_user.username, content=content, status=status, modified=modified)
            db.session.add(new_post)
            db.session.commit()
            return {'message': 'Post has successfully been created'}, 201

# Post system (Interact with specific posts)
@api.route('/post/<int:post_id>')
class ReadPost(Resource):
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
            return {'message': 'Post not found!'}, 404
        else:
            post_schema = PostSchema()
            output = post_schema.dump(post).data
            return jsonify({'post': output})

    @api.response(200, 'Post successfully been updated.')
    @api.response(404, 'Post not found!')
    @api.expect(user_post)
    def put(self, post_id):
        """
        Update or Edit a specific post
        ---
        1. Flask-SQLAlchemy will query for the post and filters it by provided id, and tries
        to get the first result of the matched unique id.
        2. If it the post is not found it will raise a 404 error, else it will
        update the post with the user provided API Payload, then it commits to the Database.
        """
        # Similar to the get method for specific post but updates instead.
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return {'message': 'Post not found!'}, 404
        else:
            # Get the new data
            data = request.get_json()
            post.content = data['content']
            post.status = data['status']
            db.session.commit()
            return {'message': 'Post has successfully been updated.'}, 200

    @api.response(200, 'Post has successfully been deleted')
    @api.response(404, 'Post not found!')
    def delete(self, post_id):
        """
        Delete a specific post by id
        """
        if authenticated():
            # Query for that post
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return {'message', 'Post not found'}, 404
            else:
                post = Posts.query.filter_by(id=post_id).delete()
                # Commit those changes
                db.session.commit()
                return {'result': 'Post has successfully been deleted'}, 200

# Liking/Unliking System (Post, Comments, Replies)
# Post liking
@api.route('/post/<int:post_id>/like')
class LikePost(Resource):
    def post(self, post_id):
        """
        Like a post.
        """
        if authenticated():
            # Query for that post
            post = Posts.query.filter_by(id=post_id).first()
            # Check if the user already liked
            liked = PostLike.query.filter_by(on_post=post_id).all()
            for like in liked:
                if like.owner_id == current_user.id:
                    return {'message': 'User has already liked the post.'}
                else:
                    pass
            else:
                # Create a like and add it
                likepost = PostLike(on_post=post.id, owner_id=current_user.id)
                # Add to session
                db.session.add(likepost)
                db.session.commit()
                return {'message': 'User has liked the post'}, 200

    def delete(self, post_id):
        """
        Unlike a post.
        """
        if authenticated():
            # Query the post and find the like
            user_like = PostLike.query.filter_by(owner_id=current_user.id).with_entities(PostLike.on_post)
            post = Posts.query.filter_by(id=post_id).first()
            for like in post.likes:
                if like.owner_id == current_user.id:
                    db.session.delete(like)
                    db.session.commit()
            return {'message': 'User has unliked the post'}, 200

# Comment liking
@api.route('/comment/<int:comment_id>/like')
class LikeComment(Resource):
    """
    Like a comment.
    """
    def post(self, comment_id):
        if authenticated():
            # Query for that comment
            comment = Comments.query.filter_by(id=comment_id).first()
            # Check if the user already liked
            liked = CommentLike.query.filter_by(on_comment=comment_id).all()
            for like in liked:
                if like.owner_id == current_user.id:
                    return {'message': 'User has already liked the comment'}
                else:
                    pass
            else:
                # Create a like and add it
                like_comment = CommentLike(on_comment=comment.id, owner_id=current_user.id)
                # Add to session
                db.session.add(like_comment)
                db.session.commit()
                return {'message': 'User has liked the comment'}, 200

    def delete(self, comment_id):
        if authenticated():
            # Query the comment and find the like
            user_like = CommentLike.query.filter_by(owner_id=current_user.id).delete()
            db.session.commit()
            return {'message': 'User has unliked the comment'}, 200

# Reply liking
@api.route('/reply/<int:reply_id>/like')
class LikeReply(Resource):
    """
    Like a reply.
    """
    def post(self, reply_id):
        if authenticated():
            # Query for that reply
            reply = Reply.query.filter_by(id=reply_id).first()
            # Check if the user already liked
            liked = ReplyLike.query.filter_by(on_reply=reply_id).all()
            for like in liked:
                if like.owner_id == current_user.id:
                    return {'message': 'User has already liked the reply'}
                else:
                    pass
            else:
                # Create a like and add it
                like_reply = ReplyLike(on_reply=reply.id, owner_id=current_user.id)
                # Add to session
                db.session.add(like_reply)
                db.session.commit()
                return {'message': 'User has liked the reply'}, 200

    def delete(self, reply_id):
        """
        Unlike a reply.
        """
        if authenticated():
            # Query the reply and find the like
            user_like = ReplyLike.query.filter_by(id=reply_id).delete()
            db.session.commit()
            return {'message': 'User has unliked the reply'}, 200

# Commenting System
@api.route('/post/<int:post_id>/comments')
class PostComments(Resource):
    """
    Comment on a post.
    """
    def get(self, post_id):
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return api.abort(404)
        else:
            post = Posts.query.filter_by(id=post_id).first()
            comments = post.comments
            comment_schema = CommentSchema(many=True)
            output = comment_schema.dump(comments).data
            return jsonify({'comments': output})

    @api.expect(user_comment)
    @api.doc(responses={
        201: 'Commented on the post'
    })
    def post(self, post_id):
        if authenticated():
            data = request.get_json()
            # Pass the information to the variables
            content = data['content']
            modified = data['modified']
            new_comment = Comments(on_post=post_id, commenter=current_user.username, content=content, modified=modified)
            db.session.add(new_comment)
            db.session.commit()
            return {'message': 'Commented on the post'}, 201

# Interact with specific comments, comment API routes.
@api.route('/post/comment/<int:comment_id>')
class InteractComment(Resource):
    """
    Interact with specific comments.
    """
    def get(self, comment_id):
        # Query for the comment
        comment = Comments.query.filter_by(id=comment_id).first()
        if not comment:
            return api.abort(404)
        else:
            comment = Comments.query.filter_by(id=comment_id).first()
            comment_schema = CommentSchema()
            output = comment_schema.dump(comment).data
            return jsonify({'comment': output})

    @api.expect(user_comment)
    @api.doc(responses={
        404: 'Comment not found!',
        401: 'Unauthorized',
        403: 'Forbidden',
        200: 'Comment successfully been updated'
    })
    def put(self, comment_id):
        """
        Update or Edit a specific comment
        """
        if authenticated():
            comment = Comments.query.filter_by(id=comment_id).first()
            if not comment:
                return api.abort(404)
            # Similar to the get method for specific post but updates instead.
            # Check if the Post belongs to the current user or the current user is an admin.
            elif comment.id == current_user.id or is_admin():
                # Get the new data
                data = request.get_json()
                comment.content = data['content']
                db.session.commit()
                return {'message': 'Comment has successfully been updated.'}, 200
            # If the Post does not belong to the User, return 403.
            elif comment.commenter != current_user.username:
                # Raise 403 error if the current user doesn't match the Post owner id
                return api.abort(403)
            else:
                return {'message': 'Uh oh! Something went wrong.'}

    def delete(self, comment_id):
        """ 
        Delete a specific comment by id
        """
        if authenticated():
            # Check if there's a post that exists with that id
            comment = Comments.query.filter_by(id=comment_id).first()
            if not comment:
                return api.abort(404)
                # Check if the Post belongs to the User or the user is an Admin
            elif comment.owner_id == current_user.id or is_admin():
                # Delete the post if it exists using the given 'post_id'
                delete_comment = Comments.query.filter_by(id=comment_id).delete()
                # Commit those changes
                db.session.commit()
                return {'result': 'Post has successfully been deleted'}, 200
            # If the Post does not belong to the User, return 403.
            elif comment.commenter != current_user.username:
                # Raise 403 error if the current user doesn't match the Post owner id
                return {'message': 'This comment does not belong to you'}
            else:
                return {'message': 'Uh oh! something went wrong'}
        
# Reply System
@api.route('/comment/<int:comment_id>/replies')
class PostComments(Resource):
    """
    Reply to a comment.
    """
    def get(self, comment_id):
        comment = Comments.query.filter_by(id=comment_id).first()
        if not comment:
            return {'message': 'Comment not found.'}, 404
        else:
            comments = Comments.query.filter_by(id=comment_id).first()
            replies = comments.replies
            reply_schema = ReplySchema(many=True)
            output = reply_schema.dump(replies).data
            return jsonify({'replies': output})

    @api.expect(user_reply)
    @api.doc(responses={
        201: 'Replied on the comment'
    })
    def post(self, comment_id):
        if authenticated():
            data = request.get_json()
            # Pass the information to the variables
            content = data['content']
            modified = data['modified']
            new_reply = Reply(on_comment=comment_id, replier=current_user.username, content=content, modified=modified)
            db.session.add(new_reply)
            db.session.commit()
            return {'message': 'Replied on the comment'}, 201

# Interact with specific replies, reply API routes.
@api.route('/comment/reply/<int:reply_id>')
class InteractComment(Resource):
    """
    Interact with specific replies
    """
    def get(self, reply_id):
        # Query for the Reply
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            return {'message': 'Reply not found'}, 404
        else:
            reply = Reply.query.filter_by(id=reply_id).first()
            reply_schema = ReplySchema()
            output = reply_schema.dump(reply).data
            return jsonify({'comment': output})

    @api.expect(user_reply)
    @api.doc(responses={
        404: 'Reply not found!',
        401: 'Unauthorized',
        403: 'Forbidden',
        200: 'Reply successfully been updated'
    })
    def put(self, reply_id):
        """
        Update or Edit a specific Reply
        """
        if authenticated():
            reply = Reply.query.filter_by(id=reply_id).first()
            if not reply:
                return api.abort(404)
            # Check if the Reply belongs to the current user or the current user is an admin.
            elif reply.replier == current_user.username or is_admin():
                # Get the new data
                data = request.get_json()
                reply.content = data['content']
                db.session.commit()
                return {'message': 'Reply has successfully been updated.'}, 200
            # If the Reply does not belong to the User, return 403.
            elif reply.replier != current_user.username:
                # Raise 403 error if the current user doesn't match the Post owner id
                return {'message': 'This reply does not belong to you'}
            else:
                return {'message': 'Uh oh! Something went wrong.'}

    def delete(self, reply_id):
        """ 
        Delete a specific reply by id
        """
        if authenticated():
            # Check if there's a reply that exists with that id
            reply = Reply.query.filter_by(id=reply_id).first()
            if not reply:
                return {'message': 'Reply not found'}, 404
                # Check if the Reply belongs to the User or the user is an Admin
            elif reply.replier == current_user.username or is_admin():
                # Delete the reply if it exists using the given 'post_id'
                delete_comment = Comments.query.filter_by(id=comment_id).delete()
                # Commit those changes
                db.session.commit()
                return {'result': 'Reply has successfully been deleted'}, 200
            # If the Post does not belong to the User, return 403.
            elif reply.replier != current_user.username:
                # Raise 403 error if the current user doesn't match the Post owner id
                return {'message': 'This reply does not belong to you'}
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
