from rest_framework import filters, mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """Class for displaying ingredients."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
