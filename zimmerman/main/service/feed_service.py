from zimmerman.main import db
from zimmerman.main.model import Posts, Comments

# Import Schema
from zimmerman.main.model import PostSchema, CommentSchema

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
    return feed

def get_posts_info(id_array):
    # Get the data in the array of post IDs
    post_schema = PostSchema()
    posts = []

    for post_id in id_array:
        # Get the post and schema
        post = Posts.query.filter_by(id=post_id).first()
        # Dump the data and append it to the posts list
        post_info = post_schema.dump(post).data
        
        # Check if the current user has liked the post.
        # Check if it has an image
        # Get the latest 5 comments

        posts.append(post_info)