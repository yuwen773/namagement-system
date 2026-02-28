"""
Celery 应用配置

为问答信息采集系统配置异步任务队列，支持爬虫异步执行。

开发环境使用内存 broker，无需安装 Redis。
"""

import os
from celery import Celery

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

# Celery Beat 定时任务配置（内存 broker 不支持，已禁用）
# 如需使用定时任务，请切换到 Redis broker
# app.conf.beat_schedule = {
#     'cleanup-expired-tasks': {
#         'task': 'crawler.tasks.cleanup_expired_tasks',
#         'schedule': crontab(hour=2, minute=0),
#     },
# }

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
