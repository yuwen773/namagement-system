"""
食材模块 - 视图

包含食材相关的视图，包括：
- 食材列表
- 食材搜索
- 管理员专用视图：admin_ingredient_list, admin_create_ingredient, admin_update_ingredient, admin_delete_ingredient
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Q
from utils.response import ApiResponse
from utils.exceptions import ValidationError as BusinessValidationError, NotFoundError, StateNotAllowedError, ErrorCode
from utils.permissions import IsAdminUser
from utils.pagination import StandardPagination
from utils.constants import IngredientCategory
from .models import Ingredient
from .serializers import (
    IngredientListSerializer,
    IngredientSerializer,
    IngredientCreateSerializer,
    IngredientUpdateSerializer
)


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


# ==================== 管理员接口 ====================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_ingredient_list(request):
    """
    管理员 - 食材管理列表接口（仅管理员可访问）

    请求方法：GET
    路由：/api/admin/ingredients/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - category: 食材分类筛选（可选）
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
                        "category_display": "肉类",
                        "created_at": "2026-01-30T12:00:00Z",
                        "updated_at": "2026-01-30T12:00:00Z"
                    }
                ]
            }
        }
    """
    # 获取筛选和搜索参数
    category = request.query_params.get('category', None)
    search = request.query_params.get('search', None)

    # 构建查询
    queryset = Ingredient.objects.all()

    # 按分类筛选
    if category:
        # 验证分类是否合法
        valid_categories = [c[0] for c in IngredientCategory.CHOICES]
        if category not in valid_categories:
            raise BusinessValidationError(
                detail=f'无效的分类，可选值: {", ".join(valid_categories)}'
            )
        queryset = queryset.filter(category=category)

    # 搜索食材名称
    if search:
        queryset = queryset.filter(name__icontains=search)

    # 排序：按分类和名称
    queryset = queryset.order_by('category', 'name')

    # 分页
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = IngredientSerializer(page, many=True)

    return ApiResponse.paginate(
        data=paginator.get_paginated_response(serializer.data),
        message='获取成功'
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_ingredient(request):
    """
    管理员 - 创建食材接口（仅管理员可访问）

    请求方法：POST
    路由：/api/admin/ingredients/create/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - name: 食材名称（必填）
        - category: 食材分类（必填，可选值：vegetable/meat/seafood/seasoning/fruit/grain/dairy/other）

    成功响应（201）：
        {
            "code": 201,
            "message": "创建成功",
            "data": {
                "id": 100,
                "name": "测试食材",
                "category": "other",
                "category_display": "其他",
                "created_at": "2026-01-31T12:00:00Z",
                "updated_at": "2026-01-31T12:00:00Z"
            }
        }
    """
    serializer = IngredientCreateSerializer(data=request.data)
    if serializer.is_valid():
        ingredient = serializer.save()
        response_serializer = IngredientSerializer(ingredient)
        return ApiResponse.success(data=response_serializer.data, message='创建成功', code=201)
    return ApiResponse.error(message='参数验证失败', errors=serializer.errors, code=400)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_ingredient(request, ingredient_id):
    """
    管理员 - 更新食材接口（仅管理员可访问）

    请求方法：PUT / PATCH
    路由：/api/admin/ingredients/{ingredient_id}/update/

    请求头：
        Authorization: Bearer <access_token>

    路径参数：
        ingredient_id: 食材ID

    请求参数：
        - name: 食材名称（可选）
        - category: 食材分类（可选）

    成功响应（200）：
        {
            "code": 200,
            "message": "更新成功",
            "data": {...}
        }
    """
    # 检查食材是否存在
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        raise NotFoundError('食材不存在')

    # 根据请求方法选择序列化器
    if request.method == 'PUT':
        serializer = IngredientUpdateSerializer(ingredient, data=request.data)
    else:  # PATCH
        serializer = IngredientUpdateSerializer(ingredient, data=request.data, partial=True)

    if serializer.is_valid():
        ingredient = serializer.save()
        response_serializer = IngredientSerializer(ingredient)
        return ApiResponse.success(data=response_serializer.data, message='更新成功')
    return ApiResponse.error(message='参数验证失败', errors=serializer.errors, code=400)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_ingredient(request, ingredient_id):
    """
    管理员 - 删除食材接口（仅管理员可访问）

    请求方法：DELETE
    路由：/api/admin/ingredients/{ingredient_id}/delete/

    请求头：
        Authorization: Bearer <access_token>

    路径参数：
        ingredient_id: 食材ID

    功能说明：
        - 检查食材是否存在
        - 检查食材是否被菜谱使用
        - 删除食材

    成功响应（200）：
        {
            "code": 200,
            "message": "删除成功",
            "data": null
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "该食材正在被菜谱使用，无法删除",
            "data": null
        }
    """
    # 检查食材是否存在
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        raise NotFoundError('食材不存在')

    # 检查是否被菜谱使用
    from recipes.models import RecipeIngredient
    is_used = RecipeIngredient.objects.filter(ingredient=ingredient).exists()

    if is_used:
        raise StateNotAllowedError(
            detail='该食材正在被菜谱使用，无法删除',
            suggestions=['请先删除使用该食材的菜谱', '或联系管理员进行处理']
        )

    # 删除食材
    ingredient.delete()

    return ApiResponse.success(message='删除成功')
