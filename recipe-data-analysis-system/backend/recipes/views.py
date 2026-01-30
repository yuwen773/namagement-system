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
from utils.constants import BehaviorType
from .models import Recipe, RecipeIngredient
from .serializers import RecipeListSerializer, RecipeDetailSerializer, RecipeImageUploadSerializer
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
