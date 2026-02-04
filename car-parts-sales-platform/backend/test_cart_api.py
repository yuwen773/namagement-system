"""
购物车 API 测试脚本

用于测试购物车相关接口
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
import json

# 配置
USERS_BASE_URL = 'http://localhost:8000/api/users'
ORDERS_BASE_URL = 'http://localhost:8000/api/orders'
PRODUCTS_BASE_URL = 'http://localhost:8000/api/products'

# 测试用户数据
TEST_USER = {
    'username': '13800138001',  # 手机号
    'password': 'test123456',
}


def print_response(response, title):
    """打印响应结果"""
    print(f"\n{'='*60}")
    print(f"【{title}】")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


def test_cart_api():
    """测试购物车 API"""

    # 1. 首先登录获取 token
    print("\n" + "="*60)
    print("【1. 用户登录】")
    print("="*60)

    login_url = f'{USERS_BASE_URL}/auth/login/'
    login_data = {
        'username': TEST_USER['username'],
        'password': TEST_USER['password']
    }

    response = requests.post(login_url, json=login_data)
    print_response(response, "登录响应")

    if response.status_code != 200:
        print("\n❌ 登录失败，请确保测试用户已存在")
        return None

    token = response.json()['data']['token']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    print(f"\n✅ 登录成功，获取到 Token")

    # 2. 获取购物车（初始为空）
    print("\n" + "="*60)
    print("【2. 获取购物车】")
    print("="*60)

    cart_url = f'{ORDERS_BASE_URL}/cart/'
    response = requests.get(cart_url, headers=headers)
    print_response(response, "获取购物车")

    if response.status_code != 200:
        print("\n❌ 获取购物车失败")
        return

    cart_id = response.json()['data']['id']
    print(f"\n✅ 购物车 ID: {cart_id}")

    # 3. 获取购物车商品列表
    print("\n" + "="*60)
    print("【3. 获取购物车商品列表】")
    print("="*60)

    response = requests.get(cart_url, headers=headers)
    print_response(response, "购物车商品列表")

    items = response.json()['data'].get('items', [])
    print(f"\n✅ 当前购物车商品数量: {len(items)}")

    # 4. 添加商品到购物车
    print("\n" + "="*60)
    print("【4. 添加商品到购物车】")
    print("="*60)

    # 先获取一个已发布的商品
    products_url = f'{PRODUCTS_BASE_URL}/products/?status=published&page_size=1'
    response = requests.get(products_url, headers=headers)
    print_response(response, "获取商品列表")

    if response.status_code == 200 and response.json()['data']['results']:
        product_id = response.json()['data']['results'][0]['id']
        print(f"\n使用商品 ID: {product_id}")

        # 添加到购物车
        add_url = f'{ORDERS_BASE_URL}/cart/items/'
        add_data = {
            'product': product_id,
            'quantity': 2
        }
        response = requests.post(add_url, json=add_data, headers=headers)
        print_response(response, "添加商品到购物车")

        if response.status_code == 200:
            cart_item_id = response.json()['data']['id']
            print(f"\n✅ 添加成功，购物车商品 ID: {cart_item_id}")
        else:
            print("\n❌ 添加失败")
            return
    else:
        print("\n⚠️ 没有找到可购买的商品，跳过添加测试")
        return

    # 5. 再次获取购物车
    print("\n" + "="*60)
    print("【5. 再次获取购物车】")
    print("="*60)

    response = requests.get(cart_url, headers=headers)
    print_response(response, "购物车内容")

    # 6. 更新商品数量
    print("\n" + "="*60)
    print("【6. 更新商品数量】")
    print("="*60)

    update_url = f'{ORDERS_BASE_URL}/cart/items/{cart_item_id}/'
    update_data = {
        'quantity': 5
    }
    response = requests.put(update_url, json=update_data, headers=headers)
    print_response(response, "更新商品数量")

    if response.status_code == 200:
        print("\n✅ 数量更新成功")
    else:
        print("\n❌ 数量更新失败")

    # 7. 获取购物车数量
    print("\n" + "="*60)
    print("【7. 获取购物车商品数量】")
    print("="*60)

    count_url = f'{ORDERS_BASE_URL}/cart/count/'
    response = requests.get(count_url, headers=headers)
    print_response(response, "购物车数量")

    # 8. 删除商品
    print("\n" + "="*60)
    print("【8. 删除购物车商品】")
    print("="*60)

    delete_url = f'{ORDERS_BASE_URL}/cart/items/{cart_item_id}/'
    response = requests.delete(delete_url, headers=headers)
    print_response(response, "删除商品")

    if response.status_code == 200:
        print("\n✅ 商品删除成功")
    else:
        print("\n❌ 商品删除失败")

    # 9. 再次添加商品，测试清空购物车
    print("\n" + "="*60)
    print("【9. 再次添加商品】")
    print("="*60)

    products_url = f'{PRODUCTS_BASE_URL}/products/?status=published&page_size=1'
    response = requests.get(products_url, headers=headers)
    if response.status_code == 200 and response.json()['data']['results']:
        product_id = response.json()['data']['results'][0]['id']

        add_url = f'{ORDERS_BASE_URL}/cart/items/'
        add_data = {
            'product': product_id,
            'quantity': 1
        }
        response = requests.post(add_url, json=add_data, headers=headers)
        print_response(response, "添加商品")

        if response.status_code == 200:
            print("\n✅ 添加成功")

            # 10. 清空购物车
            print("\n" + "="*60)
            print("【10. 清空购物车】")
            print("="*60)

            clear_url = f'{ORDERS_BASE_URL}/cart/items/'
            response = requests.delete(clear_url, headers=headers)
            print_response(response, "清空购物车")

            if response.status_code == 200:
                print("\n✅ 购物车已清空")
            else:
                print("\n❌ 清空失败")

    # 11. 最终获取购物车
    print("\n" + "="*60)
    print("【11. 最终获取购物车】")
    print("="*60)

    response = requests.get(cart_url, headers=headers)
    print_response(response, "最终购物车状态")

    final_items = response.json()['data'].get('items', [])
    print(f"\n✅ 最终购物车商品数量: {len(final_items)}")

    print("\n" + "="*60)
    print("【测试完成】")
    print("="*60)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("购物车 API 测试")
    print("="*60)

    test_cart_api()
