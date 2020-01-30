import os

from flask import current_app, url_for
from hashlib import sha256
from werkzeug.utils import secure_filename

from api.util import Message, InternalErrResp
from api.config import basedir

STATIC_FOLDER_PATH = basedir + "/main/static/"


def get_image(image, foldername):
    image_url = url_for("static", filename=f"{foldername}/{image}")

    return image_url


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# Use PIL to compress images later on.
def upload_file(files, foldername, extensions):
    if "image" not in files:
        resp = Message(False, "File not found!")
        resp["error_reason"] = "file_404"
        return resp, 404

    file = files["image"]
    # Check if there is a filename
    if file.filename == "":
        resp = Message(False, "No file selected!")
        resp["error_reason"] = "filename"
        return resp, 403

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

            resp = Message(True, "Image uploaded.")
            resp["image_id"] = hashed_file + extension
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()
