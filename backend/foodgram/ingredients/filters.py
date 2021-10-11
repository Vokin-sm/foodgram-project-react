import django_filters

from .models import Ingredient


class IngredientsFilter(django_filters.FilterSet):
    """Ingredients Filter"""
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = [
            'name',
        ]
