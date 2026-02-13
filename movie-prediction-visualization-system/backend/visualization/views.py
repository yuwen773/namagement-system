from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.db.models import Sum, Count, Avg
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Value
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from boxoffice.models import BoxOfficeRecord
from movies.models import Movie
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
        description=(
            '获取历史累计票房最高的10部电影列表，按票房总额降序排列。'
            '仅包含有票房记录的影片（box_office_total > 0）。'
            '适用于首页排行榜展示、热门影片分析等场景。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'description': '影片ID'},
                                'title': {'type': 'string', 'description': '影片名称'},
                                'box_office_total': {'type': 'number', 'description': '总票房（元）'},
                                'release_date': {'type': 'string', 'format': 'date', 'description': '上映日期'}
                            }
                        }
                    }
                }
            }
        },
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
    用于实时监控当日市场表现，展示大盘走势。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取今日大盘票房统计',
        description=(
            '获取当日全国票房统计数据，包括总票房（元）、总放映场次、总观影人次。'
            '数据来源于当日所有票房记录的汇总，适用于首页大盘展示、实时监控等场景。'
            '若无当日数据，则返回值为0。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'date': {'type': 'string', 'format': 'date', 'description': '统计日期'},
                            'total_box_office': {'type': 'number', 'description': '总票房（元）'},
                            'total_screening_count': {'type': 'integer', 'description': '总放映场次'},
                            'total_audience_count': {'type': 'integer', 'description': '总观影人次'}
                        }
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        """获取今日票房统计"""
        today = timezone.now().date()
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
    用于展示周榜冠军，支持热门影片推荐。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取本周票房冠军',
        description=(
            '获取本周（周一至当前日期）累计票房最高的影片信息。'
            '按影片汇总本周所有票房记录，返回票房冠军的影片ID、名称和周票房总额。'
            '若本周暂无票房记录，则返回null。适用于首页冠军展示、热门推荐等场景。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'oneOf': [
                            {
                                'type': 'object',
                                'properties': {
                                    'movie_id': {'type': 'integer', 'description': '影片ID'},
                                    'movie_title': {'type': 'string', 'description': '影片名称'},
                                    'weekly_box_office': {'type': 'number', 'description': '周票房（元）'}
                                }
                            },
                            {'type': 'null'}
                        ]
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        """获取本周票房最高的电影"""
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())

        # 按影片聚合周票房
        weekly_stats = BoxOfficeRecord.objects.filter(
            record_date__gte=week_start
        ).values('movie_id', 'movie__title').annotate(
            weekly_box_office=Sum('daily_box_office')
        ).order_by('-weekly_box_office')[:1]

        if weekly_stats:
            data = {
                'movie_id': weekly_stats[0]['movie_id'],
                'movie_title': weekly_stats[0]['movie__title'],
                'weekly_box_office': weekly_stats[0]['weekly_box_office']
            }
        else:
            data = None

        return Response({
            'code': 0,
            'data': data
        })


class TypeBoxOfficeView(APIView):
    """
    按类型统计票房占比视图

    提供各影片类型的票房分布数据和占比信息。
    用于饼图、柱状图展示不同类型影片的市场表现。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取各类型票房占比',
        description=(
            '获取各影片类型的票房总额及占比数据。按类型汇总所有票房记录，'
            '计算每种类型的票房占总票房的百分比，按票房降序排列。'
            '适用于类型分布饼图、市场分析柱状图等可视化场景。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type_id': {'type': 'integer', 'description': '类型ID'},
                                'type_name': {'type': 'string', 'description': '类型名称'},
                                'box_office': {'type': 'number', 'description': '类型票房（元）'},
                                'percentage': {'type': 'number', 'description': '占比（%）'}
                            }
                        }
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        """获取各类型票房占比"""
        # 计算总票房
        total = BoxOfficeRecord.objects.aggregate(
            total=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
        )['total'] or Decimal('1')

        # 按类型聚合
        type_stats = BoxOfficeRecord.objects.filter(
            movie__type__isnull=False
        ).values(
            'movie__type_id',
            'movie__type__name'
        ).annotate(
            box_office=Sum('daily_box_office')
        ).order_by('-box_office')

        result = []
        for stat in type_stats:
            percentage = float(stat['box_office']) / float(total) * 100 if total > 0 else 0
            result.append({
                'type_id': stat['movie__type_id'],
                'type_name': stat['movie__type__name'],
                'box_office': stat['box_office'],
                'percentage': round(percentage, 2)
            })

        return Response({
            'code': 0,
            'data': result
        })


class RegionBoxOfficeView(APIView):
    """
    按地域统计票房分布视图

    提供各省份的票房分布数据和影院数量统计。
    用于地域票房地图展示、区域市场分析。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取各省份票房分布',
        description=(
            '获取各省份的票房总额及影院数量统计。按省份汇总该省所有影院的票房记录，'
            '返回票房总额和影院数量，按票房降序排列。'
            '适用于地域票房地图、区域排行柱状图等可视化场景。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'region_id': {'type': 'integer', 'description': '省份ID'},
                                'region_name': {'type': 'string', 'description': '省份名称'},
                                'box_office': {'type': 'number', 'description': '省份票房（元）'},
                                'cinema_count': {'type': 'integer', 'description': '影院数量'}
                            }
                        }
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        """获取各省份票房分布"""
        # 获取所有省份
        provinces = Region.objects.filter(
            level='PROVINCE'
        ).prefetch_related('cinemas')

        result = []
        for province in provinces:
            # 计算该省份所有影院的票房
            box_office = BoxOfficeRecord.objects.filter(
                cinema__region=province
            ).aggregate(
                total=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
            )['total']

            result.append({
                'region_id': province.id,
                'region_name': province.name,
                'box_office': box_office,
                'cinema_count': province.cinemas.count()
            })

        # 按票房降序排序
        result.sort(key=lambda x: float(x['box_office']), reverse=True)

        return Response({
            'code': 0,
            'data': result
        })


