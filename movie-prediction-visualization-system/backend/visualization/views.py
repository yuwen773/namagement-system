from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.db.models import Sum, Count, Avg, Q, F, Func
from django.db.models.functions import Coalesce, ExtractWeek, ExtractMonth, ExtractYear
from django.db.models import DecimalField, Value
from django.utils import timezone
from django.db import connection
from datetime import timedelta, date
from decimal import Decimal

from boxoffice.models import BoxOfficeRecord, DailyRegionStat, DailyMovieTypeStat, DailyOverallStat
from movies.models import Movie, MovieType
from cinemas.models import Cinema, Region
from .serializers import (
    MovieBoxOfficeSerializer,
    DailyBoxOfficeSerializer,
    TypeBoxOfficeSerializer,
    RegionBoxOfficeSerializer,
    WeeklyChampionSerializer,
    DashboardStatsSerializer,
)


class BoxOfficeTop10View(APIView):
    """
    历史票房总榜 Top 10 视图

    提供历史累计票房最高的10部电影数据，用于展示票房排行榜。
    支持按票房总额降序排列，仅包含有票房记录的影片。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取票房总榜 Top 10',
        description='获取历史累计票房最高的10部电影列表，按票房总额降序排列。',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取历史票房最高的10部电影"""
        top_movies = Movie.objects.filter(
            box_office_total__gt=0
        ).order_by('-box_office_total')[:10]

        serializer = MovieBoxOfficeSerializer(top_movies, many=True)
        return Response({
            'code': 0,
            'data': serializer.data
        })


class TodayBoxOfficeView(APIView):
    """
    今日大盘总票房统计视图

    提供当日全国票房统计数据，包括总票房、总场次、总人次。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取今日大盘票房统计',
        description='获取当日全国票房统计数据，使用预聚合表优化性能',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取今日票房统计 - 使用预聚合表优化"""
        today = timezone.now().date()

        # 优先使用预聚合表
        daily_stat = DailyOverallStat.objects.filter(record_date=today).first()

        if daily_stat:
            return Response({
                'code': 0,
                'data': {
                    'date': today,
                    'total_box_office': daily_stat.total_box_office,
                    'total_screening_count': daily_stat.total_screening_count,
                    'total_audience_count': daily_stat.total_audience_count
                }
            })

        # 预聚合表没有数据时，使用原始表（首次或数据未更新时）
        stats = BoxOfficeRecord.objects.filter(
            record_date=today
        ).aggregate(
            total_box_office=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField())),
            total_screening_count=Coalesce(Sum('screening_count'), 0),
            total_audience_count=Coalesce(Sum('audience_count'), 0)
        )

        return Response({
            'code': 0,
            'data': {
                'date': today,
                'total_box_office': stats['total_box_office'],
                'total_screening_count': stats['total_screening_count'],
                'total_audience_count': stats['total_audience_count']
            }
        })


class WeeklyChampionView(APIView):
    """
    本周票房冠军视图

    提供本周（周一至当前日期）票房最高的影片信息。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取本周票房冠军',
        description='获取本周（周一至当前日期）累计票房最高的影片信息。',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取本周票房最高的电影 - 使用预聚合表优化"""
        from django.core.cache import cache

        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        cache_key = f'weekly_champion_{today}'

        # 尝试缓存
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # 从本周的 DailyOverallStat 聚合获取冠军数据
        # 注意：这里需要关联 Movie 表获取电影名称，不能直接从预聚合表获取
        weekly_stats = BoxOfficeRecord.objects.filter(
            record_date__gte=week_start
        ).values('movie_id', 'movie__title').annotate(
            weekly_box_office=Sum('daily_box_office')
        ).order_by('-weekly_box_office')[:1]

        data = None
        if weekly_stats:
            data = {
                'movie_id': weekly_stats[0]['movie_id'],
                'movie_title': weekly_stats[0]['movie__title'],
                'weekly_box_office': weekly_stats[0]['weekly_box_office']
            }

        response_data = {
            'code': 0,
            'data': data
        }

        # 缓存 1 小时
        cache.set(cache_key, response_data, 3600)

        return Response(response_data)


