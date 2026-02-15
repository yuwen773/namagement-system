from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.articles.models import Article, ArticleCategory


class ArticleUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat_knowledge = ArticleCategory.objects.create(name="健康科普", sort=1)
        self.cat_policy = ArticleCategory.objects.create(name="政策法规", sort=2)

        self.article_1 = Article.objects.create(
            title="空气质量与日常防护",
            category=self.cat_knowledge,
            content="<p>content 1</p>",
            status=Article.Status.PUBLISHED,
            is_announcement=False,
            sort_order=10,
        )
        self.article_2 = Article.objects.create(
            title="最新环保政策解读",
            category=self.cat_policy,
            content="<p>content 2</p>",
            status=Article.Status.PUBLISHED,
            is_announcement=False,
            sort_order=20,
        )
        self.draft_article = Article.objects.create(
            title="草稿文章",
            category=self.cat_policy,
            content="<p>draft</p>",
            status=Article.Status.DRAFT,
            is_announcement=False,
            sort_order=30,
        )
        self.announcement = Article.objects.create(
            title="系统公告",
            category=self.cat_knowledge,
            content="<p>announcement</p>",
            status=Article.Status.PUBLISHED,
            is_announcement=True,
            sort_order=1,
        )

    def test_article_list_and_detail(self):
        list_resp = self.client.get("/api/articles/?page=1&page_size=20")
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(list_resp.data["code"], 200)
        self.assertEqual(list_resp.data["total"], 2)

        filter_resp = self.client.get(f"/api/articles/?category_id={self.cat_policy.id}")
        self.assertEqual(filter_resp.status_code, 200)
        self.assertEqual(filter_resp.data["total"], 1)
        self.assertEqual(filter_resp.data["data"][0]["title"], self.article_2.title)

        detail_resp = self.client.get(f"/api/articles/{self.article_1.id}/")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIn("content", detail_resp.data["data"])

        draft_detail_resp = self.client.get(f"/api/articles/{self.draft_article.id}/")
        self.assertEqual(draft_detail_resp.status_code, 404)

    def test_category_and_announcement_api(self):
        category_resp = self.client.get("/api/categories/")
        self.assertEqual(category_resp.status_code, 200)
        self.assertEqual(len(category_resp.data["data"]), 2)

        announcement_resp = self.client.get("/api/announcements/?limit=5")
        self.assertEqual(announcement_resp.status_code, 200)
        self.assertEqual(len(announcement_resp.data["data"]), 1)
        self.assertTrue(announcement_resp.data["data"][0]["is_announcement"])


class ArticleManageAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="article_admin",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=self.admin)

        self.category = ArticleCategory.objects.create(name="系统公告", sort=1)
        self.article = Article.objects.create(
            title="待管理文章",
            category=self.category,
            content="<p>draft</p>",
            status=Article.Status.DRAFT,
            is_announcement=False,
            sort_order=10,
        )

    def test_article_manage_and_category_manage_api(self):
        list_resp = self.client.get("/api/admin/articles/?page=1&page_size=20")
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(list_resp.data["total"], 1)

        update_resp = self.client.put(
            "/api/admin/articles/",
            data={"id": self.article.id, "status": Article.Status.PUBLISHED, "is_announcement": True},
            format="json",
        )
        self.assertEqual(update_resp.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, Article.Status.PUBLISHED)
        self.assertTrue(self.article.is_announcement)

        category_create_resp = self.client.post(
            "/api/admin/categories/",
            data={"name": "健康科普", "sort": 2},
            format="json",
        )
        self.assertEqual(category_create_resp.status_code, 200)
        category_id = category_create_resp.data["data"]["id"]

        category_update_resp = self.client.put(
            "/api/admin/categories/",
            data={"id": category_id, "name": "健康科普更新"},
            format="json",
        )
        self.assertEqual(category_update_resp.status_code, 200)

        delete_resp = self.client.delete(
            "/api/admin/articles/",
            data={"id": self.article.id},
            format="json",
        )
        self.assertEqual(delete_resp.status_code, 200)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())
