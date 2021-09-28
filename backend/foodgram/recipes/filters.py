import django_filters

from recipes.models import Recipe
from tags.models import Tag


class RecipeFilter(django_filters.FilterSet):
    """Recipes Filter"""
    # is_favorited = django_filters.BooleanFilter()
    # is_in_shopping_cart = django_filters.BooleanFilter()
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]