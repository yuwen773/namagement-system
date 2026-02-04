#!/usr/bin/env python
"""
Phase 3 Step 4: Review API 完整验证脚本

测试内容：
1. GET /api/products/reviews/ - 评价列表
2. POST /api/products/products/{id}/reviews/ - 提交评价
3. GET /api/products/products/{id}/reviews/ - 商品评价列表
4. GET /api/products/reviews/{id}/ - 评价详情
5. DELETE /api/products/reviews/{id}/ - 删除评价

注意：测试前需要确保有商品数据
"""
import os
import sys
import json

# 设置工作目录为 backend 目录
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

# 设置 Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()


def print_section(title):
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print(f"{'=' * 60}")


def print_result(name, status_code, response=None, expected=None):
    """打印测试结果"""
    passed = status_code in [200, 201]
    if expected:
        passed = status_code == expected

    if passed:
        print(f"[PASS] {name}: HTTP {status_code}")
    else:
        print(f"[FAIL] {name}: HTTP {status_code} (expected {expected})")

    if response and hasattr(response, 'content'):
        try:
            data = json.loads(response.content)
            if isinstance(data, dict) and 'code' in data and 'message' in data:
                print(f"       Response: code={data.get('code')}, message={data.get('message')}")
                if 'data' in data:
                    data_preview = str(data['data'])[:150]
                    print(f"       Data preview: {data_preview}...")
        except:
            pass
    return passed


def test_review_list_api(client):
    """测试评价列表 API"""
    print_section("1. Review API - 评价列表测试")

    results = []

    # GET /api/products/reviews/ - 评价列表
    response = client.get('/api/products/reviews/')
    results.append(print_result("GET 评价列表", response.status_code, response, expected=200))

    return all(results)


def test_review_detail_api(client, review_id=1):
    """测试评价详情 API"""
    print_section("2. Review API - 评价详情测试")

    results = []

    # GET /api/products/reviews/{id}/ - 评价详情
    response = client.get(f'/api/products/reviews/{review_id}/')
    results.append(print_result(f"GET 评价详情(id={review_id})", response.status_code, response, expected=200))

    return all(results)


def test_product_reviews_api(client, product_id=1):
    """测试商品评价列表 API"""
    print_section("3. Product Reviews API - 商品评价列表测试")

    results = []

    # GET /api/products/products/{id}/reviews/ - 商品评价列表
    response = client.get(f'/api/products/products/{product_id}/reviews/')
    results.append(print_result(f"GET 商品评价列表(product_id={product_id})", response.status_code, response, expected=200))

    # 测试评分筛选
    response = client.get(f'/api/products/products/{product_id}/reviews/?rating=5')
    results.append(print_result(f"GET 商品评价列表(筛选rating=5)", response.status_code, response, expected=200))

    # 测试排序
    response = client.get(f'/api/products/products/{product_id}/reviews/?ordering=-created_at')
    results.append(print_result(f"GET 商品评价列表(排序)", response.status_code, response, expected=200))

    return all(results)


def test_create_review_api(client, product_id=1):
    """测试提交评价 API"""
    print_section("4. Create Review API - 提交评价测试")

    results = []

    # POST /api/products/products/{id}/reviews/ - 提交评价
    response = client.post(
        f'/api/products/products/{product_id}/reviews/',
        data=json.dumps({
            'rating': 5,
            'comment': '这是一个测试评价，商品质量很好！',
            'images': ['http://example.com/image1.jpg'],
            'is_anonymous': False
        }),
        content_type='application/json'
    )
    results.append(
        print_result(
            f"POST 提交评价(product_id={product_id})",
            response.status_code,
            response,
            expected=201
        )
    )

    # 获取创建的评价ID
    review_id = None
    if response.status_code == 201:
        try:
            data = json.loads(response.content)
            review_id = data.get('data', {}).get('id')
            print(f"       Created review ID: {review_id}")
        except:
            pass

    # 测试无效评分
    response = client.post(
        f'/api/products/products/{product_id}/reviews/',
        data=json.dumps({
            'rating': 6,  # 无效评分
            'comment': '测试无效评分'
        }),
        content_type='application/json'
    )
    results.append(print_result("POST 提交评价(无效评分)", response.status_code, response, expected=400))

    # 测试不存在的商品
    response = client.post(
        '/api/products/products/99999/reviews/',
        data=json.dumps({
            'rating': 5,
            'comment': '测试不存在的商品'
        }),
        content_type='application/json'
    )
    results.append(print_result("POST 提交评价(商品不存在)", response.status_code, response, expected=404))

    return all(results), review_id


