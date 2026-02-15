from django.db import models


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort", "id"]

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "DRAFT"
        PUBLISHED = "PUBLISHED", "PUBLISHED"
        OFFLINE = "OFFLINE", "OFFLINE"

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory, on_delete=models.PROTECT, related_name="articles"
    )
    content = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_announcement = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["status", "is_announcement"])]

    def __str__(self):
        return self.title
