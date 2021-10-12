from rest_framework import serializers

from .models import Component, Ingredient


class ComponentListSerializer(serializers.ModelSerializer):
    """Used to serialize components list."""
    name = serializers.ReadOnlyField(
        source='name.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='name.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='name.id')

    class Meta:
        model = Component
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class ComponentCreateSerializer(serializers.ModelSerializer):
    """Used to serialize component creation."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = Component
        fields = [
            'id',
            'amount',
        ]


class IngredientSerializer(serializers.ModelSerializer):
    """Is used to serialize ingredients."""
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]
