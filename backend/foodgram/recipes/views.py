from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.filters import RecipeFilter
from recipes.models import Recipe
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
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipesCreateSerializer
        return self.serializer_class
