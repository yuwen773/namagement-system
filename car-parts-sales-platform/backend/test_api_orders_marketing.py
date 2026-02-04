#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
订单和营销模块 API 测试脚本

测试 orders 和 marketing 模块的所有 API 端点
"""
import sys
# Force UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import sys
import django

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
import json
from datetime import datetime, timedelta

# 配置
BASE_URL = 'http://127.0.0.1:8000'
HEADERS = {'Content-Type': 'application/json'}

# 存储 token
admin_token = None
user_token = None
admin_headers = None
user_headers = None


def print_result(test_name, success, message='', data=None):
    """打印测试结果"""
    status = '[PASS]' if success else '[FAIL]'
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")
    if data and not success:
        print(f"   Data: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return success


def register_user(phone, password, nickname='测试用户'):
    """注册用户"""
    url = f'{BASE_URL}/api/users/auth/register/'
    data = {
        'phone': phone,
        'password': password,
        'nickname': nickname
    }
    try:
        response = requests.post(url, json=data)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, str(e)


def login_user(phone, password):
    """登录用户"""
    url = f'{BASE_URL}/api/users/auth/login/'
    data = {
        'phone': phone,
        'password': password
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json()
    except Exception as e:
        return False, str(e)


def create_address(token, is_default=False):
    """创建收货地址"""
    url = f'{BASE_URL}/api/users/addresses/'
    headers = {**HEADERS, 'Authorization': f'Bearer {token}'}
    data = {
        'recipient_name': '张三',
        'phone': '13800138000',
        'province': '广东省',
        'city': '深圳市',
        'district': '南山区',
        'address': '科技园路1号',
        'is_default': is_default
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code in [200, 201], response.json()
    except Exception as e:
        return False, str(e)


def create_category(token, name='测试分类', parent_id=None):
    """创建商品分类"""
    url = f'{BASE_URL}/api/products/categories/'
    headers = {**HEADERS, 'Authorization': f'Bearer {token}'}
    data = {
        'name': name,
        'is_active': True
    }
    if parent_id:
        data['parent'] = parent_id
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code in [200, 201], response.json()
    except Exception as e:
        return False, str(e)


def create_product(token, category_id, name='测试商品', price=99.00):
    """创建商品"""
    url = f'{BASE_URL}/api/products/products/'
    headers = {**HEADERS, 'Authorization': f'Bearer {token}'}
    data = {
        'name': name,
        'description': '这是一个测试商品',
        'price': price,
        'category': category_id,
        'stock': 100,
        'status': 'published'
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code in [200, 201], response.json()
    except Exception as e:
        return False, str(e)


def create_coupon(token, name='测试优惠券', discount_amount=10):
    """创建优惠券"""
    url = f'{BASE_URL}/api/marketing/coupons/'
    headers = {**HEADERS, 'Authorization': f'Bearer {token}'}
    now = datetime.now()
    data = {
        'name': name,
        'description': '测试优惠券描述',
        'discount_type': 'full_reduction',
        'min_amount': 50,
        'discount_amount': discount_amount,
        'valid_from': now.isoformat(),
        'valid_until': (now + timedelta(days=30)).isoformat(),
        'total_quantity': 100,
        'per_user_limit': 5,
        'is_active': True
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code in [200, 201], response.json()
    except Exception as e:
        return False, str(e)


def test_auth_api():
    """测试认证 API"""
    print("\n" + "=" * 60)
    print("测试 1: 认证 API")
    print("=" * 60)

    global admin_token, user_token, admin_headers, user_headers

    # 测试注册
    print("\n1.1 测试用户注册...")
    success, result = register_user('13800138001', 'password123', '管理员测试')
    if success:
        admin_token = result.get('data', {}).get('token')
        admin_headers = {**HEADERS, 'Authorization': f'Bearer {admin_token}'}
        print_result("用户注册成功", True, f"Token: {admin_token[:20]}...")
    else:
        # 可能已存在，尝试登录
        print_result("用户注册失败", False, str(result))
        # 尝试使用 Django admin 创建的用户登录
        success, result = login_user('admin', 'admin123')
        if success:
            admin_token = result.get('data', {}).get('token')
            admin_headers = {**HEADERS, 'Authorization': f'Bearer {admin_token}'}
            print_result("管理员登录成功", True, "使用 admin 账户")
        else:
            print_result("管理员登录失败", False, str(result))
            # 检查是否有已存在的测试用户需要处理
            print("   尝试创建超级用户...")
            import subprocess
            result = subprocess.run(
                ['python', 'manage.py', 'shell', '-c',
                 'from apps.users.models import User; '
                 'User.objects.filter(phone="13800138001").delete(); '
                 'u=User.objects.create_user(phone="13800138001", password="password123", nickname="测试用户"); print("创建成功")'],
                capture_output=True, text=True
            )
            print(f"   {result.stdout}")
            if result.returncode == 0:
                success, result = login_user('13800138001', 'password123')
                if success:
                    admin_token = result.get('data', {}).get('token')
                    admin_headers = {**HEADERS, 'Authorization': f'Bearer {admin_token}'}
                    print_result("用户登录成功", True, "通过命令行创建的用户")
                else:
                    print_result("用户登录仍然失败", False, str(result))
            else:
                print_result("创建用户失败", False, result.stderr)

    # 测试普通用户
    print("\n1.2 测试普通用户注册...")
    success, result = register_user('13800138002', 'password123', '普通用户测试')
    if success:
        user_token = result.get('data', {}).get('token')
        user_headers = {**HEADERS, 'Authorization': f'Bearer {user_token}'}
        print_result("普通用户注册成功", True)
    else:
        print_result("普通用户注册失败", False, str(result))
        success, result = login_user('13800138002', 'password123')
        if success:
            user_token = result.get('data', {}).get('token')
            user_headers = {**HEADERS, 'Authorization': f'Bearer {user_token}'}
            print_result("普通用户登录成功", True)
        else:
            print_result("普通用户登录失败", False, str(result))
            return False

    # 测试获取当前用户信息
    print("\n1.3 测试获取当前用户信息...")
    try:
        response = requests.get(f'{BASE_URL}/api/users/me/', headers=admin_headers)
        if response.status_code == 200:
            print_result("获取用户信息成功", True, response.json().get('message'))
        else:
            print_result("获取用户信息失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("获取用户信息异常", False, str(e))

    return True


def test_address_api():
    """测试用户地址 API"""
    print("\n" + "=" * 60)
    print("测试 2: 用户地址 API")
    print("=" * 60)

    if not user_token:
        print_result("跳过测试", False, "需要先登录用户")
        return False

    # 创建地址
    print("\n2.1 测试创建地址...")
    success, result = create_address(user_token, is_default=True)
    if success:
        print_result("创建地址成功", True)
    else:
        print_result("创建地址失败", False, str(result))

    # 获取地址列表
    print("\n2.2 测试获取地址列表...")
    try:
        response = requests.get(f'{BASE_URL}/api/users/addresses/', headers=user_headers)
        if response.status_code == 200:
            data = response.json()
            print_result("获取地址列表成功", True, f"数量: {len(data.get('data', {}).get('results', []))}")
        else:
            print_result("获取地址列表失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("获取地址列表异常", False, str(e))

    return True


def test_coupon_api():
    """测试优惠券 API"""
    print("\n" + "=" * 60)
    print("测试 3: 优惠券 API (Marketing)")
    print("=" * 60)

    if not admin_token:
        print_result("跳过测试", False, "需要管理员 token")
        return False

    # 创建优惠券（需要管理员权限）
    print("\n3.1 测试创建优惠券...")
    success, result = create_coupon(admin_token, '满100减20')
    if success:
        coupon_id = result.get('data', {}).get('id')
        print_result("创建优惠券成功", True, f"ID: {coupon_id}")
    else:
        print_result("创建优惠券失败", False, str(result))
        # 可能优惠券已存在，尝试获取列表
        try:
            response = requests.get(f'{BASE_URL}/api/marketing/coupons/')
            if response.status_code == 200:
                coupons = response.json().get('data', {}).get('results', [])
                if coupons:
                    coupon_id = coupons[0].get('id')
                    print_result("获取优惠券列表成功", True, f"使用现有优惠券 ID: {coupon_id}")
                else:
                    coupon_id = None
            else:
                coupon_id = None
        except Exception as e:
            print_result("获取优惠券列表异常", False, str(e))
            coupon_id = None

    # 获取优惠券列表（公开接口）
    print("\n3.2 测试获取优惠券列表（公开）...")
    try:
        response = requests.get(f'{BASE_URL}/api/marketing/coupons/')
        if response.status_code == 200:
            data = response.json()
            print_result("获取优惠券列表成功", True)
        else:
            print_result("获取优惠券列表失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("获取优惠券列表异常", False, str(e))

    # 领取优惠券
    if coupon_id and user_token:
        print("\n3.3 测试领取优惠券...")
        try:
            response = requests.post(
                f'{BASE_URL}/api/marketing/coupons/{coupon_id}/claim/',
                headers=user_headers
            )
            if response.status_code == 200:
                print_result("领取优惠券成功", True)
            else:
                print_result("领取优惠券失败", False, str(response.json()))
        except Exception as e:
            print_result("领取优惠券异常", False, str(e))

        # 获取我的优惠券 (URL: /api/marketing/coupons/my-coupons/)
        print("\n3.4 测试获取我的优惠券...")
        try:
            response = requests.get(f'{BASE_URL}/api/marketing/coupons/my-coupons/', headers=user_headers)
            if response.status_code == 200:
                print_result("获取我的优惠券成功", True)
            else:
                print_result("获取我的优惠券失败", False, f"Status: {response.status_code}, {response.text[:100]}")
        except Exception as e:
            print_result("获取我的优惠券异常", False, str(e))

    return True


def test_order_api():
    """测试订单 API"""
    print("\n" + "=" * 60)
    print("测试 4: 订单 API")
    print("=" * 60)

    if not user_token:
        print_result("跳过测试", False, "需要用户 token")
        return False

    # 先创建必要的测试数据
    print("\n4.0 准备测试数据...")
    success, result = create_address(user_token, is_default=True)
    addr_data = result.get('data', {})
    address_id = addr_data.get('id')
    print(f"   地址 ID: {address_id}")

    # 获取可用的商品
    product_id = None
    try:
        response = requests.get(f'{BASE_URL}/api/products/products/')
        if response.status_code == 200:
            products = response.json().get('data', {}).get('results', [])
            if products:
                product_id = products[0].get('id')
                print(f"   商品 ID: {product_id}")
    except Exception as e:
        print(f"   获取商品列表异常: {e}")

    if not product_id:
        print_result("跳过订单测试", False, "没有可用的商品")
        return True

    # 创建订单
    print("\n4.1 测试创建订单...")
    order_data = {
        'recipient_name': '张三',
        'recipient_phone': '13800138000',
        'recipient_province': '广东省',
        'recipient_city': '深圳市',
        'recipient_district': '南山区',
        'recipient_address': '科技园路1号',
        'items': [
            {'product': product_id, 'quantity': 2}
        ],
        'remark': '测试订单'
    }
    try:
        response = requests.post(
            f'{BASE_URL}/api/orders/orders/',
            json=order_data,
            headers=user_headers
        )
        if response.status_code in [200, 201]:
            order_result = response.json()
            order_id = order_result.get('data', {}).get('id')
            print_result("创建订单成功", True, f"订单ID: {order_id}")
        else:
            print_result("创建订单失败", False, str(response.json()))
            order_id = None
    except Exception as e:
        print_result("创建订单异常", False, str(e))
        order_id = None

    # 获取订单列表
    print("\n4.2 测试获取订单列表...")
    try:
        response = requests.get(f'{BASE_URL}/api/orders/orders/', headers=user_headers)
        if response.status_code == 200:
            data = response.json()
            print_result("获取订单列表成功", True)
        else:
            print_result("获取订单列表失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("获取订单列表异常", False, str(e))

    # 我的订单
    print("\n4.3 测试我的订单...")
    try:
        response = requests.get(f'{BASE_URL}/api/orders/orders/my-orders/', headers=user_headers)
        if response.status_code == 200:
            print_result("获取我的订单成功", True)
        else:
            print_result("获取我的订单失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("获取我的订单异常", False, str(e))

    # 订单详情和取消
    if order_id:
        print(f"\n4.4 测试订单详情 (ID: {order_id})...")
        try:
            response = requests.get(f'{BASE_URL}/api/orders/orders/{order_id}/', headers=user_headers)
            if response.status_code == 200:
                print_result("获取订单详情成功", True)
            else:
                print_result("获取订单详情失败", False, f"Status: {response.status_code}")
        except Exception as e:
            print_result("获取订单详情异常", False, str(e))

        # 取消订单
        print("\n4.5 测试取消订单...")
        try:
            response = requests.post(
                f'{BASE_URL}/api/orders/orders/{order_id}/cancel/',
                headers=user_headers
            )
            if response.status_code == 200:
                print_result("取消订单成功", True)
            else:
                result = response.json()
                print_result("取消订单失败", False, result.get('message', str(result)))
        except Exception as e:
            print_result("取消订单异常", False, str(e))

    return True


def test_return_request_api():
    """测试退换货 API"""
    print("\n" + "=" * 60)
    print("测试 5: 退换货申请 API")
    print("=" * 60)

    if not user_token:
        print_result("跳过测试", False, "需要用户 token")
        return False

    # 获取退换货列表
    print("\n5.1 测试获取退换货列表...")
    try:
        response = requests.get(f'{BASE_URL}/api/orders/returns/', headers=user_headers)
        if response.status_code == 200:
            print_result("获取退换货列表成功", True)
        else:
            print_result("获取退换货列表失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("获取退换货列表异常", False, str(e))

    return True


def test_admin_functions():
    """测试管理员功能"""
    print("\n" + "=" * 60)
    print("测试 6: 管理员功能")
    print("=" * 60)

    if not admin_token:
        print_result("跳过测试", False, "需要管理员 token")
        return False

    # 管理员查看所有订单
    print("\n6.1 测试管理员查看所有订单...")
    try:
        response = requests.get(f'{BASE_URL}/api/orders/orders/', headers=admin_headers)
        if response.status_code == 200:
            print_result("管理员查看订单成功", True)
        else:
            print_result("管理员查看订单失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("管理员查看订单异常", False, str(e))

    # 管理员查看优惠券
    print("\n6.2 测试管理员查看优惠券...")
    try:
        response = requests.get(f'{BASE_URL}/api/marketing/coupons/', headers=admin_headers)
        if response.status_code == 200:
            print_result("管理员查看优惠券成功", True)
        else:
            print_result("管理员查看优惠券失败", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("管理员查看优惠券异常", False, str(e))

    # 管理员创建商品
    print("\n6.3 测试管理员创建商品...")
    success, result = create_product(admin_token, 1, '管理员创建的商品', 199.00)
    if success:
        print_result("管理员创建商品成功", True)
    else:
        print_result("管理员创建商品失败", False, str(result))

    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("汽车改装件销售推荐平台 - API 测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")

    # 等待服务启动
    print("\n检查服务可用性...")
    try:
        response = requests.get(f'{BASE_URL}/api/', timeout=5)
        print(f"服务状态: {response.status_code}")
    except Exception as e:
        print(f"服务不可用: {e}")
        print("请确保 Django 服务已启动: python manage.py runserver")
        return

    # 运行测试
    test_auth_api()
    test_address_api()
    test_coupon_api()
    test_order_api()
    test_return_request_api()
    test_admin_functions()

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
