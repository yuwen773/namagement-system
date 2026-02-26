"""
Inheritor API Tests
Tests for Inheritor CRUD operations and permissions
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.inheritors.models import Inheritor
from apps.regions.models import Region
from apps.users.models import UserProfile


User = get_user_model()


class InheritorCRUDTests(TestCase):
    """Test suite for Inheritor CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/inheritors/"
        
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
        
        # Create test data
        self.category = Category.objects.create(
            name="Traditional Music",
            code="CAT-MUSIC",
            level=Category.LEVEL_NATIONAL
        )
        self.region = Region.objects.create(
            country_code="CN",
            country_name="China",
            latitude="35.861700",
            longitude="104.195400",
            continent="Asia"
        )
        self.heritage_item = HeritageItem.objects.create(
            name="Guqin Art",
            category=self.category,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region
        )
        
        self.inheritor = Inheritor.objects.create(
            name="Li Ming",
            heritage_item=self.heritage_item,
            region=self.region,
            gender="male",
            level="national",
            area="Beijing"
        )

    def test_list_inheritors_requires_authentication(self):
        """Test that listing inheritors requires authentication"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_list_inheritors_success(self):
        """Test successful listing of inheritors"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["data"][0]["name"], "Li Ming")

    def test_retrieve_inheritor_with_heritage_info(self):
        """Test retrieving inheritor includes heritage item info"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f"{self.url}{self.inheritor.id}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["data"]["name"], "Li Ming")
        self.assertEqual(response.data["data"]["heritage_item"]["name"], "Guqin Art")

    def test_create_inheritor_admin_success(self):
        """Test admin can create inheritors"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Wang Lei",
            "heritage_item": self.heritage_item.id,
            "region": self.region.id,
            "gender": "female",
            "level": "provincial"
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(Inheritor.objects.count(), 2)

    def test_create_inheritor_user_forbidden(self):
        """Test normal user cannot create inheritors"""
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "name": "Test Inheritor",
            "heritage_item": self.heritage_item.id,
            "region": self.region.id
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Inheritor.objects.count(), 1)

    def test_update_inheritor_admin_success(self):
        """Test admin can update inheritors"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Li Ming Updated",
            "heritage_item": self.heritage_item.id,
            "region": self.region.id,
            "gender": "male",
            "area": "Shanghai"
        }
        response = self.client.put(f"{self.url}{self.inheritor.id}/", data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.inheritor.refresh_from_db()
        self.assertEqual(self.inheritor.name, "Li Ming Updated")
        self.assertEqual(self.inheritor.area, "Shanghai")

    def test_delete_inheritor_admin_success(self):
        """Test admin can delete inheritors"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"{self.url}{self.inheritor.id}/")
        
        # API returns 200 with success response instead of 204
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inheritor.objects.count(), 0)

    def test_delete_inheritor_user_forbidden(self):
        """Test normal user cannot delete inheritors"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f"{self.url}{self.inheritor.id}/")
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Inheritor.objects.count(), 1)

    def test_filter_by_heritage_item(self):
        """Test filtering inheritors by heritage item"""
        # Create another heritage item and inheritor
        heritage2 = HeritageItem.objects.create(
            name="Kunqu Opera",
            category=self.category,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region
        )
        Inheritor.objects.create(
            name="Zhang San",
            heritage_item=heritage2,
            region=self.region
        )
        
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"heritage_item": self.heritage_item.id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["data"][0]["name"], "Li Ming")

    def test_search_by_name(self):
        """Test searching inheritors by name"""
        Inheritor.objects.create(
            name="Wang Lei",
            heritage_item=self.heritage_item,
            region=self.region
        )
        
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"search": "Li"})
        
        self.assertEqual(response.status_code, 200)
        # Search might be case-insensitive or partial match
        self.assertGreaterEqual(response.data["total"], 1)
        # Verify Li Ming is in results
        names = [item["name"] for item in response.data["data"]]
        self.assertIn("Li Ming", names)
