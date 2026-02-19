#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分析登录和注册接口的错误消息是否友好"""
import os
import sys
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality_system.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.utils.translation import activate
activate('zh-hans')

from apps.accounts.serializers import LoginSerializer, RegisterSerializer
from apps.accounts.views import LoginView, RegisterView

# 存储
unfriendly_errors = []

def test_scenario(endpoint, scenario, data, issue, suggested):
    """测试一个场景"""
    if 'login' in endpoint.lower():
        serializer = LoginSerializer(data=data)
    else:
        serializer = RegisterSerializer(data=data)

    serializer.is_valid()

    # 获取第一个错误
    if serializer.errors:
        first_field = list(serializer.errors.keys())[0]
        first_error = serializer.errors[first_field][0]
        current_message = str(first_error)

        unfriendly_errors.append({
            "endpoint": endpoint,
            "scenario": scenario,
            "current_message": current_message,
            "issue": issue,
            "suggested_message": suggested
        })

# 测试各种场景

# 1. 登录 - 缺少用户名
test_scenario(
    "POST /api/auth/login/",
    "缺少用户名",
    {'password': 'test123'},
    "DRF 默认消息，比较生硬",
    "请输入用户名"
)

# 2. 登录 - 缺少密码
test_scenario(
    "POST /api/auth/login/",
    "缺少密码",
    {'username': 'testuser'},
    "DRF 默认消息，比较生硬",
    "请输入密码"
)

# 3. 登录 - 用户名不存在（需要自定义，但当前代码返回401）
# 这在 views.py 第86行已处理："用户名或密码错误" - 友好

# 4. 登录 - 密码错误（需要自定义，但当前代码返回401）
# 这在 views.py 第86行已处理："用户名或密码错误" - 友好

# 5. 注册 - 缺少必填字段
test_scenario(
    "POST /api/auth/register/",
    "缺少用户名",
    {'password': 'test123456', 'email': 'test@example.com'},
    "DRF 默认消息，比较生硬",
    "请输入用户名"
)

test_scenario(
    "POST /api/auth/register/",
    "缺少密码",
    {'username': 'testuser', 'email': 'test@example.com'},
    "DRF 默认消息，比较生硬",
    "请输入密码"
)

test_scenario(
    "POST /api/auth/register/",
    "缺少邮箱",
    {'username': 'testuser', 'password': 'test123456'},
    "DRF 默认消息，比较生硬",
    "请输入邮箱地址"
)

# 6. 注册 - 密码长度不足
test_scenario(
    "POST /api/auth/register/",
    "密码长度不足（少于6位）",
    {'username': 'testuser', 'password': '12345', 'email': 'test@example.com'},
    "DRF 默认消息，比较生硬",
    "密码长度至少需要6位"
)

# 7. 注册 - 邮箱格式错误
test_scenario(
    "POST /api/auth/register/",
    "邮箱格式错误",
    {'username': 'testuser2', 'password': 'test123456', 'email': 'invalid-email'},
    "DRF 默认消息，比较生硬",
    "请输入有效的邮箱地址"
)

# 8. 注册 - 用户名长度不足
test_scenario(
    "POST /api/auth/register/",
    "用户名长度不足（少于3位）",
    {'username': 'ab', 'password': 'test123456', 'email': 'test@example.com'},
    "DRF 默认消息，比较生硬",
    "用户名长度至少需要3位"
)

# 9. 注册 - 用户名已存在（自定义验证）
test_scenario(
    "POST /api/auth/register/",
    "用户名已存在",
    {'username': 'admin', 'password': 'test123456', 'email': 'test2@example.com'},
    "自定义消息，但可以更友好",
    "该用户名已被注册，请更换其他用户名"
)

# 输出结果
print(json.dumps(unfriendly_errors, ensure_ascii=False, indent=4))
