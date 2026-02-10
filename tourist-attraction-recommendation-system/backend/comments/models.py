from django.db import models
from accounts.models import UserProfile
from attractions.models import Attraction


class Comment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '待审核'),
        ('APPROVED', '已通过'),
        ('REJECTED', '已驳回'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('评论内容')
    rating = models.IntegerField('评分', default=5)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_deleted = models.BooleanField('是否删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}@{self.attraction.name}'


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorites')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'attraction']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} favorite {self.attraction.name}'
