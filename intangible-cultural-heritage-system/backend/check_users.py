#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritage_system.settings')
django.setup()

from apps.users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

print(f'Total users: {User.objects.count()}')
print(f'Total profiles: {UserProfile.objects.count()}')
print('Users:')
for u in User.objects.all()[:10]:
    role = u.profile.role if hasattr(u, 'profile') else 'N/A'
    active = u.profile.is_active if hasattr(u, 'profile') else 'N/A'
    email = u.profile.email if hasattr(u, 'profile') else 'N/A'
    print(f'  - {u.username} (role: {role}, active: {active}, email: {email})')
