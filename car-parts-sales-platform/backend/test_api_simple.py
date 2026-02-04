#!/usr/bin/env python
"""
Phase 3 API 完整验证脚本
"""
import os
import sys
import json

# 添加 backend 到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置 Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# 导入必要模块
from django.test import Client
from apps.products.models import Category, Product
from apps.marketing.models import Coupon, UserCoupon
from apps.content.models import ModificationCase, FAQ
from apps.system.models import SystemConfig, Message

# 创建客户端
client = Client()

def print_section(title):
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print(f"{'=' * 60}")

def print_result(name, status_code, response=None):
    """打印测试结果"""
    if status_code in [200, 201]:
        print(f"[PASS] {name}: HTTP {status_code}")
        if response and hasattr(response, 'content'):
            try:
                data = json.loads(response.content)
                if 'code' in data and 'message' in data:
                    print(f"       响应: code={data['code']}, message={data['message']}")
            except:
                pass
        return True
    else:
        print(f"[FAIL] {name}: HTTP {status_code}")
        return False

def test_products_api():
    """测试商品 API"""
    print_section("1. Products API 测试")

    results = []

    # 分类
    results.append(print_result("分类列表", client.get('/api/products/categories/').status_code))
    results.append(print_result("分类树", client.get('/api/products/categories/tree/').status_code))

    # 商品
    results.append(print_result("商品列表", client.get('/api/products/products/').status_code))
    results.append(print_result("推荐商品", client.get('/api/products/products/featured/').status_code))
    results.append(print_result("新品上市", client.get('/api/products/products/new-arrivals/').status_code))

    # 筛选和搜索
    results.append(print_result("分类筛选", client.get('/api/products/products/?category=1').status_code))
    results.append(print_result("价格排序", client.get('/api/products/products/?ordering=-price').status_code))

    return all(results)

def test_marketing_api():
    """测试营销 API"""
    print_section("2. Marketing API 测试")

    results = []

    # 优惠券
    results.append(print_result("优惠券列表", client.get('/api/marketing/coupons/').status_code))

    return all(results)

def test_content_api():
    """测试内容管理 API"""
    print_section("3. Content API 测试")

    results = []

    # 改装案例
    results.append(print_result("改装案例列表", client.get('/api/content/cases/').status_code))

    # FAQ
    results.append(print_result("FAQ列表", client.get('/api/content/faqs/').status_code))
    results.append(print_result("FAQ分类筛选", client.get('/api/content/faqs/?category=order').status_code))

    return all(results)

def test_system_api():
    """测试系统管理 API"""
    print_section("4. System API 测试")

    results = []

    # 系统配置
    results.append(print_result("系统配置列表", client.get('/api/system/configs/').status_code))

    return all(results)

def verify_response_format():
    """验证响应格式"""
    print_section("5. 响应格式验证")

    response = client.get('/api/products/products/')
    try:
        data = json.loads(response.content)
        has_code = 'code' in data
        has_message = 'message' in data
        has_data = 'data' in data

        print(f"  code 字段: {'[PASS]' if has_code else '[FAIL]'}")
        print(f"  message 字段: {'[PASS]' if has_message else '[FAIL]'}")
        print(f"  data 字段: {'[PASS]' if has_data else '[FAIL]'}")

        if has_code and has_message and has_data:
            print("\n响应格式正确: { code: 200, message: '...', data: {...} }")
            return True
        else:
            print("\n响应格式不完整!")
            return False
    except Exception as e:
        print(f"[FAIL] 无法解析响应: {e}")
        return False

def main():
    print("=" * 60)
    print("Phase 3 API 验证测试")
    print("=" * 60)
    print(f"\n测试环境: Django Test Client")
    print(f"测试时间: {os.popen('date').read().strip()}")

    all_passed = True

    # 运行所有测试
    all_passed &= test_products_api()
    all_passed &= test_marketing_api()
    all_passed &= test_content_api()
    all_passed &= test_system_api()
    all_passed &= verify_response_format()

    # 总结
    print_section("测试完成")
    status = "[ALL PASSED]" if all_passed else "[SOME FAILED]"
    print(f"\n总体状态: {status}")

    print("\n已验证的 API 端点:")
    print("  Products:")
    print("    - GET /api/products/categories/")
    print("    - GET /api/products/categories/tree/")
    print("    - GET /api/products/products/")
    print("    - GET /api/products/products/featured/")
    print("    - GET /api/products/products/new-arrivals/")
    print("  Marketing:")
    print("    - GET /api/marketing/coupons/")
    print("  Content:")
    print("    - GET /api/content/cases/")
    print("    - GET /api/content/faqs/")
    print("  System:")
    print("    - GET /api/system/configs/")

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
