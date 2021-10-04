from rest_framework import serializers

from .models import Tag


class TagsSerializer(serializers.ModelSerializer):
    """Is used to serialize tags."""
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]
