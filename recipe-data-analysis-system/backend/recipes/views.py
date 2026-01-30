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
from .models import Recipe
from .serializers import RecipeListSerializer, RecipeDetailSerializer, RecipeImageUploadSerializer
import os


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
        - cuisine_type: 菜系分类（可选）
        - difficulty: 难度等级（可选）
        - scene_type: 场景分类（可选）

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

    # 排序
    queryset = queryset.order_by('-created_at')

    # 分页
    from utils.pagination import StandardPagination
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = RecipeListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_detail(request, recipe_id):
    """
    菜谱详情接口

    请求方法：GET
    路由：/api/recipes/{recipe_id}/

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": 1,
                "name": "宫保鸡丁",
                ...
            }
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
