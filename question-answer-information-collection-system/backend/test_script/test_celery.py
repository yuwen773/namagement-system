#!/usr/bin/env python
"""
Celery 配置测试脚本

验证 Celery 是否正确配置，并能正常运行异步任务。
"""

import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import django
django.setup()


def test_celery_connection():
    """测试 Celery 配置"""
    print("=" * 60)
    print("Celery 配置测试")
    print("=" * 60)

    # 1. 测试 Celery 应用导入
    print("\n[1] 测试 Celery 应用导入...")
    try:
        from qa_project.celery import app
        print(f"    ✅ Celery 应用名称: {app.main}"
              f"     ✅ Celery 时区: {app.conf.timezone}")
    except Exception as e:
        print(f"    ❌ 导入失败: {e}")
        return False

    # 2. 测试 Redis 连接
    print("\n[2] 测试 Redis 连接...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        r.ping()
        print("    ✅ Redis 连接成功")
    except Exception as e:
        print(f"    ❌ Redis 连接失败: {e}")
        print("    💡 请确保 Redis 服务已启动: redis-server")
        return False

    # 3. 测试 Celery 配置
    print("\n[3] 测试 Celery 配置...")
    try:
        print(f"    Broker URL: {app.conf.broker_url}")
        print(f"    Result Backend: {app.conf.result_backend}")
        print(f"    Task Track Started: {app.conf.task_track_started}")
        print(f"    ✅ Celery 配置正确")
    except Exception as e:
        print(f"    ❌ 配置读取失败: {e}")
        return False

    # 4. 测试任务发现
    print("\n[4] 测试任务发现...")
    try:
        from crawler.tasks import run_spider_task, get_task_status
        print("    ✅ 爬虫任务已发现")
        print(f"    任务名称: {run_spider_task.name}")
    except Exception as e:
        print(f"    ❌ 任务发现失败: {e}")
        return False

    # 5. 测试 Redis 读写
    print("\n[5] 测试 Redis 读写...")
    try:
        test_key = 'qa_crawler:test_connection'
        r.set(test_key, 'test_value', ex=60)
        value = r.get(test_key)
        r.delete(test_key)
        assert value == 'test_value'
        print("    ✅ Redis 读写测试通过")
    except Exception as e:
        print(f"    ❌ Redis 读写测试失败: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 所有测试通过！Celery 配置正确")
    print("=" * 60)

    print("\n📝 启动命令:")
    print("  # 启动 Django 服务:")
    print("  python manage.py runserver")
    print()
    print("  # 启动 Celery Worker（新终端）:")
    print("  celery -A qa_project worker -l info")
    print()
    print("  # 启动 Celery Beat（可选，定时任务）:")
    print("  celery -A qa_project beat -l info")

    return True


def test_async_task():
    """测试异步任务执行"""
    print("\n" + "=" * 60)
    print("异步任务测试")
    print("=" * 60)

    try:
        from crawler.tasks import run_spider_task

        # 启动一个快速测试任务（演示模式）
        print("\n🚀 启动测试任务（演示模式，limit=5）...")
        result = run_spider_task.delay(mode='demo', limit=5, api_only=True)

        print(f"   任务 ID: {result.id}")
        print("   ✅ 任务已提交到 Celery")
        print("\n💡 查看任务状态:")
        print(f"   celery -A qa_project worker -l info -Q default")

    except Exception as e:
        print(f"   ❌ 任务提交失败: {e}")
        return False

    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Celery 配置测试工具')
    parser.add_argument('--task', action='store_true', help='测试异步任务执行')

    args = parser.parse_args()

    success = test_celery_connection()

    if success and args.task:
        test_async_task()
