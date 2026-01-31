"""
菜谱模块 - 视图

包含菜谱相关的视图，包括：
- 菜谱列表
- 菜谱详情
- 图片上传
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.files.storage import default_storage
from django.utils import timezone
from django.conf import settings
from utils.response import ApiResponse
from utils.exceptions import ValidationError as BusinessValidationError, NotFoundError
from utils.permissions import IsAdminUser
from utils.constants import BehaviorType
from .models import Recipe, RecipeIngredient
from .serializers import (
    RecipeListSerializer,
    RecipeDetailSerializer,
    RecipeImageUploadSerializer,
    RecipeCreateSerializer,
    RecipeUpdateSerializer
)
from ingredients.models import Ingredient
import os
from django.db.models import Q


def _get_client_ip(request):
    """
    获取客户端 IP 地址

    Args:
        request: HTTP 请求对象

    Returns:
        str: 客户端 IP 地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _generate_image_filename(recipe_id, original_filename):
    """
    生成图片文件名

    Args:
        recipe_id: 菜谱ID
        original_filename: 原始文件名

    Returns:
        str: 生成的文件名，格式：{recipe_id}_{timestamp}.{ext}
    """
    timestamp = int(timezone.now().timestamp())
    ext = os.path.splitext(original_filename)[1]
    return f"{recipe_id}_{timestamp}{ext}"


