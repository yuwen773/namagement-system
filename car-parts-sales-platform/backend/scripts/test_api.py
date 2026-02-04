
import os
import django
import sys
from django.utils import timezone
from datetime import timedelta

# 设置 Django 环境
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from apps.orders.views import OrderViewSet
from apps.marketing.views import CouponViewSet
from apps.marketing.models import Coupon
from apps.products.models import Product
from apps.orders.models import Order

def test_marketing_api():
    print("\n--- Testing Marketing API ---")
    User = get_user_model()
    user = User.objects.filter(is_staff=True).first()
    if not user:
        user = User.objects.create_user(phone="13800138001", password="password123", is_staff=True)
    
    factory = APIRequestFactory()
    
    # 确保至少有一个优惠券
    now = timezone.now()
    coupon, created = Coupon.objects.get_or_create(
        name="测试优惠券",
        defaults={
            'discount_type': "full_reduction",
            'discount_amount': 10,
            'min_amount': 100,
            'valid_from': now - timedelta(days=1),
            'valid_until': now + timedelta(days=30),
            'total_quantity': 100,
            'per_user_limit': 1,
            'is_active': True
        }
    )
    
    # Test List
    view_list = CouponViewSet.as_view({'get': 'list'})
    request = factory.get('/api/marketing/coupons/')
    response = view_list(request)
    print(f"Coupon List Status: {response.status_code}")
    
    # Test Claim
    view_claim = CouponViewSet.as_view({'post': 'claim'})
    request = factory.post(f'/api/marketing/coupons/{coupon.id}/claim/')
    force_authenticate(request, user=user)
    response = view_claim(request, pk=coupon.id)
    print(f"Coupon Claim Status: {response.status_code}")
    print(f"Coupon Claim Data: {response.data}")
    
    if response.status_code in [200, 201]:
        print("Marketing API (Claim) is working correctly.")
    elif response.status_code == 400 and '已达到' in str(response.data):
        print("Marketing API (Claim) correctly handles already claimed status.")
    else:
        print(f"Marketing API (Claim) failed. Status: {response.status_code}")

def test_orders_api():
    print("\n--- Testing Orders API ---")
    User = get_user_model()
    user = User.objects.filter(is_staff=True).first()
    if not user:
        user = User.objects.create_user(phone="13800138001", password="password123", is_staff=True)
    
    product = Product.objects.first()
    if not product:
        print("No product found, skipping order creation test.")
        return

    factory = APIRequestFactory()
    
    # Test List
    view_list = OrderViewSet.as_view({'get': 'list'})
    request = factory.get('/api/orders/orders/')
    force_authenticate(request, user=user)
    response = view_list(request)
    print(f"Order List Status: {response.status_code}")
    
    # Test Create Order
    view_create = OrderViewSet.as_view({'post': 'create'})
    order_data = {
        "recipient_name": "测试收货人",
        "recipient_phone": "13800138000",
        "recipient_province": "广东省",
        "recipient_city": "深圳市",
        "recipient_district": "南山区",
        "recipient_address": "科技园路1号",
        "total_amount": float(product.price),
        "pay_amount": float(product.price),
        "items": [
            {"product": product.id, "quantity": 1}
        ]
    }
    request = factory.post('/api/orders/orders/', order_data, format='json')
    force_authenticate(request, user=user)
    response = view_create(request)
    print(f"Order Create Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print("Orders API (Create) is working correctly.")
    else:
        print(f"Orders API (Create) failed. Status: {response.status_code}")
        print(f"Response data: {response.data}")

if __name__ == "__main__":
    try:
        test_marketing_api()
        test_orders_api()
    except Exception as e:
        print(f"An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