class TypeBoxOfficeView(APIView):
    """
    按类型统计票房占比视图

    提供各影片类型的票房分布数据和占比信息。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取各类型票房占比',
        description='获取各影片类型的票房总额及占比数据，使用预聚合表优化',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取各类型票房占比 - 使用预聚合表优化"""
        from django.core.cache import cache

        # 尝试从缓存获取数据（缓存1小时）
        cache_key = 'type_box_office_stats'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # 使用最近3个月的数据来统计
        three_months_ago = date.today() - timedelta(days=90)

        # 1. 获取所有类型映射
        types = MovieType.objects.values('id', 'name')
        type_map = {t['id']: t['name'] for t in types}

        # 2. 聚合查询 - 使用 DailyMovieTypeStat 预聚合表
        stats = DailyMovieTypeStat.objects.filter(
            record_date__gte=three_months_ago
        ).values('movie_type').annotate(
            box_office=Coalesce(Sum('box_office'), Value(Decimal('0'), output_field=DecimalField()))
        ).order_by('-box_office')

        # 3. 如果预聚合表没有数据，回退到 BoxOfficeRecord
        if not stats.exists():
            stats = BoxOfficeRecord.objects.filter(
                record_date__gte=three_months_ago,
                movie__type__isnull=False
            ).values('movie__type').annotate(
                box_office=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
            ).order_by('-box_office')

            # 转换字段名
            stats_list = []
            for stat in stats:
                stats_list.append({
                    'movie_type': stat['movie__type'],
                    'box_office': stat['box_office']
                })
            stats = stats_list
        else:
            stats = list(stats)

        # 4. 计算总票房
        total_box_office = sum(s['box_office'] for s in stats) or Decimal('1')

        result = []
        for stat in stats:
            type_id = stat.get('movie_type') or stat.get('movie__type')
            box_office = stat['box_office']

            if not type_id:
                continue

            percentage = float(box_office) / float(total_box_office) * 100
            result.append({
                'type_id': type_id,
                'type_name': type_map.get(type_id, '未知'),
                'box_office': box_office,
                'percentage': round(percentage, 2)
            })

        response_data = {
            'code': 0,
            'data': result
        }

        # 缓存1小时
        cache.set(cache_key, response_data, 3600)

        return Response(response_data)


class RegionBoxOfficeView(APIView):
    """
    按地域统计票房分布视图

    提供各省份的票房分布数据和影院数量统计。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取各省份票房分布',
        description='获取各省份的票房总额及影院数量统计，使用预聚合表优化',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取各省份票房分布 - 使用预聚合表优化"""
        from django.core.cache import cache

        # 缓存处理
        cache_key = 'region_box_office_distribution'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # 1. 获取所有 Region 信息
        regions = Region.objects.values('id', 'name', 'parent_id', 'level')
        region_map = {r['id']: r for r in regions}

        # 初始化省份统计数据
        province_stats = {
            r['id']: {'box_office': Decimal('0'), 'cinema_count': 0, 'name': r['name'], 'id': r['id']}
            for r in regions if r['level'] == 'PROVINCE'
        }

        # 2. 聚合票房 - 使用 DailyRegionStat 预聚合表
        box_office_stats = DailyRegionStat.objects.values('region').annotate(
            total_box_office=Coalesce(Sum('box_office'), Value(Decimal('0'), output_field=DecimalField()))
        )

        # 如果预聚合表没有数据，回退到 BoxOfficeRecord
        if not box_office_stats.exists():
            box_office_stats = BoxOfficeRecord.objects.exclude(
                cinema__region__isnull=True
            ).values('cinema__region').annotate(
                total_box_office=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
            )
            # 转换字段名
            stats_list = []
            for stat in box_office_stats:
                stats_list.append({
                    'region': stat['cinema__region'],
                    'total_box_office': stat['total_box_office']
                })
            box_office_stats = stats_list
        else:
            box_office_stats = list(box_office_stats)

        # 在内存中归并票房数据
        for stat in box_office_stats:
            region_id = stat.get('region') or stat.get('cinema__region')
            total = stat['total_box_office']

            region = region_map.get(region_id)
            if not region:
                continue

            # 确定归属省份
            province_id = None
            if region['level'] == 'PROVINCE':
                province_id = region_id
            elif region['parent_id']:
                province_id = region['parent_id']

            if province_id and province_id in province_stats:
                province_stats[province_id]['box_office'] += total

        # 3. 统计影院数量 - 直接查询 Cinema 表
        cinema_regions = Cinema.objects.values_list('region', flat=True)

        for region_id in cinema_regions:
            if not region_id:
                continue

            region_obj = region_map.get(region_id)
            if not region_obj:
                continue

            province_id = None
            if region_obj['level'] == 'PROVINCE':
                province_id = region_id
            elif region_obj['parent_id']:
                province_id = region_obj['parent_id']

            if province_id and province_id in province_stats:
                province_stats[province_id]['cinema_count'] += 1

        # 4. 格式化结果
        result = []
        for stats in province_stats.values():
            if stats['box_office'] > 0 or stats['cinema_count'] > 0:
                result.append({
                    'region_id': stats['id'],
                    'region_name': stats['name'],
                    'box_office': stats['box_office'],
                    'cinema_count': stats['cinema_count']
                })

        # 按票房降序排序
        result.sort(key=lambda x: float(x['box_office']), reverse=True)

        response_data = {
            'code': 0,
            'data': result
        }

        # 缓存 1 小时
        cache.set(cache_key, response_data, 3600)

        return Response(response_data)


