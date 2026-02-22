from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.logs.models import OperationLog


class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="admin_auth",
            password="admin123",
            role=User.Role.ADMIN,
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username="normal_auth",
            password="123456",
            email="normal@example.com",
            role=User.Role.USER,
            status=True,
            is_deleted=False,
        )
        self.deleted_user = User.objects.create_user(
            username="deleted_auth",
            password="123456",
            email="deleted@example.com",
            role=User.Role.USER,
            status=True,
            is_deleted=True,
        )

    def test_register_and_login(self):
        register_resp = self.client.post(
            "/api/auth/register/",
            data={
                "username": "new_user",
                "password": "newpass1",
                "email": "new_user@example.com",
                "phone": "13800000000",
            },
            format="json",
        )
        self.assertEqual(register_resp.status_code, 200)
        self.assertEqual(register_resp.data["data"]["username"], "new_user")
        self.assertEqual(register_resp.data["data"]["role"], "USER")
        self.assertFalse(register_resp.data["data"]["is_deleted"])

        login_resp = self.client.post(
            "/api/auth/login/",
            data={"username": "new_user", "password": "newpass1"},
            format="json",
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("token", login_resp.data["data"])
        self.assertTrue(Token.objects.filter(key=login_resp.data["data"]["token"]).exists())

    def test_login_rejects_wrong_credentials_and_deleted_user(self):
        bad_password_resp = self.client.post(
            "/api/auth/login/",
            data={"username": self.user.username, "password": "bad-pass"},
            format="json",
        )
        self.assertEqual(bad_password_resp.status_code, 401)

        deleted_resp = self.client.post(
            "/api/auth/login/",
            data={"username": self.deleted_user.username, "password": "123456"},
            format="json",
        )
        self.assertEqual(deleted_resp.status_code, 401)

    def test_admin_permission_requires_valid_admin_token(self):
        no_token_resp = self.client.get("/api/admin/users/")
        self.assertEqual(no_token_resp.status_code, 401)

        user_login_resp = self.client.post(
            "/api/auth/login/",
            data={"username": self.user.username, "password": "123456"},
            format="json",
        )
        self.assertEqual(user_login_resp.status_code, 200)
        user_token = user_login_resp.data["data"]["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")
        non_admin_resp = self.client.get("/api/admin/users/")
        self.assertEqual(non_admin_resp.status_code, 403)

        self.client.credentials()
        admin_login_resp = self.client.post(
            "/api/auth/login/",
            data={"username": self.admin.username, "password": "admin123"},
            format="json",
        )
        self.assertEqual(admin_login_resp.status_code, 200)
        admin_token = admin_login_resp.data["data"]["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
        admin_resp = self.client.get("/api/admin/users/?page=1&page_size=20")
        self.assertEqual(admin_resp.status_code, 200)


class UserManageAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="user_admin",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )
        self.target_user = User.objects.create_user(
            username="normal_user",
            password="123456",
            email="u@example.com",
            role=User.Role.USER,
            status=True,
        )
        self.client.force_authenticate(user=self.admin)

    def test_user_manage_list_update_and_soft_delete(self):
        list_resp = self.client.get("/api/admin/users/?page=1&page_size=20")
        self.assertEqual(list_resp.status_code, 200)
        self.assertGreaterEqual(list_resp.data["total"], 1)

        update_resp = self.client.put(
            "/api/admin/users/",
            data={"id": self.target_user.id, "role": "ADMIN", "status": False},
            format="json",
        )
        self.assertEqual(update_resp.status_code, 200)
        self.target_user.refresh_from_db()
        self.assertEqual(self.target_user.role, "ADMIN")
        self.assertFalse(self.target_user.status)

        delete_resp = self.client.delete(
            "/api/admin/users/",
            data={"id": self.target_user.id},
            format="json",
        )
        self.assertEqual(delete_resp.status_code, 200)
        self.target_user.refresh_from_db()
        self.assertTrue(self.target_user.is_deleted)
        self.assertFalse(self.target_user.status)

        include_deleted_resp = self.client.get("/api/admin/users/?include_deleted=true")
        self.assertEqual(include_deleted_resp.status_code, 200)
        self.assertTrue(any(item["id"] == self.target_user.id for item in include_deleted_resp.data["data"]))

        self.assertTrue(OperationLog.objects.filter(operation_type="USER_UPDATE").exists())
