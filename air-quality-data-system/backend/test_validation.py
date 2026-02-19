#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试序列化器验证错误消息"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality_system.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from apps.accounts.serializers import LoginSerializer, RegisterSerializer

# 从 views.py 复制的函数
def _raise_serializer_validation_error(errors: dict):
    first_field, first_errors = next(iter(errors.items()))
    if isinstance(first_errors, (list, tuple)) and first_errors:
        message = str(first_errors[0])
    else:
        message = str(first_errors)
    print(f"字段: {first_field}")
    print(f"错误: {message}")

def test_error_messages():
    """测试各种错误场景的错误消息"""

    print("=" * 80)
    print("登录接口错误消息测试")
    print("=" * 80)

    # 测试1: 登录 - 缺少用户名
    print("\n【测试1】登录 - 缺少用户名")
    print("-" * 40)
    s = LoginSerializer(data={'password': 'test123'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试2: 登录 - 缺少密码
    print("\n【测试2】登录 - 缺少密码")
    print("-" * 40)
    s = LoginSerializer(data={'username': 'testuser'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    print("\n" + "=" * 80)
    print("注册接口错误消息测试")
    print("=" * 80)

    # 测试3: 注册 - 缺少用户名
    print("\n【测试3】注册 - 缺少用户名")
    print("-" * 40)
    s = RegisterSerializer(data={'password': 'test123456', 'email': 'test@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试4: 注册 - 缺少密码
    print("\n【测试4】注册 - 缺少密码")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'newuser123', 'email': 'test@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试5: 注册 - 缺少邮箱
    print("\n【测试5】注册 - 缺少邮箱")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'newuser123', 'password': 'test123456'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试6: 注册 - 用户名太短
    print("\n【测试6】注册 - 用户名太短（少于3个字符）")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'ab', 'password': 'test123456', 'email': 'test@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试7: 注册 - 密码太短
    print("\n【测试7】注册 - 密码太短（少于6个字符）")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'newuser123', 'password': '12345', 'email': 'test@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试8: 注册 - 邮箱格式错误
    print("\n【测试8】注册 - 邮箱格式错误")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'newuser123', 'password': 'test123456', 'email': 'invalid-email'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试9: 注册 - 用户名已存在（需要先创建一个用户）
    print("\n【测试9】注册 - 用户名已存在")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'admin', 'password': 'test123456', 'email': 'admin2@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试10: 注册 - 用户名太长
    print("\n【测试10】注册 - 用户名太长（超过20个字符）")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'a' * 25, 'password': 'test123456', 'email': 'test@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    # 测试11: 注册 - 密码太长
    print("\n【测试11】注册 - 密码太长（超过20个字符）")
    print("-" * 40)
    s = RegisterSerializer(data={'username': 'newuser123', 'password': 'a' * 25, 'email': 'test@example.com'})
    if not s.is_valid():
        _raise_serializer_validation_error(s.errors)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == '__main__':
    test_error_messages()
