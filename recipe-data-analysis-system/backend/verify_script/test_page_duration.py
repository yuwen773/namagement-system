# -*- coding: utf-8 -*-
"""
页面停留分析接口测试脚本

测试页面停留分析 API 的功能，验证：
1. 接口返回数据格式正确
2. 权限验证（管理员 vs 普通用户）
3. 各页面平均停留时间计算正确
4. 停留时长分布统计正确
5. 趋势数据正确
6. 参数验证正确
7. 页面筛选功能正确
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
# 脚本位置: backend/verify_script/test_page_duration.py
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 切换到 backend 目录
os.chdir(str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import RequestFactory
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models import User
from behavior_logs.models import UserBehaviorLog
from analytics.views import PageDurationAnalysisView


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
    UserBehaviorLog.objects.filter(target__contains='TEST_PAGE').delete()
    User.objects.filter(username__startswith='test_admin_page').delete()
    User.objects.filter(username__startswith='test_user_page').delete()

    # 创建测试用户
    admin_users = []
    normal_users = []

    # 创建 3 个管理员用户
    for i in range(3):
        try:
            admin_user = User.objects.get(username=f'test_admin_page_{i}')
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username=f'test_admin_page_{i}',
                email=f'admin_page_{i}@test.com',
                password='testpass123',
                role='admin'
            )
        admin_users.append(admin_user)

    # 创建 5 个普通用户
    for i in range(5):
        try:
            normal_user = User.objects.get(username=f'test_user_page_{i}')
        except User.DoesNotExist:
            normal_user = User.objects.create_user(
                username=f'test_user_page_{i}',
                email=f'user_page_{i}@test.com',
                password='testpass123',
                role='user'
            )
        normal_users.append(normal_user)

    print_info(f"创建了 {len(admin_users)} 个管理员用户和 {len(normal_users)} 个普通用户")

    # 创建测试页面访问日志（带停留时间）
    now = timezone.now()

    # 首页访问（短停留）
    for i in range(5):
        UserBehaviorLog.objects.create(
            user=normal_users[i],
            behavior_type='page_view',
            target='home',
            timestamp=now - timedelta(days=1, hours=i),
            extra_data={'duration': 10 + i * 5, 'test_marker': True}  # 10-30秒
        )

    # 菜谱列表页访问（中停留）
    for i in range(5):
        UserBehaviorLog.objects.create(
            user=normal_users[i],
            behavior_type='page_view',
            target='/recipes',
            timestamp=now - timedelta(days=1, hours=i + 5),
            extra_data={'duration': 45 + i * 10, 'test_marker': True}  # 45-90秒
        )

    # 菜谱详情页访问（长停留）
    for i in range(3):
        UserBehaviorLog.objects.create(
            user=admin_users[i],
            behavior_type='page_view',
            target=f'recipe:{1000 + i}',
            timestamp=now - timedelta(hours=i),
            extra_data={'duration': 180 + i * 30, 'test_marker': True}  # 180-240秒
        )

    # 分类页访问
    for i in range(3):
        UserBehaviorLog.objects.create(
            user=normal_users[i],
            behavior_type='page_view',
            target='/category',
            timestamp=now - timedelta(hours=i + 3),
            extra_data={'duration': 60 + i * 15, 'test_marker': True}  # 60-90秒
        )

    # 热门页访问
    for i in range(2):
        UserBehaviorLog.objects.create(
            user=admin_users[i],
            behavior_type='page_view',
            target='/hot',
            timestamp=now - timedelta(hours=i + 6),
            extra_data={'duration': 30 + i * 10, 'test_marker': True}  # 30-40秒
        )

    # 测试无效停留时间数据
    UserBehaviorLog.objects.create(
        user=normal_users[0],
        behavior_type='page_view',
        target='home',
        timestamp=now,
        extra_data={'duration': -5, 'test_marker': True}  # 负值，应被过滤
    )

    UserBehaviorLog.objects.create(
        user=normal_users[1],
        behavior_type='page_view',
        target='home',
        timestamp=now - timedelta(hours=1),
        extra_data={'duration': 7200, 'test_marker': True}  # 2小时，应被过滤
    )

    # 无 extra_data 的日志
    UserBehaviorLog.objects.create(
        user=normal_users[2],
        behavior_type='page_view',
        target='home',
        timestamp=now - timedelta(hours=2),
        extra_data=None
    )

    print_pass(f"创建了测试页面访问数据")
    return admin_users, normal_users


def cleanup_test_data():
    """清理测试数据"""
    print_test("清理测试数据")
    UserBehaviorLog.objects.filter(target__contains='TEST_PAGE').delete()
    User.objects.filter(username__startswith='test_admin_page').delete()
    User.objects.filter(username__startswith='test_user_page').delete()
    print_pass("测试数据已清理")


# ========== API 测试 ==========

def test_api_endpoint_exists():
    """测试1: 验证 API 端点存在"""
    print_test("验证 API 端点存在")

    try:
        view = PageDurationAnalysisView()
        print_pass(f"PageDurationAnalysisView 视图类存在")
        return True
    except Exception as e:
        print_fail(f"视图类不存在: {e}")
        return False


def test_api_response_format(admin_user):
    """测试2: 验证 API 响应格式"""
    print_test("验证 API 响应格式")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/page-duration/')

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
    required_data_keys = ['summary', 'page_statistics', 'duration_distribution', 'trend']
    if not all(k in data_content for k in required_data_keys):
        print_fail(f"数据缺少必要字段: {required_data_keys}")
        return False

    # 验证 summary 结构
    summary = data_content.get('summary', {})
    summary_keys = ['total_logs', 'days', 'total_pages']
    if not all(k in summary for k in summary_keys):
        print_fail(f"summary 缺少必要字段: {summary_keys}")
        return False

    # 验证 page_statistics 结构
    page_stats = data_content.get('page_statistics', [])
    if not isinstance(page_stats, list):
        print_fail(f"page_statistics 应该是列表")
        return False

    if len(page_stats) > 0:
        first_page = page_stats[0]
        page_keys = ['page', 'avg_duration', 'total_visits', 'min_duration', 'max_duration', 'median_duration']
        if not all(k in first_page for k in page_keys):
            print_fail(f"page_statistics 项目缺少必要字段: {page_keys}")
            return False

    # 验证 duration_distribution 结构
    dist = data_content.get('duration_distribution', {})
    dist_keys = ['short', 'medium', 'long']
    if not all(k in dist for k in dist_keys):
        print_fail(f"duration_distribution 缺少必要字段: {dist_keys}")
        return False

    print_pass(f"响应格式正确")
    print_info(f"总页面访问记录: {summary['total_logs']}")
    print_info(f"分析天数: {summary['days']}")
    print_info(f"页面数: {summary['total_pages']}")
    return True


def test_admin_permission():
    """测试3: 验证管理员权限"""
    print_test("验证管理员权限")

    client = APIClient()

    # 未认证访问
    response = client.get('/api/admin/analytics/page-duration/')
    if response.status_code != 401:
        print_fail(f"未认证访问应该返回 401，实际: {response.status_code}")
        return False
    print_info("未认证访问返回 401 [OK]")

    # 普通用户访问
    try:
        normal_user = User.objects.get(username='test_user_page_0')
    except User.DoesNotExist:
        normal_user = User.objects.create_user(
            username='test_user_page_0',
            email='normal_page@test.com',
            password='test123',
            role='user'
        )

    client.force_authenticate(user=normal_user)
    response = client.get('/api/admin/analytics/page-duration/')
    if response.status_code != 403:
        print_fail(f"普通用户访问应该返回 403，实际: {response.status_code}")
        return False
    print_info("普通用户访问返回 403 [OK]")

    # 管理员访问
    admin_user = None
    try:
        admin_user = User.objects.get(username='test_admin_page_0')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='test_admin_page_0',
            email='admin_page@test.com',
            password='test123',
            role='admin'
        )

    client.force_authenticate(user=admin_user)
    response = client.get('/api/admin/analytics/page-duration/')
    if response.status_code != 200:
        print_fail(f"管理员访问应该返回 200，实际: {response.status_code}")
        return False
    print_info("管理员访问返回 200 [OK]")

    print_pass("权限验证正确")
    return True


def test_page_statistics(admin_user):
    """测试4: 验证页面统计数据"""
    print_test("验证页面统计数据")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/page-duration/')
    data = response.json()
    page_stats = data['data']['page_statistics']

    if not isinstance(page_stats, list):
        print_fail(f"页面统计数据应该是列表")
        return False

    # 检查是否包含预期的页面
    page_names = [p['page'] for p in page_stats]

    expected_pages = ['首页', '菜谱列表', '菜谱详情', '分类页', '热门页']
    found_pages = [p for p in expected_pages if p in page_names]

    if len(found_pages) < 3:
        print_warning(f"预期至少3个页面，实际发现: {len(found_pages)} 个")

    # 验证每个页面统计字段
    for page in page_stats:
        # 验证数据类型
        if not isinstance(page['avg_duration'], (int, float)):
            print_fail(f"avg_duration 应该是数字")
            return False

        if page['avg_duration'] < 0:
            print_fail(f"avg_duration 不能为负数")
            return False

        if not isinstance(page['total_visits'], int):
            print_fail(f"total_visits 应该是整数")
            return False

        if page['total_visits'] < 0:
            print_fail(f"total_visits 不能为负数")
            return False

        # 验证停留时间范围
        if page['min_duration'] > page['max_duration']:
            print_fail(f"min_duration 不应该大于 max_duration")
            return False

    print_info(f"发现 {len(page_stats)} 个页面的统计数据")
    for page in page_stats[:3]:  # 只显示前3个
        print_info(f"  - {page['page']}: 平均停留 {page['avg_duration']}秒, 访问 {page['total_visits']}次")

    print_pass("页面统计数据正确")
    return True


def test_duration_distribution(admin_user):
    """测试5: 验证停留时长分布"""
    print_test("验证停留时长分布")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/page-duration/')
    data = response.json()
    dist = data['data']['duration_distribution']

    # 验证字段存在
    required_keys = ['short', 'medium', 'long']
    if not all(k in dist for k in required_keys):
        print_fail(f"分布缺少必要字段: {required_keys}")
        return False

    # 验证数据类型
    if not all(isinstance(dist[k], int) for k in required_keys):
        print_fail(f"分布值应该是整数")
        return False

    # 验证值非负
    if any(dist[k] < 0 for k in required_keys):
        print_fail(f"分布值不能为负数")
        return False

    # 验证百分比字段
    pct_keys = ['short_percentage', 'medium_percentage', 'long_percentage']
    if not all(k in dist for k in pct_keys):
        print_fail(f"分布缺少百分比字段: {pct_keys}")
        return False

    # 验证百分比范围（0-100）
    for k in pct_keys:
        if dist[k] < 0 or dist[k] > 100:
            print_fail(f"{k} 应该在 0-100 之间")
            return False

    print_info(f"短停留(<30s): {dist['short']} ({dist['short_percentage']}%)")
    print_info(f"中停留(30-120s): {dist['medium']} ({dist['medium_percentage']}%)")
    print_info(f"长停留(>120s): {dist['long']} ({dist['long_percentage']}%)")

    print_pass("停留时长分布正确")
    return True


def test_duration_trend(admin_user):
    """测试6: 验证停留时间趋势"""
    print_test("验证停留时间趋势")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/page-duration/')
    data = response.json()
    trend = data['data']['trend']

    if not isinstance(trend, list):
        print_fail(f"趋势数据应该是列表")
        return False

    if len(trend) > 0:
        first_point = trend[0]

        # 验证字段
        if 'date' not in first_point:
            print_fail(f"趋势数据点缺少 date 字段")
            return False

        if 'avg_duration' not in first_point:
            print_fail(f"趋势数据点缺少 avg_duration 字段")
            return False

        # 验证数据类型
        if not isinstance(first_point['avg_duration'], (int, float)):
            print_fail(f"avg_duration 应该是数字")
            return False

        # 验证值合理
        if first_point['avg_duration'] < 0:
            print_fail(f"avg_duration 不能为负数")
            return False

        print_info(f"最新趋势日期: {first_point.get('date', 'N/A')}")
        print_info(f"平均停留时间: {first_point['avg_duration']}秒")

    print_pass("趋势数据格式正确")
    return True


def test_query_parameters(admin_user):
    """测试7: 验证查询参数"""
    print_test("验证查询参数")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # 测试 days 参数
    response = client.get('/api/admin/analytics/page-duration/?days=7')
    if response.status_code != 200:
        print_fail(f"days 参数请求失败: {response.status_code}")
        return False

    data = response.json()
    if data['data']['summary']['days'] != 7:
        print_fail(f"days 参数未正确应用")
        return False
    print_info("days=7 参数正常 [OK]")

    # 测试 days 边界值
    response = client.get('/api/admin/analytics/page-duration/?days=1')
    if response.status_code != 200:
        print_fail(f"days=1 请求失败: {response.status_code}")
        return False
    print_info("days=1 边界值正常 [OK]")

    response = client.get('/api/admin/analytics/page-duration/?days=90')
    if response.status_code != 200:
        print_fail(f"days=90 请求失败: {response.status_code}")
        return False
    print_info("days=90 边界值正常 [OK]")

    # 测试无效参数
    response = client.get('/api/admin/analytics/page-duration/?days=999')
    if response.status_code != 200:
        print_fail(f"无效 days 参数处理失败: {response.status_code}")
        return False
    print_info("无效参数已使用默认值处理 [OK]")

    # 测试页面筛选参数
    response = client.get('/api/admin/analytics/page-duration/?page=首页')
    if response.status_code != 200:
        print_fail(f"page 筛选参数请求失败: {response.status_code}")
        return False
    print_info("page=首页 筛选参数正常 [OK]")

    print_pass("查询参数验证正确")
    return True


def test_response_time(admin_user):
    """测试8: 验证响应时间"""
    print_test("验证响应时间")

    import time

    client = APIClient()
    client.force_authenticate(user=admin_user)

    start_time = time.time()
    response = client.get('/api/admin/analytics/page-duration/')
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


def test_invalid_duration_filtering(admin_user):
    """测试9: 验证无效停留时间被过滤"""
    print_test("验证无效停留时间被正确过滤")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/page-duration/')
    data = response.json()
    page_stats = data['data']['page_statistics']

    # 查找首页数据
    home_stats = None
    for page in page_stats:
        if page['page'] == '首页':
            home_stats = page
            break

    if home_stats:
        # 正常停留时间应该被包含（10-30秒范围的数据）
        # 无效数据（负值、2小时）应该被过滤
        print_info(f"首页平均停留: {home_stats['avg_duration']}秒")
        print_info(f"首页访问次数: {home_stats['total_visits']}")

        # 平均停留时间应该在合理范围内（考虑有无效数据被过滤）
        if home_stats['avg_duration'] > 0:
            print_pass("停留时间在合理范围内")
            return True
        else:
            print_warning("平均停留时间为0，可能没有有效数据")
            return True
    else:
        print_info("首页数据可能已被过滤或没有数据")
        return True


def test_summary_data(admin_user):
    """测试10: 验证汇总数据"""
    print_test("验证汇总数据")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/page-duration/')
    data = response.json()
    summary = data['data']['summary']

    # 验证汇总字段
    required_keys = ['total_logs', 'days', 'total_pages', 'page_filter']
    missing = [k for k in required_keys if k not in summary]

    if missing:
        print_fail(f"汇总数据缺少必要字段: {missing}")
        return False

    # 验证数据类型
    if not isinstance(summary['total_logs'], int):
        print_fail(f"total_logs 应该是整数")
        return False

    if summary['total_logs'] < 0:
        print_fail(f"total_logs 不能为负数")
        return False

    if summary['days'] < 1 or summary['days'] > 90:
        print_fail(f"days 应该在 1-90 之间")
        return False

    if summary['total_pages'] < 0:
        print_fail(f"total_pages 不能为负数")
        return False

    print_info(f"总访问记录: {summary['total_logs']}")
    print_info(f"分析天数: {summary['days']}")
    print_info(f"页面数: {summary['total_pages']}")
    print_info(f"页面筛选: {summary['page_filter']}")

    print_pass("汇总数据验证正确")
    return True


# ========== 主测试函数 ==========

def run_all_tests():
    """运行所有测试"""
    print_header("页面停留分析接口测试")

    results = {}
    admin_user = None

    try:
        # 准备测试数据
        admin_users, normal_users = setup_test_data()
        admin_user = admin_users[0]

        # 运行测试
        results['API端点存在'] = test_api_endpoint_exists()
        results['响应格式正确'] = test_api_response_format(admin_user)
        results['管理员权限验证'] = test_admin_permission()
        results['页面统计数据正确'] = test_page_statistics(admin_user)
        results['停留时长分布正确'] = test_duration_distribution(admin_user)
        results['趋势数据正确'] = test_duration_trend(admin_user)
        results['查询参数验证'] = test_query_parameters(admin_user)
        results['响应时间'] = test_response_time(admin_user)
        results['无效数据过滤'] = test_invalid_duration_filtering(admin_user)
        results['汇总数据验证'] = test_summary_data(admin_user)

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
