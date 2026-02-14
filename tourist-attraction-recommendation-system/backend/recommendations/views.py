"""
推荐应用视图

提供三种推荐API：
1. 热门推荐 GET /api/recommendations/popular/
2. 个性化推荐 GET /api/recommendations/personalized/
3. 相似推荐 GET /api/recommendations/similar/{attraction_id}/
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .services import (
    get_popular_attractions,
    get_personalized_recommendations,
    get_similar_attractions
)
from .serializers import AttractionRecommendSerializer


class PopularRecommendView(APIView):
    """
    热门景点推荐

    GET /api/recommendations/popular/
    - 无需认证
    - 用于冷启动场景（新用户无历史数据）
    """
    permission_classes = [AllowAny]

    @extend_schema(
        responses=AttractionRecommendSerializer(many=True)
    )
    def get(self, request):
        """获取热门景点推荐"""
        limit = int(request.query_params.get('limit', 10))
        limit = min(limit, 50)  # 限制最大50

        results = get_popular_attractions(limit)

        attractions = [r['attraction'] for r in results]
        hot_scores = {r['attraction'].id: r['hot_score'] for r in results}

        serializer = AttractionRecommendSerializer(
            attractions,
            many=True,
            context={'request': request, 'hot_scores': hot_scores}
        )

        # 更新序列化器中的 hot_score
        data = serializer.data
        for i, item in enumerate(data):
            item['hot_score'] = hot_scores.get(item['id'], 0)

        return Response({
            'code': 0,
            'data': data,
            'total': len(data)
        })


class PersonalizedRecommendView(APIView):
    """
    个性化推荐

    GET /api/recommendations/personalized/
    - 需要认证
    - 基于用户历史收藏和评分推荐同类景点
    - 未登录用户返回热门推荐
    """
    permission_classes = [AllowAny]

    @extend_schema(
        responses=AttractionRecommendSerializer(many=True)
    )
    def get(self, request):
        """获取个性化推荐"""
        limit = int(request.query_params.get('limit', 10))
        limit = min(limit, 50)

        # 检查用户是否登录
        if not request.user.is_authenticated:
            # 未登录用户返回热门推荐
            results = get_popular_attractions(limit)
            attractions = [r['attraction'] for r in results]
            hot_scores = {r['attraction'].id: r['hot_score'] for r in results}

            serializer = AttractionRecommendSerializer(
                attractions,
                many=True,
                context={'request': request}
            )

            data = serializer.data
            for i, item in enumerate(data):
                item['hot_score'] = hot_scores.get(item['id'], 0)

            return Response({
                'code': 0,
                'data': data,
                'total': len(data),
                'message': '未登录，返回热门推荐'
            })

        # 已登录用户获取个性化推荐
        results = get_personalized_recommendations(request.user.id, limit)
        attractions = [r['attraction'] for r in results]
        hot_scores = {r['attraction'].id: r['hot_score'] for r in results}

        serializer = AttractionRecommendSerializer(
            attractions,
            many=True,
            context={'request': request}
        )

        data = serializer.data
        for i, item in enumerate(data):
            item['hot_score'] = hot_scores.get(item['id'], 0)

        return Response({
            'code': 0,
            'data': data,
            'total': len(data)
        })


class SimilarRecommendView(APIView):
    """
    相似景点推荐

    GET /api/recommendations/similar/{attraction_id}/
    - 无需认证
    - 基于类别和地区推荐相似景点
    """
    permission_classes = [AllowAny]

    @extend_schema(
        responses=AttractionRecommendSerializer(many=True)
    )
    def get(self, request, attraction_id):
        """获取相似景点推荐"""
        limit = int(request.query_params.get('limit', 6))
        limit = min(limit, 20)

        results = get_similar_attractions(attraction_id, limit)

        if not results:
            return Response({
                'code': -1,
                'message': '未找到相似景点'
            }, status=status.HTTP_404_NOT_FOUND)

        attractions = [r['attraction'] for r in results]
        hot_scores = {r['attraction'].id: r['hot_score'] for r in results}

        serializer = AttractionRecommendSerializer(
            attractions,
            many=True,
            context={'request': request}
        )

        data = serializer.data
        for i, item in enumerate(data):
            item['hot_score'] = hot_scores.get(item['id'], 0)

        return Response({
            'code': 0,
            'data': data,
            'total': len(data)
        })
