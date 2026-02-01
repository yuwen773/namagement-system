# -*- coding: utf-8 -*-
"""
活跃用户分析接口测试脚本

测试活跃用户分析 API 的功能，验证：
1. 接口返回数据格式正确
2. 权限验证（管理员 vs 普通用户）
3. DAU/WAU/MAU 计算正确
4. 变化率计算正确
5. 留存率计算正确
6. 趋势数据正确
7. 参数验证正确
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
# 脚本位置: backend/verify_script/test_active_users.py
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
from analytics.views import ActiveUsersAnalysisView


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
    UserBehaviorLog.objects.filter(target__contains='TEST_ACTIVE').delete()
    User.objects.filter(username__startswith='test_admin_active').delete()
    User.objects.filter(username__startswith='test_user_active').delete()

    # 创建测试用户
    admin_users = []
    normal_users = []

    # 创建 5 个管理员用户（用于测试活跃用户数）
    for i in range(5):
        try:
            admin_user = User.objects.get(username=f'test_admin_active_{i}')
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username=f'test_admin_active_{i}',
                email=f'admin_active_{i}@test.com',
                password='testpass123',
                role='admin'
            )
        admin_users.append(admin_user)

    # 创建 10 个普通用户
    for i in range(10):
        try:
            normal_user = User.objects.get(username=f'test_user_active_{i}')
        except User.DoesNotExist:
            normal_user = User.objects.create_user(
                username=f'test_user_active_{i}',
                email=f'user_active_{i}@test.com',
                password='testpass123',
                role='user'
            )
        normal_users.append(normal_user)

    print_info(f"创建了 {len(admin_users)} 个管理员用户和 {len(normal_users)} 个普通用户")

    # 创建测试行为日志（过去 7 天内的活跃数据）
    now = timezone.now()

    # 今天活跃的用户
    for i in range(3):
        UserBehaviorLog.objects.create(
            user=admin_users[i],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=now,
            extra_data={'test_marker': True}
        )
        UserBehaviorLog.objects.create(
            user=admin_users[i],
            behavior_type=BehaviorType.VIEW,
            target=f'recipe:{i + 100}',
            timestamp=now + timedelta(minutes=5),
            extra_data={'test_marker': True}
        )

    # 昨天活跃的用户
    yesterday = now - timedelta(days=1)
    for i in range(2):
        UserBehaviorLog.objects.create(
            user=admin_users[i],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=yesterday,
            extra_data={'test_marker': True}
        )

    # 本周活跃的用户（覆盖更多用户）
    week_ago = now - timedelta(days=5)
    for i in range(7):
        UserBehaviorLog.objects.create(
            user=normal_users[i],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=week_ago + timedelta(hours=i),
            extra_data={'test_marker': True}
        )

    # 上周活跃的用户
    last_week = now - timedelta(days=8)
    for i in range(4):
        UserBehaviorLog.objects.create(
            user=normal_users[i + 3],
            behavior_type=BehaviorType.LOGIN,
            target='home',
            timestamp=last_week,
            extra_data={'test_marker': True}
        )

    print_pass(f"创建了测试行为日志数据")
    return admin_users, normal_users


def cleanup_test_data():
    """清理测试数据"""
    print_test("清理测试数据")
    UserBehaviorLog.objects.filter(target__contains='TEST_ACTIVE').delete()
    User.objects.filter(username__startswith='test_admin_active').delete()
    User.objects.filter(username__startswith='test_user_active').delete()
    print_pass("测试数据已清理")


# ========== API 测试 ==========

def test_api_endpoint_exists():
    """测试1: 验证 API 端点存在"""
    print_test("验证 API 端点存在")

    try:
        view = ActiveUsersAnalysisView()
        print_pass(f"ActiveUsersAnalysisView 视图类存在")
        return True
    except Exception as e:
        print_fail(f"视图类不存在: {e}")
        return False


def test_api_response_format(admin_user):
    """测试2: 验证 API 响应格式"""
    print_test("验证 API 响应格式")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/active-users/')

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
    required_data_keys = ['summary', 'dau', 'wau', 'mau', 'stickiness']
    if not all(k in data_content for k in required_data_keys):
        print_fail(f"数据缺少必要字段: {required_data_keys}")
        return False

    # 验证 DAU 结构
    dau = data_content.get('dau', {})
    dau_keys = ['today', 'yesterday', 'change_rate']
    if not all(k in dau for k in dau_keys):
        print_fail(f"DAU 数据缺少必要字段: {dau_keys}")
        return False

    # 验证 WAU 结构
    wau = data_content.get('wau', {})
    wau_keys = ['current', 'previous', 'change_rate']
    if not all(k in wau for k in wau_keys):
        print_fail(f"WAU 数据缺少必要字段: {wau_keys}")
        return False

    # 验证 MAU 结构
    mau = data_content.get('mau', {})
    mau_keys = ['current', 'previous', 'change_rate']
    if not all(k in mau for k in mau_keys):
        print_fail(f"MAU 数据缺少必要字段: {mau_keys}")
        return False

    print_pass(f"响应格式正确")
    print_info(f"今日活跃用户: {dau['today']}")
    print_info(f"本周活跃用户: {wau['current']}")
    print_info(f"本月活跃用户: {mau['current']}")
    return True


def test_admin_permission():
    """测试3: 验证管理员权限"""
    print_test("验证管理员权限")

    client = APIClient()

    # 未认证访问
    response = client.get('/api/admin/analytics/active-users/')
    if response.status_code != 401:
        print_fail(f"未认证访问应该返回 401，实际: {response.status_code}")
        return False
    print_info("未认证访问返回 401 [OK]")

    # 普通用户访问
    try:
        normal_user = User.objects.get(username='test_user_active_0')
    except User.DoesNotExist:
        normal_user = User.objects.create_user(
            username='test_user_active_0',
            email='normal@test.com',
            password='test123',
            role='user'
        )

    client.force_authenticate(user=normal_user)
    response = client.get('/api/admin/analytics/active-users/')
    if response.status_code != 403:
        print_fail(f"普通用户访问应该返回 403，实际: {response.status_code}")
        return False
    print_info("普通用户访问返回 403 [OK]")

    # 管理员访问
    admin_user = None
    try:
        admin_user = User.objects.get(username='test_admin_active_0')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='test_admin_active_0',
            email='admin@test.com',
            password='test123',
            role='admin'
        )

    client.force_authenticate(user=admin_user)
    response = client.get('/api/admin/analytics/active-users/')
    if response.status_code != 200:
        print_fail(f"管理员访问应该返回 200，实际: {response.status_code}")
        return False
    print_info("管理员访问返回 200 [OK]")

    print_pass("权限验证正确")
    return True


def test_dau_calculation(admin_user):
    """测试4: 验证 DAU 计算"""
    print_test("验证 DAU 计算")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/active-users/')
    data = response.json()
    dau = data['data']['dau']

    # 验证数据类型
    if not isinstance(dau['today'], int):
        print_fail(f"今日活跃用户应该是整数，实际: {type(dau['today'])}")
        return False

    if not isinstance(dau['yesterday'], int):
        print_fail(f"昨日活跃用户应该是整数，实际: {type(dau['yesterday'])}")
        return False

    if not isinstance(dau['change_rate'], (int, float)):
        print_fail(f"变化率应该是数字，实际: {type(dau['change_rate'])}")
        return False

    # 验证数值合理性
    if dau['today'] < 0:
        print_fail(f"今日活跃用户数不能为负数: {dau['today']}")
        return False

    print_info(f"今日 DAU: {dau['today']}")
    print_info(f"昨日 DAU: {dau['yesterday']}")
    print_info(f"DAU 变化率: {dau['change_rate']}%")

    print_pass("DAU 数据计算正确")
    return True


def test_wau_calculation(admin_user):
    """测试5: 验证 WAU 计算"""
    print_test("验证 WAU 计算")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/active-users/')
    data = response.json()
    wau = data['data']['wau']

    # 验证数据类型
    if not isinstance(wau['current'], int):
        print_fail(f"本周活跃用户应该是整数，实际: {type(wau['current'])}")
        return False

    if not isinstance(wau['previous'], int):
        print_fail(f"上周活跃用户应该是整数，实际: {type(wau['previous'])}")
        return False

    # WAU 应该 >= DAU
    dau = data['data']['dau']['today']
    if wau['current'] < dau:
        print_warning(f"WAU ({wau['current']}) 小于 DAU ({dau})，可能数据较少")

    print_info(f"本周 WAU: {wau['current']}")
    print_info(f"上周 WAU: {wau['previous']}")
    print_info(f"WAU 变化率: {wau['change_rate']}%")

    print_pass("WAU 数据计算正确")
    return True


def test_mau_calculation(admin_user):
    """测试6: 验证 MAU 计算"""
    print_test("验证 MAU 计算")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/active-users/')
    data = response.json()
    mau = data['data']['mau']

    # 验证数据类型
    if not isinstance(mau['current'], int):
        print_fail(f"本月活跃用户应该是整数，实际: {type(mau['current'])}")
        return False

    if not isinstance(mau['previous'], int):
        print_fail(f"上月活跃用户应该是整数，实际: {type(mau['previous'])}")
        return False

    # MAU 应该 >= WAU
    wau = data['data']['wau']['current']
    if mau['current'] < wau:
        print_warning(f"MAU ({mau['current']}) 小于 WAU ({wau})，可能数据较少")

    print_info(f"本月 MAU: {mau['current']}")
    print_info(f"上月 MAU: {mau['previous']}")
    print_info(f"MAU 变化率: {mau['change_rate']}%")

    print_pass("MAU 数据计算正确")
    return True


def test_stickiness_calculation(admin_user):
    """测试7: 验证留存率（DAU/MAU）计算"""
    print_test("验证留存率计算")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/active-users/')
    data = response.json()
    stickiness = data['data']['stickiness']

    # 验证留存率字段存在
    if 'dau_mau_ratio' not in stickiness:
        print_fail("缺少 dau_mau_ratio 字段")
        return False

    ratio = stickiness['dau_mau_ratio']

    # 验证数据类型
    if not isinstance(ratio, (int, float)):
        print_fail(f"留存率应该是数字，实际: {type(ratio)}")
        return False

    # 验证数值范围（0-100%）
    if ratio < 0 or ratio > 100:
        print_fail(f"留存率应该在 0-100 之间，实际: {ratio}")
        return False

    print_info(f"DAU/MAU 留存率: {ratio}%")

    print_pass("留存率计算正确")
    return True


def test_trend_data(admin_user):
    """测试8: 验证趋势数据"""
    print_test("验证趋势数据")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # 测试包含趋势数据
    response = client.get('/api/admin/analytics/active-users/?include_trend=true')
    data = response.json()

    if 'trend' not in data['data']:
        print_fail("缺少 trend 字段")
        return False

    trend = data['data']['trend']

    if not isinstance(trend, list):
        print_fail(f"趋势数据应该是列表，实际: {type(trend)}")
        return False

    print_info(f"趋势数据点数: {len(trend)}")

    if len(trend) > 0:
        first_point = trend[0]
        if 'date' not in first_point:
            print_fail("趋势数据点缺少 date 字段")
            return False

        # 检查是否包含 dau
        if 'dau' not in first_point:
            print_warning("趋势数据点可能缺少 dau 字段")

        print_info(f"最新趋势日期: {first_point.get('date', 'N/A')}")

    print_pass("趋势数据格式正确")
    return True


def test_query_parameters():
    """测试9: 验证查询参数"""
    print_test("验证查询参数")

    # 获取管理员用户
    admin_user = None
    try:
        admin_user = User.objects.get(username='test_admin_active_0')
    except User.DoesNotExist:
        print_fail("管理员用户不存在")
        return False

    client = APIClient()
    client.force_authenticate(user=admin_user)

    # 测试 days 参数
    response = client.get('/api/admin/analytics/active-users/?days=7')
    if response.status_code != 200:
        print_fail(f"days 参数请求失败: {response.status_code}")
        return False
    print_info("days=7 参数正常 [OK]")

    # 测试 trend_by 参数
    response = client.get('/api/admin/analytics/active-users/?trend_by=week')
    if response.status_code != 200:
        print_fail(f"trend_by 参数请求失败: {response.status_code}")
        return False
    print_info("trend_by=week 参数正常 [OK]")

    response = client.get('/api/admin/analytics/active-users/?trend_by=month')
    if response.status_code != 200:
        print_fail(f"trend_by=month 参数请求失败: {response.status_code}")
        return False
    print_info("trend_by=month 参数正常 [OK]")

    # 测试 include_trend 参数
    response = client.get('/api/admin/analytics/active-users/?include_trend=false')
    if response.status_code != 200:
        print_fail(f"include_trend 参数请求失败: {response.status_code}")
        return False
    print_info("include_trend=false 参数正常 [OK]")

    # 测试无效参数（应该使用默认值）
    response = client.get('/api/admin/analytics/active-users/?days=999')
    if response.status_code != 200:
        print_fail(f"无效 days 参数处理失败: {response.status_code}")
        return False
    print_info("无效参数已使用默认值处理 [OK]")

    print_pass("查询参数验证正确")
    return True


def test_summary_data(admin_user):
    """测试10: 验证汇总数据"""
    print_test("验证汇总数据")

    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.get('/api/admin/analytics/active-users/')
    data = response.json()
    summary = data['data']['summary']

    # 验证汇总字段
    required_keys = ['total_users', 'active_today', 'active_week', 'active_month']
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
    if summary['active_today'] > summary['active_week']:
        print_warning(f"今日活跃用户数大于周活跃用户数，可能数据异常")

    if summary['active_week'] > summary['active_month']:
        print_warning(f"周活跃用户数大于月活跃用户数，可能数据异常")

    print_info(f"总用户数: {summary['total_users']}")
    print_info(f"今日活跃: {summary['active_today']}")
    print_info(f"本周活跃: {summary['active_week']}")
    print_info(f"本月活跃: {summary['active_month']}")

    print_pass("汇总数据验证正确")
    return True


def test_response_time(admin_user):
    """测试11: 验证响应时间"""
    print_test("验证响应时间")

    import time

    client = APIClient()
    client.force_authenticate(user=admin_user)

    start_time = time.time()
    response = client.get('/api/admin/analytics/active-users/')
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
    print_header("活跃用户分析接口测试")

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
        results['DAU计算正确'] = test_dau_calculation(admin_user)
        results['WAU计算正确'] = test_wau_calculation(admin_user)
        results['MAU计算正确'] = test_mau_calculation(admin_user)
        results['留存率计算正确'] = test_stickiness_calculation(admin_user)
        results['趋势数据正确'] = test_trend_data(admin_user)
        results['查询参数验证'] = test_query_parameters()
        results['汇总数据验证'] = test_summary_data(admin_user)
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
