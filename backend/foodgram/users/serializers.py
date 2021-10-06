from django.core.paginator import Paginator
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe

from .models import Follow


class CustomUserSerializer(UserSerializer):
    """Is used to serialize users."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        try:
            user_auth = self.context['request'].auth
        except KeyError:
            return False
        if user_auth:
            current_user = self.context['request'].user
            try:
                Follow.objects.get(author=obj, user=current_user)
            except Follow.DoesNotExist:
                return False
            return True
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """Is used to serialize users."""
    class Meta(UserCreateSerializer.Meta):
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        ]


class RecipesInFollow(serializers.ModelSerializer):
    """Used to serialize recipes in follows."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class FollowSerializer(serializers.ModelSerializer):
    """Is used to serialize follows."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField('paginated_recipes')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]

    def get_is_subscribed(self, obj):
        try:
            current_user = self.context['request'].user
        except KeyError:
            current_user = obj.user
        try:
            Follow.objects.get(author=obj.author, user=current_user)
        except Follow.DoesNotExist:
            return False
        return True

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def paginated_recipes(self, obj):
        try:
            page_size = (self.context['request'].
                         query_params.get('recipes_limit') or 10)
            paginator = Paginator(obj.author.recipe.all(), page_size)
            page = 1
            recipes = paginator.page(page)
            serializer = RecipesInFollow(recipes, many=True)
            return serializer.data
        except KeyError:
            recipes = obj.author.recipe.all()
            serializer = RecipesInFollow(recipes, many=True)
            return serializer.data
