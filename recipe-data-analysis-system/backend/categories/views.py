"""
分类模块 - 视图定义

本模块定义分类相关的视图，包括：
- category_list: 分类列表视图，支持按类型筛选
- 管理员专用视图：admin_category_list, admin_create_category, admin_update_category, admin_delete_category
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from utils.response import ApiResponse
from utils.pagination import StandardPagination
from utils.permissions import IsAdminUser
from utils.constants import CategoryType
from utils.exceptions import ValidationError, NotFoundError, BusinessError
from .models import Category
from .serializers import (
    CategoryListSerializer,
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer
)


# ==================== 普通用户接口 ====================

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


# ==================== 管理员接口 ====================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_category_list(request):
    """
    管理员 - 分类管理列表接口（仅管理员可访问）

    请求方法：GET
    路由：/api/admin/categories/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - type: 分类类型筛选（可选）
        - search: 搜索关键词（可选，搜索分类名称）
        - page: 页码（可选，默认1）
        - page_size: 每页数量（可选，默认20，最大100）

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "count": 50,
                "next": null,
                "previous": null,
                "results": [...]
            }
        }
    """
    # 获取筛选和搜索参数
    category_type = request.query_params.get('type', None)
    search = request.query_params.get('search', None)

    # 构建查询
    queryset = Category.objects.all()

    # 按类型筛选
    if category_type:
        valid_types = [choice[0] for choice in CategoryType.CHOICES]
        if category_type not in valid_types:
            raise ValidationError(f'无效的分类类型，可选值: {", ".join(valid_types)}')
        queryset = queryset.filter(type=category_type)

    # 搜索分类名称
    if search:
        queryset = queryset.filter(name__icontains=search)

    # 排序
    queryset = queryset.order_by('type', 'sort_order', 'id')

    # 分页
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = CategorySerializer(page, many=True)

    return ApiResponse.paginate(
        data=paginator.get_paginated_response(serializer.data),
        message='获取成功'
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_category(request):
    """
    管理员 - 创建分类接口（仅管理员可访问）

    请求方法：POST
    路由：/api/admin/categories/create/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - name: 分类名称（必填）
        - type: 分类类型（必填，可选值：cuisine/scene/crowd/taste）
        - sort_order: 排序序号（可选，默认0）

    成功响应（201）：
        {
            "code": 201,
            "message": "创建成功",
            "data": {...}
        }
    """
    serializer = CategoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.save()
        response_serializer = CategorySerializer(category)
        return ApiResponse.success(data=response_serializer.data, message='创建成功', code=201)
    return ApiResponse.error(message='参数验证失败', errors=serializer.errors, code=400)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_category(request, category_id):
    """
    管理员 - 更新分类接口（仅管理员可访问）

    请求方法：PUT / PATCH
    路由：/api/admin/categories/{category_id}/update/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - name: 分类名称（可选）
        - type: 分类类型（可选）
        - sort_order: 排序序号（可选）

    成功响应（200）：
        {
            "code": 200,
            "message": "更新成功",
            "data": {...}
        }
    """
    # 检查分类是否存在
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFoundError('分类不存在')

    # 根据请求方法选择序列化器
    if request.method == 'PUT':
        serializer = CategoryUpdateSerializer(category, data=request.data)
    else:  # PATCH
        serializer = CategoryUpdateSerializer(category, data=request.data, partial=True)

    if serializer.is_valid():
        category = serializer.save()
        response_serializer = CategorySerializer(category)
        return ApiResponse.success(data=response_serializer.data, message='更新成功')
    return ApiResponse.error(message='参数验证失败', errors=serializer.errors, code=400)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_category(request, category_id):
    """
    管理员 - 删除分类接口（仅管理员可访问）

    请求方法：DELETE
    路由：/api/admin/categories/{category_id}/delete/

    请求头：
        Authorization: Bearer <access_token>

    功能说明：
        - 检查分类是否存在
        - 检查分类是否被菜谱使用
        - 删除分类

    成功响应（200）：
        {
            "code": 200,
            "message": "删除成功",
            "data": null
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "该分类正在被使用，无法删除",
            "data": null
        }
    """
    # 检查分类是否存在
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFoundError('分类不存在')

    # 检查是否被菜谱使用
    from recipes.models import Recipe
    if category.type == CategoryType.CUISINE:
        is_used = Recipe.objects.filter(cuisine_type=category.name).exists()
    elif category.type == CategoryType.SCENE:
        is_used = Recipe.objects.filter(scene_type=category.name).exists()
    elif category.type == CategoryType.CROWD:
        is_used = Recipe.objects.filter(target_audience=category.name).exists()
    else:
        is_used = False

    if is_used:
        raise BusinessError('该分类正在被菜谱使用，无法删除')

    # 删除分类
    category.delete()

    return ApiResponse.success(message='删除成功')
