from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    """Паджинация рецептов."""
    page_size = 6
    page_size_query_param = 'limit'
