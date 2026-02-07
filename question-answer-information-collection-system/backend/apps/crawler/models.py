from django.db import models


class Tag(models.Model):
    """问答标签模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        db_table = 'crawler_tag'

    def __str__(self):
        return self.name


class Question(models.Model):
    """问答数据模型"""
    title = models.CharField(max_length=255, verbose_name='问题标题')
    description = models.TextField(blank=True, null=True, verbose_name='问题描述')
    answer_content = models.TextField(verbose_name='回答内容')
    answer_time = models.DateTimeField(blank=True, null=True, verbose_name='回答时间')
    answerer = models.CharField(max_length=100, blank=True, null=True, verbose_name='回答者')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True, verbose_name='标签')
    source_url = models.URLField(max_length=255, unique=True, verbose_name='来源链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '问答'
        verbose_name_plural = '问答'
        db_table = 'crawler_question'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['answerer']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title[:50]
