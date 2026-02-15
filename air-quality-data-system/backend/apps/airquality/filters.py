import django_filters

from .models import AirQualityData


class HistoricalDataFilter(django_filters.FilterSet):
    city_code = django_filters.CharFilter(field_name="station__city__code", lookup_expr="exact")
    station_code = django_filters.CharFilter(field_name="station__code", lookup_expr="exact")
    start_date = django_filters.DateFilter(field_name="monitor_time", lookup_expr="date__gte")
    end_date = django_filters.DateFilter(field_name="monitor_time", lookup_expr="date__lte")

    class Meta:
        model = AirQualityData
        fields = ["city_code", "station_code", "start_date", "end_date"]
