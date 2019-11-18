from zimmerman.main import db
from zimmerman.main.model.main import Post, Comment, PostLike, User
from zimmerman.main.service.like_service import check_like
from zimmerman.main.service.post_service import load_post
from zimmerman.main.service.user_service import filter_author, load_author

# Import Schemas
from zimmerman.main.model.main import PostSchema, CommentSchema, UserSchema

# Import upload path
from .upload_service import get_image

# Define the schemas
user_schema = UserSchema()
post_schema = PostSchema()

post_many_schema = PostSchema(many=True)
comment_many_schema = CommentSchema(many=True)


def uniq(a_list):
    encountered = set()
    result = []
    for elem in a_list:
        if elem not in encountered:
            result.append(elem)
        encountered.add(elem)
    return result


class Feed:
    def get_chronological():
        # Get Posts IDs by latest creation (chronological order)
        # Get Posts info
        posts = Post.query.with_entities(Post.id, Post.created).order_by(
            Post.created.desc()
        )
        # WIP
        print(posts)

    def get_activity(query_limit):
        # Get Posts IDs by latest activity (latest comment on post)

        # Get Posts info
        # Currently set limits
        posts = Post.query.with_entities(Post.id, Post.created).limit(query_limit).all()
        post_info = post_many_schema.dump(posts)

        # Comments
        comments = (
            Comment.query.with_entities(Comment.id, Comment.created, Comment.post)
            .limit(query_limit)
            .all()
        )

        comment_info = comment_many_schema.dump(comments)

        # Get the activity based on the latest comments
        post_activity_from_comments = [
            {"id": c["post"], "created": c["created"]} for c in comment_info
        ]

        feed = uniq(
            x["id"]
            for x in sorted(
                post_activity_from_comments + post_info,
                key=lambda x: x["created"],
                reverse=True,
            )
        )

        response_object = {
            "success": True,
            "message": "Post IDs sent to client.",
            "post_ids": feed,
        }
        return response_object, 200

    def get_posts_info(id_array, current_user):

        # Check if the array is empty
        if len(id_array) == 0 or id_array is None:
            ## Nothing to send back..
            return "", 204

        posts = []

        post_query = Post.query.filter(Post.id.in_(id_array)).all()

        for post in post_query:
            post_info = load_post(post, current_user.id)
            posts.append(post_info)

        response_object = {
            "success": True,
            "message": "Posts successfully sent.",
            "posts": posts,
        }
        return response_object, 200
