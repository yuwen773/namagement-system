from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q

from .models import Announcement
from .serializers import (
    AnnouncementSerializer,
    AnnouncementListSerializer,
    AnnouncementCreateSerializer
)
from users.permissions import IsAdminUser


class APIResponseMixin:
    """统一API响应格式"""

    def success_response(self, data=None, message="操作成功", total=None):
        response_data = {"code": 0, "message": message}
        if data is not None:
            response_data["data"] = data
        if total is not None:
            response_data["total"] = total
        return Response(response_data)

    def error_response(self, message="操作失败", code=-1):
        return Response({"code": code, "message": message}, status=status.HTTP_400_BAD_REQUEST)


class AnnouncementListView(APIResponseMixin, generics.ListCreateAPIView):
    """公告列表（普通用户端 - 只显示已发布）"""
    permission_classes = [AllowAny]

    def get_queryset(self):
        # 普通用户只能看到已发布的公告
        return Announcement.objects.filter(status='published')

    def get_serializer_class(self):
        return AnnouncementListSerializer

    def list(self, request, *args, **kwargs):
        """获取已发布公告列表"""
        queryset = self.get_queryset()

        # 优先级筛选
        priority = request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        page_queryset = queryset[start:end]

        serializer = self.get_serializer(page_queryset, many=True)
        return self.success_response(serializer.data, total=total)


class AnnouncementDetailView(APIResponseMixin, generics.RetrieveAPIView):
    """公告详情（普通用户端）"""
    permission_classes = [AllowAny]
    queryset = Announcement.objects.filter(status='published')
    serializer_class = AnnouncementSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """获取公告详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(serializer.data)


class AdminAnnouncementListView(APIResponseMixin, generics.ListCreateAPIView):
    """公告管理列表（管理员端 - 显示所有）"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Announcement.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnnouncementCreateSerializer
        return AnnouncementListSerializer

    def list(self, request, *args, **kwargs):
        """获取所有公告列表（含草稿）"""
        queryset = self.get_queryset()

        # 状态筛选
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 优先级筛选
        priority = request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        page_queryset = queryset[start:end]

        serializer = self.get_serializer(page_queryset, many=True)
        return self.success_response(serializer.data, total=total)

    def post(self, request, *args, **kwargs):
        """创建公告"""
        serializer = AnnouncementCreateSerializer(data=request.data)
        if serializer.is_valid():
            announcement = serializer.save(created_by=request.user)
            # 如果直接发布，设置发布时间
            if announcement.status == 'published':
                from django.utils import timezone
                announcement.published_at = timezone.now()
                announcement.save()
            response_serializer = AnnouncementSerializer(announcement)
            return self.success_response(response_serializer.data, "公告创建成功")
        return self.error_response(str(serializer.errors))


class AdminAnnouncementDetailView(APIResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    """公告管理详情（管理员端）"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """获取公告详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        """更新公告"""
        instance = self.get_object()
        serializer = AnnouncementSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(serializer.data, "更新成功")
        return self.error_response(str(serializer.errors))

    def destroy(self, request, *args, **kwargs):
        """删除公告"""
        instance = self.get_object()
        instance.delete()
        return self.success_response(message="删除成功")


class PublishAnnouncementView(APIResponseMixin, APIView):
    """发布公告"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, id):
        """发布指定的公告"""
        try:
            announcement = Announcement.objects.get(id=id)
            announcement.publish()
            serializer = AnnouncementSerializer(announcement)
            return self.success_response(serializer.data, "发布成功")
        except Announcement.DoesNotExist:
            return self.error_response("公告不存在", code=404)


class UnpublishAnnouncementView(APIResponseMixin, APIView):
    """取消发布公告"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, id):
        """取消发布指定的公告"""
        try:
            announcement = Announcement.objects.get(id=id)
            announcement.unpublish()
            serializer = AnnouncementSerializer(announcement)
            return self.success_response(serializer.data, "已取消发布")
        except Announcement.DoesNotExist:
            return self.error_response("公告不存在", code=404)
