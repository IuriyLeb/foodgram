from rest_framework import serializers
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
import base64

class RecipeImageField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        img_format, imgstr = data.split(';base64,')
        img_format = img_format.split('/')[-1]
        image_64_decode = base64.b64decode(imgstr)
        img = Image.open(BytesIO(image_64_decode))
        data = SimpleUploadedFile(
            name = '1.png',
            content=image_64_decode
        )
        return data
