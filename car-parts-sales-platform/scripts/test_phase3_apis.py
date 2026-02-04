"""
Phase 3 API 测试脚本 (Django 测试客户端版本)

测试第三阶段实现的所有 API：
1. Products API (products 模块)
2. Marketing API (marketing 模块)
3. Content API (content 模块)
4. System API (system 模块)

使用方法:
cd backend && python manage.py shell -c "exec(open('../scripts/test_phase3_apis.py').read())"
或者直接运行测试服务器测试
"""

# 此脚本需要从 backend 目录运行
# 确保在运行前执行: cd backend

try:
    django.setup()
except RuntimeError:
    # 如果已经初始化，跳过
    pass

from django.test import Client
from django.contrib.auth import get_user_model
from apps.marketing.models import Coupon
from apps.content.models import ModificationCase, FAQ
from apps.system.models import SystemConfig, Message, OperationLog
from apps.products.models import Category, Product
import json
from datetime import datetime, timedelta

# 创建测试客户端
client = Client()

# 测试数据
TEST_USER = None
ADMIN_USER = None


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


def ensure_authenticated(user):
    """确保用户已登录并返回认证头"""
    client.force_login(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {user.token}'} if hasattr(user, 'token') else {}


def make_request(method, url, data=None, user=None, **kwargs):
    """发送 HTTP 请求并返回响应"""
    try:
        if method.upper() == 'GET':
            response = client.get(url, data, **kwargs)
        elif method.upper() == 'POST':
            response = client.post(url, json.dumps(data) if data else {}, content_type='application/json', **kwargs)
        elif method.upper() == 'PUT':
            response = client.put(url, json.dumps(data) if data else {}, content_type='application/json', **kwargs)
        elif method.upper() == 'PATCH':
            response = client.patch(url, json.dumps(data) if data else {}, content_type='application/json', **kwargs)
        elif method.upper() == 'DELETE':
            response = client.delete(url, **kwargs)
        else:
            raise ValueError(f"不支持的方法: {method}")
        return response
    except Exception as e:
        print_fail(f"请求失败: {e}")
        return None


def expect_success(response, test_name):
    """检查响应是否成功"""
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
            return None
    except json.JSONDecodeError:
        print_fail(f"{test_name}: 响应不是 JSON 格式")
        print_fail(f"响应内容: {response.content[:200]}")
        return None


def setup_test_data():
    """创建测试数据"""
    global TEST_USER, ADMIN_USER
    User = get_user_model()

    print_header("0. 创建测试数据")

    # 创建测试用户
    try:
        TEST_USER, created = User.objects.get_or_create(
            username='13800138000',
            defaults={
                'nickname': '测试用户',
                'phone': '13800138000'
            }
        )
        TEST_USER.set_password('testpass123')
        TEST_USER.save()

        # 添加 token 属性用于模拟 JWT
        from rest_framework_simplejwt.tokens import RefreshToken
        TEST_USER.token = str(RefreshToken.for_user(TEST_USER).access_token)
        TEST_USER.save()

        if created:
            print_success(f"创建测试用户: {TEST_USER.username}")
        else:
            print_info(f"使用现有用户: {TEST_USER.username}")
    except Exception as e:
        print_fail(f"创建测试用户失败: {e}")
        TEST_USER = None

    # 创建管理员用户
    try:
        ADMIN_USER, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'nickname': '管理员',
                'phone': '13800000000',
                'is_staff': True,
                'is_superuser': True
            }
        )
        ADMIN_USER.set_password('admin123')
        ADMIN_USER.save()

        from rest_framework_simplejwt.tokens import RefreshToken
        ADMIN_USER.token = str(RefreshToken.for_user(ADMIN_USER).access_token)
        ADMIN_USER.save()

        if created:
            print_success(f"创建管理员用户: {ADMIN_USER.username}")
        else:
            print_info(f"使用现有管理员: {ADMIN_USER.username}")
    except Exception as e:
        print_fail(f"创建管理员失败: {e}")
        ADMIN_USER = None

    # 创建测试分类
    try:
        category, created = Category.objects.get_or_create(
            id=1,
            defaults={
                'name': '测试分类',
                'sort_order': 1
            }
        )
        if created:
            print_success("创建测试分类")
    except Exception as e:
        print_info(f"分类已存在或创建失败: {e}")

    # 创建测试商品
    try:
        product, created = Product.objects.get_or_create(
            id=1,
            defaults={
                'name': '测试商品',
                'price': '99.00',
                'status': 'published',
                'category_id': 1
            }
        )
        if created:
            print_success("创建测试商品")
    except Exception as e:
        print_info(f"商品已存在或创建失败: {e}")


