"""
用户行为日志模型

用于记录用户在系统中的各种行为，支持行为分析、数据统计和用户洞察。
"""

from django.db import models
from django.conf import settings
import json


class UserBehaviorLog(models.Model):
    """
    用户行为日志表

    记录用户的所有行为（登录、搜索、浏览、收藏等），
    用于后续的用户行为分析和数据可视化。
    """

    # 用户关联（可为空，支持未登录用户的行为记录）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='用户',
        help_text='执行行为的用户，为空表示未登录用户'
    )

    # 行为类型（登录、搜索、浏览、收藏等）
    behavior_type = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='行为类型',
        help_text='用户行为的类型，如 login/search/view/collect 等'
    )

    # 行为目标（菜谱 ID 或页面路径）
    target = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='行为目标',
        help_text='行为的目标对象，如菜谱 ID 或页面路径'
    )

    # 行为时间
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='行为时间',
        help_text='行为发生的时间'
    )

    # 额外数据（JSON 格式，存储搜索关键词、停留时长等）
    extra_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='额外数据',
        help_text='额外的行为相关数据，如搜索关键词、停留时长等，JSON 格式'
    )

    # IP 地址（可选，用于分析用户地域）
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP 地址',
        help_text='用户发起行为时的 IP 地址'
    )

    # User-Agent（可选，用于分析用户设备）
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name='用户代理',
        help_text='用户发起行为时的浏览器 User-Agent'
    )

    class Meta:
        db_table = 'user_behavior_logs'
        verbose_name = '用户行为日志'
        verbose_name_plural = '用户行为日志'
        ordering = ['-timestamp']
        # 复合索引，优化常见查询
        indexes = [
            models.Index(fields=['user', '-timestamp'], name='behavior_user_time_idx'),
            models.Index(fields=['behavior_type', '-timestamp'], name='behavior_type_time_idx'),
            models.Index(fields=['-timestamp'], name='behavior_time_idx'),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else '匿名用户'
        return f'{user_str} - {self.get_behavior_type_display()} - {self.timestamp}'

    def set_extra_data(self, data):
        """设置额外数据"""
        self.extra_data = data
        self.save(update_fields=['extra_data'])

    def get_extra_data(self, key=None, default=None):
        """
        获取额外数据

        Args:
            key: 要获取的键，为 None 时返回整个 extra_data
            default: 当 key 不存在时返回的默认值

        Returns:
            如果 key 为 None，返回整个 extra_data
            如果 key 存在，返回对应的值
            如果 key 不存在，返回 default
        """
        if self.extra_data is None:
            return default

        if key is None:
            return self.extra_data

        return self.extra_data.get(key, default)

    @classmethod
    def log_behavior(cls, user, behavior_type, target=None, extra_data=None,
                     ip_address=None, user_agent=None):
        """
        记录用户行为的便捷方法

        Args:
            user: 用户对象（可为 None）
            behavior_type: 行为类型
            target: 行为目标（可选）
            extra_data: 额外数据（可选）
            ip_address: IP 地址（可选）
            user_agent: User-Agent（可选）

        Returns:
            创建的 UserBehaviorLog 实例
        """
        return cls.objects.create(
            user=user,
            behavior_type=behavior_type,
            target=target,
            extra_data=extra_data,
            ip_address=ip_address,
            user_agent=user_agent
        )
