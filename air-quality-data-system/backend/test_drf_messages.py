#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality_system.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.utils.translation import activate
activate('zh-hans')

# 测试 DRF 默认错误消息
print("=" * 60)
print("DRF 默认错误消息（中文）")
print("=" * 60)

from rest_framework.fields import CharField, EmailField

print("\nCharField 错误消息:")
cf = CharField(min_length=3, max_length=20)
print(f"  - required: {cf.error_messages['required']}")
print(f"  - blank: {cf.error_messages['blank']}")
print(f"  - min_length: {cf.error_messages['min_length']}")
print(f"  - max_length: {cf.error_messages['max_length']}")

print("\nEmailField 错误消息:")
ef = EmailField()
print(f"  - invalid: {ef.error_messages['invalid']}")

# 测试实际验证
print("\n" + "=" * 60)
print("实际验证错误消息")
print("=" * 60)

from apps.accounts.serializers import LoginSerializer, RegisterSerializer

print("\n【登录】缺少用户名:")
s = LoginSerializer(data={'password': 'test123'})
s.is_valid()
print(f"  {s.errors['username'][0]}")

print("\n【登录】缺少密码:")
s = LoginSerializer(data={'username': 'test'})
s.is_valid()
print(f"  {s.errors['password'][0]}")

print("\n【注册】缺少用户名:")
s = RegisterSerializer(data={'password': 'test123456', 'email': 'test@example.com'})
s.is_valid()
print(f"  {s.errors['username'][0]}")

print("\n【注册】缺少密码:")
s = RegisterSerializer(data={'username': 'testuser', 'email': 'test@example.com'})
s.is_valid()
print(f"  {s.errors['password'][0]}")

print("\n【注册】缺少邮箱:")
s = RegisterSerializer(data={'username': 'testuser', 'password': 'test123456'})
s.is_valid()
print(f"  {s.errors['email'][0]}")

print("\n【注册】用户名太短（<3字符）:")
s = RegisterSerializer(data={'username': 'ab', 'password': 'test123456', 'email': 'test@example.com'})
s.is_valid()
print(f"  {s.errors['username'][0]}")

print("\n【注册】密码太短（<6字符）:")
s = RegisterSerializer(data={'username': 'testuser', 'password': '12345', 'email': 'test@example.com'})
s.is_valid()
if 'password' in s.errors:
    print(f"  {s.errors['password'][0]}")
elif 'username' in s.errors:
    print(f"  {s.errors['username'][0]}")

print("\n【注册】邮箱格式错误:")
s = RegisterSerializer(data={'username': 'testuser2', 'password': 'test123456', 'email': 'invalid-email'})
s.is_valid()
print(f"  {s.errors['email'][0]}")

print("\n【注册】用户名已存在:")
s = RegisterSerializer(data={'username': 'admin', 'password': 'test123456', 'email': 'test2@example.com'})
s.is_valid()
print(f"  {s.errors['username'][0]}")

print("\n" + "=" * 60)
