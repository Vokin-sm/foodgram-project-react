from collections import namedtuple

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ingredients.models import Component

from .filters import RecipeFilter
from .models import Favorites, Recipe, ShoppingList
from .paginations import RecipeListPagination
from .permissions import IsOwner
from .serializers import (RecipesCreateSerializer,
                          RecipesListSerializer,
                          ShoppingCartFavoriteSerializer)


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


class ShoppingCartsFavorite(APIView):
    """Adding and removing recipes and favorite."""
    permission_classes = [IsAuthenticated]

    def get(self, request, recipe_id, model):
        if model not in ('shopping_cart', 'favorite'):
            context = {'error': 'Страница не найдена'}
            return Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = get_object_or_404(
            Recipe,
            id=recipe_id
        )
        if model == 'shopping_cart':
            try:
                ShoppingList.objects.get(
                    author=request.user,
                    recipe=recipe_id
                )
            except ShoppingList.DoesNotExist:
                shopping_cart = ShoppingList.objects.create(
                    author=request.user,
                    recipe=recipe
                )
                serializer = ShoppingCartFavoriteSerializer(shopping_cart)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            context = {'error': 'Такой рецепт в списке покупок уже существует'}
            return Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            Favorites.objects.get(
                author=request.user,
                recipe=recipe_id
            )
        except Favorites.DoesNotExist:
            favorite = Favorites.objects.create(
                author=request.user,
                recipe=recipe
            )
            serializer = ShoppingCartFavoriteSerializer(favorite)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        context = {'error': 'Такой рецепт в списке избранное уже существует'}
        return Response(
            data=context,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, recipe_id, model):
        if model not in ('shopping_cart', 'favorite'):
            context = {'error': 'Страница не найдена'}
            return Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )
        if model == 'shopping_cart':
            try:
                shopping_cart = ShoppingList.objects.get(
                    author=request.user,
                    recipe=recipe_id
                )
            except ShoppingList.DoesNotExist:
                context = {'error': 'Такого рецепта нет в списке покупок'}
                return Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        try:
            favorite = Favorites.objects.get(
                author=request.user,
                recipe=recipe_id
            )
        except Favorites.DoesNotExist:
            context = {'error': 'Такого рецепта нет в списке избранное'}
            return Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
