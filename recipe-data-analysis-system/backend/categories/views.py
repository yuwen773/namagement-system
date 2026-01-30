"""
分类模块 - 视图定义

本模块定义分类相关的视图，包括：
- category_list: 分类列表视图，支持按类型筛选
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from utils.response import ApiResponse
from utils.pagination import StandardPagination
from .models import Category
from .serializers import CategoryListSerializer
from utils.constants import CategoryType
from utils.exceptions import ValidationError


@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """
    分类列表接口

    获取所有分类，支持按类型筛选。

    请求参数:
        type (可选): 分类类型 (cuisine/scene/crowd/taste/difficulty)

    返回:
        分类列表，按类型和排序序号排列

    示例:
        GET /api/categories/ - 获取所有分类
        GET /api/categories/?type=cuisine - 只获取菜系分类
    """
    # 获取筛选参数
    category_type = request.query_params.get('type', None)

    # 验证分类类型参数
    if category_type:
        valid_types = [choice[0] for choice in CategoryType.CHOICES]
        if category_type not in valid_types:
            raise ValidationError(f'无效的分类类型，可选值: {", ".join(valid_types)}')

    # 构建查询
    queryset = Category.objects.all()

    # 按类型筛选
    if category_type:
        queryset = queryset.filter(type=category_type)

    # 排序：按类型和排序序号
    queryset = queryset.order_by('type', 'sort_order', 'id')

    # 分页处理（可选，这里直接返回所有分类）
    # 分类数据量不大，通常不需要分页
    serializer = CategoryListSerializer(queryset, many=True)

    return ApiResponse.success(data=serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def category_by_type(request, category_type):
    """
    按类型获取分类接口

    获取指定类型的所有分类。

    路径参数:
        category_type: 分类类型 (cuisine/scene/crowd/taste/difficulty)

    返回:
        指定类型的分类列表

    示例:
        GET /api/categories/cuisine/ - 获取所有菜系分类
        GET /api/categories/scene/ - 获取所有场景分类
    """
    # 验证分类类型参数
    valid_types = [choice[0] for choice in CategoryType.CHOICES]
    if category_type not in valid_types:
        raise ValidationError(f'无效的分类类型，可选值: {", ".join(valid_types)}')

    # 获取指定类型的分类
    queryset = Category.get_by_type(category_type)
    serializer = CategoryListSerializer(queryset, many=True)

    return ApiResponse.success(data=serializer.data)
