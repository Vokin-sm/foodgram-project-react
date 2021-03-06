from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RecipesViewSet, ShoppingCartsFavorite,
                    download_shopping_cart)

router_v1 = DefaultRouter()

router_v1.register(
    '',
    RecipesViewSet,
    basename='recipes',
)

urlpatterns = [
    path(
        'download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path(
        '<int:recipe_id>/<str:model>/',
        ShoppingCartsFavorite.as_view(),
    ),
    path(
        '',
        include(router_v1.urls)
    ),

]
