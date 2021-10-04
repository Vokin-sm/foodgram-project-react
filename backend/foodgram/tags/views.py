from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import Tag
from .serializers import TagsSerializer


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    """Class for displaying tags."""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [AllowAny]
