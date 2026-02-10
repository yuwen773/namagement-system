from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models

from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(is_deleted=False)
        # 普通用户：只看到自己的通知 + 全员公告
        if user.role != 'ADMIN':
            queryset = queryset.filter(models.Q(user=user) | models.Q(user__isnull=True))
        return queryset

    def list(self, request):
        """我的通知列表"""
        queryset = self.get_queryset()
        # 统计未读数
        unread_count = queryset.filter(is_read=False).count()
        serializer = NotificationSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count(),
            'unread_count': unread_count
        })

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        """标记已读"""
        notification_id = request.data.get('id')
        if notification_id:
            # 标记单个
            notification = Notification.objects.filter(id=notification_id, is_deleted=False).first()
            if notification:
                notification.is_read = True
                notification.save()
                return Response({'code': 0, 'message': '已标记已读'})
            return Response({'code': -1, 'message': '通知不存在'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 全部标记已读
            queryset = self.get_queryset()
            queryset.filter(is_read=False).update(is_read=True)
            return Response({'code': 0, 'message': '已全部标记已读'})

    @action(detail=False, methods=['post'])
    def announcement(self, request):
        """发布公告（管理员）"""
        if request.user.role != 'ADMIN':
            return Response({'code': -1, 'message': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=None, type='ANNOUNCEMENT')
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '公告发布成功'
        }, status=status.HTTP_201_CREATED)
