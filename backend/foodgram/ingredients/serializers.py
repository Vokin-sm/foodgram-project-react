from rest_framework import serializers

from .models import Component


class ComponentSerializer(serializers.ModelSerializer):
    """Is used to serialize components."""
    name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Component
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]
