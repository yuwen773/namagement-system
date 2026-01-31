"""
管理员数据分析页面 - 完整测试脚本

测试管理员数据分析页面的所有功能：
1. 菜系深度分析 API
2. 难度深度分析 API
3. 热门菜谱分析 API（不同排序和限制）
4. 食材关联分析 API（不同分类和限制）
5. 权限验证（普通用户不能访问）
6. 数据结构验证
"""

import os
import sys
import django
import json

# 设置 Django 环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# 配置
BASE_URL = 'http://localhost:8000'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
TEST_USER_USERNAME = 'testuser'
TEST_USER_PASSWORD = 'testuser123'


class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_section(text):
    """打印小节"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}--- {text} ---{Colors.ENDC}\n")


def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")


def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}[FAIL] {text}{Colors.ENDC}")


def print_info(text):
    """打印信息"""
    print(f"{Colors.OKBLUE}[INFO] {text}{Colors.ENDC}")


def get_auth_token(username, password):
    """获取认证令牌"""
    client = Client()
    response = client.post('/api/accounts/login/', {
        'username': username,
        'password': password
    }, content_type='application/json')

    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('token')
    return None


def test_admin_cuisine_analysis(token):
    """测试菜系深度分析 API"""
    print_section("测试菜系深度分析 API")

    client = Client()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    response = client.get('/api/admin/analytics/cuisines/', **headers)

    if response.status_code == 200:
        data = response.json()
        print_success(f"菜系深度分析 API 返回成功 (状态码: {response.status_code})")

        # 验证数据结构
        if 'data' in data:
            content = data['data']
            checks = [
                ('summary 字段存在', 'summary' in content),
                ('cuisines 字段存在', 'cuisines' in content),
                ('total_recipes 存在', content.get('summary', {}).get('total_recipes') is not None),
                ('total_cuisines 存在', content.get('summary', {}).get('total_cuisines') is not None),
                ('cuisines 是列表', isinstance(content.get('cuisines'), list)),
            ]

            for check_name, result in checks:
                if result:
                    print_success(f"  {check_name}")
                else:
                    print_error(f"  {check_name}")

            # 验证菜系数据结构
            if content.get('cuisines'):
                cuisine = content['cuisines'][0]
                cuisine_fields = ['name', 'count', 'percentage', 'avg_view_count',
                                 'avg_favorite_count', 'avg_cooking_time', 'difficulty_distribution']
                print_info("  菜系数据字段验证:")
                for field in cuisine_fields:
                    if field in cuisine:
                        print_success(f"    {field}: {cuisine[field]}")
                    else:
                        print_error(f"    {field}: 缺失")

            # 打印统计信息
            summary = content.get('summary', {})
            print_info(f"  总菜谱数: {summary.get('total_recipes')}")
            print_info(f"  菜系类型数: {summary.get('total_cuisines')}")
            print_info(f"  菜系列表长度: {len(content.get('cuisines', []))}")

            return True
        else:
            print_error("响应中缺少 data 字段")
            return False
    else:
        print_error(f"菜系深度分析 API 请求失败 (状态码: {response.status_code})")
        print_error(f"响应内容: {response.content.decode()[:200]}")
        return False


def test_admin_difficulty_analysis(token):
    """测试难度深度分析 API"""
    print_section("测试难度深度分析 API")

    client = Client()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    response = client.get('/api/admin/analytics/difficulty/', **headers)

    if response.status_code == 200:
        data = response.json()
        print_success(f"难度深度分析 API 返回成功 (状态码: {response.status_code})")

        if 'data' in data:
            content = data['data']
            checks = [
                ('summary 字段存在', 'summary' in content),
                ('difficulties 字段存在', 'difficulties' in content),
                ('total_recipes 存在', content.get('summary', {}).get('total_recipes') is not None),
                ('difficulties 是列表', isinstance(content.get('difficulties'), list)),
            ]

            for check_name, result in checks:
                if result:
                    print_success(f"  {check_name}")
                else:
                    print_error(f"  {check_name}")

            # 验证难度数据结构
            if content.get('difficulties'):
                difficulty = content['difficulties'][0]
                difficulty_fields = ['name', 'value', 'count', 'percentage',
                                   'avg_cooking_time', 'avg_view_count', 'avg_favorite_count']
                print_info("  难度数据字段验证:")
                for field in difficulty_fields:
                    if field in difficulty:
                        print_success(f"    {field}: {difficulty[field]}")
                    else:
                        print_error(f"    {field}: 缺失")

            summary = content.get('summary', {})
            print_info(f"  总菜谱数: {summary.get('total_recipes')}")
            print_info(f"  难度等级数: {summary.get('total_difficulty_levels')}")

            return True
        else:
            print_error("响应中缺少 data 字段")
            return False
    else:
        print_error(f"难度深度分析 API 请求失败 (状态码: {response.status_code})")
        return False


def test_admin_hot_recipes_analysis(token):
    """测试热门菜谱分析 API（不同排序和限制）"""
    print_section("测试热门菜谱分析 API")

    client = Client()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    test_cases = [
        {'sort_by': 'view_count', 'limit': 20, 'name': '按点击量 Top 20'},
        {'sort_by': 'favorite_count', 'limit': 50, 'name': '按收藏量 Top 50'},
        {'sort_by': 'view_count', 'limit': 100, 'name': '按点击量 Top 100'},
    ]

    all_passed = True
    for test_case in test_cases:
        print_info(f"  测试用例: {test_case['name']}")

        params = {
            'sort_by': test_case['sort_by'],
            'limit': test_case['limit']
        }
        response = client.get('/api/admin/analytics/hot/', data=params, **headers)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                content = data['data']
                checks = [
                    ('summary 字段存在', 'summary' in content),
                    ('trends 字段存在', 'trends' in content),
                    ('recipes 字段存在', 'recipes' in content),
                    ('recipes 数量正确', len(content.get('recipes', [])) <= test_case['limit']),
                ]

                for check_name, result in checks:
                    if result:
                        print_success(f"    {check_name}")
                    else:
                        print_error(f"    {check_name}")
                        all_passed = False

                # 验证菜谱数据结构
                if content.get('recipes'):
                    recipe = content['recipes'][0]
                    recipe_fields = ['id', 'name', 'cuisine_type', 'difficulty',
                                   'view_count', 'favorite_count', 'conversion_rate']
                    for field in recipe_fields:
                        if field not in recipe:
                            print_error(f"    菜谱缺少字段: {field}")
                            all_passed = False
            else:
                print_error(f"    响应中缺少 data 字段")
                all_passed = False
        else:
            print_error(f"    请求失败 (状态码: {response.status_code})")
            all_passed = False

    return all_passed


def test_admin_ingredient_pairs_analysis(token):
    """测试食材关联分析 API（不同分类和限制）"""
    print_section("测试食材关联分析 API")

    client = Client()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    test_cases = [
        {'category': '', 'limit': 50, 'name': '全部分类 Top 50'},
        {'category': 'seasoning', 'limit': 20, 'name': '调料分类 Top 20'},
        {'category': 'vegetable', 'limit': 30, 'name': '蔬菜分类 Top 30'},
    ]

    all_passed = True
    for test_case in test_cases:
        print_info(f"  测试用例: {test_case['name']}")

        params = {}
        if test_case['category']:
            params['category'] = test_case['category']
        params['limit'] = test_case['limit']

        response = client.get('/api/admin/analytics/ingredient-pairs/', data=params, **headers)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                content = data['data']
                checks = [
                    ('summary 字段存在', 'summary' in content),
                    ('pairs 字段存在', 'pairs' in content),
                    ('pairs 数量正确', len(content.get('pairs', [])) <= test_case['limit']),
                ]

                for check_name, result in checks:
                    if result:
                        print_success(f"    {check_name}")
                    else:
                        print_error(f"    {check_name}")
                        all_passed = False

                # 验证配对数据结构
                if content.get('pairs'):
                    pair = content['pairs'][0]
                    required_fields = ['ingredient_1', 'ingredient_2', 'count', 'percentage']
                    for field in required_fields:
                        if field not in pair:
                            print_error(f"    配对缺少字段: {field}")
                            all_passed = False
                        elif field == 'ingredient_1' or field == 'ingredient_2':
                            # 验证食材对象字段
                            ingredient_fields = ['id', 'name', 'category']
                            for ing_field in ingredient_fields:
                                if ing_field not in pair[field]:
                                    print_error(f"    食材缺少字段: {ing_field}")
                                    all_passed = False
            else:
                print_error(f"    响应中缺少 data 字段")
                all_passed = False
        else:
            print_error(f"    请求失败 (状态码: {response.status_code})")
            all_passed = False

    return all_passed


def test_permission_denied_for_normal_user():
    """测试普通用户不能访问管理员分析 API"""
    print_section("测试权限验证 - 普通用户应被拒绝")

    # 获取普通用户 token
    token = get_auth_token(TEST_USER_USERNAME, TEST_USER_PASSWORD)

    if not token:
        print_info("  测试用户不存在，跳过此测试")
        return True

    client = Client()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    endpoints = [
        '/api/admin/analytics/cuisines/',
        '/api/admin/analytics/difficulty/',
        '/api/admin/analytics/hot/',
        '/api/admin/analytics/ingredient-pairs/',
    ]

    all_passed = True
    for endpoint in endpoints:
        response = client.get(endpoint, **headers)

        if response.status_code == 403:
            print_success(f"  {endpoint} - 正确拒绝访问 (403)")
        else:
            print_error(f"  {endpoint} - 应返回 403，实际返回 {response.status_code}")
            all_passed = False

    return all_passed


def test_data_accuracy(token):
    """测试数据准确性"""
    print_section("测试数据准确性")

    client = Client()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    # 获取菜系数据
    response = client.get('/api/admin/analytics/cuisines/', **headers)
    if response.status_code == 200:
        data = response.json()
        cuisines = data.get('data', {}).get('cuisines', [])

        # 验证占比总和是否接近 100%
        total_percentage = sum(c.get('percentage', 0) for c in cuisines)
        if 99.5 <= total_percentage <= 100.5:
            print_success(f"  菜系占比总和正确: {total_percentage:.2f}%")
        else:
            print_error(f"  菜系占比总和异常: {total_percentage:.2f}%")

        # 验证数量总和是否等于总菜谱数
        total_count = sum(c.get('count', 0) for c in cuisines)
        summary_total = data.get('data', {}).get('summary', {}).get('total_recipes', 0)
        if total_count == summary_total:
            print_success(f"  菜系数量总和正确: {total_count}")
        else:
            print_error(f"  菜系数量总和不匹配: {total_count} vs {summary_total}")

    # 获取难度数据
    response = client.get('/api/admin/analytics/difficulty/', **headers)
    if response.status_code == 200:
        data = response.json()
        difficulties = data.get('data', {}).get('difficulties', [])

        total_percentage = sum(d.get('percentage', 0) for d in difficulties)
        if 99.5 <= total_percentage <= 100.5:
            print_success(f"  难度占比总和正确: {total_percentage:.2f}%")
        else:
            print_error(f"  难度占比总和异常: {total_percentage:.2f}%")

    return True


def run_all_tests():
    """运行所有测试"""
    print_header("管理员数据分析页面 - 完整功能测试")

    # 获取管理员 token
    print_info("获取管理员认证令牌...")
    admin_token = get_auth_token(ADMIN_USERNAME, ADMIN_PASSWORD)

    if not admin_token:
        print_error("无法获取管理员令牌，请检查管理员账号是否存在")
        print_info("尝试创建管理员账号...")
        try:
            User.objects.filter(username=ADMIN_USERNAME).delete()
            admin = User.objects.create_user(
                username=ADMIN_USERNAME,
                password=ADMIN_PASSWORD,
                email='admin@example.com',
                role='admin'
            )
            print_success(f"管理员账号已创建: {ADMIN_USERNAME}")
            admin_token = get_auth_token(ADMIN_USERNAME, ADMIN_PASSWORD)
        except Exception as e:
            print_error(f"创建管理员账号失败: {e}")
            return False

    if not admin_token:
        print_error("仍然无法获取管理员令牌，测试终止")
        return False

    print_success("管理员令牌获取成功")

    # 确保测试用户存在
    if not User.objects.filter(username=TEST_USER_USERNAME).exists():
        User.objects.create_user(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            email='testuser@example.com',
            role='user'
        )
        print_info(f"测试用户已创建: {TEST_USER_USERNAME}")

    # 运行测试
    test_results = []

    test_results.append(("菜系深度分析 API", test_admin_cuisine_analysis(admin_token)))
    test_results.append(("难度深度分析 API", test_admin_difficulty_analysis(admin_token)))
    test_results.append(("热门菜谱分析 API", test_admin_hot_recipes_analysis(admin_token)))
    test_results.append(("食材关联分析 API", test_admin_ingredient_pairs_analysis(admin_token)))
    test_results.append(("权限验证 - 普通用户拒绝", test_permission_denied_for_normal_user()))
    test_results.append(("数据准确性验证", test_data_accuracy(admin_token)))

    # 打印测试结果汇总
    print_header("测试结果汇总")

    passed_count = sum(1 for _, result in test_results if result)
    total_count = len(test_results)

    for test_name, result in test_results:
        status = f"{Colors.OKGREEN}通过{Colors.ENDC}" if result else f"{Colors.FAIL}失败{Colors.ENDC}"
        print(f"  {test_name}: {status}")

    print(f"\n{Colors.BOLD}总计: {passed_count}/{total_count} 通过{Colors.ENDC}")

    if passed_count == total_count:
        print(f"{Colors.OKGREEN}{Colors.BOLD}所有测试通过！{Colors.ENDC}\n")
        return True
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}部分测试失败，请检查{Colors.ENDC}\n")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
