from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Count, Q
from django.db.models.functions import ExtractYear
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


class DashboardCategoryDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = list(
            Category.objects.annotate(
            heritage_count=Count("heritage_items", distinct=True),
            ).order_by("-heritage_count", "name")
        )

        total_heritage = HeritageItem.objects.count()
        if total_heritage == 0:
            data = [
                {
                    "category_name": category.name,
                    "heritage_count": category.heritage_count,
                    "percentage": 0.0,
                }
                for category in categories
            ]
            return success_response(data=data, message="获取成功")

        total_decimal = Decimal(total_heritage)
        percentages = []
        rounded_sum = Decimal("0.00")
        last_non_zero_index = None

        for index, category in enumerate(categories):
            count = category.heritage_count
            if count > 0:
                last_non_zero_index = index
            percentage = (
                Decimal(count) * Decimal("100") / total_decimal
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            percentages.append(percentage)
            rounded_sum += percentage

        if last_non_zero_index is not None and rounded_sum != Decimal("100.00"):
            percentages[last_non_zero_index] += Decimal("100.00") - rounded_sum

        data = [
            {
                "category_name": category.name,
                "heritage_count": category.heritage_count,
                "percentage": float(percentages[index]),
            }
            for index, category in enumerate(categories)
        ]

        return success_response(data=data, message="获取成功")


class DashboardCountryRankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit_param = (request.query_params.get("limit") or "").strip()
        limit = 20
        if limit_param:
            try:
                limit = int(limit_param)
            except ValueError:
                limit = 20
        if limit <= 0:
            limit = 20
        limit = min(limit, 100)

        regions = list(
            Region.objects.annotate(
                heritage_count=Count("heritage_items", distinct=True),
            )
            .filter(heritage_count__gt=0)
            .order_by("-heritage_count", "country_name")[:limit]
        )

        data = [
            {
                "rank": index + 1,
                "country_name": region.country_name,
                "heritage_count": region.heritage_count,
            }
            for index, region in enumerate(regions)
        ]

        return success_response(data=data, message="获取成功")


class DashboardTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 使用原生 MySQL YEAR() 函数，避免时区问题
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    YEAR(created_at) as year,
                    COUNT(*) as count
                FROM heritage_items
                WHERE created_at IS NOT NULL
                GROUP BY YEAR(created_at)
                ORDER BY year
            """)
            results = cursor.fetchall()

        data = [
            {
                "year": row[0],
                "count": row[1],
            }
            for row in results
        ]

        return success_response(data=data, message="获取成功")


class DashboardLevelDistributionView(APIView):
    """
    保护级别分布
    GET /dashboard/level-distribution/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.heritage.models import HeritageItem

        data = []
        for level_value, level_name in HeritageItem.LEVEL_CHOICES:
            count = HeritageItem.objects.filter(level=level_value).count()
            data.append({
                'level': level_value,
                'level_name': level_name,
                'count': count
            })

        return success_response(data=data, message="获取成功")
