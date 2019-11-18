from zimmerman.main import db
from zimmerman.main.model.main import Post, Comment
from zimmerman.main.service.post_service import load_post

# Import Schemas
from zimmerman.main.model.main import PostSchema, CommentSchema, UserSchema

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
        posts = Post.query.with_entities(Post.id, Post.created).limit(500).all()

        post_info = post_many_schema.dump(posts)

        # WIP
        feed = uniq(
            x["id"] for x in sorted(post_info, key=lambda x: x["created"], reverse=True)
        )

        response_object = {
            "success": True,
            "message": "Post IDs sent to client.",
            "post_ids": feed,
        }
        return response_object, 200

    def get_activity(query_limit):
        # Get Posts IDs by latest activity (latest comment on post)

        # Get Posts info
        # Currently set limits
        posts = Post.query.with_entities(Post.id, Post.created).limit(query_limit).all()
        post_info = post_many_schema.dump(posts)

        # Comments
        # Limit into the 10 latest active posts
        comments = (
            Comment.query.limit(10).all()
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

        try:
            for post in reversed(post_query):
                post_info = load_post(post, current_user.id)
                posts.append(post_info)

            response_object = {
                "success": True,
                "message": "Posts successfully sent.",
                "posts": posts,
            }
            return response_object, 200

        except Exception as error:
            # Log error
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_error"
            }
            return response_object, 500
