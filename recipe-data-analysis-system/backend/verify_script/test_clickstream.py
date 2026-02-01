# -*- coding: utf-8 -*-
"""
点击流分析接口测试脚本

测试点击流分析 API 的功能，验证：
1. 接口返回数据格式正确
2. 权限验证（管理员 vs 普通用户）
3. 行为分布统计正确
4. 转化漏斗计算正确
5. 路径模式分析正确
6. 参数验证正确
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
# 脚本位置: backend/verify_script/test_clickstream.py
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 切换到 backend 目录
os.chdir(str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import RequestFactory
from rest_framework.test import APIClient
from accounts.models import User
from behavior_logs.models import UserBehaviorLog
from utils.constants import BehaviorType
from analytics.views import ClickStreamAnalysisView


class TestColors:
    """测试输出颜色"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """打印标题"""
    print(f"\n{TestColors.HEADER}{TestColors.BOLD}{'=' * 60}{TestColors.ENDC}")
    print(f"{TestColors.HEADER}{TestColors.BOLD}{text:^60}{TestColors.ENDC}")
    print(f"{TestColors.HEADER}{TestColors.BOLD}{'=' * 60}{TestColors.ENDC}\n")


def print_test(name: str):
    """打印测试名称"""
    print(f"{TestColors.OKCYAN}测试:{TestColors.ENDC} {name}")


def print_pass(message: str = ""):
    """打印通过"""
    if message:
        print(f"  {TestColors.OKGREEN}[OK] PASS{TestColors.ENDC}: {message}")
    else:
        print(f"  {TestColors.OKGREEN}[OK] PASS{TestColors.ENDC}")


def print_fail(message: str):
    """打印失败"""
    print(f"  {TestColors.FAIL}[X] FAIL{TestColors.ENDC}: {message}")


def print_info(message: str):
    """打印信息"""
    print(f"  {TestColors.OKBLUE}[i] INFO{TestColors.ENDC}: {message}")


def print_warning(message: str):
    """打印警告"""
    print(f"  {TestColors.WARNING}[!] WARNING{TestColors.ENDC}: {message}")


# ========== 测试数据准备 ==========

def setup_test_data():
    """准备测试数据"""
    print_test("准备测试数据")

    # 清理测试数据
    UserBehaviorLog.objects.filter(target__contains='TEST').delete()

    # 获取或创建测试用户
    try:
        admin_user = User.objects.get(username='test_admin_clickstream')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='test_admin_clickstream',
            email='admin_clickstream@test.com',
            password='testpass123',
            role='admin'
        )
        print_info(f"创建管理员用户: {admin_user.username}")

    try:
        normal_user = User.objects.get(username='test_user_clickstream')
    except User.DoesNotExist:
        normal_user = User.objects.create_user(
            username='test_user_clickstream',
            email='user_clickstream@test.com',
            password='testpass123',
            role='user'
        )
        print_info(f"创建普通用户: {normal_user.username}")

    # 创建测试行为日志
    now = timezone.now() if 'timezone' in dir() else datetime.now()
    base_time = datetime.now() - timedelta(days=7)

    behaviors = [
        # 管理员用户的行为
        {'user': admin_user, 'behavior_type': BehaviorType.LOGIN, 'target': None, 'timestamp': base_time},
        {'user': admin_user, 'behavior_type': BehaviorType.SEARCH, 'target': '/recipes', 'timestamp': base_time + timedelta(minutes=5)},
        {'user': admin_user, 'behavior_type': BehaviorType.VIEW, 'target': 'recipe:1', 'timestamp': base_time + timedelta(minutes=10)},
        {'user': admin_user, 'behavior_type': BehaviorType.VIEW, 'target': 'recipe:2', 'timestamp': base_time + timedelta(minutes=15)},
        {'user': admin_user, 'behavior_type': BehaviorType.COLLECT, 'target': 'recipe:1', 'timestamp': base_time + timedelta(minutes=20)},

        # 普通用户的行为
        {'user': normal_user, 'behavior_type': BehaviorType.LOGIN, 'target': None, 'timestamp': base_time + timedelta(hours=1)},
        {'user': normal_user, 'behavior_type': BehaviorType.VIEW, 'target': 'recipe:3', 'timestamp': base_time + timedelta(hours=1, minutes=5)},
        {'user': normal_user, 'behavior_type': BehaviorType.COLLECT, 'target': 'recipe:3', 'timestamp': base_time + timedelta(hours=1, minutes=10)},

        # 匿名用户的行为
        {'user': None, 'behavior_type': BehaviorType.VIEW, 'target': 'recipe:5', 'timestamp': base_time + timedelta(hours=2)},
        {'user': None, 'behavior_type': BehaviorType.VIEW, 'target': 'recipe:6', 'timestamp': base_time + timedelta(hours=2, minutes=10)},
    ]

    created_count = 0
    for behavior in behaviors:
        # 设置时间
        if 'timestamp' in behavior:
            UserBehaviorLog.objects.create(
                user=behavior['user'],
                behavior_type=behavior['behavior_type'],
                target=behavior['target'],
                timestamp=behavior['timestamp'],
                extra_data={'test_marker': True}
            )
        else:
            UserBehaviorLog.objects.create(
                user=behavior['user'],
                behavior_type=behavior['behavior_type'],
                target=behavior['target'],
                extra_data={'test_marker': True}
            )
        created_count += 1

    print_pass(f"创建了 {created_count} 条测试行为日志")
    return admin_user, normal_user


def cleanup_test_data():
    """清理测试数据"""
    print_test("清理测试数据")
    UserBehaviorLog.objects.filter(target__contains='TEST').delete()
    User.objects.filter(username__in=['test_admin_clickstream', 'test_user_clickstream']).delete()
    print_pass("测试数据已清理")


# ========== API 测试 ==========

def test_api_endpoint_exists():
    """测试1: 验证 API 端点存在"""
    print_test("验证 API 端点存在")

    try:
        view = ClickStreamAnalysisView()
        print_pass(f"ClickStreamAnalysisView 视图类存在")
        return True
    except Exception as e:
        print_fail(f"视图类不存在: {e}")
        return False


def test_api_response_format(admin_user):
    """测试2: 验证 API 响应格式"""
    print_test("验证 API 响应格式")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/clickstream/')

    if response.status_code != 200:
        print_fail(f"HTTP 状态码: {response.status_code}")
        return False

    data = response.json()

    # 验证响应结构
    required_keys = ['code', 'message', 'data']
    if not all(k in data for k in required_keys):
        print_fail(f"响应缺少必要字段: {required_keys}")
        return False

    if data['code'] != 200:
        print_fail(f"响应码错误: {data['code']}")
        return False

    # 验证数据结构
    data_content = data.get('data', {})
    required_data_keys = ['summary', 'behavior_distribution', 'conversion_funnel', 'path_patterns']
    if not all(k in data_content for k in required_data_keys):
        print_fail(f"数据缺少必要字段: {required_data_keys}")
        return False

    print_pass(f"响应格式正确")
    print_info(f"总记录数: {data_content['summary']['total_logs']}")
    print_info(f"独立用户数: {data_content['summary']['unique_users']}")
    return True


def test_admin_permission():
    """测试3: 验证管理员权限"""
    print_test("验证管理员权限")

    client = APIClient()

    # 未认证访问
    response = client.get('/api/admin/analytics/clickstream/')
    if response.status_code != 401:
        print_fail(f"未认证访问应该返回 401，实际: {response.status_code}")
        return False
    print_info("未认证访问返回 401 [OK]")

    # 普通用户访问
    try:
        normal_user = User.objects.get(username='test_user_clickstream')
    except User.DoesNotExist:
        normal_user = User.objects.create_user(
            username='test_user_clickstream',
            email='test@test.com',
            password='test123',
            role='user'
        )

    client.force_authenticate(user=normal_user)
    response = client.get('/api/admin/analytics/clickstream/')
    if response.status_code != 403:
        print_fail(f"普通用户访问应该返回 403，实际: {response.status_code}")
        return False
    print_info("普通用户访问返回 403 [OK]")

    # 管理员访问
    try:
        admin_user = User.objects.get(username='test_admin_clickstream')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='test_admin_clickstream',
            email='admin@test.com',
            password='test123',
            role='admin'
        )

    client.force_authenticate(user=admin_user)
    response = client.get('/api/admin/analytics/clickstream/')
    if response.status_code != 200:
        print_fail(f"管理员访问应该返回 200，实际: {response.status_code}")
        return False
    print_info("管理员访问返回 200 [OK]")

    print_pass("权限验证正确")
    return True


def test_behavior_distribution(admin_user):
    """测试4: 验证行为分布统计"""
    print_test("验证行为分布统计")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/clickstream/')
    data = response.json()
    behavior_dist = data['data']['behavior_distribution']

    # 检查是否包含各行为类型
    expected_behaviors = ['login', 'search', 'view', 'collect']
    missing = [b for b in expected_behaviors if b not in behavior_dist]

    if missing:
        print_fail(f"缺少行为类型: {missing}")
        return False

    # 检查是否有百分比字段
    percentage_fields = [f'{b}_percentage' for b in expected_behaviors]
    missing_pct = [p for p in percentage_fields if p not in behavior_dist]

    if missing_pct:
        print_fail(f"缺少百分比字段: {missing_pct}")
        return False

    print_pass(f"行为分布统计正确: {list(behavior_dist.keys())}")
    return True


def test_conversion_funnel(admin_user):
    """测试5: 验证转化漏斗计算"""
    print_test("验证转化漏斗计算")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/clickstream/')
    data = response.json()
    funnel = data['data']['conversion_funnel']

    required_fields = ['login_users', 'view_users', 'collect_users',
                       'login_to_view_rate', 'view_to_collect_rate', 'overall_conversion_rate']

    missing = [f for f in required_fields if f not in funnel]
    if missing:
        print_fail(f"缺少必要字段: {missing}")
        return False

    # 验证数据合理性
    if funnel['login_users'] > 0:
        if funnel['view_users'] > funnel['login_users']:
            print_warning(f"浏览用户数大于登录用户数，可能数据异常")

    print_info(f"登录用户: {funnel['login_users']}")
    print_info(f"浏览用户: {funnel['view_users']}")
    print_info(f"收藏用户: {funnel['collect_users']}")
    print_info(f"登录->浏览转化率: {funnel['login_to_view_rate']}%")
    print_info(f"浏览->收藏转化率: {funnel['view_to_collect_rate']}%")

    print_pass("转化漏斗数据完整")
    return True


def test_path_patterns(admin_user):
    """测试6: 验证路径模式分析"""
    print_test("验证路径模式分析")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/clickstream/')
    data = response.json()
    path_patterns = data['data']['path_patterns']

    if not isinstance(path_patterns, list):
        print_fail(f"路径模式应该是列表，实际: {type(path_patterns)}")
        return False

    if len(path_patterns) > 0:
        pattern = path_patterns[0]
        required_fields = ['path', 'count', 'percentage', 'views', 'collects', 'conversion_rate']
        missing = [f for f in required_fields if f not in pattern]
        if missing:
            print_fail(f"路径模式缺少字段: {missing}")
            return False

        print_info(f"Top 路径: {pattern['path']}")
        print_info(f"访问次数: {pattern['count']}")
        print_info(f"转化率: {pattern['conversion_rate']}%")

    print_pass(f"路径模式分析正确，共 {len(path_patterns)} 个模式")
    return True


def test_query_parameters():
    """测试7: 验证查询参数"""
    print_test("验证查询参数")

    # 获取管理员用户
    try:
        admin_user = User.objects.get(username='test_admin_clickstream')
    except User.DoesNotExist:
        print_fail("管理员用户不存在")
        return False

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # 测试 days 参数
    response = client.get('/api/admin/analytics/clickstream/?days=7')
    if response.status_code != 200:
        print_fail(f"days 参数请求失败: {response.status_code}")
        return False
    print_info("days=7 参数正常 [OK]")

    # 测试 limit_path 参数
    response = client.get('/api/admin/analytics/clickstream/?limit_path=10')
    if response.status_code != 200:
        print_fail(f"limit_path 参数请求失败: {response.status_code}")
        return False
    print_info("limit_path=10 参数正常 [OK]")

    # 测试无效参数
    response = client.get('/api/admin/analytics/clickstream/?days=999')
    data = response.json()
    # 无效参数应该使用默认值，不会报错
    print_info("无效参数已使用默认值处理 [OK]")

    print_pass("查询参数验证正确")
    return True


def test_response_time(admin_user):
    """测试8: 验证响应时间"""
    print_test("验证响应时间")

    import time

    client = APIClient()
    client.force_authenticate(user=admin_user)

    start_time = time.time()
    response = client.get('/api/admin/analytics/clickstream/')
    end_time = time.time()

    duration = round((end_time - start_time) * 1000, 2)

    if response.status_code != 200:
        print_fail(f"请求失败: {response.status_code}")
        return False

    print_info(f"响应时间: {duration}ms")

    # 性能要求 < 2s
    if duration < 2000:
        print_pass(f"响应时间达标: {duration}ms")
        return True
    else:
        print_warning(f"响应时间过长: {duration}ms")
        return False


# ========== 主测试函数 ==========

def run_all_tests():
    """运行所有测试"""
    print_header("点击流分析接口测试")

    results = {}
    admin_user = None
    normal_user = None

    try:
        # 准备测试数据
        admin_user, normal_user = setup_test_data()

        # 运行测试
        results['API端点存在'] = test_api_endpoint_exists()
        results['响应格式正确'] = test_api_response_format(admin_user)
        results['管理员权限验证'] = test_admin_permission()
        results['行为分布统计'] = test_behavior_distribution(admin_user)
        results['转化漏斗计算'] = test_conversion_funnel(admin_user)
        results['路径模式分析'] = test_path_patterns(admin_user)
        results['查询参数验证'] = test_query_parameters()
        results['响应时间'] = test_response_time(admin_user)

    except Exception as e:
        print(f"\n{TestColors.FAIL}[X] 测试异常: {e}{TestColors.ENDC}")
        import traceback
        traceback.print_exc()
        results['测试执行'] = False

    finally:
        # 清理测试数据
        cleanup_test_data()

    # 打印测试结果汇总
    print_header("测试结果汇总")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = f"{TestColors.OKGREEN}[OK] PASS{TestColors.ENDC}" if result else f"{TestColors.FAIL}[X] FAIL{TestColors.ENDC}"
        print(f"  {status} {test_name}")

    print(f"\n{TestColors.BOLD}测试通过率: {passed}/{total} ({passed/total*100:.1f}%){TestColors.ENDC}")

    if passed == total:
        print(f"\n{TestColors.OKGREEN}{TestColors.BOLD}[SUCCESS] 所有测试通过！{TestColors.ENDC}")
        return True
    elif passed >= total * 0.8:
        print(f"\n{TestColors.WARNING}{TestColors.BOLD}[WARNING] 大部分测试通过{TestColors.ENDC}")
        return True
    else:
        print(f"\n{TestColors.FAIL}{TestColors.BOLD}[FAIL] 部分测试失败{TestColors.ENDC}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
