from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.inheritors.models import Inheritor
from apps.regions.models import Region


class DashboardOverviewViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="dashboard-user",
            password="password123",
        )
        self.url = "/api/v1/dashboard/overview/"

    def test_overview_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_overview_returns_expected_counts(self):
        self.client.force_authenticate(user=self.user)

        category_1 = Category.objects.create(
            name="Traditional Music",
            code="CAT-MUSIC",
            level=Category.LEVEL_NATIONAL,
        )
        category_2 = Category.objects.create(
            name="Traditional Dance",
            code="CAT-DANCE",
            level=Category.LEVEL_PROVINCIAL,
        )

        region_cn = Region.objects.create(
            country_code="CN",
            country_name="China",
            latitude="35.861700",
            longitude="104.195400",
            continent="Asia",
        )
        region_jp = Region.objects.create(
            country_code="JP",
            country_name="Japan",
            latitude="36.204800",
            longitude="138.252900",
            continent="Asia",
        )
        Region.objects.create(
            country_code="US",
            country_name="United States",
            latitude="37.090200",
            longitude="-95.712900",
            continent="North America",
        )

        heritage_1 = HeritageItem.objects.create(
            name="Guqin Art",
            category=category_1,
            level=HeritageItem.LEVEL_NATIONAL,
            region=region_cn,
        )
        heritage_2 = HeritageItem.objects.create(
            name="Noh Theatre",
            category=category_2,
            level=HeritageItem.LEVEL_PROVINCIAL,
            region=region_jp,
        )
        HeritageItem.objects.create(
            name="Kunqu Opera",
            category=category_1,
            level=HeritageItem.LEVEL_CITY_COUNTY,
            region=region_cn,
        )

        Inheritor.objects.create(name="Li Hua", heritage_item=heritage_1, region=region_cn)
        Inheritor.objects.create(name="Chen Gang", heritage_item=heritage_1, region=region_cn)
        Inheritor.objects.create(name="Sato Ken", heritage_item=heritage_2, region=region_jp)
        Inheritor.objects.create(name="Yamada Aoi", heritage_item=heritage_2, region=region_jp)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["message"], "获取成功")
        self.assertEqual(
            response.data["data"],
            {
                "heritage_count": 3,
                "inheritor_count": 4,
                "category_count": 2,
                "country_count": 2,
            },
        )