def test_products_api():
    """测试商品 API"""
    print_header("1. Products API 测试")

    # 1.1 获取分类列表
    print_info("1.1 获取分类列表...")
    response = make_request('GET', '/api/products/categories/')
    expect_success(response, "获取分类列表")

    # 1.2 获取分类树
    print_info("1.2 获取分类树...")
    response = make_request('GET', '/api/products/categories/tree/')
    expect_success(response, "获取分类树")

    # 1.3 获取商品列表
    print_info("1.3 获取商品列表...")
    response = make_request('GET', '/api/products/products/')
    expect_success(response, "获取商品列表")

    # 1.4 商品筛选（按分类）
    print_info("1.4 商品筛选（按分类）...")
    response = make_request('GET', '/api/products/products/?category=1')
    expect_success(response, "按分类筛选")

    # 1.5 商品搜索
    print_info("1.5 商品搜索...")
    response = make_request('GET', '/api/products/products/?search=测试')
    expect_success(response, "商品搜索")

    # 1.6 商品排序
    print_info("1.6 商品排序（按价格）...")
    response = make_request('GET', '/api/products/products/?ordering=-price')
    expect_success(response, "商品排序")

    # 1.7 获取推荐商品
    print_info("1.7 获取推荐商品...")
    response = make_request('GET', '/api/products/products/featured/')
    expect_success(response, "推荐商品")

    # 1.8 获取新品上市
    print_info("1.8 获取新品上市...")
    response = make_request('GET', '/api/products/products/new-arrivals/')
    expect_success(response, "新品上市")

    # 1.9 获取商品详情
    print_info("1.9 获取商品详情...")
    response = make_request('GET', '/api/products/products/1/')
    expect_success(response, "商品详情")

    # 1.10 获取商品图片列表
    print_info("1.10 获取商品图片列表...")
    response = make_request('GET', '/api/products/images/')
    expect_success(response, "商品图片列表")

    # 1.11 获取商品属性列表
    print_info("1.11 获取商品属性列表...")
    response = make_request('GET', '/api/products/attributes/')
    expect_success(response, "商品属性列表")


def test_marketing_api():
    """测试营销 API"""
    print_header("2. Marketing API 测试")

    # 2.1 获取优惠券列表（无需认证）
    print_info("2.1 获取优惠券列表...")
    response = make_request('GET', '/api/marketing/coupons/')
    expect_success(response, "优惠券列表")

    # 2.2 管理员创建优惠券
    if ADMIN_USER:
        print_info("2.2 管理员创建优惠券...")
        coupon_data = {
            'name': '测试优惠券',
            'description': '测试描述',
            'discount_type': 'full_reduction',
            'min_amount': '100.00',
            'discount_amount': '10.00',
            'valid_from': datetime.now().isoformat(),
            'valid_until': (datetime.now() + timedelta(days=30)).isoformat(),
            'total_quantity': 100,
            'per_user_limit': 1,
            'is_active': True
        }
        headers = ensure_authenticated(ADMIN_USER)
        response = make_request('POST', '/api/marketing/coupons/', coupon_data, **headers)
        if response and response.status_code == 201:
            expect_success(response, "创建优惠券")
        else:
            print_info("创建优惠券失败或已存在")

    # 2.3 获取我的优惠券（需要认证）
    if TEST_USER:
        print_info("2.3 获取我的优惠券...")
        headers = ensure_authenticated(TEST_USER)
        response = make_request('GET', '/api/marketing/coupons/my-coupons/', **headers)
        expect_success(response, "我的优惠券")

        # 2.4 领取优惠券（如果有优惠券）
        print_info("2.4 领取优惠券...")
        response = make_request('POST', '/api/marketing/coupons/1/claim/', **headers)
        if response and response.status_code == 200:
            expect_success(response, "领取优惠券")
        else:
            print_info("领取失败（可能已领完或优惠券不存在）")


