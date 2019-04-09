import os

from flask import request
from hashlib import sha256
from werkzeug.utils import secure_filename
from PIL import Image

from ..config import basedir

STATIC_FOLDER_PATH = basedir + '/static/'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_file(files, foldername, extensions):
    if 'image' not in files:
        response_object = {
          success: False,
          message: "File not found!",
          error_reason: "nofile"
        }
        return  response_object, 404

    file = files['image']
    # Check if there is a filename
    if file.filename == '':
        response_object = {
            'success': False,
            'message': "No file selected!",
            'error_reason': "filename"
        }
        return response_object, 403

    # Process if it passes validation
    allowed_extensions = set(extensions)
    if file and allowed_file(file.filename, allowed_extensions):
        # Get the filename
        filename = file.filename
        extension = '.' + filename.split('.')[1]

        # Hash the file and limit to 32chars
        hashed_file = sha256(str(file.filename).encode('utf-8')).hexidigest()[:32]

        # Save it and attach the extension
        try:
            file.save(os.path.join(STATIC_FOLDER_PATH + foldername, hashed_file, extension))
            response_object = {
                'success': True,
                'message': 'Image successfully uploaded',
                'image_id': hashed_file
            },
            return response_object, 201
        except:
            # Return an error message if it fails to upload
            response_object = {
                'success': False,
                'message': 'Something went wrong during the process!'
            }
            return response_object, 500