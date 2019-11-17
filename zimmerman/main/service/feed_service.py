from zimmerman.main import db
from zimmerman.main.model.main import Post, Comment, PostLike, User
from zimmerman.main.service.like_service import check_like
from zimmerman.main.service.post_service import get_initial_comments
from zimmerman.main.service.user_service import filter_author, load_author

# Import Schemas
from zimmerman.main.model.main import PostSchema, CommentSchema, UserSchema

# Import upload path
from .upload_service import get_image


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

    def get_activity():
        # Get Posts IDs by latest activity (latest comment on post)
        # Get Posts info
        posts = Post.query.with_entities(Post.id, Post.created).all()
        post_schema = PostSchema(many=True)
        post_info = post_schema.dump(posts)

        # Comments
        comments = Comment.query.all()
        comment_schema = CommentSchema(many=True)
        comment_info = comment_schema.dump(comments)

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

        # Define the schemas
        post_schema = PostSchema()
        user_schema = UserSchema()

        # Get the posts, join the latest 5 comments and the comments' latest 2 replies.
        query = (
            db.session.query(Post, User)
            .join(Post, User.id == Post.owner_id)
            .filter(Post.id.in_(id_array))
            .all()
        )

        for result in query:
            post = result.Post
            author = result.User

            post_info = post_schema.dump(post)

            # Set the author
            author = user_schema.dump(author)
            post_info["author"] = filter_author(author)

            # Get the first 5 comments if there are any
            post_info["initial_comments"] = (
                get_initial_comments(sorted(post_info["comments"])[:5])
                if post_info["comments"]
                else None
            )

            # # Check if liked
            # if current_user.id in post_info["likes"].owner_id:
            #     post_info["liked"] = True
            # else:
            #     post_info["liked"] = False

            # Get image (if exists)
            post_info["image_url"] = (
                get_image(post_info["image_file"], "postimages")
                if post_info["image_file"]
                else None
            )

            posts.append(post_info)

        response_object = {
            "success": True,
            "message": "Posts successfully sent.",
            "posts": posts,
        }
        return response_object, 200