def test_content_api():
    """测试内容管理 API"""
    print_header("3. Content API 测试")

    # 3.1 获取改装案例列表
    print_info("3.1 获取改装案例列表...")
    response = make_request('GET', '/api/content/cases/')
    expect_success(response, "改装案例列表")

    # 3.2 管理员创建案例
    if ADMIN_USER:
        print_info("3.2 管理员创建改装案例...")
        case_data = {
            'title': '测试改装案例',
            'summary': '测试摘要',
            'content': '测试内容',
            'author': '管理员',
            'status': 'published'
        }
        headers = ensure_authenticated(ADMIN_USER)
        response = make_request('POST', '/api/content/cases/', case_data, **headers)
        if response and response.status_code == 201:
            expect_success(response, "创建改装案例")
        else:
            print_info("创建案例失败或已存在")

    # 3.3 获取 FAQ 列表
    print_info("3.3 获取 FAQ 列表...")
    response = make_request('GET', '/api/content/faqs/')
    expect_success(response, "FAQ 列表")

    # 3.4 FAQ 分类筛选
    print_info("3.4 FAQ 分类筛选...")
    response = make_request('GET', '/api/content/faqs/?category=order')
    expect_success(response, "FAQ 分类筛选")


def test_system_api():
    """测试系统管理 API"""
    print_header("4. System API 测试")

    # 4.1 获取系统配置列表
    print_info("4.1 获取系统配置列表...")
    response = make_request('GET', '/api/system/configs/')
    expect_success(response, "系统配置列表")

    # 4.2 管理员创建配置
    if ADMIN_USER:
        print_info("4.2 管理员创建系统配置...")
        config_data = {
            'key': 'test_config_key',
            'value': 'test_value',
            'description': '测试配置',
            'category': 'basic',
            'is_editable': True
        }
        headers = ensure_authenticated(ADMIN_USER)
        response = make_request('POST', '/api/system/configs/', config_data, **headers)
        if response and response.status_code == 201:
            expect_success(response, "创建系统配置")
        else:
            print_info("创建配置失败或已存在")

    # 4.3 获取我的消息（需要认证）
    if TEST_USER:
        print_info("4.3 获取我的消息...")
        headers = ensure_authenticated(TEST_USER)
        response = make_request('GET', '/api/system/messages/my-messages/', **headers)
        expect_success(response, "我的消息")

    # 4.4 获取操作日志（管理员）
    if ADMIN_USER:
        print_info("4.4 获取操作日志...")
        headers = ensure_authenticated(ADMIN_USER)
        response = make_request('GET', '/api/system/logs/', **headers)
        expect_success(response, "操作日志")


def test_api_response_format():
    """测试 API 响应格式规范"""
    print_header("5. API 响应格式验证")

    # 检查响应格式
    print_info("5.1 验证响应格式...")
    response = make_request('GET', '/api/products/products/')
    if response:
        try:
            data = json.loads(response.content)
            if 'code' in data and 'message' in data and 'data' in data:
                print_success("响应格式正确: code, message, data")
            else:
                print_fail("响应格式不正确，缺少必需字段")
        except json.JSONDecodeError:
            print_fail("响应不是 JSON 格式")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Phase 3 API 测试".center(60))
    print("=" * 60)
    print(f"\n测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 创建测试数据
    setup_test_data()

    # 运行所有测试
    test_products_api()
    test_marketing_api()
    test_content_api()
    test_system_api()
    test_api_response_format()

    # 总结
    print_header("测试完成")
    print("请查看上方输出确认所有 API 是否正常工作。")
    print("\n测试说明:")
    print("- 使用 Django 测试客户端进行测试")
    print("- 测试数据会自动创建或使用现有数据")
    print("- 某些测试需要管理员权限")


if __name__ == '__main__':
    run_all_tests()
