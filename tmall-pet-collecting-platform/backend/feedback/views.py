from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackListSerializer, FeedbackUpdateSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    """反馈视图集"""
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackListSerializer
        elif self.action in ['update', 'partial_update']:
            return FeedbackUpdateSerializer
        return FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # 管理员查看所有反馈，支持状态筛选
            status_filter = self.request.query_params.get('status')
            if status_filter:
                return Feedback.objects.filter(status=status_filter).order_by('-created_at')
            return Feedback.objects.all().order_by('-created_at')
        else:
            # 普通用户只能查看自己的反馈
            return Feedback.objects.filter(user=user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """获取反馈列表"""
        queryset = self.get_queryset()

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        page_queryset = queryset[start:end]

        serializer = self.get_serializer(page_queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total
        })

    def create(self, request, *args, **kwargs):
        """创建反馈"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'code': 0,
            'message': '反馈提交成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """获取反馈详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        """用户查看自己的反馈列表"""
        feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = feedbacks.count()
        page_feedbacks = feedbacks[start:end]

        serializer = FeedbackListSerializer(page_feedbacks, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total
        })

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """管理员标记为已处理"""
        if request.user.role != 'admin':
            return Response(
                {'code': -1, 'message': '只有管理员可以操作'},
                status=status.HTTP_403_FORBIDDEN
            )
        feedback = self.get_object()
        feedback.status = 'processed'
        feedback.save()
        return Response({'code': 0, 'message': '已标记为已处理'})
