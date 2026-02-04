"""
分页配置模块
"""
from rest_framework.pagination import PageNumberPagination
from utils.response import ApiResponse


class StandardPagination(PageNumberPagination):
    """
    标准分页器
    返回格式: { count, page, page_size, results }
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return ApiResponse.paginate({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'results': data
        })
