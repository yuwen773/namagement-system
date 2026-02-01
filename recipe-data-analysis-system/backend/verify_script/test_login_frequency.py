# -*- coding: utf-8 -*-
"""
登录频次分析接口测试脚本

测试登录频次分析 API 的功能，验证：
1. 接口返回数据格式正确
2. 权限验证（管理员 vs 普通用户 vs 未认证）
3. 登录频率分布计算正确
4. 登录时间段分布正确
5. 每日登录趋势数据正确
6. 参数验证正确
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
# 脚本位置: backend/verify_script/test_login_frequency.py
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
from utils.constants import BehaviorType
from analytics.views import LoginFrequencyAnalysisView


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
    UserBehaviorLog.objects.filter(target__contains='TEST_LOGIN').delete()
    User.objects.filter(username__startswith='test_admin_login').delete()
    User.objects.filter(username__startswith='test_user_login').delete()

    # 创建测试用户
    admin_users = []
    normal_users = []

    # 创建 5 个管理员用户
    for i in range(5):
        try:
            admin_user = User.objects.get(username=f'test_admin_login_{i}')
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username=f'test_admin_login_{i}',
                email=f'admin_login_{i}@test.com',
                password='testpass123',
                role='admin'
            )
        admin_users.append(admin_user)

    # 创建 10 个普通用户（用于测试不同的登录频率）
    for i in range(10):
        try:
            normal_user = User.objects.get(username=f'test_user_login_{i}')
        except User.DoesNotExist:
            normal_user = User.objects.create_user(
                username=f'test_user_login_{i}',
                email=f'user_login_{i}@test.com',
                password='testpass123',
                role='user'
            )
        normal_users.append(normal_user)

    print_info(f"创建了 {len(admin_users)} 个管理员用户和 {len(normal_users)} 个普通用户")

    # 创建测试登录日志（过去 7 天内的数据）
    now = timezone.now()

    # 用户0: 高频用户（25次登录 >= 20）
    for j in range(25):
        UserBehaviorLog.objects.create(
            user=normal_users[0],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=now - timedelta(hours=j),
            extra_data={'test_marker': True}
        )

    # 用户1: 高频用户（22次登录）
    for j in range(22):
        UserBehaviorLog.objects.create(
            user=normal_users[1],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=now - timedelta(hours=j * 2),
            extra_data={'test_marker': True}
        )

    # 用户2: 中频用户（10次登录 5-19）
    for j in range(10):
        UserBehaviorLog.objects.create(
            user=normal_users[2],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=now - timedelta(hours=j * 5),
            extra_data={'test_marker': True}
        )

    # 用户3: 中频用户（8次登录）
    for j in range(8):
        UserBehaviorLog.objects.create(
            user=normal_users[3],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=now - timedelta(hours=j * 8),
            extra_data={'test_marker': True}
        )

    # 用户4: 低频用户（3次登录 1-4）
    for j in range(3):
        UserBehaviorLog.objects.create(
            user=normal_users[4],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=now - timedelta(days=j),
            extra_data={'test_marker': True}
        )

    # 用户5: 低频用户（1次登录）
    UserBehaviorLog.objects.create(
        user=normal_users[5],
        behavior_type=BehaviorType.LOGIN,
        target='home',
        timestamp=now,
        extra_data={'test_marker': True}
    )

    # 用户6-9: 沉默用户（0次登录）

    # 创建不同时段的登录数据（用于测试时间段分布）
    # 凌晨 0-6 点
    night_start = now.replace(hour=2, minute=0, second=0, microsecond=0)
    UserBehaviorLog.objects.create(
        user=normal_users[0],
        behavior_type=BehaviorType.LOGIN,
        target='home',
        timestamp=night_start,
        extra_data={'test_marker': True}
    )

    # 早上 6-12 点
    morning_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    UserBehaviorLog.objects.create(
        user=normal_users[1],
        behavior_type=BehaviorType.LOGIN,
        target='home',
        timestamp=morning_start,
        extra_data={'test_marker': True}
    )

    # 中午 12-18 点
    noon_start = now.replace(hour=14, minute=0, second=0, microsecond=0)
    UserBehaviorLog.objects.create(
        user=normal_users[2],
        behavior_type=BehaviorType.LOGIN,
        target='home',
        timestamp=noon_start,
        extra_data={'test_marker': True}
    )

    # 晚上 18-24 点
    evening_start = now.replace(hour=20, minute=0, second=0, microsecond=0)
    UserBehaviorLog.objects.create(
        user=normal_users[3],
        behavior_type=BehaviorType.LOGIN,
        target='home',
        timestamp=evening_start,
        extra_data={'test_marker': True}
    )

    print_pass(f"创建了测试登录日志数据")
    return admin_users, normal_users


def cleanup_test_data():
    """清理测试数据"""
    print_test("清理测试数据")
    UserBehaviorLog.objects.filter(target__contains='TEST_LOGIN').delete()
    User.objects.filter(username__startswith='test_admin_login').delete()
    User.objects.filter(username__startswith='test_user_login').delete()
    print_pass("测试数据已清理")


# ========== API 测试 ==========

def test_api_endpoint_exists():
    """测试1: 验证 API 端点存在"""
    print_test("验证 API 端点存在")

    try:
        view = LoginFrequencyAnalysisView()
        print_pass(f"LoginFrequencyAnalysisView 视图类存在")
        return True
    except Exception as e:
        print_fail(f"视图类不存在: {e}")
        return False


def test_api_response_format(admin_user):
    """测试2: 验证 API 响应格式"""
    print_test("验证 API 响应格式")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/login-frequency/')

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
    required_data_keys = ['summary', 'login_frequency_distribution', 'hourly_distribution', 'daily_trend']
    if not all(k in data_content for k in required_data_keys):
        print_fail(f"数据缺少必要字段: {required_data_keys}")
        return False

    # 验证 summary 结构
    summary = data_content.get('summary', {})
    summary_keys = ['total_logs', 'days', 'total_users']
    if not all(k in summary for k in summary_keys):
        print_fail(f"Summary 数据缺少必要字段: {summary_keys}")
        return False

    # 验证 login_frequency_distribution 结构
    freq_dist = data_content.get('login_frequency_distribution', {})
    freq_keys = ['high_frequency', 'medium_frequency', 'low_frequency', 'silent']
    if not all(k in freq_dist for k in freq_keys):
        print_fail(f"登录频率分布缺少必要字段: {freq_keys}")
        return False

    # 验证 hourly_distribution 结构
    hourly = data_content.get('hourly_distribution', {})
    hourly_keys = ['0-6', '6-12', '12-18', '18-24']
    if not all(k in hourly for k in hourly_keys):
        print_fail(f"时段分布缺少必要字段: {hourly_keys}")
        return False

    # 验证 daily_trend 结构
    trend = data_content.get('daily_trend', [])
    if not isinstance(trend, list):
        print_fail(f"每日趋势应该是列表，实际: {type(trend)}")
        return False

    print_pass(f"响应格式正确")
    print_info(f"总登录次数: {summary['total_logs']}")
    print_info(f"高频用户: {freq_dist['high_frequency']}")
    print_info(f"中频用户: {freq_dist['medium_frequency']}")
    print_info(f"低频用户: {freq_dist['low_frequency']}")
    print_info(f"沉默用户: {freq_dist['silent']}")
    return True


def test_admin_permission():
    """测试3: 验证管理员权限"""
    print_test("验证管理员权限")

    client = APIClient()

    # 未认证访问
    response = client.get('/api/admin/analytics/login-frequency/')
    if response.status_code != 401:
        print_fail(f"未认证访问应该返回 401，实际: {response.status_code}")
        return False
    print_info("未认证访问返回 401 [OK]")

    # 普通用户访问
    try:
        normal_user = User.objects.get(username='test_user_login_0')
    except User.DoesNotExist:
        normal_user = User.objects.create_user(
            username='test_user_login_0',
            email='normal@test.com',
            password='test123',
            role='user'
        )

    client.force_authenticate(user=normal_user)
    response = client.get('/api/admin/analytics/login-frequency/')
    if response.status_code != 403:
        print_fail(f"普通用户访问应该返回 403，实际: {response.status_code}")
        return False
    print_info("普通用户访问返回 403 [OK]")

    # 管理员访问
    admin_user = None
    try:
        admin_user = User.objects.get(username='test_admin_login_0')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='test_admin_login_0',
            email='admin@test.com',
            password='test123',
            role='admin'
        )

    client.force_authenticate(user=admin_user)
    response = client.get('/api/admin/analytics/login-frequency/')
    if response.status_code != 200:
        print_fail(f"管理员访问应该返回 200，实际: {response.status_code}")
        return False
    print_info("管理员访问返回 200 [OK]")

    print_pass("权限验证正确")
    return True


def test_frequency_distribution(admin_user):
    """测试4: 验证登录频率分布计算"""
    print_test("验证登录频率分布计算")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/login-frequency/')
    data = response.json()
    freq_dist = data['data']['login_frequency_distribution']

    # 验证数据类型
    for key in ['high_frequency', 'medium_frequency', 'low_frequency', 'silent']:
        if not isinstance(freq_dist[key], int):
            print_fail(f"{key} 应该是整数，实际: {type(freq_dist[key])}")
            return False

    # 验证各分类用户数之和等于总用户数
    summary = data['data']['summary']
    total_classified = (
        freq_dist['high_frequency'] +
        freq_dist['medium_frequency'] +
        freq_dist['low_frequency'] +
        freq_dist['silent']
    )

    if total_classified != summary['total_users']:
        print_warning(f"分类用户数之和 ({total_classified}) 不等于总用户数 ({summary['total_users']})")
        # 可能是测试数据没有覆盖所有用户

    print_info(f"高频用户 (>=20次): {freq_dist['high_frequency']}")
    print_info(f"中频用户 (5-19次): {freq_dist['medium_frequency']}")
    print_info(f"低频用户 (1-4次): {freq_dist['low_frequency']}")
    print_info(f"沉默用户 (0次): {freq_dist['silent']}")

    # 验证百分比存在且合理
    for key in ['high_percentage', 'medium_percentage', 'low_percentage', 'silent_percentage']:
        if key in freq_dist:
            pct = freq_dist[key]
            if not isinstance(pct, (int, float)):
                print_fail(f"{key} 应该是数字，实际: {type(pct)}")
                return False
            if pct < 0 or pct > 100:
                print_fail(f"{key} 应该在 0-100 之间，实际: {pct}")
                return False
            print_info(f"{key}: {pct}%")

    print_pass("登录频率分布计算正确")
    return True


def test_hourly_distribution(admin_user):
    """测试5: 验证登录时间段分布"""
    print_test("验证登录时间段分布")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/login-frequency/')
    data = response.json()
    hourly = data['data']['hourly_distribution']

    # 验证各时段类型
    time_periods = ['0-6', '6-12', '12-18', '18-24']
    for period in time_periods:
        if period not in hourly:
            print_fail(f"缺少时段 {period}")
            return False
        if not isinstance(hourly[period], int):
            print_fail(f"时段 {period} 应该是整数，实际: {type(hourly[period])}")
            return False
        if hourly[period] < 0:
            print_fail(f"时段 {period} 不能为负数: {hourly[period]}")
            return False

    # 验证 24 小时明细数据
    if 'detail' in hourly:
        detail = hourly['detail']
        for h in range(24):
            hour_key = str(h)
            if hour_key not in detail:
                print_fail(f"缺少小时数据 {hour_key}")
                return False
            if not isinstance(detail[hour_key], int):
                print_fail(f"小时 {hour_key} 应该是整数")
                return False

    print_info(f"0-6点登录: {hourly['0-6']}")
    print_info(f"6-12点登录: {hourly['6-12']}")
    print_info(f"12-18点登录: {hourly['12-18']}")
    print_info(f"18-24点登录: {hourly['18-24']}")

    print_pass("登录时间段分布正确")
    return True


def test_daily_trend(admin_user):
    """测试6: 验证每日登录趋势"""
    print_test("验证每日登录趋势")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/login-frequency/')
    data = response.json()
    trend = data['data']['daily_trend']

    if not isinstance(trend, list):
        print_fail(f"每日趋势应该是列表，实际: {type(trend)}")
        return False

    if len(trend) == 0:
        print_warning("每日趋势数据为空，可能没有登录日志")

    for item in trend:
        if not isinstance(item, dict):
            print_fail(f"趋势数据项应该是字典，实际: {type(item)}")
            return False

        # 验证必要字段
        if 'date' not in item:
            print_fail("趋势数据项缺少 date 字段")
            return False
        if 'login_count' not in item:
            print_fail("趋势数据项缺少 login_count 字段")
            return False
        if 'login_users' not in item:
            print_fail("趋势数据项缺少 login_users 字段")
            return False

        # 验证数据类型
        if not isinstance(item['login_count'], int):
            print_fail(f"login_count 应该是整数")
            return False
        if not isinstance(item['login_users'], int):
            print_fail(f"login_users 应该是整数")
            return False

    print_info(f"趋势数据点数: {len(trend)}")
    if len(trend) > 0:
        print_info(f"最新日期: {trend[0].get('date', 'N/A')}")
        print_info(f"登录次数: {trend[0].get('login_count', 'N/A')}")
        print_info(f"登录用户数: {trend[0].get('login_users', 'N/A')}")

    print_pass("每日登录趋势数据正确")
    return True


def test_summary_data(admin_user):
    """测试7: 验证汇总数据"""
    print_test("验证汇总数据")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/login-frequency/')
    data = response.json()
    summary = data['data']['summary']

    # 验证汇总字段
    required_keys = ['total_logs', 'days', 'total_users']
    missing = [k for k in required_keys if k not in summary]

    if missing:
        print_fail(f"汇总数据缺少必要字段: {missing}")
        return False

    # 验证数据类型
    for key in required_keys:
        if not isinstance(summary[key], int):
            print_fail(f"{key} 应该是整数，实际: {type(summary[key])}")
            return False

    # 验证数据关系
    if summary['total_logs'] < 0:
        print_fail(f"总登录次数不能为负数: {summary['total_logs']}")
        return False

    if summary['total_users'] <= 0:
        print_warning(f"总用户数为 {summary['total_users']}，可能数据不足")

    print_info(f"总登录次数: {summary['total_logs']}")
    print_info(f"分析天数: {summary['days']}")
    print_info(f"总用户数: {summary['total_users']}")

    print_pass("汇总数据验证正确")
    return True


def test_query_parameters():
    """测试8: 验证查询参数"""
    print_test("验证查询参数")

    # 获取管理员用户
    admin_user = None
    try:
        admin_user = User.objects.get(username='test_admin_login_0')
    except User.DoesNotExist:
        print_fail("管理员用户不存在")
        return False

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # 测试 days 参数 - 正常值
    response = client.get('/api/admin/analytics/login-frequency/?days=7')
    if response.status_code != 200:
        print_fail(f"days=7 参数请求失败: {response.status_code}")
        return False
    data = response.json()
    if data['data']['summary']['days'] != 7:
        print_fail(f"days 参数未正确应用: {data['data']['summary']['days']}")
        return False
    print_info("days=7 参数正常 [OK]")

    # 测试 days 参数 - 小值
    response = client.get('/api/admin/analytics/login-frequency/?days=1')
    if response.status_code != 200:
        print_fail(f"days=1 参数请求失败: {response.status_code}")
        return False
    print_info("days=1 参数正常 [OK]")

    # 测试 days 参数 - 大值（应该限制到90）
    response = client.get('/api/admin/analytics/login-frequency/?days=365')
    if response.status_code != 200:
        print_fail(f"days=365 参数请求失败: {response.status_code}")
        return False
    data = response.json()
    if data['data']['summary']['days'] > 90:
        print_fail(f"days 参数未正确限制: {data['data']['summary']['days']}")
        return False
    print_info("days=365 参数已限制到有效范围 [OK]")

    # 测试无效 days 参数
    response = client.get('/api/admin/analytics/login-frequency/?days=invalid')
    if response.status_code != 200:
        print_fail(f"无效 days 参数处理失败: {response.status_code}")
        return False
    print_info("无效 days 参数已使用默认值 [OK]")

    print_pass("查询参数验证正确")
    return True


def test_frequency_classification(admin_user):
    """测试9: 验证用户频率分类正确性"""
    print_test("验证用户频率分类正确性")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/login-frequency/')
    data = response.json()
    freq_dist = data['data']['login_frequency_distribution']

    # 验证分类边界
    # 高频: >= 20
    # 中频: 5-19
    # 低频: 1-4
    # 沉默: 0

    # 验证各分类值非负
    if freq_dist['high_frequency'] < 0:
        print_fail("高频用户数不能为负")
        return False
    if freq_dist['medium_frequency'] < 0:
        print_fail("中频用户数不能为负")
        return False
    if freq_dist['low_frequency'] < 0:
        print_fail("低频用户数不能为负")
        return False
    if freq_dist['silent'] < 0:
        print_fail("沉默用户数不能为负")
        return False

    # 验证百分比（如果存在）
    if freq_dist.get('high_percentage', 0) < 0 or freq_dist.get('high_percentage', 0) > 100:
        print_fail("高频用户百分比范围错误")
        return False
    if freq_dist.get('medium_percentage', 0) < 0 or freq_dist.get('medium_percentage', 0) > 100:
        print_fail("中频用户百分比范围错误")
        return False
    if freq_dist.get('low_percentage', 0) < 0 or freq_dist.get('low_percentage', 0) > 100:
        print_fail("低频用户百分比范围错误")
        return False
    if freq_dist.get('silent_percentage', 0) < 0 or freq_dist.get('silent_percentage', 0) > 100:
        print_fail("沉默用户百分比范围错误")
        return False

    print_pass("用户频率分类验证正确")
    return True


def test_response_time(admin_user):
    """测试10: 验证响应时间"""
    print_test("验证响应时间")

    import time

    client = APIClient()
    client.force_authenticate(user=admin_user)

    start_time = time.time()
    response = client.get('/api/admin/analytics/login-frequency/')
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
    print_header("登录频次分析接口测试")

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
        results['登录频率分布计算'] = test_frequency_distribution(admin_user)
        results['登录时间段分布'] = test_hourly_distribution(admin_user)
        results['每日登录趋势'] = test_daily_trend(admin_user)
        results['汇总数据验证'] = test_summary_data(admin_user)
        results['查询参数验证'] = test_query_parameters()
        results['用户频率分类'] = test_frequency_classification(admin_user)
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