class TimeSeriesView(APIView):
    """
    票房时间走势数据视图

    提供指定时间范围内的票房走势数据，支持按日/周/月聚合。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取票房时间走势',
        description='获取指定时间范围内的票房走势数据，使用预聚合表优化',
        parameters=[
            OpenApiParameter(name='period', type=OpenApiTypes.STR, description='聚合周期：day/week/month', default='day', enum=['day', 'week', 'month']),
            OpenApiParameter(name='days', type=OpenApiTypes.INT, description='统计天数', default=30)
        ],
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取票房时间走势 - 使用预聚合表优化"""
        from django.core.cache import cache

        period = request.query_params.get('period', 'day')
        days = int(request.query_params.get('days', 30))

        # 缓存键
        today = timezone.now().date()
        cache_key = f'time_series_{period}_{days}_{today}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        end_date = today
        start_date = end_date - timedelta(days=days)

        # 使用 DailyOverallStat 预聚合表
        queryset = DailyOverallStat.objects.filter(
            record_date__gte=start_date,
            record_date__lte=end_date
        )

        # 如果预聚合表没有数据，回退到 BoxOfficeRecord
        if not queryset.exists():
            queryset = BoxOfficeRecord.objects.filter(
                record_date__gte=start_date,
                record_date__lte=end_date
            )
            use_prefetched = False
        else:
            use_prefetched = True

        result = []

        if period == 'day':
            if use_prefetched:
                # 按日聚合 - 直接读取
                daily_stats = queryset.values(
                    'record_date', 'total_box_office', 'total_screening_count', 'total_audience_count'
                ).order_by('record_date')

                result = [{
                    'date': stat['record_date'],
                    'total_box_office': stat['total_box_office'],
                    'total_screening_count': stat['total_screening_count'],
                    'total_audience_count': stat['total_audience_count']
                } for stat in daily_stats]
            else:
                # 使用原始表聚合
                daily_stats = queryset.values('record_date').annotate(
                    total_box_office=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField())),
                    total_screening_count=Coalesce(Sum('screening_count'), 0),
                    total_audience_count=Coalesce(Sum('audience_count'), 0)
                ).order_by('record_date')

                result = [{
                    'date': stat['record_date'],
                    'total_box_office': stat['total_box_office'],
                    'total_screening_count': stat['total_screening_count'],
                    'total_audience_count': stat['total_audience_count']
                } for stat in daily_stats]

        elif period == 'week':
            if use_prefetched:
                # 按周聚合
                weekly_stats = queryset.annotate(
                    week=ExtractWeek('record_date')
                ).values('week').annotate(
                    total_box_office=Coalesce(Sum('total_box_office'), Value(Decimal('0'), output_field=DecimalField())),
                    total_screening_count=Coalesce(Sum('total_screening_count'), 0),
                    total_audience_count=Coalesce(Sum('total_audience_count'), 0)
                ).order_by('week')

                result = [{
                    'week': stat['week'],
                    'total_box_office': stat['total_box_office'],
                    'total_screening_count': stat['total_screening_count'],
                    'total_audience_count': stat['total_audience_count']
                } for stat in weekly_stats]
            else:
                weekly_stats = queryset.annotate(
                    week=ExtractWeek('record_date')
                ).values('week').annotate(
                    total_box_office=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField())),
                    total_screening_count=Coalesce(Sum('screening_count'), 0),
                    total_audience_count=Coalesce(Sum('audience_count'), 0)
                ).order_by('week')

                result = [{
                    'week': stat['week'],
                    'total_box_office': stat['total_box_office'],
                    'total_screening_count': stat['total_screening_count'],
                    'total_audience_count': stat['total_audience_count']
                } for stat in weekly_stats]

        elif period == 'month':
            if use_prefetched:
                # 按月聚合
                monthly_stats = queryset.annotate(
                    year=ExtractYear('record_date'),
                    month=ExtractMonth('record_date')
                ).values('year', 'month').annotate(
                    total_box_office=Coalesce(Sum('total_box_office'), Value(Decimal('0'), output_field=DecimalField())),
                    total_screening_count=Coalesce(Sum('total_screening_count'), 0),
                    total_audience_count=Coalesce(Sum('total_audience_count'), 0)
                ).order_by('year', 'month')

                result = [{
                    'year': stat['year'],
                    'month': stat['month'],
                    'total_box_office': stat['total_box_office'],
                    'total_screening_count': stat['total_screening_count'],
                    'total_audience_count': stat['total_audience_count']
                } for stat in monthly_stats]
            else:
                monthly_stats = queryset.annotate(
                    year=ExtractYear('record_date'),
                    month=ExtractMonth('record_date')
                ).values('year', 'month').annotate(
                    total_box_office=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField())),
                    total_screening_count=Coalesce(Sum('screening_count'), 0),
                    total_audience_count=Coalesce(Sum('audience_count'), 0)
                ).order_by('year', 'month')

                result = [{
                    'year': stat['year'],
                    'month': stat['month'],
                    'total_box_office': stat['total_box_office'],
                    'total_screening_count': stat['total_screening_count'],
                    'total_audience_count': stat['total_audience_count']
                } for stat in monthly_stats]

        else:
            return Response({
                'code': -1,
                'message': '无效的时间周期参数，支持 day/week/month'
            }, status=400)

        response_data = {
            'code': 0,
            'data': result
        }

        # 根据是否使用预聚合表设置不同的缓存时间
        # 如果使用预聚合表，可以缓存更长时间
        cache_time = 3600 if use_prefetched else 600
        cache.set(cache_key, response_data, cache_time)

        return Response(response_data)


