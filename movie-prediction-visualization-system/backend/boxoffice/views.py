from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import BoxOfficeRecord
from .serializers import (
    BoxOfficeRecordSerializer,
    BoxOfficeRecordCreateSerializer,
    BoxOfficeRecordUpdateSerializer,
    BoxOfficeStatsSerializer,
)
from accounts.permissions import IsAdmin


class BoxOfficeRecordViewSet(viewsets.ModelViewSet):
    """
    票房记录视图集
    提供完整的 CRUD 操作
    """
    queryset = BoxOfficeRecord.objects.select_related('movie', 'cinema', 'cinema__region').all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        """根据操作类型返回不同的序列化器"""
        if self.action == 'create':
            return BoxOfficeRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BoxOfficeRecordUpdateSerializer
        return BoxOfficeRecordSerializer

    def list(self, request, *args, **kwargs):
        """获取票房记录列表"""
        queryset = self.get_queryset()

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

        # 按影院筛选
        cinema_id = request.query_params.get('cinema_id')
        if cinema_id:
            queryset = queryset.filter(cinema_id=cinema_id)

        # 按地区筛选
        region_id = request.query_params.get('region_id')
        if region_id:
            queryset = queryset.filter(cinema__region_id=region_id)

        # 按排序字段
        order_by = request.query_params.get('order_by', '-record_date')
        # 防止 SQL 注入，只允许特定字段
        allowed_fields = ['record_date', 'daily_box_office', 'screening_count', 'audience_count']
        field = order_by.lstrip('-')
        if field in allowed_fields:
            queryset = queryset.order_by(order_by)

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

    def retrieve(self, request, *args, **kwargs):
        """获取票房记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

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

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """批量删除票房记录"""
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


class BoxOfficeStatsView(APIView):
    """票房统计视图"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取票房统计数据"""
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