def _validate_image_file(image_file):
    """
    验证图片文件

    Args:
        image_file: 上传的图片文件

    Raises:
        BusinessValidationError: 文件验证失败
    """
    # 检查文件大小（5MB 限制）
    max_size = 5 * 1024 * 1024
    if image_file.size > max_size:
        raise BusinessValidationError(detail='图片大小不能超过 5MB')

    # 检查文件扩展名
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(image_file.name)[1].lower()
    if ext not in valid_extensions:
        raise BusinessValidationError(detail='仅支持 jpg、jpeg、png、webp 格式的图片')


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    健康检查接口

    用于测试 recipes 模块是否正常工作。

    Returns:
        Response: 健康状态响应
    """
    return ApiResponse.success(
        data={'status': 'healthy', 'module': 'recipes'},
        message='recipes 模块运行正常'
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_list(request):
    """
    菜谱列表接口

    请求方法：GET
    路由：/api/recipes/

    请求参数：
        - page: 页码（可选，默认1）
        - page_size: 每页数量（可选，默认20，最大100）
        - ordering: 排序字段（可选，默认-created_at）
          可选值: view_count, -view_count, favorite_count, -favorite_count,
                  created_at, -created_at
        - cuisine_type: 菜系分类（可选）
        - difficulty: 难度等级（可选）
        - scene_type: 场景分类（可选）
        - target_audience: 适用人群（可选）

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "count": 100,
                "next": null,
                "previous": null,
                "results": [...]
            }
        }
    """
    # 获取查询参数
    queryset = Recipe.objects.all()

    # 筛选条件
    cuisine_type = request.query_params.get('cuisine_type')
    if cuisine_type:
        queryset = queryset.filter(cuisine_type=cuisine_type)

    difficulty = request.query_params.get('difficulty')
    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)

    scene_type = request.query_params.get('scene_type')
    if scene_type:
        queryset = queryset.filter(scene_type=scene_type)

    target_audience = request.query_params.get('target_audience')
    if target_audience:
        queryset = queryset.filter(target_audience=target_audience)

    # 排序参数
    ordering = request.query_params.get('ordering', '-created_at')
    # 验证排序字段是否合法
    valid_ordering_fields = ['view_count', '-view_count',
                             'favorite_count', '-favorite_count',
                             'created_at', '-created_at',
                             'cooking_time', '-cooking_time']
    if ordering not in valid_ordering_fields:
        ordering = '-created_at'
    queryset = queryset.order_by(ordering)

    # 分页
    from utils.pagination import StandardPagination
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = RecipeListSerializer(page, many=True)

    # 使用 ApiResponse 返回统一格式的分页响应
    return ApiResponse.paginate(
        data=paginator.get_paginated_response(serializer.data),
        message='获取成功'
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_detail(request, recipe_id):
    """
    菜谱详情接口

    请求方法：GET
    路由：/api/recipes/{recipe_id}/

    功能说明：
    - 返回菜谱完整信息（基本信息、食材列表、详细步骤等）
    - 增加菜谱点击量计数
    - 记录用户浏览行为到行为日志表

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": 1,
                "name": "宫保鸡丁",
                "cuisine_type": "川菜",
                "difficulty": "medium",
                "cooking_time": 30,
                "image_url": "...",
                "steps": "...",
                "flavor_tags": "辣,甜",
                "view_count": 100,
                "favorite_count": 20,
                "ingredients": [...],
                "flavor_list": ["辣", "甜"]
            }
        }

    错误响应（404）：
        {
            "code": 404,
            "message": "菜谱不存在",
            "data": null
        }
    """
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise NotFoundError(detail='菜谱不存在')

    serializer = RecipeDetailSerializer(recipe)

    # 更新浏览量
    recipe.view_count += 1
    recipe.save(update_fields=['view_count'])

    # 记录浏览行为到行为日志表
    from behavior_logs.models import UserBehaviorLog

    # 获取当前用户（可能为 None，表示未登录用户）
    user = request.user if request.user.is_authenticated else None

    # 获取客户端信息
    ip_address = _get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # 记录浏览行为
    UserBehaviorLog.log_behavior(
        user=user,
        behavior_type=BehaviorType.VIEW,
        target=f'recipe:{recipe_id}',
        extra_data={
            'recipe_name': recipe.name,
            'recipe_id': recipe_id,
            'cuisine_type': recipe.cuisine_type,
            'difficulty': recipe.difficulty,
        },
        ip_address=ip_address,
        user_agent=user_agent
    )

    return ApiResponse.success(
        data=serializer.data,
        message='获取成功'
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """
    通用图片上传接口

    请求方法：POST
    路由：/api/recipes/upload-image/

    请求头：
        Authorization: Bearer <access_token>

    请求参数（multipart/form-data）：
        - image: 图片文件（必填）

    成功响应（200）：
        {
            "code": 200,
            "message": "上传成功",
            "data": {
                "url": "/media/recipes/temp_1706582400.jpg",
                "full_url": "http://localhost:8000/media/recipes/temp_1706582400.jpg"
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "图片大小不能超过 5MB",
            "data": null
        }
    """
    if 'image' not in request.FILES:
        raise BusinessValidationError(detail='请上传图片文件')

    image_file = request.FILES['image']

    # 验证图片文件
    _validate_image_file(image_file)

    # 生成文件名（临时文件使用 temp_ 前缀）
    timestamp = int(timezone.now().timestamp())
    ext = os.path.splitext(image_file.name)[1]
    filename = f"temp_{timestamp}{ext}"

    # 保存文件到 recipes 目录
    path = default_storage.save(f"recipes/{filename}", image_file)

    # 返回 URL
    response_data = {
        'url': f"{settings.MEDIA_URL}{path}",
        'filename': filename
    }

    return ApiResponse.success(
        data=response_data,
        message='上传成功'
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_recipe_image(request, recipe_id):
    """
    菜谱图片上传接口（指定菜谱ID）

    请求方法：POST
    路由：/api/recipes/{recipe_id}/upload-image/

    请求头：
        Authorization: Bearer <access_token>

    请求参数（multipart/form-data）：
        - image: 图片文件（必填）

    成功响应（200）：
        {
            "code": 200,
            "message": "上传成功",
            "data": {
                "url": "/media/recipes/1_1706582400.jpg",
                "full_url": "http://localhost:8000/media/recipes/1_1706582400.jpg",
                "recipe_id": 1
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "图片大小不能超过 5MB",
            "data": null
        }

    错误响应（404）：
        {
            "code": 404,
            "message": "菜谱不存在",
            "data": null
        }
    """
    # 检查菜谱是否存在
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise NotFoundError(detail='菜谱不存在')

    if 'image' not in request.FILES:
        raise BusinessValidationError(detail='请上传图片文件')

    image_file = request.FILES['image']

    # 验证图片文件
    _validate_image_file(image_file)

    # 生成文件名
    filename = _generate_image_filename(recipe_id, image_file.name)

    # 保存文件到 recipes 目录
    path = default_storage.save(f"recipes/{filename}", image_file)

    # 更新菜谱的 image_url 字段
    recipe.image_url = f"{settings.MEDIA_URL}{path}"
    recipe.save(update_fields=['image_url'])

    # 返回 URL
    response_data = {
        'url': recipe.image_url,
        'recipe_id': recipe.id
    }

    return ApiResponse.success(
        data=response_data,
        message='上传成功'
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_search(request):
    """
    菜谱搜索接口

    请求方法：GET
    路由：/api/recipes/search/

    请求参数：
        - keyword: 搜索关键词（必填）
        - search_type: 搜索类型（可选，默认"name"）
          可选值: "name"-按菜谱名称搜索, "ingredient"-按食材搜索
        - page: 页码（可选，默认1）
        - page_size: 每页数量（可选，默认20，最大100）

    成功响应（200）：
        {
            "code": 200,
            "message": "搜索成功",
            "data": {
                "count": 10,
                "keyword": "鸡肉",
                "search_type": "name",
                "results": [...]
            }
        }
    """
    # 获取搜索关键词
    keyword = request.query_params.get('keyword', '').strip()
    if not keyword:
        raise BusinessValidationError(detail='请输入搜索关键词')

    # 获取搜索类型
    search_type = request.query_params.get('search_type', 'name')
    if search_type not in ['name', 'ingredient']:
        search_type = 'name'

    # 构建查询
    if search_type == 'name':
        # 按菜谱名称搜索（模糊匹配）
        queryset = Recipe.objects.filter(name__icontains=keyword)
    else:  # ingredient
        # 按食材搜索：先找到包含该食材的菜谱ID
        ingredient_recipes = RecipeIngredient.objects.filter(
            ingredient__name__icontains=keyword
        ).values_list('recipe_id', flat=True)
        queryset = Recipe.objects.filter(id__in=ingredient_recipes)

    # 按点击量降序排序
    queryset = queryset.order_by('-view_count')

    # 分页
    from utils.pagination import StandardPagination
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = RecipeListSerializer(page, many=True)

    # 构建响应数据
    response_data = {
        'count': queryset.count(),
        'keyword': keyword,
        'search_type': search_type,
        'results': serializer.data
    }

    return ApiResponse.success(
        data=response_data,
        message='搜索成功'
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def hot_recipes(request):
    """
    热门菜谱接口

    请求方法：GET
    路由：/api/recipes/hot/

    请求参数：
        - sort_by: 排序方式（可选，默认"view_count"）
          可选值: "view_count"-按点击量排序, "favorite_count"-按收藏量排序
        - limit: 返回数量（可选，默认20，最大50）

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "sort_by": "view_count",
                "limit": 20,
                "results": [...]
            }
        }
    """
    # 获取排序方式
    sort_by = request.query_params.get('sort_by', 'view_count')
    if sort_by not in ['view_count', 'favorite_count']:
        sort_by = 'view_count'

    # 获取返回数量限制
    try:
        limit = int(request.query_params.get('limit', 20))
        if limit < 1:
            limit = 20
        elif limit > 50:
            limit = 50
    except (ValueError, TypeError):
        limit = 20

    # 按指定字段降序排序
    ordering = f'-{sort_by}'
    queryset = Recipe.objects.all().order_by(ordering)[:limit]

    # 序列化数据
    serializer = RecipeListSerializer(queryset, many=True)

    # 构建响应数据
    response_data = {
        'sort_by': sort_by,
        'limit': limit,
        'count': len(serializer.data),
        'results': serializer.data
    }

    return ApiResponse.success(
        data=response_data,
        message='获取成功'
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_recipe_list(request):
    """
    管理员 - 菜谱管理列表接口（仅管理员可访问）

    请求方法：GET
    路由：/api/admin/recipes/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - page: 页码（可选，默认1）
        - page_size: 每页数量（可选，默认20，最大100）
        - search: 搜索关键词（可选，搜索菜谱名称）
        - cuisine_type: 菜系分类筛选（可选）
        - difficulty: 难度等级筛选（可选）
        - scene_type: 场景分类筛选（可选）
        - target_audience: 适用人群筛选（可选）
        - ordering: 排序字段（可选，默认-created_at）
          可选值: view_count, -view_count, favorite_count, -favorite_count,
                  created_at, -created_at, cooking_time, -cooking_time

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "count": 100,
                "next": null,
                "previous": "http://localhost:8000/api/admin/recipes/?page=1",
                "results": [
                    {
                        "id": 1,
                        "name": "宫保鸡丁",
                        "cuisine_type": "川菜",
                        "scene_type": "晚餐",
                        "difficulty": "medium",
                        "cooking_time": 30,
                        "target_audience": "大众",
                        "image_url": "/media/recipes/1_xxx.jpg",
                        "flavor_tags": "辣,甜",
                        "view_count": 100,
                        "favorite_count": 20,
                        "created_at": "2026-01-30T12:00:00Z"
                    }
                ]
            }
        }

    错误响应（403）：
        {
            "code": 403,
            "message": "权限不足，仅管理员可访问",
            "data": null
        }

    Returns:
        Response: 菜谱管理列表响应
    """
    from utils.pagination import StandardPagination

    # 获取查询参数
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', StandardPagination.page_size)
    search = request.query_params.get('search', '')
    cuisine_type = request.query_params.get('cuisine_type', '')
    difficulty = request.query_params.get('difficulty', '')
    scene_type = request.query_params.get('scene_type', '')
    target_audience = request.query_params.get('target_audience', '')
    ordering = request.query_params.get('ordering', '-created_at')

    # 构建查询集
    queryset = Recipe.objects.all()

    # 搜索功能（菜谱名称）
    if search:
        queryset = queryset.filter(name__icontains=search)

    # 筛选条件
    if cuisine_type:
        queryset = queryset.filter(cuisine_type=cuisine_type)

    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)

    if scene_type:
        queryset = queryset.filter(scene_type=scene_type)

    if target_audience:
        queryset = queryset.filter(target_audience=target_audience)

    # 验证排序字段是否合法
    valid_ordering_fields = [
        'view_count', '-view_count',
        'favorite_count', '-favorite_count',
        'created_at', '-created_at',
        'cooking_time', '-cooking_time'
    ]
    if ordering not in valid_ordering_fields:
        ordering = '-created_at'
    queryset = queryset.order_by(ordering)

    # 分页
    paginator = StandardPagination()
    page_size = int(page_size)
    # 限制最大 page_size
    if page_size > paginator.max_page_size:
        page_size = paginator.max_page_size

    paginator.page_size = page_size
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    # 序列化数据
    serializer = RecipeListSerializer(paginated_queryset, many=True)

    return ApiResponse.success(
        data=paginator.get_paginated_response(serializer.data),
        message='获取成功'
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_recipe(request):
    """
    管理员 - 创建菜谱接口（仅管理员可访问）

    请求方法：POST
    路由：/api/admin/recipes/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - name: 菜谱名称（必填）
        - cuisine_type: 菜系分类（可选）
        - scene_type: 场景分类（可选）
        - target_audience: 适用人群（可选）
        - difficulty: 难度等级（可选，默认medium）
        - cooking_time: 烹饪时长（分钟，可选）
        - image_url: 成品图片URL（可选）
        - steps: 制作步骤（可选）
        - flavor_tags: 口味标签，逗号分隔（可选）
        - ingredients: 食材列表（可选）
          格式：[{"ingredient_id": 1, "amount": "200g", "sort_order": 1}, ...]

    请求体示例：
        {
            "name": "红烧肉",
            "cuisine_type": "家常菜",
            "difficulty": "medium",
            "cooking_time": 60,
            "steps": "1. 焯水... 2. 炒糖色...",
            "flavor_tags": "甜,咸香",
            "ingredients": [
                {"ingredient_id": 1, "amount": "500g", "sort_order": 1},
                {"ingredient_id": 2, "amount": "适量", "sort_order": 2}
            ]
        }

    成功响应（201）：
        {
            "code": 201,
            "message": "菜谱创建成功",
            "data": {
                "id": 100,
                "name": "红烧肉",
                "cuisine_type": "家常菜",
                "difficulty": "medium",
                "cooking_time": 60,
                ...
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "参数验证失败",
            "errors": {...}
        }

    Returns:
        Response: 创建菜谱结果响应
    """
    serializer = RecipeCreateSerializer(data=request.data)

    if serializer.is_valid():
        recipe = serializer.save()
        # 返回完整的菜谱信息
        response_serializer = RecipeDetailSerializer(recipe)
        return ApiResponse.success(
            data=response_serializer.data,
            message='菜谱创建成功',
            code=201
        )

    # 验证失败，返回详细错误信息
    return ApiResponse.error(
        message='参数验证失败',
        errors=serializer.errors
    )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_recipe(request, recipe_id):
    """
    管理员 - 更新菜谱接口（仅管理员可访问）

    请求方法：PUT / PATCH
    路由：/api/admin/recipes/{recipe_id}/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        同创建接口，所有字段均为可选

    成功响应（200）：
        {
            "code": 200,
            "message": "菜谱更新成功",
            "data": {...}
        }

    错误响应（404）：
        {
            "code": 404,
            "message": "菜谱不存在",
            "data": null
        }

    Returns:
        Response: 更新菜谱结果响应
    """
    # 获取菜谱对象
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise NotFoundError(detail='菜谱不存在')

    # PATCH 请求允许部分更新
    partial = request.method == 'PATCH'

    serializer = RecipeUpdateSerializer(recipe, data=request.data, partial=partial)

    if serializer.is_valid():
        recipe = serializer.save()
        # 返回完整的菜谱信息
        response_serializer = RecipeDetailSerializer(recipe)
        return ApiResponse.success(
            data=response_serializer.data,
            message='菜谱更新成功'
        )

    # 验证失败，返回详细错误信息
    return ApiResponse.error(
        message='参数验证失败',
        errors=serializer.errors
    )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_recipe(request, recipe_id):
    """
    管理员 - 删除菜谱接口（仅管理员可访问）

    请求方法：DELETE
    路由：/api/admin/recipes/{recipe_id}/

    请求头：
        Authorization: Bearer <access_token>

    功能说明：
    - 检查菜谱是否存在
    - 删除菜谱记录
    - 自动删除相关收藏记录（CASCADE）
    - 自动删除食材关联（CASCADE）

    成功响应（200）：
        {
            "code": 200,
            "message": "菜谱删除成功",
            "data": {
                "id": 1,
                "name": "宫保鸡丁"
            }
        }

    错误响应（404）：
        {
            "code": 404,
            "message": "菜谱不存在",
            "data": null
        }

    Returns:
        Response: 删除菜谱结果响应
    """
    # 获取菜谱对象
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise NotFoundError(detail='菜谱不存在')

    # 保存菜谱信息用于返回
    recipe_info = {
        'id': recipe.id,
        'name': recipe.name
    }

    # 删除菜谱（相关数据会自动级联删除）
    recipe.delete()

    return ApiResponse.success(
        data=recipe_info,
        message='菜谱删除成功'
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_import_recipes(request):
    """
    管理员 - 批量导入菜谱接口（仅管理员可访问）

    请求方法：POST
    路由：/api/admin/recipes/import/

    请求头：
        Authorization: Bearer <access_token>
        Content-Type: multipart/form-data

    请求参数：
        - file: 导入文件（必填，支持 CSV 或 JSON 格式）
        - file_type: 文件类型（可选，自动检测或指定 csv/json）

    请求体示例（multipart/form-data）：
        file: recipes.json

    JSON 文件格式示例：
        [
            {
                "name": "红烧肉",
                "cuisine_type": "家常菜",
                "scene_type": "晚餐",
                "target_audience": "大众",
                "difficulty": "medium",
                "cooking_time": 60,
                "steps": "1. 焯水... 2. 炒糖色...",
                "flavor_tags": "甜,咸香",
                "image_url": "",
                "ingredients": [
                    {"ingredient_id": 1, "amount": "500g", "sort_order": 1},
                    {"ingredient_id": 2, "amount": "适量", "sort_order": 2}
                ]
            }
        ]

    CSV 文件格式示例：
        name,cuisine_type,scene_type,target_audience,difficulty,cooking_time,steps,flavor_tags,image_url
        红烧肉,家常菜,晚餐,大众,medium,60,"1. 焯水... 2. 炒糖色...",甜,咸香,
        宫保鸡丁,川菜,晚餐,大众,medium,30,"1. 切配... 2. 炒制...",辣,甜,

    成功响应（200）：
        {
            "code": 200,
            "message": "菜谱导入完成",
            "data": {
                "total": 100,
                "success_count": 95,
                "failed_count": 5,
                "failed_records": [
                    {"row": 3, "name": "测试菜谱", "error": "菜谱名称不能为空"}
                ]
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "请上传导入文件",
            "data": null
        }

    Returns:
        Response: 批量导入结果响应
    """
    import json
    import csv
    import io
    from django.db import transaction

    # 检查是否有文件上传
    if 'file' not in request.FILES:
        raise BusinessValidationError(detail='请上传导入文件')

    uploaded_file = request.FILES['file']

    # 获取文件类型（可通过参数指定或自动检测）
    file_type = request.data.get('file_type', '')

    # 如果没有指定文件类型，根据文件扩展名自动检测
    if not file_type:
        filename = uploaded_file.name.lower()
        if filename.endswith('.json'):
            file_type = 'json'
        elif filename.endswith('.csv'):
            file_type = 'csv'
        else:
            raise BusinessValidationError(detail='不支持的文件格式，请上传 JSON 或 CSV 文件')

    # 读取文件内容
    try:
        file_content = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        # 尝试使用 GBK 编码（中文 Excel 导出的 CSV 常用）
        try:
            uploaded_file.seek(0)
            file_content = uploaded_file.read().decode('gbk')
        except Exception:
            raise BusinessValidationError(detail='文件编码错误，请使用 UTF-8 编码的文件')

    # 解析文件数据
    recipes_data = []

    if file_type == 'json':
        try:
            recipes_data = json.loads(file_content)
            if not isinstance(recipes_data, list):
                raise BusinessValidationError(detail='JSON 文件格式错误：根元素必须是数组')
        except json.JSONDecodeError as e:
            raise BusinessValidationError(detail=f'JSON 文件格式错误：{str(e)}')

    elif file_type == 'csv':
        try:
            csv_reader = csv.DictReader(io.StringIO(file_content))
            recipes_data = list(csv_reader)

            if not recipes_data:
                raise BusinessValidationError(detail='CSV 文件为空或格式错误')

            # 将 CSV 数据转换为 JSON 格式（处理 ingredients 字段）
            for row in recipes_data:
                # 处理空字符串
                for key, value in row.items():
                    if value == '' or value is None:
                        row[key] = None

                # CSV 中 ingredients 需要特殊处理（可能是 JSON 字符串）
                if row.get('ingredients'):
                    try:
                        row['ingredients'] = json.loads(row['ingredients'])
                    except (json.JSONDecodeError, TypeError):
                        # 如果解析失败，设置为空列表
                        row['ingredients'] = []
                else:
                    row['ingredients'] = []

        except Exception as e:
            raise BusinessValidationError(detail=f'CSV 文件解析错误：{str(e)}')

    else:
        raise BusinessValidationError(detail=f'不支持的文件类型：{file_type}')

    # 批量导入菜谱
    total_count = len(recipes_data)
    success_count = 0
    failed_count = 0
    failed_records = []

    for idx, recipe_data in enumerate(recipes_data, start=1):
        try:
            # 使用序列化器验证数据
            serializer = RecipeCreateSerializer(data=recipe_data)

            if serializer.is_valid():
                # 使用事务创建菜谱
                with transaction.atomic():
                    serializer.save()
                success_count += 1
            else:
                # 收集验证错误
                error_msg = []
                for field, errors in serializer.errors.items():
                    error_msg.append(f'{field}: {", ".join([str(e) for e in errors])}')
                failed_records.append({
                    'row': idx,
                    'name': recipe_data.get('name', '未知'),
                    'error': '; '.join(error_msg)
                })
                failed_count += 1

        except Exception as e:
            failed_records.append({
                'row': idx,
                'name': recipe_data.get('name', '未知'),
                'error': str(e)
            })
            failed_count += 1

    # 构建响应数据
    result_data = {
        'total': total_count,
        'success_count': success_count,
        'failed_count': failed_count,
        'failed_records': failed_records if failed_records else []
    }

    message = f'菜谱导入完成，成功 {success_count} 条'
    if failed_count > 0:
        message += f'，失败 {failed_count} 条'

    return ApiResponse.success(
        data=result_data,
        message=message
    )
