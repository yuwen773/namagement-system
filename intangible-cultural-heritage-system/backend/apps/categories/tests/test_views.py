"""
Category API Tests
Tests for Category CRUD operations, tree structure, and permissions
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.users.models import UserProfile


User = get_user_model()


class CategoryCRUDTests(TestCase):
    """Test suite for Category CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/categories/"
        
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
        
        # Create test categories
        self.parent_category = Category.objects.create(
            name="Traditional Arts",
            code="CAT-ARTS",
            level=Category.LEVEL_NATIONAL
        )
        self.child_category = Category.objects.create(
            name="Traditional Music",
            code="CAT-MUSIC",
            level=Category.LEVEL_PROVINCIAL,
            parent=self.parent_category
        )

    def test_list_categories_all_users(self):
        """Test all authenticated users can list categories"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["total"], 2)

    def test_retrieve_category_success(self):
        """Test retrieving a single category"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f"{self.url}{self.parent_category.id}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["data"]["name"], "Traditional Arts")

    def test_tree_structure_endpoint(self):
        """Test tree structure endpoint returns hierarchical data"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f"{self.url}tree/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        # Should have parent with children
        tree_data = response.data["data"]
        self.assertTrue(len(tree_data) > 0)

    def test_create_category_admin_success(self):
        """Test admin can create categories"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Traditional Dance",
            "code": "CAT-DANCE",
            "level": "national"
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(Category.objects.count(), 3)

    def test_create_category_with_parent(self):
        """Test creating category with parent relationship"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Folk Music",
            "code": "CAT-FOLK",
            "level": "city_county",
            "parent": self.child_category.id
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 201)
        new_category = Category.objects.get(code="CAT-FOLK")
        self.assertEqual(new_category.parent, self.child_category)

    def test_create_category_user_forbidden(self):
        """Test normal user cannot create categories"""
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "name": "Test Category",
            "code": "CAT-TEST",
            "level": "national"
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category_admin_success(self):
        """Test admin can update categories"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "Traditional Arts Updated",
            "code": "CAT-ARTS",
            "level": "national"
        }
        response = self.client.put(f"{self.url}{self.parent_category.id}/", data)
        
        self.assertEqual(response.status_code, 200)
        self.parent_category.refresh_from_db()
        self.assertEqual(self.parent_category.name, "Traditional Arts Updated")

    def test_update_category_user_forbidden(self):
        """Test normal user cannot update categories"""
        self.client.force_authenticate(user=self.normal_user)
        
        data = {
            "name": "Updated Name",
            "code": "CAT-ARTS",
            "level": "national"
        }
        response = self.client.put(f"{self.url}{self.parent_category.id}/", data)
        
        self.assertEqual(response.status_code, 403)

    def test_delete_category_admin_success(self):
        """Test admin can delete categories"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"{self.url}{self.child_category.id}/")
        
        # API returns 200 with success response instead of 204
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)

    def test_delete_category_user_forbidden(self):
        """Test normal user cannot delete categories"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f"{self.url}{self.child_category.id}/")
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Category.objects.count(), 2)
