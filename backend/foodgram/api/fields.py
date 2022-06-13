import imghdr

from rest_framework import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
import base64
import uuid


class RecipeImageField(serializers.Field):
    """
    Get the base64 string and save it to MEDIA_ROOT/images as a .png image.
    """
    def to_representation(self, value):

        return value.url

    def to_internal_value(self, data):
        header, data = data.split(';base64,')
        decoded_file = base64.b64decode(data)
        file_name = str(uuid.uuid4())
        extension = imghdr.what(file_name, decoded_file)
        complete_file_name = file_name + '.' + extension
        data = SimpleUploadedFile(
            name=complete_file_name,
            content=decoded_file,
            content_type='image/png'

        )

        return data
