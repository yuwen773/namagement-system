from django.db import models


class Question(models.Model):
    """问题模型 - 360问答数据采集

    对应数据源:
    - data/360_qa.csv (问题列表)
    - data/360_qa_detail.csv (问题详情)
    """
    # ========== 原始数据字段 ==========
    question_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='问题ID',
        help_text='360问答原始问题ID，用于去重和数据关联'
    )
    title = models.CharField(
        max_length=500,
        verbose_name='问题标题'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='问题描述'
    )

    # ========== 元数据字段 ==========
    category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='分类',
        db_index=True,
        help_text='如：影视、烦恼、软件等（去除方括号）'
    )
    publish_time = models.DateField(
        blank=True,
        null=True,
        verbose_name='发布时间',
        db_index=True,
        help_text='问题发布日期，格式：YYYY.MM.DD'
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='地理位置',
        db_index=True,
        help_text='问题发布地，如：美国、广东、浙江'
    )
    answer_count = models.IntegerField(
        default=0,
        verbose_name='回答数量',
        help_text='该问题的回答总数'
    )
    crawl_page = models.IntegerField(
        default=1,
        verbose_name='爬取页码',
        help_text='数据来源于第几页'
    )

    # ========== 来源信息 ==========
    source_url = models.URLField(
        max_length=500,
        unique=True,
        verbose_name='来源链接',
        help_text='360问答详情页URL'
    )

    # ========== 系统字段 ==========
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='入库时间',
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = '问题'
        db_table = 'crawler_question'
        ordering = ['-publish_time', '-created_at']
        indexes = [
            models.Index(fields=['question_id'], name='idx_question_id'),
            models.Index(fields=['publish_time'], name='idx_publish_time'),
            models.Index(fields=['category'], name='idx_category'),
            models.Index(fields=['location'], name='idx_location'),
            models.Index(fields=['-created_at'], name='idx_created_desc'),
            models.Index(fields=['answer_count'], name='idx_answer_count'),
        ]

    def __str__(self):
        return f"{self.question_id}: {self.title[:50]}"

    @property
    def answer_list(self):
        """获取答案列表（反向关联）"""
        return self.answers.all()


class Answer(models.Model):
    """答案模型

    将原来的answer_content字段拆分为独立模型，
    支持对每个答案的独立查询、统计和分析。
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='问题',
        db_index=True
    )
    content = models.TextField(
        verbose_name='答案内容'
    )
    answerer = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='回答者',
        db_index=True
    )
    answer_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='回答时间'
    )
    source_order = models.IntegerField(
        default=1,
        verbose_name='在源页面中的顺序',
        help_text='用于保持答案在源页面的原始顺序'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='入库时间'
    )

    class Meta:
        verbose_name = '答案'
        verbose_name_plural = '答案'
        db_table = 'crawler_answer'
        ordering = ['source_order']
        indexes = [
            models.Index(fields=['question'], name='idx_answer_question'),
            models.Index(fields=['answerer'], name='idx_answerer'),
            models.Index(fields=['answer_time'], name='idx_answer_time'),
        ]
        unique_together = [['question', 'source_order']]

    def __str__(self):
        return f"Answer for {self.question.question_id}: {self.content[:30]}..."
