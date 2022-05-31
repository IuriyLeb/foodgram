from rest_framework import serializers
from base64 import b64decode

class RecipeImageField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        image = b64decode(data)
        return image
