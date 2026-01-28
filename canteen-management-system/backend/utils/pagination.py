"""
分页配置模块

提供自定义的分页类，统一分页响应格式
"""
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    标准分页类

    配置默认分页参数，返回统一格式的分页响应

    Attributes:
        page_size: 默认每页数量
        page_size_query_param: 每页数量查询参数名
        max_page_size: 最大每页数量
    """

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        返回统一格式的分页响应

        配合 ApiResponse.paginate() 使用时，返回 data 字典内容

        Args:
            data: 序列化后的数据列表

        Returns:
            dict: 包含 count, next, previous, results 的字典
        """
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }
