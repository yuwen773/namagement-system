"""
测试订单支付接口

验证模拟支付功能是否正常工作
"""
import os
import django
import sys
import io

# 设置 UTF-8 输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置 Django 环境
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from apps.orders.views import OrderViewSet
from apps.orders.models import Order
from apps.products.models import Product, Category
from apps.users.models import UserAddress
from decimal import Decimal


def setup_test_data():
    """创建必要的测试数据"""
    print("正在设置测试数据...")

    User = get_user_model()

    # 1. 创建测试用户
    user, created = User.objects.get_or_create(
        phone="13900139000",
        defaults={
            'nickname': '测试用户',
            'password': 'password123'  # 明文密码，仅用于测试
        }
    )
    if created:
        print("  ✓ 创建测试用户")

    # 2. 创建商品分类
    category, _ = Category.objects.get_or_create(
        name="测试分类",
        defaults={'is_active': True}
    )

    # 3. 创建已上架商品
    product, created = Product.objects.get_or_create(
        name="测试商品-支付测试",
        defaults={
            'category': category,
            'description': '这是一个用于测试支付接口的商品',
            'price': Decimal('99.00'),
            'original_price': Decimal('129.00'),
            'stock_quantity': 100,
            'status': 'published',
            'main_image': 'https://example.com/product.jpg'
        }
    )
    if created:
        print("  ✓ 创建测试商品")

    # 4. 创建收货地址
    address, _ = UserAddress.objects.get_or_create(
        user=user,
        phone="13900139000",
        defaults={
            'recipient_name': '测试收货人',
            'province': '广东省',
            'city': '深圳市',
            'district': '南山区',
            'address': '科技园路1号',
            'is_default': True
        }
    )

    return user, product, address


def test_pay_api():
    """测试订单支付接口"""
    print("\n=== 测试订单支付接口 ===")

    # 设置测试数据
    user, product, address = setup_test_data()

    factory = APIRequestFactory()

    # 创建一个待付款订单
    view_create = OrderViewSet.as_view({'post': 'create'})
    order_data = {
        "recipient_name": address.recipient_name,
        "recipient_phone": address.phone,
        "recipient_province": address.province,
        "recipient_city": address.city,
        "recipient_district": address.district,
        "recipient_address": address.address,
        "total_amount": float(product.price),
        "pay_amount": float(product.price),
        "items": [
            {"product": product.id, "quantity": 1}
        ]
    }
    request = factory.post('/api/orders/orders/', order_data, format='json')
    force_authenticate(request, user=user)
    response = view_create(request)

    print(f"订单创建响应状态码: {response.status_code}")
    print(f"订单创建响应数据: {response.data}")

    if response.status_code not in [200, 201]:
        print(f"创建订单失败: {response.data}")
        return

    # 检查响应结构
    if 'data' in response.data:
        order_id = response.data['data'].get('id')
    else:
        print(f"响应中没有找到 'data' 字段: {response.data}")
        return

    order = Order.objects.get(id=order_id)
    print(f"订单创建成功: {order.order_no}, 状态: {order.status}")

    # 4. 测试支付接口
    view_pay = OrderViewSet.as_view({'post': 'pay'})
    request = factory.post(f'/api/orders/orders/{order.id}/pay/')
    force_authenticate(request, user=user)
    response = view_pay(request, pk=order.id)

    print(f"支付接口响应状态码: {response.status_code}")
    print(f"支付接口响应数据: {response.data}")

    # 5. 验证结果
    order.refresh_from_db()
    if response.status_code == 200:
        print(f"✓ 支付成功!")
        print(f"  - 订单号: {order.order_no}")
        print(f"  - 订单状态: {order.status} (应为 pending_shipment)")
        print(f"  - 支付时间: {order.paid_at}")
        if order.status == Order.Status.PENDING_SHIPMENT:
            print("✓ 订单状态正确变更为 pending_shipment")
            return True
        else:
            print(f"✗ 订单状态错误: {order.status}")
            return False
    else:
        print(f"✗ 支付失败: {response.data}")
        return False


def test_pay_validation():
    """测试支付接口的各种验证"""
    print("\n=== 测试支付接口验证 ===")

    User = get_user_model()

    # 使用主测试用户
    user, product, address = setup_test_data()

    # 创建另一个用户用于测试权限验证
    other_user, _ = User.objects.get_or_create(
        phone="13900139002",
        defaults={'nickname': '其他用户', 'password': 'password123'}
    )

    factory = APIRequestFactory()

    # 1. 测试支付非待付款状态的订单
    completed_order = Order.objects.filter(
        user=user,
        status=Order.Status.COMPLETED
    ).first()

    if completed_order:
        view_pay = OrderViewSet.as_view({'post': 'pay'})
        request = factory.post(f'/api/orders/orders/{completed_order.id}/pay/')
        force_authenticate(request, user=user)
        response = view_pay(request, pk=completed_order.id)
        if response.status_code == 400:
            print("✓ 正确拒绝支付已完成订单")
        else:
            print(f"✗ 应该拒绝支付已完成订单，但返回: {response.data}")

    # 2. 测试用户无法支付他人的订单
    pending_order = Order.objects.filter(
        status=Order.Status.PENDING_PAYMENT
    ).exclude(user=user).first()

    if pending_order:
        view_pay = OrderViewSet.as_view({'post': 'pay'})
        request = factory.post(f'/api/orders/orders/{pending_order.id}/pay/')
        force_authenticate(request, user=user)
        response = view_pay(request, pk=pending_order.id)
        if response.status_code == 400:
            print("✓ 正确拒绝支付他人订单")
        else:
            print(f"✗ 应该拒绝支付他人订单，但返回: {response.data}")

    print("\n验证测试完成!")


if __name__ == "__main__":
    try:
        success = test_pay_api()
        if success:
            test_pay_validation()
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
