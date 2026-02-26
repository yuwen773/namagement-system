from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.pagination import StandardPageNumberPagination
from utils.response import success_response
from apps.users.permissions import IsAdmin

from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('author')
    serializer_class = AnnouncementSerializer
    pagination_class = StandardPageNumberPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return AnnouncementCreateSerializer
        return AnnouncementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 处理筛选参数
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        is_published = self.request.query_params.get('is_published')
        if is_published is not None:
            if is_published.lower() == 'true':
                queryset = queryset.filter(is_published=True)
            elif is_published.lower() == 'false':
                queryset = queryset.filter(is_published=False)

        # 普通用户只能看到已发布的公告（list 和 retrieve 动作）
        if self.action in ('list', 'retrieve'):
            # 检查是否不是管理员
            from apps.users.models import get_user_role
            user_role = get_user_role(self.request.user)
            if user_role != 'admin':
                queryset = queryset.filter(is_published=True)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total = self.paginator.page.paginator.count
            return success_response(
                data=serializer.data,
                message='Fetched successfully',
                total=total,
            )
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Fetched successfully',
            total=len(serializer.data),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message='Fetched successfully')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return success_response(
            data=serializer.data,
            message='Created successfully',
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Updated successfully')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message='Deleted successfully')
