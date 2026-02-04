"""
系统管理模型

包含系统配置、消息通知、操作日志等模型
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class SystemConfig(models.Model):
    """
    系统配置模型

    用于存储平台运行所需的配置参数，如网站名称、SEO设置等
    """
    key = models.CharField('配置键', max_length=100, unique=True, db_index=True)
    value = models.TextField('配置值')
    description = models.CharField('描述', max_length=500, blank=True, default='')

    # 分类
    category = models.CharField(
        '分类',
        max_length=50,
        choices=[
            ('basic', '基础配置'),
            ('seo', 'SEO配置'),
            ('trade', '交易配置'),
            ('other', '其他配置'),
        ],
        default='other',
        db_index=True
    )

    # 是否可修改
    is_editable = models.BooleanField('是否可编辑', default=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'system_configs'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置管理'

    def __str__(self):
        return f"{self.key} = {self.value[:50]}..." if len(self.value) > 50 else f"{self.key} = {self.value}"


class Message(models.Model):
    """
    站内消息模型

    用于向用户发送系统公告或通知
    """

    # 消息类型
    class MessageType(models.TextChoices):
        ANNOUNCEMENT = 'announcement', '系统公告'
        NOTIFICATION = 'notification', '订单通知'
        PROMOTION = 'promotion', '促销通知'
        SYSTEM = 'system', '系统通知'

    # 状态
    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        SENT = 'sent', '已发送'
        READ = 'read', '已读'

    # 接收者（为空表示全员）
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True,
        blank=True,
        verbose_name='接收用户'
    )

    # 消息内容
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    message_type = models.CharField(
        '消息类型',
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.NOTIFICATION,
        db_index=True
    )

    # 状态
    status = models.CharField(
        '状态',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )

    # 发送时间
    sent_at = models.DateTimeField('发送时间', null=True, blank=True)

    # 阅读时间
    read_at = models.DateTimeField('阅读时间', null=True, blank=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'messages'
        verbose_name = '站内消息'
        verbose_name_plural = '站内消息管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class OperationLog(models.Model):
    """
    操作日志模型

    记录管理员的关键操作行为，便于审计和追踪
    """

    # 操作类型
    class ActionType(models.TextChoices):
        CREATE = 'create', '创建'
        UPDATE = 'update', '更新'
        DELETE = 'delete', '删除'
        LOGIN = 'login', '登录'
        LOGOUT = 'logout', '登出'
        OTHER = 'other', '其他'

    # 操作人
    operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operation_logs',
        verbose_name='操作人'
    )

    # 操作类型
    action_type = models.CharField(
        '操作类型',
        max_length=20,
        choices=ActionType.choices,
        default=ActionType.OTHER,
        db_index=True
    )

    # 操作对象（表名）
    object_type = models.CharField('操作对象类型', max_length=100, blank=True, default='')

    # 操作对象ID
    object_id = models.CharField('操作对象ID', max_length=100, blank=True, default='')

    # 操作详情
    detail = models.TextField('操作详情', blank=True, default='')

    # IP地址
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)

    # User Agent
    user_agent = models.TextField('User Agent', blank=True, default='')

    # 状态
    status = models.CharField(
        '状态',
        max_length=20,
        choices=[
            ('success', '成功'),
            ('failed', '失败'),
        ],
        default='success',
        db_index=True
    )

    # 错误信息（如果失败）
    error_message = models.TextField('错误信息', blank=True, default='')

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now, db_index=True)

    class Meta:
        db_table = 'operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志管理'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operator} - {self.action_type} - {self.object_type} at {self.created_at}"
