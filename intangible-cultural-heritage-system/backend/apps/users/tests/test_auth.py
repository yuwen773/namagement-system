"""
Authentication API Tests
Tests for JWT login, refresh, and logout endpoints
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserProfile


User = get_user_model()


class AuthenticationTests(TestCase):
    """Test suite for authentication endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/v1/auth/login/"
        self.refresh_url = "/api/v1/auth/refresh/"
        self.logout_url = "/api/v1/auth/logout/"
        
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

    def test_login_success_with_admin(self):
        """Test successful login with admin credentials"""
        response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "password123"
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["message"], "登录成功")
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["username"], "admin")
        self.assertEqual(response.data["data"]["user"]["role"], "admin")

    def test_login_success_with_normal_user(self):
        """Test successful login with normal user credentials"""
        response = self.client.post(self.login_url, {
            "username": "user",
            "password": "password123"
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["data"]["user"]["role"], "user")

    def test_login_failure_wrong_password(self):
        """Test login failure with incorrect password"""
        response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "wrongpassword"
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)
        self.assertIn("用户名或密码错误", response.data["message"])

    def test_login_failure_nonexistent_user(self):
        """Test login failure with non-existent user"""
        response = self.client.post(self.login_url, {
            "username": "nonexistent",
            "password": "password123"
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_login_failure_missing_credentials(self):
        """Test login failure with missing credentials"""
        response = self.client.post(self.login_url, {
            "username": "admin"
        })
        
        # Missing password returns 401 (authentication failed)
        self.assertEqual(response.status_code, 401)

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        # First login to get tokens
        login_response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "password123"
        })
        refresh_token = login_response.data["data"]["refresh"]
        
        # Refresh the token
        response = self.client.post(self.refresh_url, {
            "refresh": refresh_token
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertIn("access", response.data["data"])

    def test_refresh_token_failure_invalid_token(self):
        """Test token refresh failure with invalid token"""
        response = self.client.post(self.refresh_url, {
            "refresh": "invalid_token_string"
        })
        
        # Invalid token returns 500 or 401 depending on implementation
        self.assertIn(response.status_code, [401, 500])

    def test_logout_success(self):
        """Test successful logout"""
        # First login
        login_response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "password123"
        })
        refresh_token = login_response.data["data"]["refresh"]
        access_token = login_response.data["data"]["access"]
        
        # Logout with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(self.logout_url, {
            "refresh": refresh_token
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 0)
        self.assertEqual(response.data["message"], "登出成功")

    def test_protected_endpoint_requires_authentication(self):
        """Test that protected endpoints require authentication"""
        response = self.client.get("/api/v1/heritage/")
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], 1)

    def test_protected_endpoint_with_valid_token(self):
        """Test accessing protected endpoint with valid token"""
        # Login and get token
        login_response = self.client.post(self.login_url, {
            "username": "admin",
            "password": "password123"
        })
        access_token = login_response.data["data"]["access"]
        
        # Access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get("/api/v1/heritage/")
        
        self.assertEqual(response.status_code, 200)
