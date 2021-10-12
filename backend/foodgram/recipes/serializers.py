from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ingredients.models import Component
from ingredients.serializers import (ComponentCreateSerializer,
                                     ComponentListSerializer)
from tags.serializers import TagsSerializer
from users.serializers import CustomUserSerializer

from .models import Favorites, Recipe, ShoppingList


class RecipesListSerializer(serializers.ModelSerializer):
    """Used to serialize recipes list."""
    image = Base64ImageField()
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = ComponentListSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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

    def get_true_or_false(self, obj, model):
        """Gets true or false."""
        try:
            user_auth = self.context['request'].auth
        except KeyError:
            return False
        if user_auth:
            current_user = self.context['request'].user
            try:
                model.objects.get(recipe=obj, author=current_user)
            except model.DoesNotExist:
                return False
            return True
        return False

    def get_is_favorited(self, obj):
        return self.get_true_or_false(obj, Favorites)

    def get_is_in_shopping_cart(self, obj):
        return self.get_true_or_false(obj, ShoppingList)


def components_add(obj, components_data):
    """Adds components to an object."""
    for component_data in components_data:
        component, created = Component.objects.get_or_create(
            amount=component_data['amount'],
            name=component_data['id'],
        )
        obj.ingredients.add(component)
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
        recipe.tags.set(tags_data)
        components_add(recipe, components_data)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        components_data = validated_data.pop('ingredients')
        instance.ingredients.clear()
        components_add(instance, components_data)
        for update_data in validated_data:
            setattr(instance, update_data, validated_data[update_data])
        instance.save()
        return instance


class ShoppingCartFavoriteSerializer(serializers.ModelSerializer):
    """Used to serialize shopping carts and favorite."""
    id = serializers.SlugField(source='recipe.id')
    name = serializers.SlugField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.SlugField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingList
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
