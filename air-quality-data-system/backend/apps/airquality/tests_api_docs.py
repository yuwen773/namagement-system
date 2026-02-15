from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient


class APIDocumentationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_schema_and_swagger_endpoints_available(self):
        schema_resp = self.client.get("/api/schema/")
        self.assertEqual(schema_resp.status_code, 200)
        self.assertEqual(schema_resp.data.get("openapi"), "3.0.3")
        self.assertIn("/api/overview/", schema_resp.data.get("paths", {}))
        self.assertIn("/api/auth/login/", schema_resp.data.get("paths", {}))
        self.assertIn("/api/admin/users/", schema_resp.data.get("paths", {}))

        docs_resp = self.client.get("/api/docs/")
        self.assertEqual(docs_resp.status_code, 200)
        self.assertIn("swagger", docs_resp.content.decode("utf-8").lower())

    def test_export_api_docs_command(self):
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "API_DOCS.md"
            schema_json_path = Path(temp_dir) / "openapi.json"
            call_command(
                "export_api_docs",
                output=str(output_path),
                schema_json=str(schema_json_path),
            )

            self.assertTrue(output_path.exists())
            self.assertTrue(schema_json_path.exists())

            markdown = output_path.read_text(encoding="utf-8")
            self.assertIn("## 用户端接口", markdown)
            self.assertIn("## 管理端接口", markdown)
            self.assertIn("`GET /api/overview/`", markdown)
            self.assertIn("`GET /api/admin/dashboard/`", markdown)
            self.assertIn("`POST /api/auth/login/`", markdown)
            self.assertIn("`GET /api/admin/users/`", markdown)
