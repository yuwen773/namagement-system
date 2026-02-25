from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.inheritors.models import Inheritor
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
