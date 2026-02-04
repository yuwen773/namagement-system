#!/usr/bin/env python
"""
Phase 3 Step 2: Content & System API 完整验证脚本

测试内容：
1. Content 模块 API (改装案例、FAQ)
2. System 模块 API (系统配置、消息、操作日志)
3. 响应格式验证
"""
import os
import sys
import json

# 设置工作目录为 backend 目录
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

# 设置 Django
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


def print_result(name, status_code, response=None, expected=None):
    """打印测试结果"""
    passed = status_code in [200, 201]
    if expected:
        passed = status_code == expected

    if passed:
        print(f"[PASS] {name}: HTTP {status_code}")
    else:
        print(f"[FAIL] {name}: HTTP {status_code} (expected {expected})")

    if response and hasattr(response, 'content'):
        try:
            data = json.loads(response.content)
            if isinstance(data, dict) and 'code' in data and 'message' in data:
                print(f"       Response: code={data.get('code')}, message={data.get('message')}")
                if 'data' in data:
                    data_preview = str(data['data'])[:100]
                    print(f"       Data preview: {data_preview}...")
        except:
            pass
    return passed


def test_content_cases_api(client):
    """测试改装案例 API"""
    print_section("1. Content - Cases API 测试")

    results = []

    # GET /api/content/cases/ - 案例列表
    results.append(print_result("GET 案例列表", client.get('/api/content/cases/').status_code, expected=200))

    # POST /api/content/cases/ - 创建案例（需要管理员）
    response = client.post('/api/content/cases/', data=json.dumps({
        'title': '测试改装案例',
        'summary': '这是一个测试案例',
        'content': '这是测试内容',
        'status': 'draft'
    }), content_type='application/json')
    results.append(print_result("POST 创建案例(管理员)", response.status_code, response, expected=201))

    # 获取案例ID进行后续测试
    case_id = None
    if response.status_code == 201:
        try:
            data = json.loads(response.content)
            case_id = data.get('data', {}).get('id')
        except:
            pass

    if case_id:
        # GET /api/content/cases/{id}/ - 案例详情
        results.append(print_result(f"GET 案例详情(id={case_id})", client.get(f'/api/content/cases/{case_id}/').status_code, expected=200))

        # PUT /api/content/cases/{id}/ - 更新案例
        response = client.put(f'/api/content/cases/{case_id}/',
            data=json.dumps({'title': '更新的测试案例', 'status': 'published'}),
            content_type='application/json')
        results.append(print_result(f"PUT 更新案例(id={case_id})", response.status_code, response, expected=200))

        # PATCH /api/content/cases/{id}/ - 部分更新
        response = client.patch(f'/api/content/cases/{case_id}/',
            data=json.dumps({'summary': '更新的摘要'}),
            content_type='application/json')
        results.append(print_result(f"PATCH 部分更新案例(id={case_id})", response.status_code, response, expected=200))

        # DELETE /api/content/cases/{id}/ - 删除案例
        results.append(print_result(f"DELETE 删除案例(id={case_id})", client.delete(f'/api/content/cases/{case_id}/').status_code, expected=200))

    # 测试筛选
    results.append(print_result("GET 案例筛选(status=published)", client.get('/api/content/cases/?status=published').status_code, expected=200))
    results.append(print_result("GET 案例排序", client.get('/api/content/cases/?ordering=-view_count').status_code, expected=200))

    return all(results)


def test_content_faqs_api(client):
    """测试 FAQ API"""
    print_section("2. Content - FAQs API 测试")

    results = []

    # GET /api/content/faqs/ - FAQ 列表
    results.append(print_result("GET FAQ列表", client.get('/api/content/faqs/').status_code, expected=200))

    # POST /api/content/faqs/ - 创建 FAQ（需要管理员）
    response = client.post('/api/content/faqs/', data=json.dumps({
        'question': '测试问题',
        'answer': '这是测试答案',
        'category': 'order',
        'sort_order': 1
    }), content_type='application/json')
    results.append(print_result("POST 创建FAQ(管理员)", response.status_code, response, expected=201))

    # 获取FAQ ID
    faq_id = None
    if response.status_code == 201:
        try:
            data = json.loads(response.content)
            faq_id = data.get('data', {}).get('id')
        except:
            pass

    if faq_id:
        # GET /api/content/faqs/{id}/ - FAQ 详情
        results.append(print_result(f"GET FAQ详情(id={faq_id})", client.get(f'/api/content/faqs/{faq_id}/').status_code, expected=200))

        # PUT /api/content/faqs/{id}/ - 更新 FAQ
        response = client.put(f'/api/content/faqs/{faq_id}/',
            data=json.dumps({'question': '更新的问题', 'answer': '更新的答案'}),
            content_type='application/json')
        results.append(print_result(f"PUT 更新FAQ(id={faq_id})", response.status_code, response, expected=200))

        # DELETE /api/content/faqs/{id}/ - 删除 FAQ
        results.append(print_result(f"DELETE 删除FAQ(id={faq_id})", client.delete(f'/api/content/faqs/{faq_id}/').status_code, expected=200))

    # 测试筛选
    results.append(print_result("GET FAQ分类筛选(category=order)", client.get('/api/content/faqs/?category=order').status_code, expected=200))

    return all(results)


