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


def tags_and_components_add(obj, tags_data, components_data):
    """Adds tags and components to an object."""
    for tag_data in tags_data:
        obj.tags.add(tag_data)
    for component_data in components_data:
        ingredient = Ingredient.objects.get(
            id=component_data['name']['id']
        )
        component = Component.objects.create(
            amount=component_data['amount'],
            name=ingredient,
        )
        obj.ingredients.add(component)
    obj.save()
    return obj


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
        recipe = Recipe.objects.create(**validated_data)
        return tags_and_components_add(recipe, tags_data, components_data)

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.tags.clear()
        components_data = validated_data.pop('ingredients')
        Component.objects.filter(recipe=instance).delete()
        for update_data in validated_data:
            setattr(instance, update_data, validated_data[update_data])
        return tags_and_components_add(instance, tags_data, components_data)
