"""
爬虫 Celery 任务模块

提供异步爬虫任务支持，包括断点续传、进度更新和详细日志记录。
"""

import os
import sys
import django
import redis
import json
import subprocess
from datetime import datetime
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

# Setup Django（确保能访问 Django ORM）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
django.setup()

from django.utils import timezone


# Redis 连接配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Redis Key 前缀
REDIS_KEY_PREFIX = 'qa_crawler:'


def get_redis():
    """获取 Redis 连接"""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def get_progress_key(task_id: str) -> str:
    """获取进度存储的 Redis Key"""
    return f'{REDIS_KEY_PREFIX}progress:{task_id}'


def get_status_key(task_id: str) -> str:
    """获取状态存储的 Redis Key"""
    return f'{REDIS_KEY_PREFIX}status:{task_id}'


def get_resume_key(mode: str) -> str:
    """获取断点信息的 Redis Key"""
    return f'{REDIS_KEY_PREFIX}resume:{mode}'


@shared_task(bind=True, name='crawler.tasks.run_spider_task')
def run_spider_task(self, mode: str = 'demo', limit: int = 20, resume: bool = False,
                    api_only: bool = False):
    """
    Celery 爬虫任务

    Args:
        self: Celery 任务实例
        mode: 采集模式 ('demo' 或 'full')
        limit: 采集数量限制
        resume: 是否从断点继续
        api_only: 是否使用纯API模式

    Returns:
        dict: 任务执行结果和统计信息
    """
    import apps.crawler.settings as my_settings

    task_id = self.request.id or 'unknown'
    redis_client = get_redis()

    # 初始化进度状态
    progress_key = get_progress_key(task_id)
    status_key = get_status_key(task_id)

    initial_status = {
        'task_id': task_id,
        'mode': mode,
        'limit': limit,
        'status': 'running',
        'progress': 0,
        'collected': 0,
        'failed': 0,
        'start_time': timezone.now().isoformat(),
        'current_page': 0,
        'message': '任务启动中...',
    }

    redis_client.setex(status_key, 86400, json.dumps(initial_status))  # 24小时过期
    redis_client.setex(progress_key, 86400, json.dumps({
        'timestamp': timezone.now().isoformat(),
        'current_page': 0,
        'collected': 0,
        'failed': 0,
    }))

    try:
        # 更新状态：准备启动
        update_status(status_key, {
            'status': 'running',
            'message': '正在初始化爬虫...',
        })

        # 构造 Scrapy 命令参数
        cmd_args = [
            sys.executable,  # 当前 Python 解释器
            '-c',
            f'''
import os
import sys
sys.path.insert(0, r'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import json

# 导入爬虫模块
api_only = {api_only}
if api_only:
    from apps.crawler.spiders import WendaAPISpider as SpiderClass
else:
    from apps.crawler.spiders import WendaSpider as SpiderClass

import apps.crawler.settings as my_settings

# 创建爬虫设置
crawler_settings = Settings()
for key in dir(my_settings):
    if key.isupper():
        crawler_settings.set(key, getattr(my_settings, key))

# 进度回调
class ProgressCallback:
    def __init__(self, task_id, redis_host, redis_port):
        self.task_id = task_id
        self.redis = __import__('redis').Redis(host=redis_host, port=redis_port, decode_responses=True)

    def update(self, collected, failed, current_page, message=''):
        import json
        from django.utils import timezone
        data = {{
            'timestamp': timezone.now().isoformat(),
            'collected': collected,
            'failed': failed,
            'current_page': current_page,
            'message': message,
        }}
        self.redis.setex(f'qa_crawler:progress:{self.task_id}', 86400, json.dumps(data))

progress_cb = ProgressCallback('{task_id}', '{REDIS_HOST}', {REDIS_PORT})

# 启动爬虫
process = CrawlerProcess(settings=crawler_settings)

class CustomSpider(SpiderClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collected_count = 0
        self._failed_count = 0
        self._current_page = 0
        self._last_progress_update = 0

    def update_progress(self, collected, failed, page):
        self._collected_count = collected
        self._failed_count = failed
        self._current_page = page
        # 每采集 50 条更新一次 Redis
        if collected - self._last_progress_update >= 50:
            progress_cb.update(collected, failed, page, f'已采集 {{collected}} 条数据')
            self._last_progress_update = collected

process.crawl(CustomSpider, mode='{mode}', limit={limit}, resume={resume})
process.start()
'''
        ]

        # 更新状态：开始爬取
        update_status(status_key, {
            'status': 'running',
            'message': '正在执行爬虫任务...',
        })

        # 执行爬虫命令
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=3600,  # 1小时超时
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # 解析最终统计
        collected = 0
        failed = 0

        if result.returncode == 0:
            # 尝试从输出中提取统计信息
            for line in result.stdout.split('\n'):
                if 'collected' in line.lower():
                    try:
                        collected = int(line.split(':')[-1].strip())
                    except:
                        pass

            status = 'completed'
            message = f'采集完成！共采集 {collected} 条数据'
        else:
            status = 'failed'
            message = f'采集失败: {result.stderr[:200]}'
            # 记录错误日志
            error_log_key = f'{REDIS_KEY_PREFIX}error:{task_id}'
            redis_client.setex(error_log_key, 86400, result.stderr)

        # 更新最终状态
        final_status = {
            'task_id': task_id,
            'mode': mode,
            'limit': limit,
            'status': status,
            'progress': 100 if status == 'completed' else 0,
            'collected': collected,
            'failed': failed,
            'end_time': timezone.now().isoformat(),
            'message': message,
            'logs_available': True,
        }
        redis_client.setex(status_key, 86400, json.dumps(final_status))

        return {
            'status': status,
            'task_id': task_id,
            'collected': collected,
            'failed': failed,
            'message': message,
        }

    except SoftTimeLimitExceeded:
        # 任务超时
        update_status(status_key, {
            'status': 'timeout',
            'message': '任务执行超时（超过1小时）',
        })
        return {
            'status': 'timeout',
            'task_id': task_id,
            'message': '任务执行超时',
        }

    except Exception as e:
        # 任务异常
        update_status(status_key, {
            'status': 'error',
            'message': f'任务异常: {str(e)}',
        })
        return {
            'status': 'error',
            'task_id': task_id,
            'message': f'任务异常: {str(e)}',
        }


