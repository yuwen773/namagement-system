from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.logs.models import OperationLog


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
