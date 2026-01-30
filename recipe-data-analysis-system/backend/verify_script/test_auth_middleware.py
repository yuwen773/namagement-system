"""
JWT 认证中间件测试脚本

测试 Token 验证中间件的各种场景。
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


def print_header(text):
    """打印标题"""
    print(f"\n{'=' * 60}")
    print(f"{text}")
    print('=' * 60)


def print_success(text):
    """打印成功信息"""
    print(f"  [OK] {text}")


def print_error(text):
    """打印错误信息"""
    print(f"  [FAIL] {text}")


def print_info(text):
    """打印信息"""
    print(f"  [INFO] {text}")


def create_test_user():
    """创建测试用户"""
    print_header("创建测试用户")

    # 删除已存在的测试用户
    User.objects.filter(username='auth_test_user').delete()

    # 创建新用户
    user = User.objects.create_user(
        username='auth_test_user',
        email='authtest@example.com',
        password='AuthTest1234'
    )
    print_success(f"创建测试用户: {user.username}")

    # 激活用户
    user.is_active = True
    user.save()
    print_success("用户已激活")

    return user


def login_and_get_token(user):
    """登录并获取 Token"""
    print_header("获取 JWT Token")

    # 生成 JWT Token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    print_info(f"Access Token: {access_token[:50]}...")
    print_info(f"Refresh Token: {refresh_token[:50]}...")

    return access_token, refresh_token


def test_valid_token(access_token, base_url):
    """测试有效 Token"""
    print_header("[测试] 有效 Token 访问受保护接口")

    import requests

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'{base_url}/api/accounts/me/', headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print_success("请求成功")
            print_info(f"用户名: {data['data']['username']}")
            print_info(f"邮箱: {data['data']['email']}")
            print_info(f"角色: {data['data']['role']}")
            return True
        else:
            print_error(f"请求失败，状态码: {response.status_code}")
            print_info(f"响应: {response.text}")
            return False

    except Exception as e:
        print_error(f"请求异常: {str(e)}")
        return False


def test_no_token(base_url):
    """测试无 Token 访问"""
    print_header("[测试] 无 Token 访问受保护接口")

    import requests

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'{base_url}/api/accounts/me/', headers=headers, timeout=5)

        if response.status_code == 401:
            print_success("正确拒绝访问 (401)")
            print_info(f"错误消息: {response.json().get('message', 'N/A')}")
            return True
        else:
            print_error(f"应该返回 401，实际返回: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"请求异常: {str(e)}")
        return False


def test_invalid_token(base_url):
    """测试无效 Token"""
    print_header("[测试] 无效 Token 访问受保护接口")

    import requests

    headers = {
        'Authorization': 'Bearer invalid_token_12345',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'{base_url}/api/accounts/me/', headers=headers, timeout=5)

        if response.status_code == 401:
            print_success("正确拒绝访问 (401)")
            print_info(f"错误消息: {response.json().get('message', 'N/A')}")
            return True
        else:
            print_error(f"应该返回 401，实际返回: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"请求异常: {str(e)}")
        return False


def test_wrong_token_format(base_url, access_token):
    """测试错误的 Token 格式"""
    print_header("[测试] 错误的 Token 格式")

    import requests

    # 测试没有 'Bearer ' 前缀
    headers = {
        'Authorization': access_token,  # 缺少 'Bearer ' 前缀
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'{base_url}/api/accounts/me/', headers=headers, timeout=5)

        if response.status_code == 401:
            print_success("正确拒绝访问 (401) - 缺少 Bearer 前缀")
            return True
        else:
            print_error(f"应该返回 401，实际返回: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"请求异常: {str(e)}")
        return False


def test_inactive_user(base_url):
    """测试已禁用用户"""
    print_header("[测试] 已禁用用户访问")

    import requests

    # 禁用测试用户
    user = User.objects.get(username='auth_test_user')
    user.is_active = False
    user.save()

    # 重新登录获取 Token（已禁用用户的 Token）
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'{base_url}/api/accounts/me/', headers=headers, timeout=5)

        # 恢复用户状态
        user.is_active = True
        user.save()

        if response.status_code == 401:
            print_success("正确拒绝访问 (401) - 用户已禁用")
            print_info(f"错误消息: {response.json().get('message', 'N/A')}")
            return True
        else:
            print_error(f"应该返回 401，实际返回: {response.status_code}")
            return False

    except Exception as e:
        # 恢复用户状态
        user.is_active = True
        user.save()
        print_error(f"请求异常: {str(e)}")
        return False


def main():
    """主函数"""
    print_header("JWT 认证中间件测试")

    # 测试基础 URL
    base_url = 'http://localhost:8000'
    print_info(f"测试服务器: {base_url}")

    # 结果统计
    results = []

    # 创建测试用户
    user = create_test_user()

    # 获取 Token
    access_token, refresh_token = login_and_get_token(user)

    # 运行测试
    print("\n开始测试...\n")

    # 测试 1: 有效 Token
    result = test_valid_token(access_token, base_url)
    results.append(('有效 Token', result))

    # 测试 2: 无 Token
    result = test_no_token(base_url)
    results.append(('无 Token', result))

    # 测试 3: 无效 Token
    result = test_invalid_token(base_url)
    results.append(('无效 Token', result))

    # 测试 4: 错误的 Token 格式
    result = test_wrong_token_format(base_url, access_token)
    results.append(('错误 Token 格式', result))

    # 测试 5: 已禁用用户
    result = test_inactive_user(base_url)
    results.append(('已禁用用户', result))

    # 打印测试结果汇总
    print_header("测试结果汇总")

    passed = 0
    failed = 0

    for name, result in results:
        if result:
            print_success(f"PASS  {name}")
            passed += 1
        else:
            print_error(f"FAIL  {name}")
            failed += 1

    print()
    print(f"总计: {passed} 通过, {failed} 失败")

    if failed == 0:
        print_header("[OK] 所有测试通过！认证中间件功能正常")
    else:
        print_header("[FAIL] 部分测试失败，请检查日志")

    # 清理测试用户
    print()
    print_info("清理测试数据...")
    User.objects.filter(username='auth_test_user').delete()
    print_success("测试用户已删除")


if __name__ == '__main__':
    main()
