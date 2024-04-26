from rest_framework.pagination import PageNumberPagination


class Todolistpagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'