from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.articles.models import ArticleCategory
from apps.logs.models import ErrorLog, OperationLog


class LogManageAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="log_admin",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=self.admin)

        OperationLog.objects.create(
            user=self.admin,
            operation_type="USER_UPDATE",
            operation_content="test update",
            ip_address="127.0.0.1",
        )
        ErrorLog.objects.create(
            error_type="ValueError",
            error_message="invalid value",
            stack_trace="trace",
        )

    def test_operation_and_error_logs_api(self):
        operation_resp = self.client.get(
            f"/api/admin/logs/operations/?user_id={self.admin.id}&page=1&page_size=20"
        )
        self.assertEqual(operation_resp.status_code, 200)
        self.assertGreaterEqual(operation_resp.data["total"], 1)

        error_resp = self.client.get("/api/admin/logs/errors/?page=1&page_size=20")
        self.assertEqual(error_resp.status_code, 200)
        self.assertGreaterEqual(error_resp.data["total"], 1)

    def test_admin_operation_middleware_logs_write_request(self):
        before_count = OperationLog.objects.count()
        post_resp = self.client.post(
            "/api/admin/categories/",
            data={"name": "Middleware Category", "sort": 99},
            format="json",
        )
        self.assertEqual(post_resp.status_code, 200)
        self.assertTrue(ArticleCategory.objects.filter(name="Middleware Category").exists())
        self.assertGreater(OperationLog.objects.count(), before_count)
