from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.inheritors.models import Inheritor
from apps.regions.models import Region
from utils.response import success_response


class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "heritage_count": HeritageItem.objects.count(),
            "inheritor_count": Inheritor.objects.count(),
            "category_count": Category.objects.count(),
            "country_count": HeritageItem.objects.values("region_id").distinct().count(),
        }
        return success_response(data=data, message="获取成功")


class DashboardMapDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = (
            request.query_params.get("category")
            or request.query_params.get("category_id")
            or ""
        ).strip()

        heritage_filter = Q()
        inheritor_filter = Q()
        if category:
            heritage_filter = Q(heritage_items__category_id=category)
            inheritor_filter = Q(inheritors__heritage_item__category_id=category)

        queryset = (
            Region.objects.annotate(
                heritage_count=Count(
                    "heritage_items",
                    filter=heritage_filter,
                    distinct=True,
                ),
                inheritor_count=Count(
                    "inheritors",
                    filter=inheritor_filter,
                    distinct=True,
                ),
            )
            .filter(Q(heritage_count__gt=0) | Q(inheritor_count__gt=0))
            .order_by("country_name")
        )

        data = [
            {
                "country_code": region.country_code,
                "country_name": region.country_name,
                "longitude": float(region.longitude),
                "latitude": float(region.latitude),
                "heritage_count": region.heritage_count,
                "inheritor_count": region.inheritor_count,
            }
            for region in queryset
        ]

        return success_response(data=data, message="获取成功")