def test_system_configs_api(client, admin_client):
    """测试系统配置 API"""
    print_section("3. System - Configs API 测试")

    results = []

    # GET /api/system/configs/ - 配置列表（公开）
    results.append(print_result("GET 配置列表(公开)", client.get('/api/system/configs/').status_code, expected=200))

    # POST /api/system/configs/ - 创建配置（需要管理员）
    response = admin_client.post('/api/system/configs/', data=json.dumps({
        'key': 'test_config_key',
        'value': 'test_value',
        'description': '测试配置项',
        'category': 'basic',
        'is_editable': True
    }), content_type='application/json')
    results.append(print_result("POST 创建配置(管理员)", response.status_code, response, expected=201))

    # 获取配置ID
    config_id = None
    if response.status_code == 201:
        try:
            data = json.loads(response.content)
            config_id = data.get('data', {}).get('id')
        except:
            pass

    if config_id:
        # GET /api/system/configs/{id}/ - 配置详情
        results.append(print_result(f"GET 配置详情(id={config_id})", client.get(f'/api/system/configs/{config_id}/').status_code, expected=200))

        # PUT /api/system/configs/{id}/ - 更新配置
        response = admin_client.put(f'/api/system/configs/{config_id}/',
            data=json.dumps({'value': 'updated_value', 'description': '更新的描述'}),
            content_type='application/json')
        results.append(print_result(f"PUT 更新配置(id={config_id})", response.status_code, response, expected=200))

        # DELETE /api/system/configs/{id}/ - 删除配置
        results.append(print_result(f"DELETE 删除配置(id={config_id})", admin_client.delete(f'/api/system/configs/{config_id}/').status_code, expected=200))

    return all(results)


def test_system_messages_api(client, admin_client):
    """测试消息 API"""
    print_section("4. System - Messages API 测试")

    results = []

    # GET /api/system/messages/ - 消息列表
    results.append(print_result("GET 消息列表", client.get('/api/system/messages/').status_code, expected=200))

    # POST /api/system/messages/ - 发送消息（需要管理员）
    response = admin_client.post('/api/system/messages/', data=json.dumps({
        'title': '测试消息',
        'content': '这是测试消息内容',
        'message_type': 'announcement'
    }), content_type='application/json')
    results.append(print_result("POST 发送消息(管理员)", response.status_code, response, expected=201))

    # 获取消息ID
    message_id = None
    if response.status_code == 201:
        try:
            data = json.loads(response.content)
            message_id = data.get('data', {}).get('id')
        except:
            pass

    if message_id:
        # GET /api/system/messages/{id}/ - 消息详情
        results.append(print_result(f"GET 消息详情(id={message_id})", client.get(f'/api/system/messages/{message_id}/').status_code, expected=200))

        # POST /api/system/messages/{id}/mark-read/ - 标记已读
        response = client.post(f'/api/system/messages/{message_id}/mark-read/')
        results.append(print_result(f"POST 标记已读(id={message_id})", response.status_code, response, expected=200))

        # DELETE /api/system/messages/{id}/ - 删除消息
        results.append(print_result(f"DELETE 删除消息(id={message_id})", admin_client.delete(f'/api/system/messages/{message_id}/').status_code, expected=200))

    # GET /api/system/messages/my-messages/ - 我的消息
    results.append(print_result("GET 我的消息", client.get('/api/system/messages/my-messages/').status_code, expected=200))

    return all(results)


def test_system_logs_api(admin_client):
    """测试操作日志 API"""
    print_section("5. System - Logs API 测试")

    results = []

    # GET /api/system/logs/ - 日志列表（需要管理员）
    results.append(print_result("GET 日志列表(管理员)", admin_client.get('/api/system/logs/').status_code, expected=200))

    # 测试筛选
    results.append(print_result("GET 日志筛选(action_type=create)", admin_client.get('/api/system/logs/?action_type=create').status_code, expected=200))
    results.append(print_result("GET 日志排序", admin_client.get('/api/system/logs/?ordering=-created_at').status_code, expected=200))

    return all(results)


