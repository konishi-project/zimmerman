import os
from datetime import datetime
from uuid import uuid4
from glob import glob

from flask import request, jsonify, url_for
from flask_jwt_extended import get_jwt_identity

from zimmerman.main import db
from zimmerman.main.model.main import Post, PostLike

from .user_service import load_author
from .upload_service import get_image

# Import Schema
from zimmerman.main.model.main import PostSchema, UserSchema


def add_post_and_flush(data):
    db.session.add(data)
    db.session.flush()

    post_schema = PostSchema()
    latest_post = post_schema.dump(data)

    db.session.commit()

    return latest_post


class PostService:
    def create(data, current_user):
        # Assign the vars
        content = data["content"]
        image_id = data["image_id"]

        # Check if the content doesn't exceed limit
        # This limit can be changed, 2000 - just for testing.
        limit = 2000
        if len(content) > limit:
            response_object = {
                "success": False,
                "message": "Content exceeds limit (%s)" % limit,
            }
            return response_object, 403

        if not content:
            response_object = {"success": False, "message": "Content cannot be empty!"}
            return response_object, 403

        # Create new post obj.
        new_post = Post(
            public_id=str(uuid4().int)[:15],
            owner_id=current_user.id,
            creator_public_id=current_user.public_id,
            content=content,
            image_file=image_id,
            status="normal",
            created=datetime.utcnow(),
        )

        latest_post = add_post_and_flush(new_post)

        # Check if the latest post has an image
        if latest_post["image_file"]:
            latest_post["image_url"] = get_image(
                latest_post["image_file"], "postimages"
            )

        # Add the author's info
        latest_post["author"] = load_author(latest_post["creator_public_id"])

        response_object = {
            "success": True,
            "message": "Post has successfully been created.",
            "post": latest_post,
        }
        return response_object, 201

    def delete(post_public_id, current_user):
        # Query for the post
        post = Post.query.filter_by(public_id=post_public_id).first()
        if not post:
            response_object = {"success": False, "message": "Post not found!"}
            return response_object, 404

        # Check post owner
        elif (
            current_user.public_id == post.creator_public_id
        ):  # or is_admin(current_user)
            post = Post.query.filter_by(public_id=post_public_id).first()

            try:
                db.session.delete(post)
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": "Post has successfully been deleted.",
                }
                return response_object, 200

            except Exception as error:
                print(error)
                response_object = {
                    "success": False,
                    "message": "Something went wrong during the process!",
                }
                return response_object, 500

        # Return a 403 response if the current is not the owner or the admin
        response_object = {"success": False, "message": "Insufficient permisions!"}
        return response_object, 403

    def update(post_public_id, data, current_user):
        post = Post.query.filter_by(public_id=post_public_id).first()
        if not post:
            response_object = {
                "success": False,
                "message": "Post not found!",
                "error_reason": "postNotFound",
            }
            return response_object, 404

        # Check the post owner
        elif (
            current_user.public_id == post.creator_public_id and post.status == "normal"
        ):
            # Get the new data
            if not data["content"]:
                response_object = {
                    "success": False,
                    "message": "Content data not found!",
                    "error_reason": "noData",
                }
                return response_object, 404

            try:
                # Update the post
                post.content = data["content"]
                post.edited = True
                # Commit the changes
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": "Post has successfully been updated.",
                }
                return response_object, 200

            except Exception as error:
                print(error)
                response_object = {
                    "success": False,
                    "message": "Something went wrong during the process!",
                }
                return response_object, 500

        # Check if the post is locked
        elif post.status.lower() == "locked":
            response_object = {
                "success": False,
                "message": "Post is locked!",
                "error_reason": "locked",
            }
            return response_object, 403

        response_object = {
            "success": False,
            "message": "Insufficient permissions!",
            "error_reason": "permission",
        }
        return response_object, 403

    def get(post_public_id):
        # Get the specific post using its public id
        post = Post.query.filter_by(public_id=post_public_id).first()
        if not post:
            response_object = {"success": False, "message": "Post not found!"}
            return response_object, 404

        post_schema = PostSchema()
        post_info = post_schema.dump(post)

        post_info["author"] = load_author(post_info["creator_public_id"])

        # Check for an image file and add it.
        if post_info["image_file"]:
            post_info["image_url"] = get_image(post["image_file"], "postimages")

        response_object = {
            "success": True,
            "message": "Post info successfully sent.",
            "post": post_info,
        }
        return response_object, 200
