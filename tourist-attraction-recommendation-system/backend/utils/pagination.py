from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    自定义分页类，返回统一的响应格式
    """
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'code': 0,
            'data': data,
            'total': self.page.paginator.count,
            'page': self.page.number,
            'size': self.page.paginator.per_page,
            'total_pages': self.page.paginator.num_pages
        })
