from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.models import Recipe
from recipes.permissions import IsOwner
from recipes.serializers import RecipesSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Class for displaying, creating, editing and deleting recipes."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    # filterset_class = TitlesFilter

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