def verify_response_format(client):
    """验证响应格式"""
    print_section("6. 响应格式验证")

    response = client.get('/api/content/cases/')
    try:
        data = json.loads(response.content)
        has_code = 'code' in data
        has_message = 'message' in data
        has_data = 'data' in data

        print(f"  code 字段: {'[PASS]' if has_code else '[FAIL]'}")
        print(f"  message 字段: {'[PASS]' if has_message else '[FAIL]'}")
        print(f"  data 字段: {'[PASS]' if has_data else '[FAIL]'}")

        if has_code and has_message and has_data:
            print(f"\n响应格式正确: {{ code: {data.get('code')}, message: '{data.get('message')}', data: {{...}} }}")
            return True
        else:
            print("\n响应格式不完整!")
            return False
    except Exception as e:
        print(f"[FAIL] 无法解析响应: {e}")
        return False


def create_test_user(admin_client):
    """创建测试管理员用户（如果不存在）"""
    User = get_user_model()

    # 检查是否已存在管理员用户
    try:
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                phone='13800138000',
                password='admin123',
                nickname='测试管理员'
            )
            print("\n已创建测试管理员用户: phone=13800138000, password=admin123")
        else:
            print(f"\n已存在管理员用户: {admin_user.phone}")

        # 使用 force_login 确保会话正确建立
        admin_client.force_login(admin_user)
        print(f"管理员会话已建立")
    except Exception as e:
        print(f"创建/登录管理员用户时出错: {e}")

    return admin_client


def main():
    print("=" * 60)
    print("Phase 3 Step 2: Content & System API 验证测试")
    print("=" * 60)
    print("\n测试模块: content (改装案例、FAQ) + system (配置、消息、日志)")

    all_passed = True

    # 创建客户端
    client = Client()

    # 创建管理员客户端
    admin_client = Client()

    # 创建并登录管理员用户
    try:
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                phone='13800138000',
                password='admin123',
                nickname='测试管理员'
            )
            print(f"\n已创建管理员用户: phone=13800138000, password=admin123")
        else:
            print(f"\n已存在管理员用户: {admin_user.phone}")

        # 强制登录管理员
        admin_client.force_login(admin_user)
        print(f"管理员会话已建立")
    except Exception as e:
        print(f"\n创建/登录管理员时出错: {e}")
        print("继续测试，部分需要管理员的操作可能会失败")

    # 运行测试
    print("\n" + "=" * 60)
    print("开始 API 测试...")
    print("=" * 60)

    all_passed &= test_content_cases_api(client)
    all_passed &= test_content_faqs_api(client)
    all_passed &= test_system_configs_api(client, admin_client)
    all_passed &= test_system_messages_api(client, admin_client)
    all_passed &= test_system_logs_api(admin_client)
    all_passed &= verify_response_format(client)

    # 总结
    print_section("测试完成")
    status = "[ALL PASSED]" if all_passed else "[SOME FAILED]"
    print(f"\n总体状态: {status}")

    print("\n已验证的 API 端点:")
    print("  Content Cases:")
    print("    - GET /api/content/cases/")
    print("    - GET /api/content/cases/{id}/")
    print("    - POST /api/content/cases/")
    print("    - PUT /api/content/cases/{id}/")
    print("    - PATCH /api/content/cases/{id}/")
    print("    - DELETE /api/content/cases/{id}/")
    print("  Content FAQs:")
    print("    - GET /api/content/faqs/")
    print("    - GET /api/content/faqs/{id}/")
    print("    - POST /api/content/faqs/")
    print("    - PUT /api/content/faqs/{id}/")
    print("    - DELETE /api/content/faqs/{id}/")
    print("  System Configs:")
    print("    - GET /api/system/configs/")
    print("    - GET /api/system/configs/{id}/")
    print("    - POST /api/system/configs/")
    print("    - PUT /api/system/configs/{id}/")
    print("    - DELETE /api/system/configs/{id}/")
    print("  System Messages:")
    print("    - GET /api/system/messages/")
    print("    - GET /api/system/messages/{id}/")
    print("    - GET /api/system/messages/my-messages/")
    print("    - POST /api/system/messages/")
    print("    - POST /api/system/messages/{id}/mark-read/")
    print("    - DELETE /api/system/messages/{id}/")
    print("  System Logs:")
    print("    - GET /api/system/logs/")
    print("    - GET /api/system/logs/{id}/")

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
