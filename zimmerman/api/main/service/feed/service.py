from flask import current_app

from zimmerman.utils import Message, InternalErrResp

# Import Schemas
from zimmerman.models.content import Post, Comment

from ..comment.utils import comments_schema
from ..post.utils import load_post
from ..comment.utils import load_comment
from .utils import uniq, load_info_many


class FeedService:
    @staticmethod
    def get_chronological(query_limit):
        # Get Post IDs by latest creation (chronological order)

        # Get Posts info
        posts = Post.query.with_entities(Post.id, Post.created).limit(query_limit).all()

        post_info = load_info_many(posts)

        feed = uniq(
            x["id"] for x in sorted(post_info, key=lambda x: x["created"], reverse=True)
        )

        resp = Message(True, "Post IDs sent.")
        resp["post_ids"] = feed
        return resp, 200

    @staticmethod
    def get_activity(query_limit):
        # Get Posts IDs by latest activity (latest comment on post)

        # Get Posts info
        # Currently set limits
        posts = Post.query.with_entities(Post.id, Post.created).limit(query_limit).all()

        post_info = load_info_many(posts)

        # Comments
        # Limit into 10 latest active posts
        comments = Comment.query.limit(10).all()

        comment_info = comments_schema.dump(comments)

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

    @staticmethod
    def get_posts_data(id_array, current_user):

        # Check if the array is empty
        if len(id_array) == 0 or id_array is None:
            ## Nothing to send back..
            return "", 204

        posts = []

        posts_query = Post.query.filter(Post.id.in_(id_array)).all()

        try:
            for post in posts_query:
                post_info = load_post(post, current_user.id)
                posts.append(post_info)

            # Re-sort it back to the original array
            res = [post for id in id_array for post in posts if post["id"] == id]

            resp = Message(True, "Posts info sent.")
            resp["posts"] = res
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def get_comments_data(id_array, current_user):
        # Check if the array is empty
        if len(id_array) == 0 or id_array is None:
            ## Nothing to send back...
            return "", 204

        comments = []

        comments_query = Comment.query.filter(Comment.id.in_(id_array)).all()

        try:
            for comment in comments_query:
                comment_info = load_comment(comment, current_user.id)
                comments.append(comment_info)

            # Re-sort it back to the original array
            res = [
                comment
                for id in id_array
                for comment in comments
                if comment["id"] == id
            ]

            resp = Message(True, "Comments info sent.")
            resp["comments"] = res
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()