class DashboardView(APIView):
    """
    仪表盘概览数据视图

    提供仪表盘所需的综合统计数据。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取仪表盘概览数据',
        description='获取仪表盘所需的综合统计数据',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        """获取仪表盘所需的所有统计数据"""
        from django.core.cache import cache

        # 尝试从缓存获取数据（缓存5分钟）
        cache_key = 'dashboard_stats'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())

        # 今日票房 - 使用预聚合表
        today_stat = DailyOverallStat.objects.filter(record_date=today).first()
        if today_stat:
            today_box_office = today_stat.total_box_office
        else:
            # 回退到原始表
            today_box_office = BoxOfficeRecord.objects.filter(
                record_date=today
            ).aggregate(
                total=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
            )['total']

        # 本周冠军
        weekly_stats = BoxOfficeRecord.objects.filter(
            record_date__gte=week_start
        ).values('movie_id', 'movie__title').annotate(
            weekly_box_office=Sum('daily_box_office')
        ).order_by('-weekly_box_office')[:1]

        champion = None
        if weekly_stats:
            champion = {
                'movie_id': weekly_stats[0]['movie_id'],
                'movie_title': weekly_stats[0]['movie__title'],
                'weekly_box_office': weekly_stats[0]['weekly_box_office']
            }

        # 总数统计
        total_movies = Movie.objects.only('id').count()
        total_cinemas = Cinema.objects.only('id').count()

        response_data = {
            'code': 0,
            'data': {
                'today_box_office': today_box_office,
                'week_champion': champion,
                'total_movies': total_movies,
                'total_cinemas': total_cinemas
            }
        }

        # 缓存5分钟
        cache.set(cache_key, response_data, 300)

        return Response(response_data)


class OverviewStatsView(APIView):
    """
    管理端概览统计数据视图

    提供 Dashboard 所需的综合统计数据。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取管理端概览统计',
        description='获取管理端 Dashboard 所需的综合统计数据',
        responses={200: {'type': 'object'}},
        tags=['数据可视化']
    )
    def get(self, request):
        from accounts.models import User

        # 1. 影片总数
        total_movies = Movie.objects.count()

        # 2. 影院总数
        total_cinemas = Cinema.objects.count()

        # 3. 累计票房（从Movie表获取）
        total_box_office = Movie.objects.aggregate(
            total=Coalesce(Sum('box_office_total'), Value(Decimal('0'), output_field=DecimalField()))
        )['total'] * 10000  # 转换万元到元

        # 4. 用户总数
        total_users = User.objects.count()

        # 5. 最近5条票房记录
        recent_records = BoxOfficeRecord.objects.select_related(
            'movie', 'cinema'
        ).order_by('-record_date', '-id')[:5]

        recent_data = []
        for record in recent_records:
            recent_data.append({
                'id': record.id,
                'date': record.record_date,
                'movie_title': record.movie.title if record.movie else None,
                'cinema_name': record.cinema.name if record.cinema else None,
                'box_office': record.daily_box_office,
                'show_times': record.screening_count,
                'viewer_count': record.audience_count
            })

        return Response({
            'code': 0,
            'data': {
                'total_movies': total_movies,
                'total_cinemas': total_cinemas,
                'total_box_office': total_box_office,
                'total_users': total_users,
                'recent_records': recent_data
            }
        })
