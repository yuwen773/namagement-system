"""
测试密码重置接口

运行方式：
1. 确保后端服务已启动 (python manage.py runserver)
2. python scripts/test_password_reset.py
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

def test_password_reset():
    """测试密码重置功能"""
    print("=" * 50)
    print("测试密码重置接口")
    print("=" * 50)

    # 测试数据
    test_cases = [
        {
            "name": "正常重置密码",
            "data": {
                "username": "13800138000",
                "new_password": "newpass123",
                "code": "123456"
            },
            "expected_code": 200
        },
        {
            "name": "缺少必填字段",
            "data": {
                "username": "13800138000",
                "new_password": "newpass123"
            },
            "expected_code": 400
        },
        {
            "name": "验证码错误",
            "data": {
                "username": "13800138000",
                "new_password": "newpass123",
                "code": "000000"
            },
            "expected_code": 400
        },
        {
            "name": "用户不存在",
            "data": {
                "username": "19999999999",
                "new_password": "newpass123",
                "code": "123456"
            },
            "expected_code": 400
        },
        {
            "name": "新密码长度不足",
            "data": {
                "username": "13800138000",
                "new_password": "12345",
                "code": "123456"
            },
            "expected_code": 400
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {case['name']}")
        print(f"请求数据: {json.dumps(case['data'], ensure_ascii=False)}")

        try:
            response = requests.post(
                f"{BASE_URL}/password/reset/",
                json=case['data'],
                headers={'Content-Type': 'application/json'}
            )

            result = response.json()
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('code') == case['expected_code']:
                print(f"✓ 测试通过")
            else:
                print(f"✗ 测试失败: 期望 code={case['expected_code']}, 实际 code={result.get('code')}")

        except requests.exceptions.ConnectionError:
            print(f"✗ 连接失败: 请确保后端服务已启动 (python manage.py runserver)")
            break
        except Exception as e:
            print(f"✗ 测试异常: {str(e)}")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    test_password_reset()
