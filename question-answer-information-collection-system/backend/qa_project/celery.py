"""
Celery 应用配置

为问答信息采集系统配置异步任务队列，支持爬虫异步执行和断点续传。
"""

import os
from celery import Celery
from celery.schedules import crontab

# 移除 django-celery-results 相关导入（使用 Redis 后端不需要）
# 如果需要数据库存储结果，取消下面的注释并运行迁移：
# CELERY_RESULT_BACKEND = 'django-db'

# 设置 Django 默认模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')

# 创建 Celery 应用
app = Celery('qa_project')

# 从 Django 配置中加载 Celery 设置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有注册的任务（包括 apps 下的 tasks）
app.autodiscover_tasks()

# 配置时区（与 Django 保持一致）
app.conf.timezone = 'Asia/Shanghai'

# Celery Beat 定时任务配置（可选）
app.conf.beat_schedule = {
    # 示例定时任务：每天凌晨2点清理过期任务
    'cleanup-expired-tasks': {
        'task': 'crawler.tasks.cleanup_expired_tasks',
        'schedule': crontab(hour=2, minute=0),
    },
}

# 任务结果序列化
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# 任务超时设置
app.conf.task_time_limit = 3600  # 1小时
app.conf.task_soft_time_limit = 3000  # 50分钟

# 任务重试配置
app.conf.task_autoretry_for = (Exception,)
app.conf.task_retry_backoff = True
app.conf.task_max_retries = 5
app.conf.task_retry_delay = 60  # 60秒后重试


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """调试任务，用于测试 Celery 是否正常工作"""
    print(f'Request: {self.request!r}')
