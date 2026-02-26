"""
Heritage Item API Tests
Tests for Heritage CRUD operations and permissions
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.regions.models import Region
from apps.users.models import UserProfile


User = get_user_model()


class HeritageItemCRUDTests(TestCase):
    """Test suite for Heritage Item CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/heritage/"
        
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
            region=self.region,
            area="Beijing",
            description="Ancient Chinese musical instrument"
        )

    def test_list_heritage_items_requires_authentication(self):
        """Test that listing heritage items requires authentication"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_list_heritage_items_success(self):
        """Test successful listing of heritage items"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Guqin Art")

    def test_retrieve_heritage_item_success(self):
        """Test retrieving a single heritage item"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f"{self.url}{self.heritage_item.id}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["data"]["name"], "Guqin Art")
        self.assertEqual(response.data["data"]["category"]["name"], "Traditional Music")
        self.assertEqual(response.data["data"]["region"]["country_name"], "China")

    def test_create_heritage_item_admin_success(self):
        """Test admin can create heritage items"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Kunqu Opera",
            "category": self.category.id,
            "level": "provincial",
            "region": self.region.id,
            "area": "Suzhou",
            "description": "Traditional Chinese opera"
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(HeritageItem.objects.count(), 2)
        self.assertEqual(HeritageItem.objects.latest("id").name, "Kunqu Opera")

    def test_create_heritage_item_user_forbidden(self):
        """Test normal user cannot create heritage items"""
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "name": "Test Heritage",
            "category": self.category.id,
            "level": "national",
            "region": self.region.id
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(HeritageItem.objects.count(), 1)

    def test_update_heritage_item_admin_success(self):
        """Test admin can update heritage items"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Guqin Art Updated",
            "category": self.category.id,
            "level": "national",
            "region": self.region.id,
            "description": "Updated description"
        }
        response = self.client.put(f"{self.url}{self.heritage_item.id}/", data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.heritage_item.refresh_from_db()
        self.assertEqual(self.heritage_item.name, "Guqin Art Updated")
        self.assertEqual(self.heritage_item.description, "Updated description")

    def test_update_heritage_item_user_forbidden(self):
        """Test normal user cannot update heritage items"""
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "name": "Updated Name",
            "category": self.category.id,
            "level": "national",
            "region": self.region.id
        }
        response = self.client.put(f"{self.url}{self.heritage_item.id}/", data)
        
        self.assertEqual(response.status_code, 403)

    def test_delete_heritage_item_admin_success(self):
        """Test admin can delete heritage items"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"{self.url}{self.heritage_item.id}/")
        
        # API returns 200 with success response instead of 204
        self.assertEqual(response.status_code, 200)
        self.assertEqual(HeritageItem.objects.count(), 0)

    def test_delete_heritage_item_user_forbidden(self):
        """Test normal user cannot delete heritage items"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f"{self.url}{self.heritage_item.id}/")
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(HeritageItem.objects.count(), 1)

    def test_filter_by_category(self):
        """Test filtering heritage items by category"""
        # Create another category and item
        category2 = Category.objects.create(
            name="Traditional Dance",
            code="CAT-DANCE",
            level=Category.LEVEL_NATIONAL
        )
        HeritageItem.objects.create(
            name="Dragon Dance",
            category=category2,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region
        )
        
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"category": self.category.id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["data"][0]["name"], "Guqin Art")

    def test_filter_by_level(self):
        """Test filtering heritage items by level"""
        HeritageItem.objects.create(
            name="Provincial Heritage",
            category=self.category,
            level=HeritageItem.LEVEL_PROVINCIAL,
            region=self.region
        )
        
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"level": "national"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["data"][0]["level"], "national")

    def test_search_by_name(self):
        """Test searching heritage items by name"""
        HeritageItem.objects.create(
            name="Kunqu Opera",
            category=self.category,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region
        )
        
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"search": "Guqin"})
        
        self.assertEqual(response.status_code, 200)
        # Search might be case-insensitive or partial match
        self.assertGreaterEqual(response.data["total"], 1)
        # Verify Guqin Art is in results
        names = [item["name"] for item in response.data["data"]]
        self.assertIn("Guqin Art", names)

    def test_pagination(self):
        """Test pagination of heritage items"""
        # Create more items
        for i in range(25):
            HeritageItem.objects.create(
                name=f"Heritage {i}",
                category=self.category,
                level=HeritageItem.LEVEL_NATIONAL,
                region=self.region
            )
        
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url, {"page": 1, "page_size": 20})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 20)
        self.assertEqual(response.data["total"], 26)
