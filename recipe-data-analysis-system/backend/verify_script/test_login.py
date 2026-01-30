"""
用户登录接口测试脚本

测试用户登录功能是否正常工作。
"""
import os
import sys
import json

# Windows 控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import django

# 设置 Django settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 添加项目路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# 设置 Django
django.setup()

from django.test import Client, override_settings
from accounts.models import User


# 清理测试数据
def cleanup_test_users():
    """清理测试用户"""
    User.objects.filter(username__in=['testuser_login', 'testuser_login2']).delete()


def create_test_users():
    """创建测试用户"""
    print("创建测试用户...")
    # 创建测试用户1
    user1 = User.objects.create_user(
        username='testuser_login',
        email='testlogin@example.com',
        password='Test1234'
    )
    user1.is_active = True
    user1.save()

    # 创建测试用户2（未激活）
    user2 = User.objects.create_user(
        username='testuser_login2',
        email='testlogin2@example.com',
        password='Test1234'
    )
    user2.is_active = False
    user2.save()

    print("  ✓ 创建 2 个测试用户")


@override_settings(ALLOWED_HOSTS=['*'])
def test_login_success():
    """测试成功登录"""
    print("\n[测试] 正确的用户名密码登录...")
    client = Client()
    response = client.post(
        '/api/accounts/login/',
        data=json.dumps({
            'username': 'testuser_login',
            'password': 'Test1234'
        }),
        content_type='application/json'
    )

    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 200:
            token = data.get('data', {}).get('token')
            user_info = data.get('data', {}).get('user', {})
            print(f"  ✓ 登录成功")
            print(f"  ✓ Token: {token[:50]}..." if token else "  ✗ Token 缺失")
            print(f"  ✓ 用户名: {user_info.get('username')}")
            print(f"  ✓ 角色: {user_info.get('role')}")
            print(f"  ✓ 邮箱: {user_info.get('email')}")
            # 验证 last_login 已更新
            user = User.objects.get(username='testuser_login')
            if user.last_login:
                print(f"  ✓ 最后登录时间已更新: {user.last_login}")
            return True
        else:
            print(f"  ✗ 响应码错误: {data.get('code')}")
            print(f"  ✗ 消息: {data.get('message')}")
            return False
    else:
        print(f"  ✗ HTTP 状态码错误: {response.status_code}")
        print(f"  ✗ 响应: {response.content.decode()}")
        return False


@override_settings(ALLOWED_HOSTS=['*'])
def test_login_wrong_password():
    """测试错误密码登录"""
    print("\n[测试] 错误的用户名密码登录...")
    client = Client()
    response = client.post(
        '/api/accounts/login/',
        data=json.dumps({
            'username': 'testuser_login',
            'password': 'WrongPassword'
        }),
        content_type='application/json'
    )

    if response.status_code == 400:
        data = response.json()
        if data.get('code') == 400:
            print(f"  ✓ 正确拒绝登录")
            print(f"  ✓ 消息: {data.get('message')}")
            return True
        else:
            print(f"  ✗ 响应码错误: {data.get('code')}")
            return False
    else:
        print(f"  ✗ HTTP 状态码错误: {response.status_code}")
        print(f"  ✗ 应返回 400，实际: {response.status_code}")
        return False


@override_settings(ALLOWED_HOSTS=['*'])
def test_login_nonexistent_user():
    """测试不存在的用户登录"""
    print("\n[测试] 不存在的用户登录...")
    client = Client()
    response = client.post(
        '/api/accounts/login/',
        data=json.dumps({
            'username': 'nonexistent_user',
            'password': 'Test1234'
        }),
        content_type='application/json'
    )

    if response.status_code == 400:
        data = response.json()
        if data.get('code') == 400:
            print(f"  ✓ 正确拒绝登录")
            print(f"  ✓ 消息: {data.get('message')}")
            return True
        else:
            print(f"  ✗ 响应码错误: {data.get('code')}")
            return False
    else:
        print(f"  ✗ HTTP 状态码错误: {response.status_code}")
        return False


@override_settings(ALLOWED_HOSTS=['*'])
def test_login_inactive_user():
    """测试未激活用户登录"""
    print("\n[测试] 未激活用户登录...")
    client = Client()
    response = client.post(
        '/api/accounts/login/',
        data=json.dumps({
            'username': 'testuser_login2',
            'password': 'Test1234'
        }),
        content_type='application/json'
    )

    if response.status_code == 400:
        data = response.json()
        if data.get('code') == 400:
            print(f"  ✓ 正确拒绝登录")
            print(f"  ✓ 消息: {data.get('message')}")
            return True
        else:
            print(f"  ✗ 响应码错误: {data.get('code')}")
            return False
    else:
        print(f"  ✗ HTTP 状态码错误: {response.status_code}")
        return False


@override_settings(ALLOWED_HOSTS=['*'])
def test_login_missing_fields():
    """测试缺少必填字段"""
    print("\n[测试] 缺少必填字段...")
    client = Client()

    # 缺少密码
    print("\n  [子测试] 缺少密码...")
    response = client.post(
        '/api/accounts/login/',
        data=json.dumps({
            'username': 'testuser_login'
        }),
        content_type='application/json'
    )
    if response.status_code == 400:
        print("    ✓ 正确拒绝（缺少密码）")
    else:
        print(f"    ✗ 应返回 400，实际: {response.status_code}")
        return False

    # 缺少用户名
    print("\n  [子测试] 缺少用户名...")
    response = client.post(
        '/api/accounts/login/',
        data=json.dumps({
            'password': 'Test1234'
        }),
        content_type='application/json'
    )
    if response.status_code == 400:
        print("    ✓ 正确拒绝（缺少用户名）")
        return True
    else:
        print(f"    ✗ 应返回 400，实际: {response.status_code}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("用户登录接口测试")
    print("=" * 60)

    results = []

    try:
        # 清理旧数据
        cleanup_test_users()

        # 创建测试用户
        create_test_users()

        # 运行测试
        results.append(("正确密码登录", test_login_success()))
        results.append(("错误密码登录", test_login_wrong_password()))
        results.append(("不存在用户登录", test_login_nonexistent_user()))
        results.append(("未激活用户登录", test_login_inactive_user()))
        results.append(("缺少必填字段", test_login_missing_fields()))

        # 清理测试数据
        cleanup_test_users()

        # 打印测试结果汇总
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)

        passed = 0
        failed = 0
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {status}  {test_name}")
            if result:
                passed += 1
            else:
                failed += 1

        print(f"\n总计: {passed} 通过, {failed} 失败")

        if failed == 0:
            print("\n" + "=" * 60)
            print("[OK] 所有测试通过！登录功能正常")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("[FAIL] 部分测试失败，请检查登录功能")
            print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        # 确保清理测试数据
        cleanup_test_users()


if __name__ == "__main__":
    run_all_tests()
