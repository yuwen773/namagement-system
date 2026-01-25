from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from HRMS.permissions import IsHROrAdmin
from .models import PerformanceReview, PerformanceTemplate
from .serializers import (
    PerformanceReviewSerializer,
    PerformanceReviewListSerializer,
    PerformanceReviewCreateSerializer,
    PerformanceReviewUpdateSerializer,
    PerformanceTemplateSerializer,
    PerformanceTemplateListSerializer,
    PerformanceTemplateCreateUpdateSerializer
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

        # 按考核周期筛选
        review_period = self.request.query_params.get('review_period')
        if review_period:
            queryset = queryset.filter(review_period=review_period)

        # 按员工ID筛选
        employee_id = self.request.query_params.get('employee_id')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        # 按状态筛选
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 按分数范围筛选
        score_min = self.request.query_params.get('score_min')
        score_max = self.request.query_params.get('score_max')
        if score_min:
            queryset = queryset.filter(score__gte=score_min)
        if score_max:
            queryset = queryset.filter(score__lte=score_max)

        # 按员工姓名关键词搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(employee__real_name__icontains=keyword)

        # 按部门筛选（通过员工档案关联部门）
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(employee__employee_profile__department_id=department_id)

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


# ==================== 绩效模板管理 ====================

class PerformanceTemplateViewSet(viewsets.ModelViewSet):
    """
    绩效模板 ViewSet

    list: 获取模板列表
    create: 创建模板（HR/Admin）
    retrieve: 获取模板详情
    update: 更新模板（HR/Admin）
    destroy: 删除模板（HR/Admin）
    toggle-active: 切换启用/停用状态
    """
    queryset = PerformanceTemplate.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PerformanceTemplateListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PerformanceTemplateCreateUpdateSerializer
        return PerformanceTemplateSerializer

    def get_queryset(self):
        # 只返回启用的模板或全部（根据参数）
        is_active = self.request.query_params.get('is_active')
        keyword = self.request.query_params.get('keyword')
        queryset = PerformanceTemplate.objects.all()

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # 按模板名称关键词搜索
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsHROrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        切换模板的启用/停用状态
        """
        template = self.get_object()
        template.is_active = not template.is_active
        template.save()

        serializer = PerformanceTemplateSerializer(template)
        status_text = '启用' if template.is_active else '停用'
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': f'模板已{status_text}'
        })
