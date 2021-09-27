import base64

from rest_framework import serializers

from recipes.models import Recipe


class Base64Field(serializers.Field):
    """Base64 encodes and decodes."""
    def to_representation(self, value):
        image_file = value.open('rb')
        image_bytes = image_file.read()
        value.close()
        return base64.encodebytes(image_bytes)

    def to_internal_value(self, data):
        image_bytes = base64.decodebytes(data)
        image_file = open('image.jpeg', 'wb')
        image_file.write(image_bytes)
        image_file.close()
        return image_file


class RecipesSerializer(serializers.ModelSerializer):
    """Is used to serialize recipes."""
    image = Base64Field()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]
