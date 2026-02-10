from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import BoxOfficeRecord
from .serializers import (
    BoxOfficeRecordSerializer,
    BoxOfficeRecordCreateSerializer,
    BoxOfficeRecordUpdateSerializer,
    BoxOfficeStatsSerializer,
    BoxOfficeBatchInputSerializer,
    BoxOfficeBatchInputRecordSerializer,
)
from .filters import BoxOfficeRecordFilter
from accounts.permissions import IsAdmin


class BoxOfficeRecordViewSet(viewsets.ModelViewSet):
    """
    票房记录视图集

    提供完整的 CRUD 操作和批量操作功能，仅限管理员访问。

    **操作列表：**
    - `list`: 获取票房记录列表（支持日期/影片/影院/地域筛选）
    - `create`: 创建单条票房记录
    - `retrieve`: 获取票房记录详情
    - `update`: 更新票房记录
    - `partial_update`: 部分更新票房记录
    - `destroy`: 删除票房记录
    - `batch_delete`: 批量删除票房记录
    - `batch_input`: 批量录入票房记录（每次最多100条）

    **权限要求：** 需要登录且具有管理员权限

    **筛选字段：**
    - movie: 影片ID
    - cinema: 影院ID
    - cinema__region: 地域ID
    - record_date_start: 记录日期开始
    - record_date_end: 记录日期结束
    - min_daily_box_office: 最低日票房
    - max_daily_box_office: 最高日票房
    """
    queryset = BoxOfficeRecord.objects.select_related('movie', 'cinema', 'cinema__region').all()
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_class = BoxOfficeRecordFilter
    ordering_fields = ['record_date', 'daily_box_office', 'screening_count', 'audience_count']
    ordering = ['-record_date', '-created_at']

    def get_serializer_class(self):
        """
        根据操作类型返回不同的序列化器

        Returns:
            - BoxOfficeRecordCreateSerializer: 创建操作
            - BoxOfficeRecordUpdateSerializer: 更新操作
            - BoxOfficeRecordSerializer: 其他操作
        """
        if self.action == 'create':
            return BoxOfficeRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BoxOfficeRecordUpdateSerializer
        return BoxOfficeRecordSerializer

    @extend_schema(
        summary='获取票房记录列表',
        description='获取票房记录列表，支持多维度筛选和排序。返回包含影片、影院、地域关联信息的完整数据。',
        parameters=[
            OpenApiParameter(name='movie', description='影片ID', type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name='cinema', description='影院ID', type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name='cinema__region', description='地域ID', type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name='record_date_start', description='记录日期开始（YYYY-MM-DD）', type=OpenApiTypes.DATE, required=False),
            OpenApiParameter(name='record_date_end', description='记录日期结束（YYYY-MM-DD）', type=OpenApiTypes.DATE, required=False),
            OpenApiParameter(name='min_daily_box_office', description='最低日票房（元）', type=OpenApiTypes.NUMBER, required=False),
            OpenApiParameter(name='max_daily_box_office', description='最高日票房（元）', type=OpenApiTypes.NUMBER, required=False),
            OpenApiParameter(name='ordering', description='排序字段（如：-record_date）', type=OpenApiTypes.STR, required=False),
            OpenApiParameter(name='page', description='页码', type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name='page_size', description='每页数量', type=OpenApiTypes.INT, required=False),
        ],
        responses={200: BoxOfficeRecordSerializer},
        tags=['票房数据']
    )
    def list(self, request, *args, **kwargs):
        """获取票房记录列表（使用过滤器进行筛选）"""
        queryset = self.filter_queryset(self.get_queryset())

        # 分页
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

    @extend_schema(
        summary='创建票房记录',
        description='创建新的票房记录。系统会自动验证记录日期不早于影片上映日期，并更新影片的累计票房。',
        request=BoxOfficeRecordCreateSerializer,
        responses={201: BoxOfficeRecordSerializer},
        tags=['票房数据']
    )
    def create(self, request, *args, **kwargs):
        """创建票房记录"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            return Response({
                'code': 0,
                'message': '票房记录创建成功',
                'data': BoxOfficeRecordSerializer(record).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '票房记录创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='获取票房记录详情',
        description='根据ID获取单条票房记录的详细信息，包含关联的影片、影院和地域信息。',
        responses={200: BoxOfficeRecordSerializer},
        tags=['票房数据']
    )
    def retrieve(self, request, *args, **kwargs):
        """获取票房记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary='更新票房记录',
        description='完全更新指定ID的票房记录。更新后自动重新计算影片的累计票房。注意：不支持修改关联的影片、影院和记录日期。',
        request=BoxOfficeRecordUpdateSerializer,
        responses={200: BoxOfficeRecordSerializer},
        tags=['票房数据']
    )
    def update(self, request, *args, **kwargs):
        """更新票房记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            record = serializer.save()
            return Response({
                'code': 0,
                'message': '票房记录更新成功',
                'data': BoxOfficeRecordSerializer(record).data
            })
        return Response({
            'code': -1,
            'message': '票房记录更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='删除票房记录',
        description='删除指定ID的票房记录。删除后自动重新计算影片的累计票房。',
        responses={204: None},
        tags=['票房数据']
    )
    def destroy(self, request, *args, **kwargs):
        """删除票房记录"""
        instance = self.get_object()
        movie = instance.movie
        instance.delete()

        # 更新影片累计票房
        if movie:
            total = BoxOfficeRecord.objects.filter(movie=movie).aggregate(
                total=Coalesce(Sum('daily_box_office'), 0)
            )['total']
            movie.box_office_total = total / 10000
            movie.save()

        return Response({
            'code': 0,
            'message': '票房记录删除成功'
        }, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary='批量删除票房记录',
        description='根据ID列表批量删除多条票房记录。删除后会自动更新所有相关影片的累计票房。',
        request={
            'type': 'object',
            'properties': {
                'ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': '要删除的票房记录ID列表'
                }
            },
            'required': ['ids']
        },
        tags=['票房数据']
    )
    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """
        批量删除票房记录

        请求体示例：
        ```json
        {
            "ids": [1, 2, 3, 4, 5]
        }
        ```

        删除流程：
        1. 验证是否提供了要删除的ID列表
        2. 批量删除票房记录
        3. 重新计算所有相关影片的累计票房

        Returns:
            Response: 包含删除结果的消息
        """
        ids = request.data.get('ids', [])
        if not ids:
            return Response({
                'code': -1,
                'message': '请选择要删除的记录'
            }, status=status.HTTP_400_BAD_REQUEST)

        records = self.get_queryset().filter(id__in=ids)
        movies_to_update = set()

        for record in records:
            movies_to_update.add(record.movie)
            record.delete()

        # 更新相关影片的累计票房
        for movie in movies_to_update:
            total = BoxOfficeRecord.objects.filter(movie=movie).aggregate(
                total=Coalesce(Sum('daily_box_office'), 0)
            )['total']
            movie.box_office_total = total / 10000
            movie.save()

        return Response({
            'code': 0,
            'message': f'成功删除 {len(ids)} 条记录'
        })

    @extend_schema(
        summary='批量录入票房记录',
        description='批量创建多条票房记录，每次最多支持100条。系统会验证每条记录的数据完整性和正确性，包括检查重复记录、日期范围等。录入成功后自动更新影片的累计票房。',
        request=BoxOfficeBatchInputSerializer,
        tags=['票房数据']
    )
    @action(detail=False, methods=['post'])
    def batch_input(self, request):
        """
        批量录入票房记录（管理员专用）

        每次最多100条记录。

        请求体示例：
        ```json
        {
            "records": [
                {
                    "movie": 1,
                    "cinema": 1,
                    "record_date": "2024-01-01",
                    "daily_box_office": 500000,
                    "screening_count": 10,
                    "audience_count": 500
                },
                {
                    "movie": 2,
                    "cinema": 1,
                    "record_date": "2024-01-01",
                    "daily_box_office": 300000
                }
            ]
        }
        ```

        录入流程：
        1. 验证请求数据格式和记录数量
        2. 逐条验证每条记录的数据
        3. 检查是否存在重复记录（相同影片、影院、日期）
        4. 创建有效记录，记录错误信息
        5. 更新所有相关影片的累计票房

        Returns:
            Response: 包含录入结果的详细报告
        """
        # 验证请求数据
        serializer = BoxOfficeBatchInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': -1,
                'message': '批量录入数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        records_data = serializer.validated_data['records']
        created_records = []
        errors = []
        movies_to_update = set()

        # 处理每条记录
        for idx, record_data in enumerate(records_data):
            record_serializer = BoxOfficeBatchInputRecordSerializer(data=record_data)

            if record_serializer.is_valid():
                try:
                    # 检查是否已存在相同记录
                    exists = BoxOfficeRecord.objects.filter(
                        movie=record_data['movie'],
                        cinema=record_data['cinema'],
                        record_date=record_data['record_date']
                    ).exists()

                    if exists:
                        errors.append({
                            'index': idx,
                            'message': '该日期的票房记录已存在',
                            'data': record_data
                        })
                        continue

                    record = record_serializer.save()
                    created_records.append(record)
                    movies_to_update.add(record.movie)
                except Exception as e:
                    errors.append({
                        'index': idx,
                        'message': str(e),
                        'data': record_data
                    })
            else:
                errors.append({
                    'index': idx,
                    'message': '数据验证失败',
                    'errors': record_serializer.errors,
                    'data': record_data
                })

        # 更新相关影片的累计票房
        for movie in movies_to_update:
            total = BoxOfficeRecord.objects.filter(movie=movie).aggregate(
                total=Coalesce(Sum('daily_box_office'), 0)
            )['total']
            movie.box_office_total = total / 10000
            movie.save()

        # 构建响应
        result = {
            'created_count': len(created_records),
            'error_count': len(errors),
        }

        if created_records:
            result['created_records'] = BoxOfficeRecordSerializer(created_records, many=True).data

        if errors:
            result['errors'] = errors

        if created_records and not errors:
            return Response({
                'code': 0,
                'message': f'成功录入 {len(created_records)} 条票房记录',
                'data': result
            }, status=status.HTTP_201_CREATED)
        elif created_records and errors:
            return Response({
                'code': 0,
                'message': f'部分成功录入: {len(created_records)} 条成功, {len(errors)} 条失败',
                'data': result
            }, status=status.HTTP_207_MULTI_STATUS)
        else:
            return Response({
                'code': -1,
                'message': '批量录入失败',
                'data': result
            }, status=status.HTTP_400_BAD_REQUEST)


class BoxOfficeStatsView(APIView):
    """
    票房统计视图

    提供票房数据的统计分析功能，支持按日期范围和影片进行筛选统计。
    所有登录用户均可访问。

    **统计指标：**
    - total_box_office: 总票房金额（元）
    - total_screening_count: 总场次
    - total_audience_count: 总人次
    - record_count: 记录数量
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取票房统计数据',
        description='获取票房数据的统计汇总信息。支持按日期范围和影片ID进行筛选，返回该范围内票房的总金额、总场次、总人次等统计数据。',
        parameters=[
            OpenApiParameter(name='start_date', description='开始日期（YYYY-MM-DD）', type=OpenApiTypes.DATE, required=False),
            OpenApiParameter(name='end_date', description='结束日期（YYYY-MM-DD）', type=OpenApiTypes.DATE, required=False),
            OpenApiParameter(name='movie_id', description='影片ID', type=OpenApiTypes.INT, required=False),
        ],
        responses={200: BoxOfficeStatsSerializer},
        tags=['票房数据']
    )
    def get(self, request):
        """
        获取票房统计数据

        查询参数：
        - start_date: 开始日期（可选）
        - end_date: 结束日期（可选）
        - movie_id: 影片ID（可选）

        Returns:
            Response: 包含统计数据的响应对象

        示例：
        ```
        GET /api/boxoffice/stats/?start_date=2024-01-01&end_date=2024-01-31&movie_id=1
        ```
        """
        queryset = BoxOfficeRecord.objects.all()

        # 按日期范围筛选
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(record_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(record_date__lte=end_date)

        # 按影片筛选
        movie_id = request.query_params.get('movie_id')
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)

        stats = queryset.aggregate(
            total_box_office=Coalesce(Sum('daily_box_office'), 0),
            total_screening_count=Coalesce(Sum('screening_count'), 0),
            total_audience_count=Coalesce(Sum('audience_count'), 0),
            record_count=Coalesce(Sum('id', distinct=True), 0)
        )

        serializer = BoxOfficeStatsSerializer({
            'total_box_office': stats['total_box_office'],
            'total_screening_count': stats['total_screening_count'],
            'total_audience_count': stats['total_audience_count'],
            'record_count': queryset.count()
        })

        return Response({
            'code': 0,
            'data': serializer.data
        })
