from django.db import models
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attraction
from .serializers import (
    AttractionListSerializer,
    AttractionDetailSerializer,
    AttractionCreateUpdateSerializer
)
from accounts.permissions import IsAdmin
import os
import uuid
from django.conf import settings


class AttractionViewSet(viewsets.ModelViewSet):
    """景点视图集"""
    queryset = Attraction.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return AttractionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AttractionCreateUpdateSerializer
        return AttractionDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthenticated(), IsAdmin()]

    def get_queryset(self):
        queryset = Attraction.objects.filter(is_deleted=False)

        # 类别筛选 - 支持英文值和中文值
        category = self.request.query_params.get('category')
        if category:
            # 英文到中文的映射
            category_map = {
                'NATURE': '自然风光',
                'HISTORY': '人文古迹',
                'THEME': '主题乐园',
                'OTHER': '其他',
                'MODERN': '现代建筑',
            }
            # 如果是英文值，转换为中文
            if category in category_map:
                category = category_map[category]
            queryset = queryset.filter(category=category)

        # 地区筛选
        region = self.request.query_params.get('region')
        if region:
            # 地区也需要转换（如果有映射的话）
            region_map = {
                'beijing': '北京',
                'shanghai': '上海',
                'hangzhou': '杭州',
                'chengdu': '成都',
                'xian': '西安',
            }
            if region.lower() in region_map:
                region = region_map[region.lower()]
            queryset = queryset.filter(region__icontains=region)

        # 关键词搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                models.Q(name__icontains=keyword) |
                models.Q(description__icontains=keyword) |
                models.Q(address__icontains=keyword)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        """获取景点列表"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 无分页时返回全部数据
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    def retrieve(self, request, *args, **kwargs):
        """获取景点详情"""
        instance = self.get_object()
        # 增加浏览量
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """创建景点"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '创建成功'
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """更新景点"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '更新成功'
        })

    def destroy(self, request, *args, **kwargs):
        """删除景点（逻辑删除）"""
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({
            'code': 0,
            'message': '删除成功'
        })

    @action(detail=False, methods=['get'])
    def search(self, request):
        """景点搜索"""
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response({
                'code': -1,
                'message': '请输入搜索关键词'
            })

        queryset = Attraction.objects.filter(
            is_deleted=False,
            name__icontains=keyword
        ) | Attraction.objects.filter(
            is_deleted=False,
            description__icontains=keyword
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def upload(self, request):
        """上传景点图片"""
        file = request.FILES.get('file')
        if not file:
            return Response({
                'code': -1,
                'message': '请选择要上传的图片'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查文件类型
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            return Response({
                'code': -1,
                'message': '仅支持 JPG、PNG、GIF、WebP 格式的图片'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查文件大小 (最大 5MB)
        if file.size > 5 * 1024 * 1024:
            return Response({
                'code': -1,
                'message': '图片大小不能超过 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 生成唯一文件名
        ext = os.path.splitext(file.name)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join('attractions', filename)

        # 保存文件
        from django.core.files.storage import default_storage
        saved_path = default_storage.save(filepath, file)

        # 返回文件 URL（添加域名）
        file_url = default_storage.url(saved_path)
        # 获取请求的域名
        host = request.get_host() if request.get_host() else 'localhost:8123'
        if file_url.startswith('/'):
            file_url = f"{request.scheme}://{host}{file_url}"

        return Response({
            'code': 0,
            'data': {
                'url': file_url,
                'filename': filename
            },
            'message': '上传成功'
        })
