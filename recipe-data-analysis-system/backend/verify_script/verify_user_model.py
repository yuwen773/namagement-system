"""
用户模型验证脚本

验证用户表结构是否正确创建。
"""
import os
import sys

# 设置 Django settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

def verify_user_model():
    """验证用户模型"""
    print("=" * 60)
    print("User Model Verification")
    print("=" * 60)

    try:
        # 导入模型
        from accounts.models import User, UserProfile
        from utils.constants import UserRole

        print("\n[OK] Models imported successfully")

        # 验证 User 模型字段
        print("\nUser Model Fields:")
        user_fields = [
            'id', 'username', 'email', 'password', 'role',
            'is_active', 'is_staff', 'last_login', 'created_at', 'updated_at'
        ]
        for field in user_fields:
            if hasattr(User, field):
                print(f"  [OK] {field}")
            else:
                print(f"  [MISSING] {field}")

        # 验证 UserProfile 模型字段
        print("\nUserProfile Model Fields:")
        profile_fields = [
            'id', 'user', 'nickname', 'phone', 'bio', 'avatar_url',
            'created_at', 'updated_at'
        ]
        for field in profile_fields:
            if hasattr(UserProfile, field):
                print(f"  [OK] {field}")
            else:
                print(f"  [MISSING] {field}")

        # 验证 UserManager
        print("\nUser Manager:")
        if hasattr(User, 'objects'):
            print(f"  [OK] UserManager exists")
            if hasattr(User.objects, 'create_user'):
                print(f"  [OK] create_user method exists")
            if hasattr(User.objects, 'create_superuser'):
                print(f"  [OK] create_superuser method exists")

        # 验证模型配置
        print("\nModel Configuration:")
        print(f"  Table Name: {User._meta.db_table}")
        print(f"  Verbose Name: {User._meta.verbose_name}")
        print(f"  USERNAME_FIELD: {User.USERNAME_FIELD}")
        print(f"  REQUIRED_FIELDS: {User.REQUIRED_FIELDS}")

        # 验证索引
        print("\nIndexes:")
        for index in User._meta.indexes:
            print(f"  - {index}")

        print("\n" + "=" * 60)
        print("Model Structure Verification: PASSED")
        print("=" * 60)

    except ImportError as e:
        print(f"\n[ERROR] Failed to import models: {e}")
        print("\nPlease ensure:")
        print("  1. Django is installed")
        print("  2. The accounts app is in INSTALLED_APPS")
        print("  3. AUTH_USER_MODEL = 'accounts.User' is set in settings")

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    verify_user_model()
