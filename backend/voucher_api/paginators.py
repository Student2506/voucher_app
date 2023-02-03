"""Paginator module."""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Adjust Pagination Logic."""

    page_size_query_param = 'page_size'
    max_page_size = 1000
