from djoser.views import UserViewSet

from users.paginations import UserListPagination


class CustomUserViewSet(UserViewSet):
    """Class for displaying, creating and deleting users."""
    pagination_class = UserListPagination
