from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from HRMS.permissions import IsHROrAdmin
from .models import PerformanceReview
from .serializers import (
    PerformanceReviewSerializer,
    PerformanceReviewListSerializer,
    PerformanceReviewCreateSerializer,
    PerformanceReviewUpdateSerializer
)


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """
    绩效评估 ViewSet

    list: 获取绩效评估列表
    create: 创建绩效评估（HR/Admin）
    retrieve: 获取绩效评估详情
    update: 更新绩效评估（HR/Admin）
    destroy: 删除绩效评估（HR/Admin）
    my-reviews: 获取我的绩效（员工查看自己的绩效）
    """
    queryset = PerformanceReview.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PerformanceReviewListSerializer
        elif self.action == 'create':
            return PerformanceReviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PerformanceReviewUpdateSerializer
        return PerformanceReviewSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = PerformanceReview.objects.select_related('employee', 'reviewer')

        # 普通员工只能看自己已发布的绩效
        if user.role == 'employee':
            queryset = queryset.filter(employee=user, status='published')

        # 人事/管理员可以看全部，但普通员工查看时只能看已发布的
        # HR/Admin 可以看草稿和已发布的
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsHROrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        reviewer = self.request.user
        serializer.save(reviewer=reviewer)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """
        获取当前用户的绩效评估列表（仅已发布的）
        """
        user = request.user
        reviews = PerformanceReview.objects.filter(
            employee=user,
            status='published'
        ).select_related('employee', 'reviewer').order_by('-created_at')

        serializer = PerformanceReviewListSerializer(reviews, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        获取待处理的绩效评估草稿列表（HR/Admin）
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        reviews = PerformanceReview.objects.filter(
            status='draft'
        ).select_related('employee', 'reviewer').order_by('-created_at')

        serializer = PerformanceReviewListSerializer(reviews, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        发布绩效评估
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        review = self.get_object()
        review.status = 'published'
        review.save()

        serializer = PerformanceReviewSerializer(review)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '绩效评估已发布'
        })

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """
        撤回绩效评估
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        review = self.get_object()
        review.status = 'draft'
        review.save()

        serializer = PerformanceReviewSerializer(review)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '绩效评估已撤回'
        })
