"""
食材模块 - 视图

包含食材相关的视图，包括：
- 食材列表
- 食材搜索
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Q
from utils.response import ApiResponse
from utils.exceptions import ValidationError as BusinessValidationError
from .models import Ingredient
from .serializers import IngredientListSerializer
from utils.pagination import StandardPagination


@api_view(['GET'])
@permission_classes([AllowAny])
def ingredient_list(request):
    """
    食材列表接口

    请求方法：GET
    路由：/api/ingredients/

    请求参数：
        - category: 食材分类筛选（可选）
          可选值: vegetable, meat, seafood, seasoning, fruit, grain, dairy, other
        - search: 搜索食材名称（可选，模糊匹配）
        - page: 页码（可选，默认1）
        - page_size: 每页数量（可选，默认20，最大100）

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "count": 100,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "name": "鸡肉",
                        "category": "meat",
                        "category_display": "肉类"
                    }
                ]
            }
        }
    """
    # 获取查询参数
    queryset = Ingredient.objects.all()

    # 按分类筛选
    category = request.query_params.get('category')
    if category:
        # 验证分类是否合法
        from utils.constants import IngredientCategory
        valid_categories = [c[0] for c in IngredientCategory.CHOICES]
        if category not in valid_categories:
            raise BusinessValidationError(
                detail=f'无效的分类，可选值: {", ".join(valid_categories)}'
            )
        queryset = queryset.filter(category=category)

    # 搜索食材名称
    search = request.query_params.get('search', '').strip()
    if search:
        queryset = queryset.filter(name__icontains=search)

    # 默认按分类和名称排序
    queryset = queryset.order_by('category', 'name')

    # 分页
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = IngredientListSerializer(page, many=True)

    # 使用 ApiResponse 返回统一格式的分页响应
    return ApiResponse.paginate(
        data=paginator.get_paginated_response(serializer.data),
        message='获取成功'
    )
