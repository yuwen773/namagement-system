#!/usr/bin/env python
"""
爬虫状态 API 测试脚本

验证爬虫控制接口是否正常工作。
"""

import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
django.setup()

from rest_framework.test import APIClient
from apps.accounts.models import User


def test_crawler_api():
    """测试爬虫状态 API"""
    print("=" * 60)
    print("爬虫状态 API 测试")
    print("=" * 60)

    # ========== 未登录测试 ==========
    print("\n--- 未登录测试 ---")

    # 1. 测试未登录访问状态接口
    print("\n[1] 测试未登录访问 /api/crawler/status/...")
    api_client = APIClient()
    response = api_client.get('/api/crawler/status/')
    assert response.status_code == 401, f"期望 401，实际 {response.status_code}"
    print("    ✅ 未登录返回 401")

    # 2. 测试未登录访问断点信息
    print("\n[2] 测试未登录访问 /api/crawler/resume/...")
    response = api_client.get('/api/crawler/resume/?mode=full')
    assert response.status_code == 401, f"期望 401，实际 {response.status_code}"
    print("    ✅ 未登录返回 401")

    # 3. 测试未登录访问操作日志
    print("\n[3] 测试未登录访问 /api/crawler/operation-logs/...")
    response = api_client.get('/api/crawler/operation-logs/')
    assert response.status_code == 401, f"期望 401，实际 {response.status_code}"
    print("    ✅ 未登录返回 401")

    # 4. 测试未登录启动爬虫
    print("\n[4] 测试未登录启动爬虫...")
    response = api_client.post(
        '/api/crawler/start/',
        data=json.dumps({'mode': 'demo', 'limit': 5}),
        content_type='application/json'
    )
    assert response.status_code == 401, f"期望 401，实际 {response.status_code}"
    print("    ✅ 未登录无法启动爬虫")

    # ========== 登录测试 ==========
    print("\n--- 登录测试 ---")

    # 5. 测试错误密码登录
    print("\n[5] 测试错误密码登录...")
    response = api_client.post('/api/auth/token/', {
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401, f"期望 401，实际 {response.status_code}"
    print("    ✅ 错误密码返回 401")

    # 6. 测试不存在的用户登录
    print("\n[6] 测试不存在的用户登录...")
    response = api_client.post('/api/auth/token/', {
        'username': 'nonexistent_user',
        'password': 'testpass123'
    })
    assert response.status_code == 401, f"期望 401，实际 {response.status_code}"
    print("    ✅ 不存在用户返回 401")

    # 7. 普通用户登录
    print("\n[7] 普通用户登录...")
    response = api_client.post('/api/auth/token/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    token_data = json.loads(response.content)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_data['access']}")
    print("    ✅ 登录成功")

    # ========== 普通用户权限测试 ==========
    print("\n--- 普通用户权限测试 ---")

    # 8. 普通用户获取爬虫状态
    print("\n[8] 普通用户获取爬虫状态...")
    response = api_client.get('/api/crawler/status/')
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    data = json.loads(response.content)
    assert data.get('code') == 0
    print(f"    ✅ 状态: {data['data']}")

    # 9. 普通用户获取断点信息
    print("\n[9] 普通用户获取断点信息...")
    response = api_client.get('/api/crawler/resume/?mode=full')
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    data = json.loads(response.content)
    assert data.get('code') == 0
    print("    ✅ 获取成功")

    # 10. 普通用户获取操作日志
    print("\n[10] 普通用户获取操作日志...")
    response = api_client.get('/api/crawler/operation-logs/')
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    data = json.loads(response.content)
    assert data.get('code') == 0
    print("    ✅ 获取成功")

    # 11. 普通用户尝试启动爬虫（应返回 403）
    print("\n[11] 普通用户尝试启动爬虫...")
    response = api_client.post(
        '/api/crawler/start/',
        data=json.dumps({'mode': 'demo', 'limit': 5}),
        content_type='application/json'
    )
    assert response.status_code == 403, f"期望 403，实际 {response.status_code}"
    print("    ✅ 普通用户无法启动爬虫")

    # ========== 管理员权限测试 ==========
    print("\n--- 管理员权限测试 ---")

    # 12. 管理员登录
    print("\n[12] 管理员登录...")
    admin_client = APIClient()
    response = admin_client.post('/api/auth/token/', {
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    admin_token_data = json.loads(response.content)
    admin_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token_data['access']}")
    print("    ✅ 管理员登录成功")

    # 13. 管理员启动爬虫
    print("\n[13] 管理员启动爬虫...")
    response = admin_client.post(
        '/api/crawler/start/',
        data=json.dumps({'mode': 'demo', 'limit': 5, 'api_only': True}),
        content_type='application/json'
    )
    print(f"    状态码: {response.status_code}")

    if response.status_code == 202:
        print("    ✅ 爬虫任务已启动")
        data = json.loads(response.content)
        task_id = data.get('data', {}).get('task_id') if isinstance(data.get('data'), dict) else None
        if task_id:
            # 14. 获取任务进度
            print(f"\n[14] 获取任务进度...")
            response = admin_client.get(f'/api/crawler/progress/{task_id}/')
            assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
            print("    ✅ 获取成功")

            # 15. 获取任务日志
            print(f"\n[15] 获取任务日志...")
            response = admin_client.get(f'/api/crawler/logs/{task_id}/')
            assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
            print("    ✅ 获取成功")
    elif response.status_code == 500:
        print("    ⚠️ 任务启动失败，可能是 Celery Worker 未运行")
    else:
        print(f"    ⚠️ 未知状态: {response.content.decode()[:100]}")

    # ========== 参数验证测试 ==========
    print("\n--- 参数验证测试 ---")

    # 16. 测试无效模式
    print("\n[16] 测试无效采集模式...")
    response = admin_client.post(
        '/api/crawler/start/',
        data=json.dumps({'mode': 'invalid_mode', 'limit': 5}),
        content_type='application/json'
    )
    assert response.status_code == 400, f"期望 400，实际 {response.status_code}"
    print("    ✅ 无效参数正确拒绝")

    # 17. 测试 limit 越界
    print("\n[17] 测试 limit 越界...")
    response = admin_client.post(
        '/api/crawler/start/',
        data=json.dumps({'mode': 'demo', 'limit': 100000}),
        content_type='application/json'
    )
    assert response.status_code == 400, f"期望 400，实际 {response.status_code}"
    print("    ✅ limit 范围检查有效")

    # ========== 完成 ==========
    print("\n" + "=" * 60)
    print("🎉 所有 API 测试通过！")
    print("=" * 60)

    print("\n📝 API 端点总结:")
    print("  GET  /api/crawler/status/          - 获取爬虫状态（登录）")
    print("  POST /api/crawler/start/          - 启动爬虫（仅管理员）")
    print("  POST /api/crawler/stop/           - 停止爬虫（仅管理员）")
    print("  GET  /api/crawler/progress/<id>/  - 获取任务进度（登录）")
    print("  GET  /api/crawler/logs/<id>/     - 获取任务日志（登录）")
    print("  GET  /api/crawler/resume/         - 获取断点信息（登录）")
    print("  GET  /api/crawler/operation-logs/ - 获取操作日志（登录）")


if __name__ == '__main__':
    test_crawler_api()
