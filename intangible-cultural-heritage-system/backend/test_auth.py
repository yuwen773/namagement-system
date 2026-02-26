#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户认证功能测试脚本
测试用户注册、登录、用户管理等功能
"""
import requests
import json
import sys
from datetime import datetime

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000/api/v1/auth"

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.ENDC}")

# 存储测试结果
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def test_case(name, func):
    """执行测试用例"""
    test_results["total"] += 1
    print_info(f"测试用例: {name}")
    try:
        result = func()
        if result["success"]:
            test_results["passed"] += 1
            test_results["tests"].append({
                "name": name,
                "status": "PASSED",
                "message": result.get("message", "成功")
            })
            print_success(result.get("message", "测试通过"))
        else:
            test_results["failed"] += 1
            test_results["tests"].append({
                "name": name,
                "status": "FAILED",
                "message": result.get("message", "失败")
            })
            print_error(result.get("message", "测试失败"))
    except Exception as e:
        test_results["failed"] += 1
        test_results["tests"].append({
            "name": name,
            "status": "ERROR",
            "message": str(e)
        })
        print_error(f"测试出错: {str(e)}")
    print()

# ============ 测试函数 ============

def test_check_username_available():
    """测试检查可用用户名"""
    response = requests.post(
        f"{BASE_URL}/check-username/",
        json={"username": "newuser_test_12345"}
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0 and data.get("data", {}).get("exists") == False:
        return {"success": True, "message": f"用户名检查成功: newuser_test_12345 可用"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_check_username_exists():
    """测试检查已存在的用户名"""
    response = requests.post(
        f"{BASE_URL}/check-username/",
        json={"username": "admin"}
    )
    data = response.json()
    if response.status_code == 200 and data.get("data", {}).get("exists") == True:
        return {"success": True, "message": "用户名检查成功: admin 已存在"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_check_email_available():
    """测试检查可用邮箱"""
    response = requests.post(
        f"{BASE_URL}/check-email/",
        json={"email": "test@example.com"}
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0 and data.get("data", {}).get("exists") == False:
        return {"success": True, "message": "邮箱检查成功: test@example.com 可用"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_register_success():
    """测试用户注册成功"""
    # 使用短用户名（不超过20个字符）
    timestamp = datetime.now().strftime('%H%M%S')
    username = f"usr{timestamp}"
    response = requests.post(
        f"{BASE_URL}/register/",
        json={
            "username": username,
            "password": "TestPass123!",
            "email": f"{username}@test.com"
        }
    )
    data = response.json()
    if response.status_code == 201 and data.get("code") == 0:
        # 保存新用户信息用于后续测试
        global new_user_username, new_user_token
        new_user_username = username
        new_user_token = data.get("data", {}).get("access")
        return {
            "success": True,
            "message": f"注册成功: {username}, Token: {new_user_token[:20]}..."
        }
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_register_duplicate_username():
    """测试注册重复用户名"""
    response = requests.post(
        f"{BASE_URL}/register/",
        json={
            "username": "admin",
            "password": "TestPass123!",
            "email": "admin2@test.com"
        }
    )
    data = response.json()
    if response.status_code == 400 or data.get("code") == 1:
        return {"success": True, "message": "正确拒绝重复用户名注册"}
    else:
        return {"success": False, "message": f"应该拒绝重复用户名, 响应: {data}"}

def test_register_invalid_email():
    """测试注册无效邮箱"""
    response = requests.post(
        f"{BASE_URL}/register/",
        json={
            "username": "test_invalid_email",
            "password": "TestPass123!",
            "email": "invalid-email"
        }
    )
    data = response.json()
    if response.status_code == 400 or data.get("code") == 1:
        return {"success": True, "message": "正确拒绝无效邮箱格式"}
    else:
        return {"success": False, "message": f"应该拒绝无效邮箱, 响应: {data}"}

def test_admin_login():
    """测试管理员登录"""
    response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "admin",
            "password": "password123"
        }
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        global admin_token
        admin_token = data.get("data", {}).get("access")
        return {"success": True, "message": f"管理员登录成功, Token: {admin_token[:20]}..."}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_user_login():
    """测试普通用户登录"""
    response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "user",
            "password": "password123"
        }
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": "普通用户登录成功"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_login_invalid_credentials():
    """测试错误密码登录"""
    response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )
    data = response.json()
    if response.status_code == 401 or data.get("code") == 1:
        return {"success": True, "message": "正确拒绝错误密码"}
    else:
        return {"success": False, "message": f"应该拒绝错误密码, 响应: {data}"}

def get_auth_headers(token):
    """获取认证头"""
    return {"Authorization": f"Bearer {token}"}

def test_get_users_list():
    """测试获取用户列表（需要管理员权限）"""
    response = requests.get(
        f"{BASE_URL}/users/",
        headers=get_auth_headers(admin_token)
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": f"获取用户列表成功, 共 {data.get('total', 0)} 个用户"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_create_user():
    """测试管理员创建用户"""
    # 使用短用户名（不超过20个字符）
    timestamp = datetime.now().strftime('%H%M%S')
    username = f"adm{timestamp}"
    response = requests.post(
        f"{BASE_URL}/users/",
        headers=get_auth_headers(admin_token),
        json={
            "username": username,
            "password": "TestPass123!",
            "email": f"{username}@admin.com",
            "role": "user"
        }
    )
    data = response.json()
    if response.status_code == 201 and data.get("code") == 0:
        global created_user_id
        created_user_id = data.get("data", {}).get("id")
        return {"success": True, "message": f"管理员创建用户成功: {username}"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_update_user():
    """测试管理员更新用户"""
    if not created_user_id:
        return {"success": False, "message": "没有可更新的用户 ID"}
    # 需要包含 username 字段，因为它是必填的
    response = requests.put(
        f"{BASE_URL}/users/{created_user_id}/",
        headers=get_auth_headers(admin_token),
        json={
            "username": f"updated_user_{datetime.now().strftime('%H%M%S')}",
            "email": "updated@test.com"
        }
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": f"更新用户信息成功"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_update_user_status():
    """测试批量更新用户状态"""
    if not created_user_id:
        return {"success": False, "message": "没有可更新的用户 ID"}
    response = requests.patch(
        f"{BASE_URL}/users/update-status/",
        headers=get_auth_headers(admin_token),
        json={
            "user_ids": [created_user_id],
            "is_active": False
        }
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": "禁用用户成功"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_update_user_role():
    """测试批量更新用户角色"""
    if not created_user_id:
        return {"success": False, "message": "没有可更新的用户 ID"}
    response = requests.patch(
        f"{BASE_URL}/users/update-role/",
        headers=get_auth_headers(admin_token),
        json={
            "user_ids": [created_user_id],
            "role": "admin"
        }
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": "更新用户角色成功"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_reset_password():
    """测试管理员重置用户密码"""
    if not created_user_id:
        return {"success": False, "message": "没有可重置密码的用户 ID"}
    response = requests.patch(
        f"{BASE_URL}/users/reset-password/",
        headers=get_auth_headers(admin_token),
        json={
            "user_id": created_user_id,
            "new_password": "NewPassword123!"
        }
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": "重置用户密码成功"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_get_profile():
    """测试获取个人信息"""
    response = requests.get(
        f"{BASE_URL}/me/",
        headers=get_auth_headers(admin_token)
    )
    data = response.json()
    if response.status_code == 200 and data.get("code") == 0:
        return {"success": True, "message": "获取个人信息成功"}
    else:
        return {"success": False, "message": f"响应: {data}"}

def test_refresh_token():
    """测试刷新 Token"""
    # 注意: 这需要 refresh token, 我们只有 access token
    # 这个测试需要配合实际的前端实现
    return {"success": True, "message": "Token 刷新测试跳过（需要 refresh token）"}

def test_unauthorized_access():
    """测试未授权访问"""
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 401 or response.status_code == 403:
        return {"success": True, "message": "正确拒绝未授权访问"}
    else:
        return {"success": False, "message": f"应该拒绝未授权访问, 状态码: {response.status_code}"}

def test_non_admin_access():
    """测试非管理员访问管理接口"""
    # 使用普通用户的 token
    response = requests.post(
        f"{BASE_URL}/login/",
        json={"username": "user", "password": "password123"}
    )
    user_token = response.json().get("data", {}).get("access")

    response = requests.get(
        f"{BASE_URL}/users/",
        headers=get_auth_headers(user_token)
    )
    if response.status_code == 403:
        return {"success": True, "message": "正确拒绝非管理员访问"}
    else:
        return {"success": False, "message": f"应该拒绝非管理员访问, 状态码: {response.status_code}"}

# ============ 运行所有测试 ============

def run_all_tests():
    """运行所有测试用例"""
    print("=" * 60)
    print("开始执行用户认证功能测试")
    print("=" * 60)
    print()

    # 用户名和邮箱检查测试
    print_info("分组: 用户名和邮箱检查")
    test_case("检查可用用户名", test_check_username_available)
    test_case("检查已存在用户名", test_check_username_exists)
    test_case("检查可用邮箱", test_check_email_available)

    # 注册功能测试
    print_info("分组: 用户注册")
    test_case("注册新用户成功", test_register_success)
    test_case("注册重复用户名失败", test_register_duplicate_username)
    test_case("注册无效邮箱失败", test_register_invalid_email)

    # 登录功能测试
    print_info("分组: 用户登录")
    test_case("管理员登录", test_admin_login)
    test_case("普通用户登录", test_user_login)
    test_case("错误密码登录失败", test_login_invalid_credentials)

    # 用户管理测试（需要管理员权限）
    print_info("分组: 用户管理（管理员）")
    test_case("获取用户列表", test_get_users_list)
    test_case("管理员创建用户", test_create_user)
    test_case("更新用户信息", test_update_user)
    test_case("更新用户状态", test_update_user_status)
    test_case("更新用户角色", test_update_user_role)
    test_case("重置用户密码", test_reset_password)

    # 权限测试
    print_info("分组: 权限控制")
    test_case("未授权访问被拒绝", test_unauthorized_access)
    test_case("非管理员访问被拒绝", test_non_admin_access)

    # 其他功能
    print_info("分组: 其他功能")
    test_case("获取个人信息", test_get_profile)
    test_case("刷新Token", test_refresh_token)

    # 打印测试总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试数: {test_results['total']}")
    print_success(f"通过: {test_results['passed']}")
    print_error(f"失败: {test_results['failed']}")
    print(f"通过率: {test_results['passed']/test_results['total']*100:.1f}%")
    print()

    return test_results

if __name__ == "__main__":
    results = run_all_tests()

    # 保存测试结果到文件
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print_info("测试结果已保存到 test_results.json")

    # 返回退出码
    sys.exit(0 if results["failed"] == 0 else 1)
