from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import MovieType, Movie
from .serializers import (
    MovieTypeSerializer,
    MovieTypeCreateSerializer,
    MovieSerializer,
    MovieListSerializer,
    MovieCreateUpdateSerializer,
)
from .filters import MovieTypeFilter, MovieFilter


class MovieTypeViewSet(viewsets.ModelViewSet):
    """
    影片类型视图集

    提供影片类型的增删改查功能，支持类型列表查询、创建、更新和删除操作。
    删除类型时会检查是否有影片关联，有关联影片的类型无法删除。
    """
    queryset = MovieType.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieTypeFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MovieTypeSerializer
        return MovieTypeCreateSerializer

    @extend_schema(
        summary='获取影片类型列表',
        description='''
        获取所有影片类型的列表，支持按名称搜索、排序和分页。

        支持的查询参数：
        - search: 按类型名称模糊搜索
        - ordering: 排序字段（name, created_at）
        - page: 页码
        - page_size: 每页数量
        ''',
        parameters=[
            OpenApiParameter(
                name='search',
                description='类型名称搜索',
                type=OpenApiTypes.STR,
                required=False
            ),
            OpenApiParameter(
                name='ordering',
                description='排序字段',
                type=OpenApiTypes.STR,
                required=False,
                enum=['name', '-name', 'created_at', '-created_at']
            ),
        ],
        responses=MovieTypeSerializer,
        tags=['影片类型管理']
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'code': 0,
                'data': serializer.data,
                'total': self.paginator.page.paginator.count
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @extend_schema(
        summary='获取影片类型详情',
        description='根据ID获取单个影片类型的详细信息，包含该类型下的影片数量。',
        responses=MovieTypeSerializer,
        tags=['影片类型管理']
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary='创建影片类型',
        description='''
        创建新的影片类型。

        请求体：
        - name: 类型名称（必填）
        ''',
        request=MovieTypeCreateSerializer,
        responses=MovieTypeSerializer,
        tags=['影片类型管理']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'code': 0,
                'message': '影片类型创建成功',
                'data': MovieTypeSerializer(instance).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '影片类型创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='更新影片类型',
        description='''
        更新指定ID的影片类型信息。

        请求体：
        - name: 类型名称
        ''',
        request=MovieTypeCreateSerializer,
        responses=MovieTypeSerializer,
        tags=['影片类型管理']
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'code': 0,
                'message': '影片类型更新成功',
                'data': MovieTypeSerializer(instance).data
            })
        return Response({
            'code': -1,
            'message': '影片类型更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='部分更新影片类型',
        description='''
        部分更新指定ID的影片类型信息。

        请求体：
        - name: 类型名称
        ''',
        request=MovieTypeCreateSerializer,
        responses=MovieTypeSerializer,
        tags=['影片类型管理']
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='删除影片类型',
        description='''
        删除指定ID的影片类型。

        注意：如果该类型下存在关联的影片，则无法删除，会返回错误信息。
        ''',
        responses={
            200: {'description': '删除成功'},
            400: {'description': '类型下存在影片，无法删除'}
        },
        tags=['影片类型管理']
    )
    def destroy(self, request, *args, **kwargs):
        """删除类型时检查是否有影片关联"""
        instance = self.get_object()
        if instance.movies.exists():
            return Response({
                'code': -1,
                'message': '该类型下存在影片，无法删除'
            }, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({
            'code': 0,
            'message': f'类型 {instance.name} 已删除'
        })


class MovieViewSet(viewsets.ModelViewSet):
    """
    影片视图集

    提供影片的完整 CRUD 功能，包括列表查询、详情查看、创建、更新和删除操作。
    支持按标题、导演、演员搜索，按类型、状态筛选，以及按上映日期、票房等字段排序。
    提供已上映影片和即将上映影片的快捷查询接口。
    """
    queryset = Movie.objects.select_related('type').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'director', 'actors']
    ordering_fields = ['release_date', 'box_office_total', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return MovieCreateUpdateSerializer
        return MovieSerializer

    @extend_schema(
        summary='获取影片列表',
        description='''
        获取影片列表，支持多条件筛选、搜索、排序和分页。

        支持的查询参数：
        - search: 按标题、导演、演员模糊搜索
        - type: 按类型ID筛选
        - status: 按状态筛选（RELEASED-已上映, COMING-即将上映）
        - release_date_after: 上映日期（之后）
        - release_date_before: 上映日期（之前）
        - ordering: 排序字段（release_date, box_office_total, created_at）
        - page: 页码
        - page_size: 每页数量
        ''',
        parameters=[
            OpenApiParameter(
                name='search',
                description='影片标题、导演、演员搜索',
                type=OpenApiTypes.STR,
                required=False
            ),
            OpenApiParameter(
                name='type',
                description='类型ID',
                type=OpenApiTypes.INT,
                required=False
            ),
            OpenApiParameter(
                name='status',
                description='影片状态',
                type=OpenApiTypes.STR,
                required=False,
                enum=['RELEASED', 'COMING']
            ),
            OpenApiParameter(
                name='ordering',
                description='排序字段',
                type=OpenApiTypes.STR,
                required=False,
                enum=['release_date', '-release_date', 'box_office_total', '-box_office_total', 'created_at', '-created_at']
            ),
        ],
        responses=MovieListSerializer,
        tags=['影片管理']
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'code': 0,
                'data': serializer.data,
                'total': self.paginator.page.paginator.count
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @extend_schema(
        summary='获取影片详情',
        description='根据ID获取单个影片的完整详细信息，包含类型、票房等所有字段。',
        responses=MovieSerializer,
        tags=['影片管理']
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary='创建影片',
        description='''
        创建新的影片记录。

        请求体：
        - title: 影片标题（必填）
        - director: 导演
        - actors: 演员
        - release_date: 上映日期
        - duration: 片长（分钟）
        - type: 类型ID（必填）
        - poster_url: 海报URL
        - description: 剧情简介
        - status: 状态（RELEASED-已上映, COMING-即将上映）
        ''',
        request=MovieCreateUpdateSerializer,
        responses=MovieSerializer,
        tags=['影片管理']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'code': 0,
                'message': '影片创建成功',
                'data': MovieSerializer(instance).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '影片创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='更新影片',
        description='''
        更新指定ID的影片信息。

        请求体：
        - title: 影片标题
        - director: 导演
        - actors: 演员
        - release_date: 上映日期
        - duration: 片长（分钟）
        - type: 类型ID
        - poster_url: 海报URL
        - description: 剧情简介
        - status: 状态（RELEASED-已上映, COMING-即将上映）
        ''',
        request=MovieCreateUpdateSerializer,
        responses=MovieSerializer,
        tags=['影片管理']
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'code': 0,
                'message': '影片更新成功',
                'data': MovieSerializer(instance).data
            })
        return Response({
            'code': -1,
            'message': '影片更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='部分更新影片',
        description='''
        部分更新指定ID的影片信息。

        请求体：
        - title: 影片标题
        - director: 导演
        - actors: 演员
        - release_date: 上映日期
        - duration: 片长（分钟）
        - type: 类型ID
        - poster_url: 海报URL
        - description: 剧情简介
        - status: 状态（RELEASED-已上映, COMING-即将上映）
        ''',
        request=MovieCreateUpdateSerializer,
        responses=MovieSerializer,
        tags=['影片管理']
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='删除影片',
        description='''
        删除指定ID的影片记录。

        **限制：**
        - 如果该影片有关联的票房记录，则无法删除

        **影响：**
        - 影片数据将被永久删除
        - 相关的类型引用将被清除

        **权限要求：**
        需要管理员权限
        ''',
        responses={
            200: {'description': '删除成功'},
            400: {'description': '影片存在票房记录，无法删除'}
        },
        tags=['影片管理']
    )
    def destroy(self, request, *args, **kwargs):
        """
        删除影片

        Args:
            request: 请求对象
            pk: 影片ID

        Returns:
            Response: 返回操作结果
        """
        instance = self.get_object()

        # 检查是否有关联的票房记录
        from boxoffice.models import BoxOfficeRecord
        if BoxOfficeRecord.objects.filter(movie=instance).exists():
            return Response({
                'code': -1,
                'message': f'影片《{instance.title}》存在票房记录，无法删除'
            }, status=status.HTTP_400_BAD_REQUEST)

        title = instance.title
        instance.delete()
        return Response({
            'code': 0,
            'message': f'影片《{title}》已删除'
        })

    @extend_schema(
        summary='获取已上映影片',
        description='''
        获取所有已上映状态的影片列表。

        返回状态为 RELEASED 的影片，支持分页。
        ''',
        responses=MovieListSerializer,
        tags=['影片管理']
    )
    @action(detail=False, methods=['get'])
    def released(self, request):
        """获取已上映影片"""
        queryset = self.get_queryset().filter(status='RELEASED')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary='获取即将上映影片',
        description='''
        获取所有即将上映状态的影片列表。

        返回状态为 COMING 的影片，支持分页。
        ''',
        responses=MovieListSerializer,
        tags=['影片管理']
    )
    @action(detail=False, methods=['get'])
    def coming(self, request):
        """获取即将上映影片"""
        queryset = self.get_queryset().filter(status='COMING')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary='获取影片详细信息',
        description='''
        获取指定ID影片的完整详细信息。

        包含影片的所有字段信息，包括类型名称、票房数据等。
        ''',
        responses=MovieSerializer,
        tags=['影片管理']
    )
    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """获取影片详情"""
        movie = self.get_object()
        serializer = MovieSerializer(movie)
        return Response({
            'code': 0,
            'data': serializer.data
        })
