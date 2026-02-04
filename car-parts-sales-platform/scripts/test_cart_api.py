"""
购物车 API 测试脚本 (Django 测试客户端版本)

测试购物车功能：
1. 获取购物车
2. 添加商品到购物车
3. 更新购物车商品数量
4. 删除购物车商品
5. 清空购物车
6. 获取购物车商品总数

使用方法:
cd backend && python manage.py shell -c "exec(open('../scripts/test_cart_api.py').read())"
"""

import os
import sys
import json
import django
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# 设置 Django 环境
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, Category
from apps.orders.models import Cart, CartItem

def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"{text:^60}")
    print(f"{'=' * 60}\n")

def print_success(text):
    print(f"[PASS] {text}")

def print_fail(text):
    print(f"[FAIL] {text}")

def print_info(text):
    print(f"[INFO] {text}")

def expect_success(response, test_name):
    if response is None:
        print_fail(f"{test_name}: 无响应")
        return False
    try:
        data = json.loads(response.content)
        if data.get('code') == 200:
            print_success(f"{test_name}: {data.get('message', '成功')}")
            return data
        else:
            print_fail(f"{test_name}: 失败 - {data.get('message')}")
            if 'errors' in data:
                print_fail(f"错误详情: {data['errors']}")
            return None
    except json.JSONDecodeError:
        print_fail(f"{test_name}: 响应不是 JSON 格式")
        return None

def test_cart():
    client = Client()
    User = get_user_model()
    
    print_header("购物车 API 测试")
    
    # 1. 准备测试数据
    print_info("1. 准备测试数据...")
    user, _ = User.objects.get_or_create(phone='13900000001', defaults={'nickname': '购物车测试员'})
    user.set_password('testpass123')
    user.save()
    
    category, _ = Category.objects.get_or_create(name='测试分类')
    product, _ = Product.objects.get_or_create(
        name='购物车测试商品', 
        defaults={
            'price': 100.00, 
            'stock_quantity': 10, 
            'status': 'published',
            'category': category
        }
    )
    product.stock_quantity = 10
    product.status = 'published'
    product.save()
    
    # 清理已有的购物车数据
    Cart.objects.filter(user=user).delete()
    
    # 强制登录
    client.force_login(user)
    
    # 2. 获取初始购物车 (应该是空的)
    print_info("2. 获取初始购物车...")
    response = client.get('/api/orders/cart/')
    data = expect_success(response, "获取购物车")
    if data:
        items = data['data'].get('items', [])
        if len(items) == 0:
            print_success("初始购物车为空，符合预期")
        else:
            print_fail(f"初始购物车不为空: {len(items)} 个商品")

    # 3. 添加商品到购物车
    print_info("3. 添加商品到购物车...")
    add_data = {'product': product.id, 'quantity': 2}
    response = client.post('/api/orders/cart/items/', data=json.dumps(add_data), content_type='application/json')
    data = expect_success(response, "添加商品")
    
    # 验证购物车内容
    response = client.get('/api/orders/cart/')
    data = expect_success(response, "再次获取购物车")
    if data:
        items = data['data'].get('items', [])
        if len(items) == 1 and items[0]['product'] == product.id and items[0]['quantity'] == 2:
            print_success(f"商品已正确添加到购物车，数量: {items[0]['quantity']}")
            cart_item_id = items[0]['id']
        else:
            print_fail("购物车商品信息不匹配")
            return

    # 4. 更新商品数量
    print_info("4. 更新商品数量...")
    update_data = {'quantity': 5}
    response = client.patch(f'/api/orders/cart/items/{cart_item_id}/', data=json.dumps(update_data), content_type='application/json')
    data = expect_success(response, "更新商品数量")
    
    # 验证更新
    response = client.get('/api/orders/cart/')
    data = expect_success(response, "验证更新后的购物车")
    if data:
        items = data['data'].get('items', [])
        if items[0]['quantity'] == 5:
            print_success("商品数量更新成功")
        else:
            print_fail(f"商品数量更新失败: 预期 5, 实际 {items[0]['quantity']}")

    # 5. 测试库存限制
    print_info("5. 测试库存限制...")
    update_data = {'quantity': 100} # 超过库存 10
    response = client.patch(f'/api/orders/cart/items/{cart_item_id}/', data=json.dumps(update_data), content_type='application/json')
    if response.status_code == 200: # ApiResponse 返回 200 但 code 可能不是 200
        data = json.loads(response.content)
        if data.get('code') != 200:
            print_success(f"库存限制生效: {data.get('message')}")
        else:
            print_fail("库存限制未生效")

    # 6. 获取商品总数
    print_info("6. 获取商品总数...")
    response = client.get('/api/orders/cart/count/')
    data = expect_success(response, "获取商品总数")
    if data:
        count = data['data'].get('count')
        if count == 5:
            print_success(f"商品总数正确: {count}")
        else:
            print_fail(f"商品总数错误: 预期 5, 实际 {count}")

    # 7. 删除商品
    print_info("7. 删除商品...")
    response = client.delete(f'/api/orders/cart/items/{cart_item_id}/')
    expect_success(response, "删除商品")
    
    # 验证删除
    response = client.get('/api/orders/cart/')
    data = expect_success(response, "验证删除后的购物车")
    if data:
        if len(data['data'].get('items', [])) == 0:
            print_success("商品删除成功")
        else:
            print_fail("商品删除失败")

    # 8. 清空购物车
    print_info("8. 清空购物车测试...")
    # 先加一个回来
    client.post('/api/orders/cart/items/', data=json.dumps({'product': product.id, 'quantity': 1}), content_type='application/json')
    response = client.delete('/api/orders/cart/clear/')
    expect_success(response, "清空购物车")
    
    # 验证清空
    response = client.get('/api/orders/cart/')
    data = expect_success(response, "验证清空后的购物车")
    if data and len(data['data'].get('items', [])) == 0:
        print_success("购物车清空成功")
    else:
        print_fail("购物车清空失败")

    print_header("购物车 API 测试完成")

if __name__ == "__main__":
    test_cart()
