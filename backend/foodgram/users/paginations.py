from rest_framework.pagination import PageNumberPagination


class UserListPagination(PageNumberPagination):
    """Used to paginate a list of users."""
    page_size = 3
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 10


class FollowPagination(PageNumberPagination):
    """Used to paginate a list of follows"""
    page_size = 3
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 10