class TimeSeriesView(APIView):
    """
    票房时间走势数据视图

    提供指定时间范围内的票房走势数据，支持按日/周/月聚合。
    用于折线图展示票房趋势，分析市场变化规律。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取票房时间走势',
        description=(
            '获取指定时间范围内的票房走势数据，支持按日/周/月三种聚合方式。'
            '返回每日/每周/每月的票房总额、放映场次和观影人次，适用于折线图展示。'
            '可用于分析票房趋势、周期性规律、季节性变化等。'
        ),
        parameters=[
            OpenApiParameter(
                name='period',
                type=OpenApiTypes.STR,
                description='聚合周期：day（按日）、week（按周）、month（按月）',
                default='day',
                enum=['day', 'week', 'month']
            ),
            OpenApiParameter(
                name='days',
                type=OpenApiTypes.INT,
                description='统计天数（最近N天），默认30天',
                default=30
            )
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'date': {'type': 'string', 'format': 'date', 'description': '日期（按日时）'},
                                'week': {'type': 'integer', 'description': '周数（按周时）'},
                                'year': {'type': 'integer', 'description': '年份（按月时）'},
                                'month': {'type': 'integer', 'description': '月份（按月时）'},
                                'total_box_office': {'type': 'number', 'description': '票房总额（元）'},
                                'total_screening_count': {'type': 'integer', 'description': '总场次'},
                                'total_audience_count': {'type': 'integer', 'description': '总人次'}
                            }
                        }
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': -1},
                    'message': {'type': 'string', 'example': '无效的时间周期参数，支持 day/week/month'}
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        """
        获取票房时间走势
        支持按日/周/月聚合
        """
        period = request.query_params.get('period', 'day')
        days = int(request.query_params.get('days', 30))

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        queryset = BoxOfficeRecord.objects.filter(
            record_date__gte=start_date,
            record_date__lte=end_date
        )

        if period == 'day':
            # 按日聚合
            daily_stats = queryset.values('record_date').annotate(
                total_box_office=Sum('daily_box_office'),
                total_screening_count=Sum('screening_count'),
                total_audience_count=Sum('audience_count')
            ).order_by('record_date')

            result = [{
                'date': stat['record_date'],
                'total_box_office': stat['total_box_office'],
                'total_screening_count': stat['total_screening_count'],
                'total_audience_count': stat['total_audience_count']
            } for stat in daily_stats]

        elif period == 'week':
            # 按周聚合
            from django.db.models.functions import ExtractWeek
            weekly_stats = queryset.annotate(
                week=ExtractWeek('record_date')
            ).values('week').annotate(
                total_box_office=Sum('daily_box_office'),
                total_screening_count=Sum('screening_count'),
                total_audience_count=Sum('audience_count')
            ).order_by('week')

            result = [{
                'week': stat['week'],
                'total_box_office': stat['total_box_office'],
                'total_screening_count': stat['total_screening_count'],
                'total_audience_count': stat['total_audience_count']
            } for stat in weekly_stats]

        elif period == 'month':
            # 按月聚合
            from django.db.models.functions import ExtractMonth, ExtractYear
            monthly_stats = queryset.annotate(
                year=ExtractYear('record_date'),
                month=ExtractMonth('record_date')
            ).values('year', 'month').annotate(
                total_box_office=Sum('daily_box_office'),
                total_screening_count=Sum('screening_count'),
                total_audience_count=Sum('audience_count')
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

        return Response({
            'code': 0,
            'data': result
        })


class DashboardView(APIView):
    """
    仪表盘概览数据视图

    提供仪表盘所需的综合统计数据，包括今日票房、本周冠军、影片总数、影院总数。
    用于首页仪表盘展示，提供系统整体运行状态的一览视图。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取仪表盘概览数据',
        description=(
            '获取仪表盘所需的综合统计数据，包括：'
            '1. 今日大盘票房总额；'
            '2. 本周票房冠军影片信息；'
            '3. 系统影片总数；'
            '4. 系统影院总数。'
            '适用于首页仪表盘展示，提供系统整体运行状态的快速概览。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'today_box_office': {
                                'type': 'number',
                                'description': '今日大盘票房（元）'
                            },
                            'week_champion': {
                                'oneOf': [
                                    {
                                        'type': 'object',
                                        'properties': {
                                            'movie_id': {'type': 'integer', 'description': '影片ID'},
                                            'movie_title': {'type': 'string', 'description': '影片名称'},
                                            'weekly_box_office': {'type': 'number', 'description': '周票房（元）'}
                                        }
                                    },
                                    {'type': 'null'}
                                ]
                            },
                            'total_movies': {'type': 'integer', 'description': '影片总数'},
                            'total_cinemas': {'type': 'integer', 'description': '影院总数'}
                        }
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        """获取仪表盘所需的所有统计数据"""
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())

        # 今日票房
        today_stats = BoxOfficeRecord.objects.filter(
            record_date=today
        ).aggregate(
            total=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
        )

        # 本周冠军
        weekly_stats = BoxOfficeRecord.objects.filter(
            record_date__gte=week_start
        ).values('movie_id', 'movie__title').annotate(
            weekly_box_office=Sum('daily_box_office')
        ).order_by('-weekly_box_office').first()

        champion = None
        if weekly_stats:
            champion = {
                'movie_id': weekly_stats['movie_id'],
                'movie_title': weekly_stats['movie__title'],
                'weekly_box_office': weekly_stats['weekly_box_office']
            }

        # 总数统计
        total_movies = Movie.objects.count()
        total_cinemas = Cinema.objects.count()

        return Response({
            'code': 0,
            'data': {
                'today_box_office': today_stats['total'],
                'week_champion': champion,
                'total_movies': total_movies,
                'total_cinemas': total_cinemas
            }
        })


