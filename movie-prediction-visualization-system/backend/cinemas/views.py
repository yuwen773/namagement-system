from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Region, Cinema
from .serializers import (
    RegionSerializer,
    RegionCreateSerializer,
    RegionTreeSerializer,
    CinemaSerializer,
    CinemaCreateSerializer,
    CinemaUpdateSerializer,
)
from accounts.permissions import IsAdmin


class RegionViewSet(viewsets.ModelViewSet):
    """
    地域管理视图集

    提供地域（省份/城市）的完整 CRUD 操作，支持省/市两级层级管理。
    默认仅管理员可访问，用于管理系统中所有地域信息。

    功能包括：
    - 地域列表查询（支持按层级、父级筛选，支持树形结构返回）
    - 创建新地域（省份或城市）
    - 地域详情查看
    - 地域信息更新
    - 地域删除（需检查是否有子地域或关联影院）
    - 获取所有省份列表
    - 获取指定省份下的所有城市
    """
    queryset = Region.objects.prefetch_related('children').all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        """根据操作类型返回不同的序列化器"""
        if self.action == 'create':
            return RegionCreateSerializer
        elif self.action == 'list':
            # 列表默认返回简单序列化
            return RegionSerializer
        return RegionSerializer

    @extend_schema(
        summary="获取地域列表",
        description="""
        获取地域列表，支持多种筛选和查询方式。

        **查询参数：**
        - `level`: 地域层级（PROVINCE-省份/CITY-城市）
        - `parent_id`: 父级地域ID
        - `tree`: 是否返回树形结构（true/false），默认false
        - `order_by`: 排序字段

        **默认行为：**
        - 未指定任何参数时，默认返回所有省份（顶级地域）
        - 指定 tree=true 时，返回完整的省-市树形结构

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": [
                {
                    "id": 1,
                    "name": "北京市",
                    "level": "PROVINCE",
                    "parent": null,
                    "parent_name": null,
                    "children_count": 0,
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ],
            "total": 1
        }
        ```
        """,
        parameters=[
            OpenApiParameter(
                name='level',
                description='地域层级（PROVINCE/CITY）',
                type=OpenApiTypes.STR,
                required=False
            ),
            OpenApiParameter(
                name='parent_id',
                description='父级地域ID',
                type=OpenApiTypes.INT,
                required=False
            ),
            OpenApiParameter(
                name='tree',
                description='是否返回树形结构（true/false）',
                type=OpenApiTypes.BOOL,
                required=False
            ),
        ],
        responses={
            200: RegionSerializer(many=True),
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    def list(self, request, *args, **kwargs):
        """获取地域列表"""
        queryset = self.get_queryset()

        # 按层级筛选
        level = request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        # 按父级筛选
        parent_id = request.query_params.get('parent_id')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        else:
            # 默认只显示顶级（省份）
            if not level:
                queryset = queryset.filter(parent__isnull=True)

        # 如果请求树形结构
        if request.query_params.get('tree') == 'true':
            # 只返回顶级节点，子节点通过嵌套获取
            queryset = queryset.filter(parent__isnull=True)
            serializer = RegionTreeSerializer(queryset, many=True)
            return Response({
                'code': 0,
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @extend_schema(
        summary="创建地域",
        description="""
        创建新的地域记录（省份或城市）。

        **验证规则：**
        - 省份（level=PROVINCE）不能有父级
        - 城市（level=CITY）必须指定父级省份
        - 父级地域必须是省份级别

        **请求体：**
        ```json
        {
            "name": "上海市",
            "level": "PROVINCE",
            "parent": null
        }
        ```

        **成功响应：**
        ```json
        {
            "code": 0,
            "message": "地域创建成功",
            "data": {
                "id": 2,
                "name": "上海市",
                "level": "PROVINCE",
                "parent": null,
                "parent_name": null,
                "children_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
        ```
        """,
        request=RegionCreateSerializer,
        responses={
            201: RegionSerializer,
            400: {"description": "请求参数错误"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    def create(self, request, *args, **kwargs):
        """创建地域"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            region = serializer.save()
            return Response({
                'code': 0,
                'message': '地域创建成功',
                'data': RegionSerializer(region).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '地域创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="获取地域详情",
        description="""
        获取指定地域的详细信息。

        **路径参数：**
        - `id`: 地域ID

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": {
                "id": 1,
                "name": "北京市",
                "level": "PROVINCE",
                "parent": null,
                "parent_name": null,
                "children_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
        ```
        """,
        responses={
            200: RegionSerializer,
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "地域不存在"}
        },
        tags=['影院管理']
    )
    def retrieve(self, request, *args, **kwargs):
        """获取地域详情"""
        instance = self.get_object()
        serializer = RegionSerializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary="更新地域",
        description="""
        更新指定地域的信息。

        **路径参数：**
        - `id`: 地域ID

        **请求体：**
        ```json
        {
            "name": "北京市",
            "parent": null,
            "level": "PROVINCE"
        }
        ```

        **验证规则：**
        - 省份不能有父级
        - 城市必须指定父级省份
        - 父级地域必须是省份级别

        **成功响应：**
        ```json
        {
            "code": 0,
            "message": "地域更新成功",
            "data": {
                "id": 1,
                "name": "北京市",
                "level": "PROVINCE",
                "parent": null,
                "parent_name": null,
                "children_count": 0,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
        ```
        """,
        request=RegionCreateSerializer,
        responses={
            200: RegionSerializer,
            400: {"description": "请求参数错误"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "地域不存在"}
        },
        tags=['影院管理']
    )
    def update(self, request, *args, **kwargs):
        """更新地域"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            region = serializer.save()
            return Response({
                'code': 0,
                'message': '地域更新成功',
                'data': RegionSerializer(region).data
            })
        return Response({
            'code': -1,
            'message': '地域更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="删除地域",
        description="""
        删除指定的地域记录。

        **删除限制：**
        - 如果该地域下存在子地域，无法删除
        - 如果该地域下存在关联的影院，无法删除

        **路径参数：**
        - `id`: 地域ID

        **成功响应：**
        ```json
        {
            "code": 0,
            "message": "地域删除成功"
        }
        ```

        **错误响应：**
        ```json
        {
            "code": -1,
            "message": "无法删除，该地域下存在子地域"
        }
        ```
        """,
        responses={
            204: {"description": "删除成功"},
            400: {"description": "无法删除（存在关联数据）"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "地域不存在"}
        },
        tags=['影院管理']
    )
    def destroy(self, request, *args, **kwargs):
        """删除地域"""
        instance = self.get_object()

        # 检查是否有子地域
        if instance.children.exists():
            return Response({
                'code': -1,
                'message': '无法删除，该地域下存在子地域'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否有关联的影院
        if instance.cinemas.exists():
            return Response({
                'code': -1,
                'message': '无法删除，该地域下存在关联的影院'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            'code': 0,
            'message': '地域删除成功'
        }, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="获取所有省份",
        description="""
        获取系统中所有的省份列表。

        此接口返回所有 level=PROVINCE 的地域记录，
        不包含城市级别的地域。

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": [
                {
                    "id": 1,
                    "name": "北京市",
                    "level": "PROVINCE",
                    "parent": null,
                    "parent_name": null,
                    "children_count": 0,
                    "created_at": "2024-01-01T00:00:00Z"
                },
                {
                    "id": 2,
                    "name": "上海市",
                    "level": "PROVINCE",
                    "parent": null,
                    "parent_name": null,
                    "children_count": 0,
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ],
            "total": 2
        }
        ```
        """,
        responses={
            200: RegionSerializer(many=True),
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    @action(detail=False, methods=['get'])
    def provinces(self, request):
        """获取所有省份"""
        provinces = Region.objects.filter(level='PROVINCE').all()
        serializer = RegionSerializer(provinces, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': provinces.count()
        })

    @extend_schema(
        summary="获取省份下的城市",
        description="""
        获取指定省份下的所有城市列表。

        **路径参数：**
        - `id`: 省份地域ID

        **使用限制：**
        - 只能查询省份（level=PROVINCE）下的城市
        - 如果传入的城市ID，将返回错误

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": [
                {
                    "id": 3,
                    "name": "朝阳区",
                    "level": "CITY",
                    "parent": 1,
                    "parent_name": "北京市",
                    "children_count": 0,
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ],
            "total": 1
        }
        ```

        **错误响应：**
        ```json
        {
            "code": -1,
            "message": "只能获取省份下的城市"
        }
        ```
        """,
        responses={
            200: RegionSerializer(many=True),
            400: {"description": "指定的地域不是省份"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "地域不存在"}
        },
        tags=['影院管理']
    )
    @action(detail=True, methods=['get'])
    def cities(self, request, pk=None):
        """获取某省份下的所有城市"""
        region = self.get_object()
        if region.level != 'PROVINCE':
            return Response({
                'code': -1,
                'message': '只能获取省份下的城市'
            }, status=status.HTTP_400_BAD_REQUEST)

        cities = Region.objects.filter(parent=region).all()
        serializer = RegionSerializer(cities, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': cities.count()
        })


class CinemaViewSet(viewsets.ModelViewSet):
    """
    影院管理视图集

    提供影院的完整 CRUD 操作，支持按地域、省份、城市等多种方式筛选影院。
    默认仅管理员可访问，用于管理系统中所有影院信息。

    功能包括：
    - 影院列表查询（支持多维度筛选和排序）
    - 创建新影院
    - 影院详情查看（包含累计票房统计）
    - 影院信息更新
    - 影院删除（需检查是否有票房记录）
    - 获取营业中的影院列表
    - 按地域统计影院数量
    """
    queryset = Cinema.objects.select_related('region', 'region__parent').all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        """根据操作类型返回不同的序列化器"""
        if self.action == 'create':
            return CinemaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CinemaUpdateSerializer
        return CinemaSerializer

    @extend_schema(
        summary="获取影院列表",
        description="""
        获取影院列表，支持多种筛选和查询方式。

        **查询参数：**
        - `region_id`: 地域ID（筛选指定地域的影院）
        - `province_id`: 省份ID（筛选该省下所有城市的影院）
        - `city_id`: 城市ID（筛选指定城市的影院）
        - `search`: 影院名称模糊搜索
        - `is_active`: 营业状态（true-营业中/false-已停业）
        - `order_by`: 排序字段（name/screen_count/seats_count/created_at/is_active），支持升序/降序
        - `page`: 页码
        - `page_size`: 每页数量

        **默认行为：**
        - 默认按创建时间倒序排序
        - 支持分页查询

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": [
                {
                    "id": 1,
                    "name": "万达影城（CBD店）",
                    "address": "北京市朝阳区建国路93号",
                    "phone": "010-12345678",
                    "region": 3,
                    "region_name": "朝阳区",
                    "parent_region_name": "北京市",
                    "screen_count": 10,
                    "seats_count": 1500,
                    "is_active": true,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "box_office_total": 5000.00
                }
            ],
            "total": 1
        }
        ```
        """,
        parameters=[
            OpenApiParameter(
                name='region_id',
                description='地域ID',
                type=OpenApiTypes.INT,
                required=False
            ),
            OpenApiParameter(
                name='province_id',
                description='省份ID',
                type=OpenApiTypes.INT,
                required=False
            ),
            OpenApiParameter(
                name='city_id',
                description='城市ID',
                type=OpenApiTypes.INT,
                required=False
            ),
            OpenApiParameter(
                name='search',
                description='影院名称模糊搜索',
                type=OpenApiTypes.STR,
                required=False
            ),
            OpenApiParameter(
                name='is_active',
                description='营业状态（true/false）',
                type=OpenApiTypes.BOOL,
                required=False
            ),
            OpenApiParameter(
                name='order_by',
                description='排序字段（支持 - 前缀降序）',
                type=OpenApiTypes.STR,
                required=False
            ),
        ],
        responses={
            200: CinemaSerializer(many=True),
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    def list(self, request, *args, **kwargs):
        """获取影院列表"""
        queryset = self.get_queryset()

        # 按地域筛选
        region_id = request.query_params.get('region_id')
        if region_id:
            queryset = queryset.filter(region_id=region_id)

        # 按省份筛选（会自动包含该省下所有城市的影院）
        province_id = request.query_params.get('province_id')
        if province_id:
            queryset = queryset.filter(region__parent_id=province_id)

        # 按城市筛选
        city_id = request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(region_id=city_id)

        # 按影院名称搜索
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        # 按状态筛选
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # 按排序字段
        order_by = request.query_params.get('order_by', '-created_at')
        allowed_fields = ['name', 'screen_count', 'seats_count', 'created_at', 'is_active']
        field = order_by.lstrip('-')
        if field in allowed_fields:
            queryset = queryset.order_by(order_by)

        # 分页
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
        summary="创建影院",
        description="""
        创建新的影院记录。

        **验证规则：**
        - 屏幕数量必须大于0
        - 座位数量必须大于0
        - 必须指定所属地域（城市级别）

        **请求体：**
        ```json
        {
            "name": "万达影城（CBD店）",
            "address": "北京市朝阳区建国路93号",
            "phone": "010-12345678",
            "region": 3,
            "screen_count": 10,
            "seats_count": 1500,
            "is_active": true
        }
        ```

        **成功响应：**
        ```json
        {
            "code": 0,
            "message": "影院创建成功",
            "data": {
                "id": 1,
                "name": "万达影城（CBD店）",
                "address": "北京市朝阳区建国路93号",
                "phone": "010-12345678",
                "region": 3,
                "region_name": "朝阳区",
                "parent_region_name": "北京市",
                "screen_count": 10,
                "seats_count": 1500,
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "box_office_total": 0
            }
        }
        ```
        """,
        request=CinemaCreateSerializer,
        responses={
            201: CinemaSerializer,
            400: {"description": "请求参数错误"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    def create(self, request, *args, **kwargs):
        """创建影院"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cinema = serializer.save()
            return Response({
                'code': 0,
                'message': '影院创建成功',
                'data': CinemaSerializer(cinema).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '影院创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="获取影院详情",
        description="""获取指定影院的详细信息。

**路径参数：**
- `id`: 影院ID

**响应格式：**
```json
{
    "code": 0,
    "data": {
        "id": 1,
        "name": "万达影城（CBD店）",
        "address": "北京市朝阳区建国路93号",
        "phone": "010-12345678",
        "region": 3,
        "region_name": "朝阳区",
        "parent_region_name": "北京市",
        "screen_count": 10,
        "seats_count": 1500,
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "box_office_total": 5000.00
    }
}
```

**说明：**
- `box_office_total`: 该影院累计票房（单位：万元）
- `region_name`: 所属城市名称
- `parent_region_name`: 所属省份名称""",
        responses={
            200: CinemaSerializer,
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "影院不存在"}
        },
        tags=['影院管理']
    )
    def retrieve(self, request, *args, **kwargs):
        """获取影院详情"""
        instance = self.get_object()
        serializer = CinemaSerializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary="更新影院",
        description="""
        更新指定影院的信息。

        **路径参数：**
        - `id`: 影院ID

        **请求体：**
        ```json
        {
            "name": "万达影城（CBD店）",
            "address": "北京市朝阳区建国路93号",
            "phone": "010-12345678",
            "region": 3,
            "screen_count": 12,
            "seats_count": 1800,
            "is_active": true
        }
        ```

        **验证规则：**
        - 屏幕数量必须大于0
        - 座位数量必须大于0

        **成功响应：**
        ```json
        {
            "code": 0,
            "message": "影院更新成功",
            "data": {
                "id": 1,
                "name": "万达影城（CBD店）",
                "address": "北京市朝阳区建国路93号",
                "phone": "010-12345678",
                "region": 3,
                "region_name": "朝阳区",
                "parent_region_name": "北京市",
                "screen_count": 12,
                "seats_count": 1800,
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
                "box_office_total": 5000.00
            }
        }
        ```
        """,
        request=CinemaUpdateSerializer,
        responses={
            200: CinemaSerializer,
            400: {"description": "请求参数错误"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "影院不存在"}
        },
        tags=['影院管理']
    )
    def update(self, request, *args, **kwargs):
        """更新影院"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            cinema = serializer.save()
            return Response({
                'code': 0,
                'message': '影院更新成功',
                'data': CinemaSerializer(cinema).data
            })
        return Response({
            'code': -1,
            'message': '影院更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="删除影院",
        description="""
        删除指定的影院记录。

        **删除限制：**
        - 如果该影院存在关联的票房记录，无法删除

        **路径参数：**
        - `id`: 影院ID

        **成功响应：**
        ```json
        {
            "code": 0,
            "message": "影院删除成功"
        }
        ```

        **错误响应：**
        ```json
        {
            "code": -1,
            "message": "无法删除，该影院存在关联的票房记录"
        }
        ```
        """,
        responses={
            204: {"description": "删除成功"},
            400: {"description": "无法删除（存在关联数据）"},
            401: {"description": "未认证"},
            403: {"description": "权限不足"},
            404: {"description": "影院不存在"}
        },
        tags=['影院管理']
    )
    def destroy(self, request, *args, **kwargs):
        """删除影院"""
        instance = self.get_object()

        # 检查是否有关联的票房记录
        from boxoffice.models import BoxOfficeRecord
        if BoxOfficeRecord.objects.filter(cinema=instance).exists():
            return Response({
                'code': -1,
                'message': '无法删除，该影院存在关联的票房记录'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            'code': 0,
            'message': '影院删除成功'
        }, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="获取营业中的影院",
        description="""
        获取所有营业中的影院列表（is_active=true）。

        此接口用于筛选当前正在营业的影院，
        不包含已停业的影院。

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": [
                {
                    "id": 1,
                    "name": "万达影城（CBD店）",
                    "address": "北京市朝阳区建国路93号",
                    "phone": "010-12345678",
                    "region": 3,
                    "region_name": "朝阳区",
                    "parent_region_name": "北京市",
                    "screen_count": 10,
                    "seats_count": 1500,
                    "is_active": true,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "box_office_total": 5000.00
                }
            ],
            "total": 1
        }
        ```
        """,
        responses={
            200: CinemaSerializer(many=True),
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取所有营业中的影院"""
        cinemas = Cinema.objects.filter(is_active=True).select_related('region').all()
        serializer = CinemaSerializer(cinemas, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': cinemas.count()
        })

    @extend_schema(
        summary="按地域统计影院数量",
        description="""
        按地域统计影院数量，包括总数和营业中的数量。

        **查询参数：**
        - `region_id`: 地域ID（可选）
          - 如果指定，统计该地域及其子地域的影院
          - 如果不指定，统计所有影院

        **响应格式：**
        ```json
        {
            "code": 0,
            "data": {
                "total": 100,
                "active": 85
            }
        }
        ```

        **字段说明：**
        - `total`: 影院总数
        - `active`: 营业中的影院数量

        **使用场景：**
        - 统计某个省份或城市的影院总数
        - 统计营业中影院占比
        - 数据可视化展示
        """,
        parameters=[
            OpenApiParameter(
                name='region_id',
                description='地域ID（可选，不指定则统计全部）',
                type=OpenApiTypes.INT,
                required=False
            ),
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "total": {"type": "integer", "description": "影院总数"},
                            "active": {"type": "integer", "description": "营业中影院数"}
                        }
                    }
                }
            },
            401: {"description": "未认证"},
            403: {"description": "权限不足"}
        },
        tags=['影院管理']
    )
    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """按地域统计影院数量"""
        from django.db.models import Count

        region_id = request.query_params.get('region_id')
        if region_id:
            # 获取指定地域及其子地域的影院
            region = Region.objects.get(pk=region_id)
            child_region_ids = list(region.children.values_list('id', flat=True))
            all_region_ids = [region_id] + child_region_ids

            cinemas = Cinema.objects.filter(region_id__in=all_region_ids)
        else:
            cinemas = Cinema.objects.all()

        stats = cinemas.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(is_active=True))
        )

        return Response({
            'code': 0,
            'data': stats
        })