def update_status(status_key: str, updates: dict):
    """更新任务状态"""
    redis_client = get_redis()
    try:
        current = json.loads(redis_client.get(status_key) or '{}')
        current.update(updates)
        redis_client.setex(status_key, 86400, json.dumps(current))
    except Exception:
        pass


@shared_task(name='crawler.tasks.get_task_status')
def get_task_status(task_id: str) -> dict:
    """
    获取任务状态

    Args:
        task_id: Celery 任务 ID

    Returns:
        dict: 任务状态信息
    """
    redis_client = get_redis()
    status_key = get_status_key(task_id)

    status_data = redis_client.get(status_key)
    if status_data:
        return json.loads(status_data)

    # 如果 Redis 中没有，查询 Celery 结果
    from qa_project.celery import app
    result = app.AsyncResult(task_id)
    return {
        'task_id': task_id,
        'status': str(result.status),
        'result': str(result.result) if result.result else None,
    }


@shared_task(name='crawler.tasks.get_task_progress')
def get_task_progress(task_id: str) -> dict:
    """
    获取任务进度详情

    Args:
        task_id: Celery 任务 ID

    Returns:
        dict: 进度详情
    """
    redis_client = get_redis()
    progress_key = get_progress_key(task_id)

    progress_data = redis_client.get(progress_key)
    if progress_data:
        return json.loads(progress_data)

    return {
        'timestamp': None,
        'current_page': 0,
        'collected': 0,
        'failed': 0,
        'message': '暂无进度信息',
    }


@shared_task(name='crawler.tasks.get_task_logs')
def get_task_logs(task_id: str) -> str:
    """
    获取任务执行日志

    Args:
        task_id: Celery 任务 ID

    Returns:
        str: 日志内容
    """
    redis_client = get_redis()
    error_log_key = f'{REDIS_KEY_PREFIX}error:{task_id}'

    error_log = redis_client.get(error_log_key)
    if error_log:
        return error_log

    # 如果没有错误日志，返回占位信息
    return '暂无日志'


@shared_task(name='crawler.tasks.get_resume_info')
def get_resume_info(mode: str = 'full') -> dict:
    """
    获取断点续传信息

    Args:
        mode: 采集模式

    Returns:
        dict: 断点信息
    """
    redis_client = get_redis()
    resume_key = get_resume_key(mode)

    resume_data = redis_client.get(resume_key)
    if resume_data:
        return json.loads(resume_data)

    return {
        'mode': mode,
        'has_resume': False,
        'message': '没有可用的断点信息',
    }


@shared_task(name='crawler.tasks.cleanup_expired_tasks')
def cleanup_expired_tasks():
    """
    清理过期任务数据

    运行于 Celery Beat（定时任务）
    """
    redis_client = get_redis()
    pattern = f'{REDIS_KEY_PREFIX}*'
    deleted_count = 0

    for key in redis_client.scan_iter(match=pattern):
        # 检查 TTL，如果接近过期则删除
        ttl = redis_client.ttl(key)
        if ttl and ttl < 3600:  # 小于1小时
            redis_client.delete(key)
            deleted_count += 1

    return {
        'deleted_count': deleted_count,
        'cleanup_time': timezone.now().isoformat(),
    }


@shared_task(name='crawler.tasks.stop_spider')
def stop_spider(task_id: str) -> dict:
    """
    停止正在运行的爬虫任务

    Args:
        task_id: 要停止的任务 ID

    Returns:
        dict: 操作结果
    """
    try:
        from qa_project.celery import app
        app.control.revoke(task_id, terminate=True)

        # 更新状态
        redis_client = get_redis()
        status_key = get_status_key(task_id)
        redis_client.setex(status_key, 86400, json.dumps({
            'task_id': task_id,
            'status': 'stopped',
            'message': '任务已被用户停止',
            'stopped_at': timezone.now().isoformat(),
        }))

        return {
            'status': 'success',
            'task_id': task_id,
            'message': '任务已停止',
        }
    except Exception as e:
        return {
            'status': 'error',
            'task_id': task_id,
            'message': f'停止任务失败: {str(e)}',
        }
