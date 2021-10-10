import django_filters

from recipes.models import Favorites, Recipe, ShoppingList
from tags.models import Tag


class RecipeFilter(django_filters.FilterSet):
    """Recipes Filter"""
    is_favorited = django_filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
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

    def get_is_favorited(self, queryset, name, value):
        if self.request.auth:
            if not value:
                return queryset
            favorites_recipes = Favorites.objects.filter(
                author=self.request.user
            )
            return queryset.filter(favorites__in=favorites_recipes)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.auth:
            if not value:
                return queryset
            recipes_in_shopping_cart = ShoppingList.objects.filter(
                author=self.request.user
            )
            return queryset.filter(shopping_list__in=recipes_in_shopping_cart)
        return queryset
