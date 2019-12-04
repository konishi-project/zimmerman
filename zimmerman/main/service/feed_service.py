from flask import current_app

from zimmerman.main import db
from zimmerman.util import Message, ErrResp
from zimmerman.main.model.main import Post, Comment
from zimmerman.main.service.post_service import load_post

# Import Schemas
from zimmerman.main.model.schemas import PostSchema, CommentSchema, UserSchema

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
    def get_chronological(query_limit):
        # Get Posts IDs by latest creation (chronological order)

        # Get Posts info
        posts = Post.query.with_entities(Post.id, Post.created).limit(query_limit).all()

        post_info = post_many_schema.dump(posts)

        feed = uniq(
            x["id"] for x in sorted(post_info, key=lambda x: x["created"], reverse=True)
        )

        resp = Message(True, "Post IDs sent.")
        resp["post_ids"] = feed
        return resp, 200

    def get_activity(query_limit):
        # Get Posts IDs by latest activity (latest comment on post)

        # Get Posts info
        # Currently set limits
        posts = Post.query.with_entities(Post.id, Post.created).limit(query_limit).all()
        post_info = post_many_schema.dump(posts)

        # Comments
        # Limit into the 10 latest active posts
        comments = Comment.query.limit(10).all()

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

        resp = Message(True, "Post IDs sent.")
        resp["post_ids"] = feed
        return resp, 200

    def get_posts_info(id_array, current_user):

        # Check if the array is empty
        if len(id_array) == 0 or id_array is None:
            ## Nothing to send back..
            return "", 204

        posts = []

        post_query = Post.query.filter(Post.id.in_(id_array)).all()

        try:
            for post in post_query:
                post_info = load_post(post, current_user.id)
                posts.append(post_info)

            # Re-sort it back the the original array
            res = [post for id in id_array for post in posts if post["id"] == id]

            resp = Message(True, "Posts sent.")
            resp["posts"] = res
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            ErrResp()
