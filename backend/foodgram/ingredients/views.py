from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .filters import IngredientsFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """Class for displaying ingredients."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filterset_class = IngredientsFilter
