from djoser.views import UserViewSet
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Follow, User
from .paginations import FollowPagination, UserListPagination
from .serializers import FollowSerializer


class CustomUserViewSet(UserViewSet):
    """Class for displaying, creating and deleting users."""
    pagination_class = UserListPagination


class FollowViewSet(mixins.ListModelMixin,
                    GenericViewSet):
    """Class for displaying follows."""
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FollowPagination

    def get_queryset(self):
        current_user = self.request.user
        return Follow.objects.filter(user=current_user)


class FollowAddDelete(APIView):
    """Adding and removing follow."""
    permission_classes = [IsAuthenticated]

    def get(self, request, following_id):
        current_user = request.user
        author = get_object_or_404(User, id=following_id)
        if current_user == author:
            context = {'error': 'Вы не можете подписаться на самого себя'}
            return Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
        follow, created = Follow.objects.get_or_create(
            user=current_user,
            author=author,
        )
        if created:
            serializer = FollowSerializer(follow)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        context = {'error': 'Вы уже подписаны на этого пользователя'}
        return Response(
            data=context,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, following_id):
        current_user = request.user
        author = get_object_or_404(User, id=following_id)
        try:
            follow = Follow.objects.get(
                user=current_user,
                author=author
            )
        except Follow.DoesNotExist:
            context = {'error': 'Вы не подписаны на этого пользователя'}
            return Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
