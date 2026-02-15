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
