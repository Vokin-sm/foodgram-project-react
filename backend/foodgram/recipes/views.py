from collections import namedtuple

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from ingredients.models import Component
from recipes.filters import RecipeFilter
from recipes.models import Recipe, ShoppingList
from recipes.paginations import RecipeListPagination
from recipes.permissions import IsOwner
from recipes.serializers import RecipesCreateSerializer, RecipesListSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Class for displaying, creating, editing and deleting recipes."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesListSerializer
    pagination_class = RecipeListPagination
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipesCreateSerializer
        return self.serializer_class


@api_view()
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    content = dict()
    ComponentProperties = namedtuple(
        'ComponentProperties',
        'measurement_unit amount'
    )
    shopping_carts = ShoppingList.objects.filter(author=request.user)
    for shopping_cart in shopping_carts:
        components = Component.objects.filter(recipe=shopping_cart.recipe)
        for component in components:
            if component.name.name not in content:
                content[component.name.name] = ComponentProperties(
                    component.name.measurement_unit,
                    component.amount
                )
            else:
                element = content[component.name.name]
                amount = content[component.name.name].amount + component.amount
                content[component.name.name] = element._replace(amount=amount)

    with open('static/shopping_carts/shopping_cart.txt', 'w') as shopping_cart:
        for name_ingredient, properties in content.items():
            shopping_cart.write(
                f'*  {name_ingredient} ({properties.measurement_unit})'
                f' ----- {properties.amount}\n'
            )

    with open('static/shopping_carts/shopping_cart.txt') as shopping_cart:
        return HttpResponse(shopping_cart, content_type='text/plain')
