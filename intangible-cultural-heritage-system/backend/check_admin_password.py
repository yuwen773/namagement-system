#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritage_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 检查并重置 admin 密码
admin = User.objects.filter(username='admin').first()
if admin:
    admin.set_password('password123')
    admin.save()
    print(f"Admin password reset to 'password123'")
else:
    print("No admin user found")
