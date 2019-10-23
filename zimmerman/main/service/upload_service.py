import os

from flask import request, url_for
from hashlib import sha256
from werkzeug.utils import secure_filename

from zimmerman.config import basedir

STATIC_FOLDER_PATH = basedir + "/main/static/"


def get_image(image, foldername):
    image_url = url_for("static", filename=f"{foldername}/{image}")

    return image_url


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# Use PIL to compress images later on.
def upload_file(files, foldername, extensions):
    if "image" not in files:
        response_object = {
            success: False,
            message: "File not found!",
            error_reason: "nofile",
        }
        return response_object, 404

    file = files["image"]
    # Check if there is a filename
    if file.filename == "":
        response_object = {
            "success": False,
            "message": "No file selected!",
            "error_reason": "filename",
        }
        return response_object, 403

    # Process if it passes validation
    allowed_extensions = set(extensions)
    if file and allowed_file(file.filename, allowed_extensions):
        # Get the filename
        filename = file.filename
        extension = "." + filename.split(".")[1]

        # Hash the file and limit to 32chars
        hashed_file = sha256(str(file.filename).encode("utf-8")).hexdigest()[:32]

        # Save it and attach the extension
        try:
            file.save(
                os.path.join(
                    STATIC_FOLDER_PATH + foldername + "/", hashed_file + extension
                )
            )
            response_object = {
                "success": True,
                "message": "Image successfully uploaded",
                # Add the extension to the image id for now, will use glob later on
                "image_id": hashed_file + extension,
            }
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
            }
            return response_object, 500
