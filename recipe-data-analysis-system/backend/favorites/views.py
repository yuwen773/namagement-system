"""
收藏模块 - 视图

本模块定义收藏相关的 API 视图，包括：
- 收藏菜谱
- 取消收藏
- 获取收藏列表
- 检查收藏状态
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import IntegrityError
from django.utils import timezone

from utils.response import ApiResponse
from utils.exceptions import ValidationError as BusinessValidationError, NotFoundError, StateNotAllowedError
from utils.constants import BehaviorType
from utils.pagination import StandardPagination

from .models import UserFavorite
from .serializers import FavoriteCreateSerializer, FavoriteListSerializer
from recipes.models import Recipe


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


class FavoriteViewSet(viewsets.ViewSet):
    """
    收藏视图集

    处理收藏的创建和列表操作
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        收藏菜谱接口

        请求方法：POST
        路由：/api/favorites/

        请求头：
            Authorization: Bearer <access_token>

        请求参数（JSON）：
            {
                "recipe_id": 1
            }

        成功响应（200）：
            {
                "code": 200,
                "message": "收藏成功",
                "data": {
                    "id": 1,
                    "recipe": {...},
                    "created_at": "2026-01-30T12:00:00Z"
                }
            }

        错误响应（400）：
            {
                "code": 400,
                "message": "菜谱不存在",
                "data": null
            }

        错误响应（400）：
            {
                "code": 400,
                "message": "已经收藏过该菜谱",
                "data": null
            }
        """
        # 验证输入数据
        serializer = FavoriteCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise BusinessValidationError(detail=serializer.errors)

        recipe_id = serializer.validated_data['recipe_id']
        user = request.user

        # 检查是否已收藏
        if UserFavorite.objects.filter(user=user, recipe_id=recipe_id).exists():
            raise StateNotAllowedError(detail='已经收藏过该菜谱')

        # 获取菜谱对象
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise NotFoundError(detail='菜谱不存在')

        # 创建收藏记录
        try:
            favorite = UserFavorite.objects.create(
                user=user,
                recipe=recipe
            )
        except IntegrityError:
            raise StateNotAllowedError(detail='已经收藏过该菜谱')

        # 增加菜谱的收藏量
        recipe.favorite_count += 1
        recipe.save(update_fields=['favorite_count'])

        # 记录收藏行为到行为日志表
        from behavior_logs.models import UserBehaviorLog

        ip_address = _get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        UserBehaviorLog.log_behavior(
            user=user,
            behavior_type=BehaviorType.COLLECT,
            target=f'recipe:{recipe_id}',
            extra_data={
                'recipe_name': recipe.name,
                'recipe_id': recipe_id,
                'cuisine_type': recipe.cuisine_type,
            },
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 序列化并返回
        from .serializers import FavoriteSerializer
        response_serializer = FavoriteSerializer(favorite)

        return ApiResponse.success(
            data=response_serializer.data,
            message='收藏成功'
        )

    def list(self, request):
        """
        获取当前用户的收藏列表接口

        请求方法：GET
        路由：/api/favorites/

        请求头：
            Authorization: Bearer <access_token>

        请求参数：
            - page: 页码（可选，默认1）
            - page_size: 每页数量（可选，默认20，最大100）
            - ordering: 排序字段（可选，默认-created_at）
              可选值: created_at, -created_at

        成功响应（200）：
            {
                "code": 200,
                "message": "获取成功",
                "data": {
                    "count": 10,
                    "next": null,
                    "previous": null,
                    "results": [...]
                }
            }
        """
        user = request.user
        queryset = UserFavorite.objects.filter(user=user)

        # 排序
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering not in ['created_at', '-created_at']:
            ordering = '-created_at'
        queryset = queryset.order_by(ordering)

        # 分页
        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = FavoriteListSerializer(page, many=True)

        return ApiResponse.paginate(
            data=paginator.get_paginated_response(serializer.data),
            message='获取成功'
        )


class FavoriteDetailView(APIView):
    """
    收藏详情视图

    处理单个收藏的操作（取消收藏）
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, recipe_id):
        """
        取消收藏接口

        请求方法：DELETE
        路由：/api/favorites/{recipe_id}/

        请求头：
            Authorization: Bearer <access_token>

        成功响应（200）：
            {
                "code": 200,
                "message": "取消收藏成功",
                "data": null
            }

        错误响应（400）：
            {
                "code": 400,
                "message": "未收藏该菜谱",
                "data": null
            }
        """
        user = request.user

        # 查找收藏记录
        try:
            favorite = UserFavorite.objects.get(user=user, recipe_id=recipe_id)
        except UserFavorite.DoesNotExist:
            raise StateNotAllowedError(detail='未收藏该菜谱')

        # 获取菜谱对象（用于减少收藏量）
        recipe = favorite.recipe

        # 删除收藏记录
        favorite.delete()

        # 减少菜谱的收藏量（确保不小于0）
        if recipe.favorite_count > 0:
            recipe.favorite_count -= 1
            recipe.save(update_fields=['favorite_count'])

        # 记录取消收藏行为到行为日志表
        from behavior_logs.models import UserBehaviorLog

        ip_address = _get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        UserBehaviorLog.log_behavior(
            user=user,
            behavior_type=BehaviorType.UNCOLLECT,
            target=f'recipe:{recipe_id}',
            extra_data={
                'recipe_name': recipe.name,
                'recipe_id': recipe_id,
            },
            ip_address=ip_address,
            user_agent=user_agent
        )

        return ApiResponse.success(
            data=None,
            message='取消收藏成功'
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favorite_status(request, recipe_id):
    """
    检查收藏状态接口

    请求方法：GET
    路由：/api/favorites/check/{recipe_id}/

    请求头：
        Authorization: Bearer <access_token>

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "is_favorited": true,
                "recipe_id": 1
            }
        }
    """
    user = request.user
    is_favorited = UserFavorite.objects.filter(
        user=user,
        recipe_id=recipe_id
    ).exists()

    return ApiResponse.success(
        data={
            'is_favorited': is_favorited,
            'recipe_id': recipe_id
        },
        message='获取成功'
    )
