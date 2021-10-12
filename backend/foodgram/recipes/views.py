from collections import namedtuple

from django.http import HttpResponse
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen.canvas import Canvas
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
from .serializers import (RecipesCreateSerializer, RecipesListSerializer,
                          ShoppingCartFavoriteSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    """Class for displaying, creating, editing and deleting recipes."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesListSerializer
    pagination_class = RecipeListPagination
    filterset_class = RecipeFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save(author=self.request.user)
        serializer_output = RecipesListSerializer(recipe)
        headers = self.get_success_headers(serializer_output.data)
        return Response(
            serializer_output.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(request.data)
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        serializer_output = RecipesListSerializer(recipe)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer_output.data)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
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

    # file_name = 'Список ингредиентов'
    # file_title = 'Необходимый список ингредиентов'
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] =
    # f'attachment; filename="{file_name}.pdf"'
    # shopping_cart_pdf = Canvas(response)
    # shopping_cart_pdf.setTitle(file_title)
    # pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    # shopping_cart_pdf.setFont('FreeSans', 18)
    # height = 762
    # width = 15
    # for name_ingredient, properties in content.items():
    #     shopping_cart_pdf.drawString(
    #         width,
    #         height,
    #         f'*  {name_ingredient} ({properties.measurement_unit}) '
    #         f'----- {properties.amount}'
    #     )
    #     height -= 30
    # shopping_cart_pdf.showPage()
    # shopping_cart_pdf.save()
    with open('static/shopping_carts/shopping_cart.txt', 'w') as f:
        f.write('Проверка связи!!!!!!!')
    with open('static/shopping_carts/shopping_cart.txt', 'r') as f:
        response = HttpResponse(f, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=f.txt'
        return response


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
            shopping_cart, created = ShoppingList.objects.get_or_create(
                author=request.user,
                recipe=recipe,
            )
            if created:
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
        favorite, created = Favorites.objects.get_or_create(
            author=request.user,
            recipe=recipe,
        )
        if created:
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