def test_delete_review_api(client, review_id):
    """测试删除评价 API"""
    print_section("5. Delete Review API - 删除评价测试")

    results = []

    if review_id:
        # DELETE /api/products/reviews/{id}/ - 删除评价
        response = client.delete(f'/api/products/reviews/{review_id}/')
        results.append(print_result(f"DELETE 删除评价(id={review_id})", response.status_code, response, expected=200))

        # 验证已删除
        response = client.get(f'/api/products/reviews/{review_id}/')
        results.append(print_result(f"GET 已删除评价(id={review_id})", response.status_code, response, expected=404))
    else:
        print("       [SKIP] 没有可删除的评价ID")

    return all(results) if review_id else True


def check_products_exist(client):
    """检查是否有商品数据"""
    response = client.get('/api/products/products/')
    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            products = data.get('data', [])
            if isinstance(products, list):
                return products[:3] if products else []
            elif isinstance(products, dict) and 'results' in products:
                return products['results'][:3]
            return []
        except:
            return []
    return []


def main():
    print("\n" + "=" * 60)
    print("Phase 3 Step 4: Review API 测试")
    print("=" * 60)

    # 创建测试客户端
    client = Client()

    # 先检查商品数据
    print_section("检查商品数据")
    products = check_products_exist(client)
    if not products:
        print("[WARN] 没有找到商品数据，请先创建商品")
        # 尝试创建一个测试商品
        print("尝试创建测试商品...")
        response = client.post(
            '/api/products/products/',
            data=json.dumps({
                'name': '测试商品-用于评价测试',
                'price': '99.00',
                'status': 'published',
                'stock_quantity': 100
            }),
            content_type='application/json'
        )
        if response.status_code == 201:
            print("[INFO] 测试商品创建成功")
            products = [{'id': 1}]
        else:
            print("[ERROR] 无法创建测试商品，测试可能失败")
    else:
        print(f"[INFO] 找到 {len(products)} 个商品")

    # 获取商品ID
    product_id = products[0]['id'] if products else 1
    print(f"[INFO] 使用商品ID: {product_id}")

    all_passed = True

    # 1. 测试评价列表
    if not test_review_list_api(client):
        all_passed = False

    # 2. 测试商品评价列表
    if not test_product_reviews_api(client, product_id):
        all_passed = False

    # 3. 测试提交评价
    create_passed, review_id = test_create_review_api(client, product_id)
    if not create_passed:
        all_passed = False

    # 4. 测试评价详情（如果创建成功）
    if review_id:
        if not test_review_detail_api(client, review_id):
            all_passed = False

    # 5. 测试删除评价
    if review_id:
        if not test_delete_review_api(client, review_id):
            all_passed = False

    # 总结
    print_section("测试总结")
    if all_passed:
        print("[SUCCESS] 所有 Review API 测试通过！")
    else:
        print("[WARNING] 部分测试未通过，请检查输出")

    print("\n可用 API 端点:")
    print("  GET    /api/products/reviews/                    - 评价列表")
    print("  GET    /api/products/reviews/{id}/              - 评价详情")
    print("  POST   /api/products/products/{id}/reviews/     - 提交评价")
    print("  GET    /api/products/products/{id}/reviews/      - 商品评价列表")
    print("  DELETE /api/products/reviews/{id}/              - 删除评价")

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
