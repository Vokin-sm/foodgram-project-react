from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ingredients.models import Component, Ingredient
from ingredients.serializers import (ComponentCreateSerializer,
                                     ComponentListSerializer)
from tags.serializers import TagsSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe


class RecipesListSerializer(serializers.ModelSerializer):
    """Used to serialize recipes list."""
    image = Base64ImageField()
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = ComponentListSerializer(many=True)

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


class RecipesCreateSerializer(serializers.ModelSerializer):
    """Used to serialize recipe creation."""
    image = Base64ImageField()
    ingredients = ComponentCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        components_data = validated_data.pop('ingredients')
        print(tags_data)
        print(components_data)
        print(validated_data)
        recipe = Recipe.objects.create(**validated_data)
        for tag_data in tags_data:
            recipe.tags.add(tag_data)
        for component_data in components_data:
            ingredient = Ingredient.objects.get(id=component_data['amount'])
            component = Component.objects.create(
                amount=component_data['amount'],
                name=ingredient,
            )
            recipe.ingredients.add(component)
        recipe.save()
        return recipe
