from rest_framework.pagination import PageNumberPagination


class RecipeListPagination(PageNumberPagination):
    """Used to paginate a list of recipes."""
    page_size = 3
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 10
