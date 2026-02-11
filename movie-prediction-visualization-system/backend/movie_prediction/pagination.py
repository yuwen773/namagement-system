"""
自定义分页类

返回符合项目规范的响应格式：{ code: 0, data: [], total: n }
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页类

    默认分页参数：
    - page: 页码，默认 1
    - page_size: 每页数量，默认 10，最大 100
    - pageSize: 前端使用的驼峰命名（兼容）

    返回格式：
    {
        "code": 0,
        "data": [...],
        "total": n
    }
    """
    page = 1
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        """
        支持前端驼峰命名 pageSize
        """
        # 先尝试驼峰命名 pageSize
        if 'pageSize' in request.query_params:
            try:
                page_size = int(request.query_params['pageSize'])
                if page_size > 0:
                    return min(page_size, self.max_page_size)
            except (ValueError, TypeError):
                pass
        # 回退到默认的 page_size
        return super().get_page_size(request)

    def get_paginated_response(self, data):
        """
        返回符合项目规范的自定义分页响应格式
        """
        return Response({
            'code': 0,
            'data': data,
            'total': self.page.paginator.count
        })
