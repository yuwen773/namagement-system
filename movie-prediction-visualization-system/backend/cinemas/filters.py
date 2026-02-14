import django_filters
from django.db.models import Q
from .models import Region, Cinema


class RegionFilter(django_filters.FilterSet):
    """
    地域过滤器
    支持按层级、父级、名称搜索筛选
    """
    level = django_filters.ChoiceFilter(
        field_name='level',
        choices=Region.LEVEL_CHOICES,
        label='层级'
    )
    parent_id = django_filters.NumberFilter(
        field_name='parent_id',
        label='父级地域ID'
    )
    has_children = django_filters.BooleanFilter(
        field_name='children',
        lookup_expr='exists',
        label='是否有子地域'
    )
    search = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='名称搜索'
    )

    class Meta:
        model = Region
        fields = ['level', 'parent_id', 'has_children', 'search']


class CinemaFilter(django_filters.FilterSet):
    """
    影院过滤器
    支持按地域、名称、状态筛选
    """
    region_id = django_filters.NumberFilter(
        field_name='region_id',
        label='地域ID'
    )
    province_id = django_filters.NumberFilter(
        method='filter_province',
        label='省份ID'
    )
    city_id = django_filters.NumberFilter(
        field_name='region__parent_id',
        label='城市ID（通过父地域筛选）'
    )
    search = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='影院名称搜索'
    )
    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        label='是否营业'
    )
    min_screen_count = django_filters.NumberFilter(
        field_name='screen_count',
        lookup_expr='gte',
        label='最小屏幕数量'
    )
    max_screen_count = django_filters.NumberFilter(
        field_name='screen_count',
        lookup_expr='lte',
        label='最大屏幕数量'
    )
    min_seats_count = django_filters.NumberFilter(
        field_name='seats_count',
        lookup_expr='gte',
        label='最小座位数量'
    )
    max_seats_count = django_filters.NumberFilter(
        field_name='seats_count',
        lookup_expr='lte',
        label='最大座位数量'
    )
    has_region = django_filters.BooleanFilter(
        method='filter_has_region',
        label='是否有地域关联'
    )

    class Meta:
        model = Cinema
        fields = [
            'region_id', 'province_id', 'city_id', 'search',
            'is_active', 'min_screen_count', 'max_screen_count',
            'min_seats_count', 'max_seats_count'
        ]

    def filter_province(self, queryset, name, value):
        """
        按省份筛选 - 包含该省下所有城市的影院
        """
        return queryset.filter(
            Q(region__parent_id=value) | Q(region__parent__parent_id=value)
        )

    def filter_has_region(self, queryset, name, value):
        """
        筛选是否有地域关联
        """
        if value:
            return queryset.filter(region__isnull=False)
        return queryset.filter(region__isnull=True)
