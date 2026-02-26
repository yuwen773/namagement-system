from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.inheritors.models import Inheritor
from apps.regions.models import Region

User = get_user_model()


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


class DashboardMapDistributionViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="dashboard-map-user",
            password="password123",
        )
        self.url = "/api/v1/dashboard/map-distribution/"

        self.category_music = Category.objects.create(
            name="Traditional Music",
            code="CAT-MAP-MUSIC",
            level=Category.LEVEL_NATIONAL,
        )
        self.category_dance = Category.objects.create(
            name="Traditional Dance",
            code="CAT-MAP-DANCE",
            level=Category.LEVEL_PROVINCIAL,
        )

        self.region_cn = Region.objects.create(
            country_code="CN",
            country_name="China",
            latitude="35.861700",
            longitude="104.195400",
            continent="Asia",
        )
        self.region_jp = Region.objects.create(
            country_code="JP",
            country_name="Japan",
            latitude="36.204800",
            longitude="138.252900",
            continent="Asia",
        )
        self.region_us = Region.objects.create(
            country_code="US",
            country_name="United States",
            latitude="37.090200",
            longitude="-95.712900",
            continent="North America",
        )
        Region.objects.create(
            country_code="FR",
            country_name="France",
            latitude="46.227600",
            longitude="2.213700",
            continent="Europe",
        )

        self.heritage_guqin = HeritageItem.objects.create(
            name="Guqin Art",
            category=self.category_music,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region_cn,
        )
        self.heritage_kunqu = HeritageItem.objects.create(
            name="Kunqu Opera",
            category=self.category_music,
            level=HeritageItem.LEVEL_CITY_COUNTY,
            region=self.region_cn,
        )
        self.heritage_noh = HeritageItem.objects.create(
            name="Noh Theatre",
            category=self.category_dance,
            level=HeritageItem.LEVEL_PROVINCIAL,
            region=self.region_jp,
        )

        Inheritor.objects.create(
            name="Li Hua",
            heritage_item=self.heritage_guqin,
            region=self.region_cn,
        )
        Inheritor.objects.create(
            name="Wang Lei",
            heritage_item=self.heritage_kunqu,
            region=self.region_cn,
        )
        Inheritor.objects.create(
            name="Sato Ken",
            heritage_item=self.heritage_noh,
            region=self.region_jp,
        )
        Inheritor.objects.create(
            name="Amy Walker",
            heritage_item=self.heritage_guqin,
            region=self.region_us,
        )

    def test_map_distribution_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_map_distribution_returns_counts_and_coordinates(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["message"], "获取成功")

        data_by_code = {
            item["country_code"]: item
            for item in response.data["data"]
        }
        self.assertEqual(set(data_by_code.keys()), {"CN", "JP", "US"})

        self.assertEqual(data_by_code["CN"]["country_name"], "China")
        self.assertAlmostEqual(data_by_code["CN"]["longitude"], 104.1954, places=4)
        self.assertAlmostEqual(data_by_code["CN"]["latitude"], 35.8617, places=4)
        self.assertEqual(data_by_code["CN"]["heritage_count"], 2)
        self.assertEqual(data_by_code["CN"]["inheritor_count"], 2)

        self.assertEqual(data_by_code["JP"]["heritage_count"], 1)
        self.assertEqual(data_by_code["JP"]["inheritor_count"], 1)
        self.assertEqual(data_by_code["US"]["heritage_count"], 0)
        self.assertEqual(data_by_code["US"]["inheritor_count"], 1)

    def test_map_distribution_supports_category_filter(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.url,
            {"category": self.category_music.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)

        data_by_code = {
            item["country_code"]: item
            for item in response.data["data"]
        }
        self.assertEqual(set(data_by_code.keys()), {"CN", "US"})
        self.assertEqual(data_by_code["CN"]["heritage_count"], 2)
        self.assertEqual(data_by_code["CN"]["inheritor_count"], 2)
        self.assertEqual(data_by_code["US"]["heritage_count"], 0)
        self.assertEqual(data_by_code["US"]["inheritor_count"], 1)


class DashboardCategoryDistributionViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="dashboard-category-user",
            password="password123",
        )
        self.url = "/api/v1/dashboard/category-distribution/"

        self.region_cn = Region.objects.create(
            country_code="CN",
            country_name="China",
            latitude="35.861700",
            longitude="104.195400",
            continent="Asia",
        )
        self.category_music = Category.objects.create(
            name="Traditional Music",
            code="CAT-DIST-MUSIC",
            level=Category.LEVEL_NATIONAL,
        )
        self.category_dance = Category.objects.create(
            name="Traditional Dance",
            code="CAT-DIST-DANCE",
            level=Category.LEVEL_PROVINCIAL,
        )
        self.category_craft = Category.objects.create(
            name="Traditional Craft",
            code="CAT-DIST-CRAFT",
            level=Category.LEVEL_CITY_COUNTY,
        )

        HeritageItem.objects.create(
            name="Guqin Art",
            category=self.category_music,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region_cn,
        )
        HeritageItem.objects.create(
            name="Kunqu Opera",
            category=self.category_music,
            level=HeritageItem.LEVEL_PROVINCIAL,
            region=self.region_cn,
        )
        HeritageItem.objects.create(
            name="Ancient Ballad",
            category=self.category_music,
            level=HeritageItem.LEVEL_CITY_COUNTY,
            region=self.region_cn,
        )
        HeritageItem.objects.create(
            name="Fan Dance",
            category=self.category_dance,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region_cn,
        )

    def test_category_distribution_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_category_distribution_returns_all_categories_sorted_with_percentage(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["message"], "获取成功")

        data = response.data["data"]
        self.assertEqual(
            [item["category_name"] for item in data],
            [
                "Traditional Music",
                "Traditional Dance",
                "Traditional Craft",
            ],
        )
        self.assertEqual([item["heritage_count"] for item in data], [3, 1, 0])
        self.assertAlmostEqual(sum(item["percentage"] for item in data), 100.0, places=2)
        self.assertEqual([item["percentage"] for item in data], [75.0, 25.0, 0.0])


class DashboardCountryRankingViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="dashboard-ranking-user",
            password="password123",
        )
        self.url = "/api/v1/dashboard/country-ranking/"
        self.category = Category.objects.create(
            name="Traditional Performance",
            code="CAT-RANKING",
            level=Category.LEVEL_NATIONAL,
        )

    def _create_country_with_heritage(self, code, name, heritage_count, index):
        region = Region.objects.create(
            country_code=code,
            country_name=name,
            latitude=f"{30 + index}.000000",
            longitude=f"{100 + index}.000000",
            continent="Test",
        )
        for item_index in range(heritage_count):
            HeritageItem.objects.create(
                name=f"{name} Heritage {item_index}",
                category=self.category,
                level=HeritageItem.LEVEL_NATIONAL,
                region=region,
            )
        return region

    def test_country_ranking_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_country_ranking_defaults_to_top_20(self):
        self.client.force_authenticate(user=self.user)

        for index in range(1, 23):
            self._create_country_with_heritage(
                code=f"C{index:02d}",
                name=f"Country {index:02d}",
                heritage_count=1,
                index=index,
            )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(len(response.data["data"]), 20)
        self.assertEqual(
            [item["rank"] for item in response.data["data"]],
            list(range(1, 21)),
        )

    def test_country_ranking_supports_limit_and_desc_order(self):
        self.client.force_authenticate(user=self.user)

        self._create_country_with_heritage("CN", "China", 5, 1)
        self._create_country_with_heritage("JP", "Japan", 3, 2)
        self._create_country_with_heritage("US", "United States", 1, 3)
        self._create_country_with_heritage("FR", "France", 0, 4)

        response = self.client.get(self.url, {"limit": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(
            response.data["data"],
            [
                {
                    "rank": 1,
                    "country_name": "China",
                    "heritage_count": 5,
                },
                {
                    "rank": 2,
                    "country_name": "Japan",
                    "heritage_count": 3,
                },
            ],
        )


class DashboardTrendViewTests(APITestCase):
    """时间趋势 API 测试"""

    def setUp(self):
        """创建测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # 创建测试用类别和地区
        self.category = Category.objects.create(
            name='测试类别',
            code='TEST',
            level='national'
        )
        self.region = Region.objects.create(
            country_code='CN',
            country_name='China',
            latitude='39.9',
            longitude='116.4'
        )

        # 创建不同年份的非遗项目
        # Note: created_at has auto_now_add=True, so we need to create first, then update
        item_2008 = HeritageItem.objects.create(
            name='2008年项目',
            category=self.category,
            region=self.region,
            level='national',
        )
        item_2008.created_at = make_aware(datetime(2008, 6, 15))
        item_2008.save()

        item_2010_1 = HeritageItem.objects.create(
            name='2010年项目',
            category=self.category,
            region=self.region,
            level='national',
        )
        item_2010_1.created_at = make_aware(datetime(2010, 3, 20))
        item_2010_1.save()

        item_2010_2 = HeritageItem.objects.create(
            name='2010年项目2',
            category=self.category,
            region=self.region,
            level='national',
        )
        item_2010_2.created_at = make_aware(datetime(2010, 8, 10))
        item_2010_2.save()

    def test_trend_returns_yearly_counts(self):
        """测试返回按年份统计的数据"""
        # Debug: Check what's actually in the database
        items = HeritageItem.objects.all()
        print(f"DEBUG: Total HeritageItem count: {items.count()}")
        for item in items:
            print(f"DEBUG: Item: {item.name}, created_at: {item.created_at}")

        response = self.client.get('/api/v1/dashboard/trend/')
        self.assertEqual(response.status_code, 200)
        data = response.data['data']
        print(f"DEBUG: data = {data}")
        print(f"DEBUG: len(data) = {len(data)}")
        self.assertEqual(len(data), 2)

        # 验证数据结构
        self.assertIn('year', data[0])
        self.assertIn('count', data[0])

    def test_trend_ordered_by_year(self):
        """测试数据按年份排序"""
        response = self.client.get('/api/v1/dashboard/trend/')
        data = response.data['data']
        years = [item['year'] for item in data]
        self.assertEqual(years, sorted(years))

    def test_trend_requires_auth(self):
        """测试需要认证"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/dashboard/trend/')
        self.assertEqual(response.status_code, 401)


class DashboardLevelDistributionViewTests(APITestCase):
    """保护级别分布 API 测试"""

    def setUp(self):
        """创建测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name='测试类别',
            code='TEST',
            level='national'
        )
        self.region = Region.objects.create(
            country_code='CN',
            country_name='China',
            latitude=39.9,
            longitude=116.4
        )

        # 创建不同级别的项目
        HeritageItem.objects.create(
            name='国家级项目1',
            category=self.category,
            region=self.region,
            level='national'
        )
        HeritageItem.objects.create(
            name='国家级项目2',
            category=self.category,
            region=self.region,
            level='national'
        )
        HeritageItem.objects.create(
            name='省级项目',
            category=self.category,
            region=self.region,
            level='provincial'
        )
        HeritageItem.objects.create(
            name='县级项目',
            category=self.category,
            region=self.region,
            level='city_county'
        )

    def test_level_distribution_returns_all_levels(self):
        """测试返回所有保护级别"""
        response = self.client.get('/api/v1/dashboard/level-distribution/')
        self.assertEqual(response.status_code, 200)
        data = response.data['data']
        self.assertEqual(len(data), 3)

    def test_level_distribution_counts_are_correct(self):
        """测试统计数据正确"""
        response = self.client.get('/api/v1/dashboard/level-distribution/')
        data = response.data['data']

        level_counts = {item['level']: item['count'] for item in data}
        self.assertEqual(level_counts['national'], 2)
        self.assertEqual(level_counts['provincial'], 1)
        self.assertEqual(level_counts['city_county'], 1)

    def test_level_distribution_has_level_name(self):
        """测试返回级别中文名"""
        response = self.client.get('/api/v1/dashboard/level-distribution/')
        data = response.data['data']

        self.assertIn('level_name', data[0])
