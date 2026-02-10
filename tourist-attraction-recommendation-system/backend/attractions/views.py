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

        # 类别筛选
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # 地区筛选
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)

        return queryset

    def list(self, request, *args, **kwargs):
        """获取景点列表"""
        queryset = self.get_queryset()
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
