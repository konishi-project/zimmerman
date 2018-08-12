"""
views.py
---
Import the Flask app, ma, and the api from 'app.py'.
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
from app import app, api, ma, jwt, limiter
from flask import jsonify, request
from flask_admin import Admin, AdminIndexView
from flask_restplus import Resource, SchemaModel
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import *
from serializers import *
from decorators import *
from datetime import datetime, timedelta
from uuid import uuid4
import json
import glob
import os
import hashlib

"""
This is the Admin route, how it is protected can be found in 'models.py'.
"""
admin = Admin(app, name='Admin Area', template_mode='bootstrap3', index_view=MainAdminIndexView())

# Get an array of post feeds
@api.route('/feed')
class IdFeed(Resource):
    def get(self):
        """  Get Post IDs from Database. """
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
    @jwt_required
    @limiter.limit('20/day;10/hour;5/minute')
    def get(self):
        """ Read all the posts. """
        # Query all the posts and order them by newest to oldest
        posts = Posts.query.order_by(Posts.created.desc())
        # Grab the post schema
        post_schema = PostSchema(many=True)
        # Dump the information of the posts
        output = post_schema.dump(posts).data
        return jsonify(output)

    @api.response(201, 'Post has successfully been created')
    @api.expect(user_post)
    @jwt_required
    @limiter.limit('10/day;5/hour')
    def post(self):
        """ Create a new post. """
        current_user = load_user(get_jwt_identity())
        # Get the incoming JSON body.
        data = request.get_json()
        # Pass the information to the variables
        content = data['content']
        image_id = data['image_id']
        # Create a new post and commit to database.
        new_post = Posts(owner_id=current_user.id, creator_name=current_user.username, 
                   content=content, image_file=image_id,status='NORMAL', modified=datetime.now())
        db.session.add(new_post)
        db.session.commit()
        return {'message': 'Post has successfully been created', 'success': True}, 201

# Post system (Interact with specific posts)
@api.route('/post/<int:post_id>')
class ReadPost(Resource):
    @api.response(404, 'Post not found!')
    def get(self, post_id):
        """ Interact with a specific post. """
        # Get specific post using the post_id
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return {'message': 'Post not found!'}, 404
        else:
            post = Posts.query.filter_by(id=post_id).first()
            post_schema = PostSchema()
            output = post_schema.dump(post).data
            # Check if there's an image file
            if post.image_file != None:
                # Get the id
                img_id = post.image_file
                # Search for the img in the post image files
                img_url = glob.glob(os.path.join(POST_UPLOAD_PATH, '{}.*'.format(img_id)))
                # Attach it and jsonify the output
                output['image_url'] = img_url[0]
                return jsonify({'post': output})
            return jsonify({'post': output})

    @api.response(200, 'Post successfully been updated.')
    @api.response(404, 'Post not found!')
    @api.expect(user_post)
    @jwt_required
    def put(self, post_id):
        """ Update or Edit a specific post. """
        current_user = load_user(get_jwt_identity())
        # Similar to the get method for specific post but updates instead.
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return {'message': 'Post not found!'}, 404
        elif current_user.id == post.owner_id and post.status == 'NORMAL' or is_admin(current_user):
            # Get the new data
            data = request.get_json()
            post.content = data['content']
            db.session.commit()
            return {'message': 'Post has successfully been updated.'}, 200
        elif post.status == 'LOCKED':
            return {'message': 'This post is locked.'}, 403
        else:
            return jsonify({'message': 'You do not own this post.'}), 403

    @api.response(200, 'Post has successfully been deleted')
    @api.response(404, 'Post not found!')
    @jwt_required
    def delete(self, post_id):
        """ Delete a specific post by id. """
        current_user = load_user(get_jwt_identity())
        # Query for that post
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return {'message', 'Post not found.'}, 404
        elif current_user.id == post.owner_id or is_admin(current_user):
            post = Posts.query.filter_by(id=post_id).delete()
            # Commit those changes
            db.session.commit()
            return jsonify({'result': 'Post has successfully been deleted.'}), 200

# Liking/Unliking System (Post, Comments, Replies)
# Post liking
@api.route('/post/<int:post_id>/like')
class LikePost(Resource):
    @jwt_required
    def post(self, post_id):
        """ Like a post. """
        current_user = load_user(get_jwt_identity())
        # Query for that post
        post = Posts.query.filter_by(id=post_id).first()
        # Check if the user already liked
        likes = PostLike.query.filter_by(on_post=post_id).all()
        if check_like(likes, current_user):
            return {'message': 'User has already liked the post.'}, 403
        else:
            # Create a like and add it
            likepost = PostLike(on_post=post.id, owner_id=current_user.id)
            # Add to session
            db.session.add(likepost)
            db.session.commit()
            return {'message': 'User has liked the post.'}, 201

    @jwt_required
    def delete(self, post_id):
        """ Unlike a post. """
        current_user = load_user(get_jwt_identity())
        # Query the post and find the like
        post = Posts.query.filter_by(id=post_id).first()
        for like in post.likes:
            if like.owner_id == current_user.id:
                db.session.delete(like)
                db.session.commit()
        return {'message': 'User has unliked the post.'}, 200

# Comment liking
@api.route('/comment/<int:comment_id>/like')
class LikeComment(Resource):
    @jwt_required
    def post(self, comment_id):
        """ Like a comment. """
        current_user = load_user(get_jwt_identity())
        # Query for that comment
        comment = Comments.query.filter_by(id=comment_id).first()
        # Check if the user already liked
        likes = CommentLike.query.filter_by(on_comment=comment_id).all()
        if check_like(likes, current_user):
            return jsonify({'message': 'User has already liked the comment.'}), 403
        else:
            # Create a like and add it
            like_comment = CommentLike(on_comment=comment.id, owner_id=current_user.id)
            # Add to session
            db.session.add(like_comment)
            db.session.commit()
            return jsonify({'message': 'User has liked the comment.'}), 201

    @jwt_required
    def delete(self, comment_id):
        """ Unlike a comment. """
        current_user = load_user(get_jwt_identity())
        # Query the comment and find the like
        comment = Comments.query.filter_by(id=comment_id).first()
        for like in comment.likes:
            if like.owner_id == current_user.id:
                db.session.delete(like)
                db.session.commit()
        return {'message': 'User has unliked the comment.'}, 200

# Reply liking
@api.route('/reply/<int:reply_id>/like')
class LikeReply(Resource):
    @jwt_required
    def post(self, reply_id):
        """ Like a reply. """
        current_user = load_user(get_jwt_identity())
        # Query for that reply
        reply = Reply.query.filter_by(id=reply_id).first()
        # Check if the user already liked
        likes = ReplyLike.query.filter_by(on_reply=reply_id).all()
        if check_like(likes, current_user):
            return {'message': 'User has already liked the reply.'}, 403
        else:
            # Create a like and add it
            like_reply = ReplyLike(on_reply=reply.id, owner_id=current_user.id)
            # Add to session
            db.session.add(like_reply)
            db.session.commit()
            return {'message': 'User has liked the reply.'}, 201

    def delete(self, reply_id):
        """ Unlike a reply. """
        # Query the comment and find the like
        reply = Reply.query.filter_by(id=reply_id).first()
        for like in reply.likes:
            if like.owner_id == current_user.id:
                db.session.delete(like)
                db.session.commit()
        return {'message': 'User has unliked the reply.'}, 200

# Commenting System
@api.route('/post/<int:post_id>/comments')
class PostComments(Resource):
    def get(self, post_id):
        """ Read comments on a specific post. """
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            return {'message': 'Post not found!'}, 404
        else:
            post = Posts.query.filter_by(id=post_id).first()
            comments = post.comments
            comment_schema = CommentSchema(many=True)
            output = comment_schema.dump(comments).data
            return jsonify({'comments': output})

    @api.expect(user_comment)
    @api.doc(responses={
        201: 'Commented on the post.'
    })
    @jwt_required
    def post(self, post_id):
        """ Comment on a specific post. """
        post = Posts.query.filter_by(id=post_id).first()
        # Check if post is not locked.
        if post.status.lower() == 'normal':
            current_user = load_user(get_jwt_identity())
            data = request.get_json()
            # Pass the information to the variables
            content = data['content']
            new_comment = Comments(on_post=post_id, commenter=current_user.username,
                                   content=content, modified=datetime.now())
            db.session.add(new_comment)
            db.session.commit()
            return {'message': 'Commented on the post.'}, 201
        else:
            return {'message': 'Post is locked, unable to comment.'}, 403

# Interact with specific comments, comment API routes.
@api.route('/post/comment/<int:comment_id>')
class InteractComment(Resource):
    def get(self, comment_id):
        """
        Get a specific comment.
        """
        # Query for the comment
        comment = Comments.query.filter_by(id=comment_id).first()
        if not comment:
            return {'message': 'Comment not found.'}, 404
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
    @jwt_required
    def put(self, comment_id):
        """
        Update or Edit a specific comment
        """
        current_user = load_user(get_jwt_identity())
        # Get information
        comment = Comments.query.filter_by(id=comment_id).first()
        if not comment:
            return {'message': 'Comment not found!'}, 404
        # Check if the Post belongs to the current user or the current user is an admin.
        elif comment.commenter == current_user.username or is_admin(current_user):
            # Get the new data
            data = request.get_json()
            comment.content = data['content']
            db.session.commit()
            return jsonify({'message': 'Comment has successfully been updated.'}), 200
        # If the Post does not belong to the User, return 403.
        elif comment.commenter != current_user.username:
            # Raise 403 error if the current user doesn't match the Post owner id
            return {'message': 'This comment does not belong to you.'}, 403
        else:
            return {'message': 'Uh oh! Something went wrong.'}, 500

    @jwt_required
    def delete(self, comment_id):
        """ 
        Delete a specific comment by id
        """
        current_user = load_user(get_jwt_identity())
        # Check if there's a post that exists with that id
        comment = Comments.query.filter_by(id=comment_id).first()
        if not comment:
            return {'message': 'Comment not found.'}, 404
            # Check if the Post belongs to the User or the user is an Admin
        elif comment.commenter == current_user.username or is_admin(current_user):
            # Delete the post if it exists using the given 'post_id'
            delete_comment = Comments.query.filter_by(id=comment_id).delete()
            # Commit those changes
            db.session.commit()
            return {'message': 'Post has successfully been deleted.'}, 200
        # If the Post does not belong to the User, return 403.
        elif comment.commenter != current_user.username:
            # Raise 403 error if the current user doesn't match the Post owner id
            return {'message': 'This comment does not belong to you.'}, 403
        else:
            return {'message': 'Uh oh! Something went wrong,'}, 500
        
# Reply System
@api.route('/comment/<int:comment_id>/replies')
class PostComments(Resource):
    def get(self, comment_id):
        """ Reply to a comment. """
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
        201: 'Replied on the comment.'
    })
    @jwt_required
    def post(self, comment_id):
        """ Reply on a specific comment. """
        current_user = load_user(get_jwt_identity())
        data = request.get_json()
        # Pass the information to the variables
        content = data['content']
        new_reply = Reply(on_comment=comment_id, replier=current_user.username, 
                          content=content, modified=datetime.now())
        db.session.add(new_reply)
        db.session.commit()
        return {'message': 'Replied on the comment.'}, 201

# Interact with specific replies, reply API routes.
@api.route('/comment/reply/<int:reply_id>')
class InteractComment(Resource):
    def get(self, reply_id):
        """
        Get a specific reply.
        """
        # Query for the Reply
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            return {'message': 'Reply not found.'}, 404
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
    @jwt_required
    def put(self, reply_id):
        """ Update or Edit a specific Reply. """
        current_user = load_user(get_jwt_identity())
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            return {'message': 'Reply not found!'}, 404
        # Check if the Reply belongs to the current user or the current user is an admin.
        elif reply.replier == current_user.username or is_admin(current_user):
            # Get the new data
            data = request.get_json()
            reply.content = data['content']
            db.session.commit()
            return {'message': 'Reply has successfully been updated.'}, 200
        # If the Reply does not belong to the User, return 403.
        elif reply.replier != current_user.username:
            # Raise 403 error if the current user doesn't match the Post owner id
            return {'message': 'This reply does not belong to you.'}, 403
        else:
            return {'message': 'Uh oh! Something went wrong.'}, 500

    @jwt_required
    def delete(self, reply_id):
        """ Delete a specific reply by id. """
        current_user = load_user(get_jwt_identity())
        # Check if there's a reply that exists with that id
        reply = Reply.query.filter_by(id=reply_id).first()
        if not reply:
            return {'message': 'Reply not found'}, 404
            # Check if the Reply belongs to the User or the user is an Admin
        elif reply.replier == current_user.username or is_admin(current_user):
            # Delete the reply if it exists using the given 'post_id'
            delete_comment = Comments.query.filter_by(id=comment_id).delete()
            # Commit those changes
            db.session.commit()
            return {'result': 'Reply has successfully been deleted'}, 200
        # If the Post does not belong to the User, return 403.
        elif reply.replier != current_user.username:
            # Raise 403 error if the current user doesn't match the Post owner id
            return {'message': 'This reply does not belong to you'}, 403
        else:
            return {'message': 'Uh oh! Something went wrong.'}, 500

# Will be removed once everything works well.
@api.route('/protected')
class Protect(Resource):
    @jwt_required
    def get(self):
        """ Route for testing jwt and security. """
        current_user = load_user(get_jwt_identity())
        if is_admin(current_user):
            return {
                'username': current_user.username,
                'public_id': current_user.public_id,
                'status': current_user.status,
            }, 200
        return jsonify({'message': current_user.username})

@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_login)
    @limiter.limit('5/day;1/minute')
    def post(self):
        """ Login and get a token. """
        data = request.get_json()
        if not data or not data['username'] or not data['password']:
            return {'msg': 'No login data found!'}, 404
        username = data['username']
        password = data['password']
        # Query and check if the User is in the Database
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found!'}, 404
        if user.username == username and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username, expires_delta=False)
            return {'access_token': access_token, 'success': True}, 200
        else:
            return {'msg': 'Invalid credentials!'}, 401

@api.route('/currentuser')
class CurrentUser(Resource):
    @jwt_required
    def get(self):
        currentUser = load_user(get_jwt_identity())
        userSchema = UserSchema()
        output = userSchema.dump(currentUser).data
        return jsonify(output)

@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_registration)
    def post(self):
        """ Register to Konishi. """
        # Get json objects
        data = request.get_json()
        # Pass the data
        email = data['email']
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        first_name = data['first_name']
        last_name = data['last_name']
        entry_key = data['entry_key']
        # Check if the email is used
        if User.query.filter_by(email=email).first() is not None:
            return {'message': 'Email already taken!', 'reason': 'email'}, 403
        # Check if the username exists
        if User.query.filter_by(username=username).first() is not None:
            return {'message': 'Username already taken!', 'reason': 'username'}, 403
        if password != confirm_password:
            return {'message': 'Passwords don\'t match!'}, 406
        # Check if entry key is right
        if entry_key != app.config['ENTRY_KEY']:
            return {'message': 'Entry key not correct!', 'reason': 'key'}, 406
        else:
            pass
        hashed_password = generate_password_hash(password, method='sha512')
        new_user = User(public_id=str(uuid4()), email=email, username=username, password=hashed_password,
                        first_name=first_name, last_name=last_name, joined_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Successfully registered!', 'success': True}, 200

# Uploading
POST_UPLOAD_PATH = 'static/user_files/contentimg/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/imageupload')
class PostImage(Resource):
    @jwt_required
    def post(self):
        """ Upload an image. """
        # Check if there's a file
        if 'file' not in request.files:
            return {'message': 'File not found!'}, 404
        file = request.files['file']
        # Check if the filename is not none
        if file.filename == '':
            return {'message': 'No select file.'}, 403
        if file and allowed_file(file.filename):
            # Get the filename
            filename = file.filename
            extension = '.' + filename.split('.')[1]
            # Hash the file and limit to 32 chars
            hashed_file = hashlib.sha256(str(file.filename).encode('utf-8')).hexdigest()[:32]
            # Save it and attach the extension
            file.save(os.path.join(POST_UPLOAD_PATH, hashed_file + extension))
            # Return hashed filename to the client
            return jsonify({'success': True, 'image_id': hashed_file})

""" 
Add Admin Views,
This will add the models for Flask-Admin which will appear in the Admin
page, then we can CRUD these models and objects within it using Flask-Admin.
"""
admin.add_view(ProtectedModelView(User, db.session))
admin.add_view(ProtectedModelView(Posts, db.session))
admin.add_view(ProtectedModelView(Role, db.session))
