from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Feedback
from .serializers import FeedbackSerializer
from .permissions import IsAdminOrOwnerReadWrite


class FeedbackViewSet(viewsets.ModelViewSet):
    """反馈建议 CRUD API"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrOwnerReadWrite]

    def get_queryset(self):
        """根据用户角色返回不同范围的反馈"""
        user = self.request.user
        if user.role == 'admin':
            # 管理员可以看到全部反馈
            return Feedback.objects.all()
        # 普通用户只看自己的反馈
        return Feedback.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        """获取反馈列表（支持分页、搜索和筛选）"""
        queryset = self.get_queryset()

        # 搜索
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 类型筛选
        feedback_type = request.query_params.get('feedback_type')
        if feedback_type:
            queryset = queryset.filter(feedback_type=feedback_type)

        # 状态筛选
        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # 创建时间范围筛选
        created_at_after = request.query_params.get('created_at_after')
        created_at_before = request.query_params.get('created_at_before')
        if created_at_after:
            queryset = queryset.filter(created_at__gte=created_at_after)
        if created_at_before:
            queryset = queryset.filter(created_at__lte=created_at_before)

        # 排序
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at', 'title', '-title', 'status', '-status']:
            queryset = queryset.order_by(ordering)

        # 分页
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            page_size = min(page_size, 100)
        except (ValueError, TypeError):
            page, page_size = 1, 20

        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total
        })

    def retrieve(self, request, *args, **kwargs):
        """获取反馈详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 0, "data": serializer.data})

    def create(self, request, *args, **kwargs):
        """创建反馈"""
        # 自动关联当前用户
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"code": 0, "data": serializer.data, "message": "提交成功"}, status=201)

    def update(self, request, *args, **kwargs):
        """更新反馈（管理员可更新状态和回复）"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 如果管理员正在添加回复，设置回复时间和回复人
        if request.user.role == 'admin' and 'admin_reply' in request.data:
            if request.data.get('admin_reply') and not instance.admin_reply:
                request.data['replied_at'] = timezone.now()
                request.data['replied_by'] = request.user.id

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"code": 0, "data": serializer.data, "message": "更新成功"})

    def destroy(self, request, *args, **kwargs):
        """删除反馈"""
        instance = self.get_object()
        instance.delete()
        return Response({"code": 0, "message": "删除成功"})

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """获取筛选选项"""
        from .models import Feedback

        return Response({
            'code': 0,
            'data': {
                'feedback_types': [
                    {'value': choice[0], 'label': choice[1]}
                    for choice in Feedback.FEEDBACK_TYPE_CHOICES
                ],
                'statuses': [
                    {'value': choice[0], 'label': choice[1]}
                    for choice in Feedback.STATUS_CHOICES
                ]
            }
        })
