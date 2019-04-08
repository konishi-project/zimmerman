from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import UploadDto
from ..service.upload_service import upload_file

api = UploadDto.api

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
        return upload_file(files, upload_folder)