class OverviewStatsView(APIView):
    """
    管理端概览统计数据视图

    提供 Dashboard 所需的综合统计数据，包括：
    - 影片总数
    - 影院总数
    - 历史累计票房
    - 注册用户数
    - 最近5条票房记录

    一次请求获取全部数据，优化前端性能。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取管理端概览统计',
        description=(
            '获取管理端 Dashboard 所需的综合统计数据，包括：'
            '影片总数、影院总数、累计票房、用户总数、最近5条票房记录。'
            '一次请求获取全部数据，避免多次接口调用。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'total_movies': {'type': 'integer', 'description': '影片总数'},
                            'total_cinemas': {'type': 'integer', 'description': '影院总数'},
                            'total_box_office': {'type': 'number', 'description': '累计票房（元）'},
                            'total_users': {'type': 'integer', 'description': '用户总数'},
                            'recent_records': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'date': {'type': 'string', 'format': 'date'},
                                        'movie_title': {'type': 'string'},
                                        'cinema_name': {'type': 'string'},
                                        'box_office': {'type': 'number'},
                                        'show_times': {'type': 'integer'},
                                        'viewer_count': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        from accounts.models import User

        # 1. 影片总数
        total_movies = Movie.objects.count()

        # 2. 影院总数
        total_cinemas = Cinema.objects.count()

        # 3. 累计票房（后端直接计算，避免传输大量数据）
        total_box_office = BoxOfficeRecord.objects.aggregate(
            total=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
        )['total']

        # 4. 用户总数
        total_users = User.objects.count()

        # 5. 最近5条票房记录
        recent_records = BoxOfficeRecord.objects.select_related(
            'movie', 'cinema'
        ).order_by('-record_date')[:5]

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
