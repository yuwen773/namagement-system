import django_filters
from .models import MovieType, Movie


class MovieTypeFilter(django_filters.FilterSet):
    """影片类型过滤器"""

    class Meta:
        model = MovieType
        fields = {
            'name': ['exact', 'icontains'],
            'created_at': ['gte', 'lte'],
        }


class MovieFilter(django_filters.FilterSet):
    """影片过滤器"""

    class Meta:
        model = Movie
        fields = {
            'title': ['exact', 'icontains'],
            'director': ['icontains'],
            'type': ['exact'],
            'status': ['exact'],
            'release_date': ['gte', 'lte', 'exact'],
            'box_office_total': ['gte', 'lte'],
        }
