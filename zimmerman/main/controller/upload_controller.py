from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import UploadDto
from ..service.upload_service import upload_file

api = UploadDto.api

DEFAULT_EXTENSIONS = ['jpg', 'jpeg', 'png']

@api.route('/postimage')
class UploadPostImage(Resource):

    """ Upload image for posts """
    @api.doc('Post image upload route.',
        responses = {
            201: 'Image uploaded successfully.',
            403: 'No file selected!',
            404: 'File not found!'
        }
    )
    @jwt_required
    def post(self):
        """ Uploads an image for posts """
        files = request.files
        upload_folder = 'postimages'
        # Add post unique extensions
        extensions = DEFAULT_EXTENSIONS + ['gif']
        return upload_file(files, upload_folder, extensions)

@api.route('/avatar')
class UploadProfilePic(Resource):
    
    """ Upload image for profile pictures """
    @api.doc('Profile image upload route.',
        responses = {
            201: 'Image uploaded successfully.',
            403: 'No file selected!',
            404: 'File not found!'
        }
    )
    @jwt_required
    def post(self):
        """ Uploads user profile picture """
        files = request.files
        upload_folder = 'avatars'
        # Profile pictures will use the default extensions.
        return upload_file(files, upload_folder, DEFAULT_EXTENSIONS)