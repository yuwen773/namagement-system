import django_filters
from django.db.models import Q
from .models import BoxOfficeRecord


class BoxOfficeRecordFilter(django_filters.FilterSet):
    """
    票房记录过滤器
    支持按日期范围、影片、影院、地域进行过滤
    """
    # 日期范围过滤
    start_date = django_filters.DateFilter(
        field_name='record_date',
        lookup_expr='gte',
        help_text='开始日期 (record_date >= start_date)'
    )
    end_date = django_filters.DateFilter(
        field_name='record_date',
        lookup_expr='lte',
        help_text='结束日期 (record_date <= end_date)'
    )

    # 影片过滤
    movie_id = django_filters.NumberFilter(
        field_name='movie_id',
        help_text='影片ID'
    )
    movie_title = django_filters.CharFilter(
        field_name='movie__title',
        lookup_expr='icontains',
        help_text='影片名称（模糊搜索）'
    )

    # 影院过滤
    cinema_id = django_filters.NumberFilter(
        field_name='cinema_id',
        help_text='影院ID'
    )
    cinema_name = django_filters.CharFilter(
        field_name='cinema__name',
        lookup_expr='icontains',
        help_text='影院名称（模糊搜索）'
    )

    # 地域过滤
    region_id = django_filters.NumberFilter(
        field_name='cinema__region_id',
        help_text='地域ID'
    )
    region_name = django_filters.CharFilter(
        field_name='cinema__region__name',
        lookup_expr='icontains',
        help_text='地域名称（模糊搜索）'
    )

    # 票房金额范围过滤
    min_box_office = django_filters.NumberFilter(
        field_name='daily_box_office',
        lookup_expr='gte',
        help_text='最低票房'
    )
    max_box_office = django_filters.NumberFilter(
        field_name='daily_box_office',
        lookup_expr='lte',
        help_text='最高票房'
    )

    class Meta:
        model = BoxOfficeRecord
        fields = [
            'movie_id',
            'cinema_id',
            'region_id',
            'record_date',
        ]

    @property
    def qs(self):
        """返回过滤后的查询集"""
        queryset = super().qs
        # 添加 select_related 优化查询
        return queryset.select_related('movie', 'cinema', 'cinema__region')
