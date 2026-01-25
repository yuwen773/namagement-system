from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Notice
from .serializers import (
    NoticeSerializer, NoticeListSerializer, 
    NoticeCreateSerializer, NoticePublishSerializer
)
from HRMS.permissions import IsAdmin


class NoticeViewSet(viewsets.ModelViewSet):
    """公告管理视图集"""
    queryset = Notice.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NoticeListSerializer
        elif self.action == 'create':
            return NoticeCreateSerializer
        return NoticeSerializer
    
    def get_queryset(self):
        """获取公告列表"""
        queryset = Notice.objects.all()

        # 过滤条件
        is_published = self.request.query_params.get('is_published')
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published.lower() == 'true')

        is_pinned = self.request.query_params.get('is_pinned')
        if is_pinned is not None:
            queryset = queryset.filter(is_pinned=is_pinned.lower() == 'true')

        # 按标题关键词搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)

        # 按日期范围筛选
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        if date_start:
            queryset = queryset.filter(created_at__date__gte=date_start)
        if date_end:
            queryset = queryset.filter(created_at__date__lte=date_end)

        # 按发布人筛选
        publisher_id = self.request.query_params.get('publisher_id')
        if publisher_id:
            queryset = queryset.filter(published_by_id=publisher_id)

        return queryset
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布公告"""
        notice = self.get_object()
        if notice.is_published:
            return Response(
                {'code': 400, 'message': '公告已发布'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = NoticePublishSerializer(
            notice, 
            data={}, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'code': 0,
            'message': '公告发布成功',
            'data': NoticeSerializer(notice).data
        })
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """撤回公告"""
        notice = self.get_object()
        if not notice.is_published:
            return Response(
                {'code': 400, 'message': '公告未发布'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notice.unpublish()
        
        return Response({
            'code': 0,
            'message': '公告已撤回',
            'data': NoticeSerializer(notice).data
        })


class NoticePublicViewSet(viewsets.ReadOnlyModelViewSet):
    """公开公告视图集（所有认证用户可查看已发布公告）"""
    serializer_class = NoticeListSerializer
    permission_classes = []  # 允许所有认证用户访问

    def get_queryset(self):
        """只返回已发布的公告"""
        # 验证用户已登录
        if not self.request.user.is_authenticated:
            return Notice.objects.none()

        queryset = Notice.objects.filter(is_published=True)

        # 按标题关键词搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)

        # 按日期范围筛选（发布时间）
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        if date_start:
            queryset = queryset.filter(published_at__date__gte=date_start)
        if date_end:
            queryset = queryset.filter(published_at__date__lte=date_end)

        # 按是否置顶筛选
        is_pinned = self.request.query_params.get('is_pinned')
        if is_pinned is not None:
            queryset = queryset.filter(is_pinned=is_pinned.lower() == 'true')

        return queryset

    def list(self, request, *args, **kwargs):
        """重写 list 方法返回统一响应格式"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })

    def retrieve(self, request, *args, **kwargs):
        """重写 retrieve 方法返回统一响应格式"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'code': 0,
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        获取最新公告列表
        GET /api/notice/public/latest/?limit=5
        """
        limit = int(request.query_params.get('limit', 5))
        queryset = Notice.objects.filter(is_published=True)[:limit]
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })
