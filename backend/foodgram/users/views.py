from djoser.views import UserViewSet

from users.paginations import UserListPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = UserListPagination
