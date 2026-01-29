"""
分页配置模块

提供标准分页类，确保所有列表接口返回一致的分页格式。
"""
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """标准分页类"""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        返回统一格式的分页响应

        配合 ApiResponse 使用时，返回 data 字典内容
        """
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }
