"""
Region API Tests
Tests for Region CRUD operations and permissions
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.regions.models import Region
from apps.users.models import UserProfile


User = get_user_model()


class RegionCRUDTests(TestCase):
    """Test suite for Region CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/regions/"
        
        # Create test users
        self.admin_user = User.objects.create_user(
            username="admin",
            password="password123"
        )
        UserProfile.objects.filter(user=self.admin_user).update(role="admin")
        
        self.normal_user = User.objects.create_user(
            username="user",
            password="password123"
        )
        UserProfile.objects.filter(user=self.normal_user).update(role="user")
        
        # Create test regions
        self.region_cn = Region.objects.create(
            country_code="CN",
            country_name="China",
            latitude="35.861700",
            longitude="104.195400",
            continent="Asia"
        )
        self.region_jp = Region.objects.create(
            country_code="JP",
            country_name="Japan",
            latitude="36.204800",
            longitude="138.252900",
            continent="Asia"
        )

    def test_list_regions_all_users(self):
        """Test all authenticated users can list regions"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["total"], 2)

    def test_search_regions_by_name(self):
        """Test searching regions by country name"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"search": "China"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["data"][0]["country_name"], "China")

    def test_search_regions_by_code(self):
        """Test searching regions by country code"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"search": "JP"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["data"][0]["country_code"], "JP")

    def test_create_region_admin_success(self):
        """Test admin can create regions"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "country_code": "US",
            "country_name": "United States",
            "latitude": "37.090200",
            "longitude": "-95.712900",
            "continent": "North America"
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(Region.objects.count(), 3)

    def test_create_region_user_forbidden(self):
        """Test normal user cannot create regions"""
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "country_code": "FR",
            "country_name": "France",
            "latitude": "46.227600",
            "longitude": "2.213700",
            "continent": "Europe"
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Region.objects.count(), 2)

    def test_update_region_admin_success(self):
        """Test admin can update regions"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "country_code": "CN",
            "country_name": "People's Republic of China",
            "latitude": "35.861700",
            "longitude": "104.195400",
            "continent": "Asia"
        }
        response = self.client.put(f"{self.url}{self.region_cn.id}/", data)
        
        self.assertEqual(response.status_code, 200)
        self.region_cn.refresh_from_db()
        self.assertEqual(self.region_cn.country_name, "People's Republic of China")

    def test_delete_region_admin_success(self):
        """Test admin can delete regions"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"{self.url}{self.region_jp.id}/")
        
        # API returns 200 with success response instead of 204
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Region.objects.count(), 1)

    def test_delete_region_user_forbidden(self):
        """Test normal user cannot delete regions"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f"{self.url}{self.region_jp.id}/")
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Region.objects.count(), 2)
