import os
from glob import glob
from flask import url_for

from zimmerman.main import db
from zimmerman.main.model.user import Posts, Comments, Reply, PostLike, CommentLike, ReplyLike
from zimmerman.main.service.like_service import check_like
from zimmerman.main.service.post_service import load_author

# Import Schema
from zimmerman.main.model.user import PostSchema, CommentSchema, ReplySchema

# Import upload path
from .post_service import POST_UPLOAD_PATH

def uniq(a_list):
    encountered = set()
    result = []
    for elem in a_list:
        if elem not in encountered:
            result.append(elem)
        encountered.add(elem)
    return result

def get_post_ids():
    # Get Posts info
    posts = Posts.query.with_entities(Posts.id, Posts.created).all()
    post_schema = PostSchema(many=True)
    post_info = post_schema.dump(posts).data

    # Comments
    comments = Comments.query.all()
    comment_schema = CommentSchema(many=True)
    comment_info = comment_schema.dump(comments).data

    # Get the activity based on the latest comments
    post_activity_from_comments = [
        {
            'id': c['posts'],
            'created': c['created']
        } for c in comment_info
    ]

    feed = uniq(x['id'] for x in sorted(post_activity_from_comments + post_info,
                                        key=lambda x: x['created'],
                                        reverse=True))
    response_object = {
        'success': True,
        'message': 'Post IDs sent to client',
        'post_ids': feed
    }
    return response_object, 200

def get_posts_info(id_array, current_user):
    # Get the data in the array of post IDs
    post_schema = PostSchema()
    posts = []

    for post_id in id_array:
        # Get the post and schema
        post = Posts.query.filter_by(id=post_id).first()
        # Dump the data and append it to the posts list
        post_info = post_schema.dump(post).data

        # Add the author
        post_info['author'] = load_author(post_info['creator_public_id'])
        
        # Check if the current user has liked the post.
        user_likes = PostLike.query.filter_by(on_post=post_id).order_by(PostLike.liked_on.desc())
        if check_like(user_likes, current_user.id):
            post_info['liked'] = True
        else:
            post_info['liked'] = False

        # Check if it has an image
        if post_info['image_file']:
            # Get the image ID
            img_id = post_info['image_file']
            # Search for the image in the static directory
            img_url = url_for('static', filename='postimages/' + img_id)
            # Attach it
            post_info['image_url'] = img_url

        # Get the latest 5 comments
        if post_info['comments']:
            post_info['initial_comments'] = get_comments(post_info, current_user.id)

        posts.append(post_info)
    
    response_object = {
        'success': True,
        'message': 'Post IDs successfully delivered.',
        'posts': posts
    }
    return response_object, 200

def get_comments(post_info, current_user_id):
    comments = []
    comment_schema = CommentSchema()
    # Get the first five comments
    for comment_id in sorted(post_info['comments'], reverse=True)[:5]:
        # Get the coment info
        comment = Comments.query.filter_by(id=comment_id).first()
        comment_info = comment_schema.dump(comment).data

        # Check if the comment is liked
        user_likes = CommentLike.query.filter_by(on_comment=comment_id).order_by(CommentLike.liked_on.desc())
        if check_like(user_likes, current_user_id):
            comment_info['liked'] = True
        else:
            comment_info['liked'] = False

        # if comment_info['replies']:
        #     comment_info['latest_replies'] = get_replies(comment_info, current_user_id)

        print(comment_info)

        comments.append(comment_info)

    return comments

def get_replies(comment_info, current_user_id):
    replies = []
    reply_schema = ReplySchema()
    # Get the latest 2 replies if they are existent
    for reply_id in sorted(comment_info['replies'])[:2]:
        reply = Reply.query.filter_by(id=reply_id).first()
        reply_info = reply_schema.dump(reply).data
        # Check if the reply is liked
        user_likes = ReplyLike.query.filter_by(on_reply=reply_id).order_by(ReplyLike.liked_on.desc())
        if check_like(user_likes, current_user_id):
            reply_info['liked'] = True
        else:
            reply_info['liked'] = False
        
        replies.append(reply_info)

    return replies