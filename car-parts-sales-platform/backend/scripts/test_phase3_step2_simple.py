#!/usr/bin/env python
"""
简化版 Phase 3 Step 2 测试脚本 - 直接验证 API 端点
"""
import os
import sys
import json

# 设置工作目录
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()


def print_section(title):
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print(f"{'=' * 60}")


def test_api(name, method, url, client, expected=None, data=None):
    """测试单个 API"""
    if method == 'GET':
        response = client.get(url)
    elif method == 'POST':
        response = client.post(url, data=json.dumps(data), content_type='application/json')
    elif method == 'PUT':
        response = client.put(url, data=json.dumps(data), content_type='application/json')
    elif method == 'PATCH':
        response = client.patch(url, data=json.dumps(data), content_type='application/json')
    elif method == 'DELETE':
        response = client.delete(url)

    status = "PASS" if expected is None or response.status_code == expected else "FAIL"
    print(f"[{status}] {method} {name}: HTTP {response.status_code}", end="")

    if expected:
        print(f" (expected {expected})", end="")

    if response.status_code in [200, 201]:
        try:
            data = json.loads(response.content)
            if 'message' in data:
                print(f" - {data.get('message')}")
        except:
            print()
    else:
        try:
            data = json.loads(response.content)
            if 'message' in data:
                print(f" - {data.get('message')}")
        except:
            print()

    return response.status_code in [200, 201] if expected else True


def main():
    print("=" * 60)
    print("Phase 3 Step 2: Content & System API 验证测试")
    print("=" * 60)

    # 创建客户端
    client = Client()

    # 创建管理员用户
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            phone='13800138000',
            password='admin123',
            nickname='测试管理员'
        )
        print(f"\n已创建管理员用户: {admin_user.phone}")
    else:
        print(f"\n使用现有管理员用户: {admin_user.phone}")

    admin_client = Client()
    admin_client.force_login(admin_user)

    all_pass = True

    # ============ Content 模块 ============
    print_section("1. Content - Cases API")

    # 公开 API
    all_pass &= test_api("案例列表", "GET", "/api/content/cases/", client, 200)
    all_pass &= test_api("案例筛选", "GET", "/api/content/cases/?status=published", client, 200)

    # 管理员 API
    case_data = {
        'title': '测试改装案例',
        'summary': '测试摘要',
        'content': '测试内容',
        'status': 'published'
    }
    resp = admin_client.post('/api/content/cases/', data=json.dumps(case_data), content_type='application/json')
    all_pass &= test_api("创建案例", "POST", "/api/content/cases/", admin_client, 201, case_data)

    case_id = None
    if resp.status_code == 201:
        try:
            case_id = json.loads(resp.content).get('data', {}).get('id')
        except:
            pass

    if case_id:
        all_pass &= test_api(f"案例详情(id={case_id})", "GET", f"/api/content/cases/{case_id}/", client, 200)
        all_pass &= test_api(f"更新案例(id={case_id})", "PUT", f"/api/content/cases/{case_id}/", admin_client, 200, {
            'title': '更新后的案例', 'status': 'published'
        })
        all_pass &= test_api(f"删除案例(id={case_id})", "DELETE", f"/api/content/cases/{case_id}/", admin_client, 200)

    print_section("2. Content - FAQs API")

    # 公开 API
    all_pass &= test_api("FAQ列表", "GET", "/api/content/faqs/", client, 200)
    all_pass &= test_api("FAQ分类筛选", "GET", "/api/content/faqs/?category=order", client, 200)

    # 管理员 API
    faq_data = {
        'question': '测试问题？',
        'answer': '这是测试答案',
        'category': 'order',
        'sort_order': 1
    }
    resp = admin_client.post('/api/content/faqs/', data=json.dumps(faq_data), content_type='application/json')
    all_pass &= test_api("创建FAQ", "POST", "/api/content/faqs/", admin_client, 201, faq_data)

    faq_id = None
    if resp.status_code == 201:
        try:
            faq_id = json.loads(resp.content).get('data', {}).get('id')
        except:
            pass

    if faq_id:
        all_pass &= test_api(f"删除FAQ(id={faq_id})", "DELETE", f"/api/content/faqs/{faq_id}/", admin_client, 200)

    # ============ System 模块 ============
    print_section("3. System - Configs API")

    # 公开 API
    all_pass &= test_api("配置列表", "GET", "/api/system/configs/", client, 200)

    # 管理员 API
    config_data = {
        'key': 'site_name',
        'value': '汽车改装件销售平台',
        'description': '网站名称',
        'category': 'basic'
    }
    resp = admin_client.post('/api/system/configs/', data=json.dumps(config_data), content_type='application/json')
    all_pass &= test_api("创建配置", "POST", "/api/system/configs/", admin_client, 201, config_data)

    config_id = None
    if resp.status_code == 201:
        try:
            config_id = json.loads(resp.content).get('data', {}).get('id')
        except:
            pass

    if config_id:
        all_pass &= test_api(f"配置详情(id={config_id})", "GET", f"/api/system/configs/{config_id}/", client, 200)
        all_pass &= test_api(f"删除配置(id={config_id})", "DELETE", f"/api/system/configs/{config_id}/", admin_client, 200)

    print_section("4. System - Messages API")

    # 公开 API (已登录用户)
    all_pass &= test_api("消息列表", "GET", "/api/system/messages/", admin_client, 200)
    all_pass &= test_api("我的消息", "GET", "/api/system/messages/my-messages/", admin_client, 200)

    # 管理员 API
    msg_data = {
        'title': '测试公告',
        'content': '这是测试公告内容',
        'message_type': 'announcement'
    }
    resp = admin_client.post('/api/system/messages/', data=json.dumps(msg_data), content_type='application/json')
    all_pass &= test_api("发送消息", "POST", "/api/system/messages/", admin_client, 201, msg_data)

    msg_id = None
    if resp.status_code == 201:
        try:
            msg_id = json.loads(resp.content).get('data', {}).get('id')
        except:
            pass

    if msg_id:
        all_pass &= test_api(f"消息详情(id={msg_id})", "GET", f"/api/system/messages/{msg_id}/", admin_client, 200)
        all_pass &= test_api(f"标记已读(id={msg_id})", "POST", f"/api/system/messages/{msg_id}/mark-read/", admin_client, 200)
        all_pass &= test_api(f"删除消息(id={msg_id})", "DELETE", f"/api/system/messages/{msg_id}/", admin_client, 200)

    print_section("5. System - Logs API")

    # 管理员 API
    all_pass &= test_api("日志列表", "GET", "/api/system/logs/", admin_client, 200)
    all_pass &= test_api("日志筛选", "GET", "/api/system/logs/?action_type=create", admin_client, 200)

    # ============ 响应格式验证 ============
    print_section("6. 响应格式验证")

    response = client.get('/api/content/cases/')
    try:
        data = json.loads(response.content)
        has_all = all(k in data for k in ['code', 'message', 'data'])
        print(f"  响应格式: {'PASS' if has_all else 'FAIL'} - {list(data.keys())}")
        all_pass &= has_all
    except:
        print("  响应格式: FAIL - 无法解析")
        all_pass = False

    # 总结
    print_section("测试完成")
    status = "[ALL PASSED]" if all_pass else "[SOME FAILED]"
    print(f"\n总体状态: {status}")

    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
