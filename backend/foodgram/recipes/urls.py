from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes import views

router = DefaultRouter()
router.register(
    '',
    views.RecipesViewSet,
    basename='recipes',
)

urlpatterns = [
    path(
        'download_shopping_cart/',
        views.download_shopping_cart,
        name='download_shopping_cart'
    ),
    path(
        '',
        include(router.urls)
    ),

]
