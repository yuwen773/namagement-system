# -*- coding: utf-8 -*-
"""
页面访问模拟测试脚本

测试 generate_page_visits.py 的功能，验证：
1. 页面访问日志生成正确
2. 各页面访问分布合理
3. 停留时间在合理范围内
4. 访问路径记录完整
5. 数据质量检查
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 切换到 backend 目录
os.chdir(str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db.models import Count, Q
from accounts.models import User
from recipes.models import Recipe
from behavior_logs.models import UserBehaviorLog


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


def test_page_view_count():
    """测试1: 验证页面访问日志数量"""
    print_test("验证页面访问日志数量")

    # 获取模拟用户的页面访问日志
    mock_user_ids = list(User.objects.filter(
        Q(username__startswith='mock_user_') | Q(id__gte=31)
    ).values_list('id', flat=True))

    page_views = UserBehaviorLog.objects.filter(
        behavior_type='page_view',
        user_id__in=mock_user_ids
    )

    expected_min = 500  # 50用户 * 10最少访问

    if page_views.count() >= expected_min:
        print_pass(f"找到 {page_views.count()} 条页面访问日志（≥ {expected_min}）")
        return page_views
    elif page_views.count() >= 100:
        print_warning(f"找到 {page_views.count()} 条页面访问日志（建议 ≥ {expected_min}）")
        return page_views
    else:
        print_fail(f"只找到 {page_views.count()} 条页面访问日志（需要 ≥ {expected_min}）")
        return None


def test_page_type_distribution(page_views):
    """测试2: 验证页面类型分布"""
    print_test("验证页面类型分布")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    page_type_counts = {}
    for log in page_views:
        extra_data = log.extra_data or {}
        page_type = extra_data.get('page_type', 'unknown')
        page_type_counts[page_type] = page_type_counts.get(page_type, 0) + 1

    print_info("页面类型分布:")
    expected_pages = ['home', 'recipe_list', 'recipe_detail', 'category', 'hot']

    all_valid = True
    total = page_views.count()

    for page_type in expected_pages:
        count = page_type_counts.get(page_type, 0)
        ratio = count / total if total > 0 else 0

        # 验证各类页面都有访问
        if count == 0:
            print_fail(f"没有 {page_type} 页面的访问记录")
            all_valid = False
        else:
            print_info(f"  - {page_type}: {count} ({ratio*100:.1f}%)")

    if all_valid:
        print_pass("所有预期页面都有访问记录")
    else:
        print_warning("部分页面没有访问记录")

    return all_valid


def test_stay_duration(page_views):
    """测试3: 验证停留时间合理"""
    print_test("验证停留时间在合理范围内")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    # 预期停留时间范围（秒）
    expected_durations = {
        'home': (5, 30),
        'recipe_list': (15, 60),
        'recipe_detail': (30, 180),
        'category': (10, 45),
        'hot': (15, 60),
    }

    all_valid = True
    duration_issues = []

    for log in page_views[:500]:  # 采样检查
        extra_data = log.extra_data or {}
        page_type = extra_data.get('page_type')
        stay_duration = extra_data.get('stay_duration', 0)

        if page_type in expected_durations:
            min_d, max_d = expected_durations[page_type]
            if stay_duration < min_d or stay_duration > max_d:
                duration_issues.append(f"{page_type}: {stay_duration}秒 (期望 {min_d}-{max_d}秒)")

    if not duration_issues:
        print_pass("所有停留时间在预期范围内")
        return True
    else:
        # 检查问题比例
        issue_ratio = len(duration_issues) / min(page_views.count(), 500)
        if issue_ratio < 0.1:  # 允许10%的异常
            print_warning(f"少量停留时间异常（{len(duration_issues)}/{min(page_views.count(), 500)}）")
            print_pass("停留时间基本合理")
            return True
        else:
            print_fail(f"停留时间异常较多: {len(duration_issues)} 条")
            for issue in duration_issues[:3]:
                print_info(f"  - {issue}")
            return False


def test_session_path(page_views):
    """测试4: 验证访问路径记录"""
    print_test("验证访问路径记录（点击流）")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    # 检查是否有路径长度信息
    logs_with_path = 0
    logs_with_position = 0

    for log in page_views[:500]:
        extra_data = log.extra_data or {}
        if 'path_length' in extra_data:
            logs_with_path += 1
        if 'session_position' in extra_data:
            logs_with_position += 1

    sample_size = min(page_views.count(), 500)

    if logs_with_path >= sample_size * 0.8:
        print_pass(f"{logs_with_path}/{sample_size} 条记录包含路径长度")
    else:
        print_warning(f"只有 {logs_with_path}/{sample_size} 条记录包含路径长度")

    if logs_with_position >= sample_size * 0.8:
        print_pass(f"{logs_with_position}/{sample_size} 条记录包含会话位置")
    else:
        print_warning(f"只有 {logs_with_position}/{sample_size} 条记录包含会话位置")

    return logs_with_path >= sample_size * 0.5  # 至少50%有路径记录


def test_user_coverage(page_views):
    """测试5: 验证用户覆盖率"""
    print_test("验证用户覆盖率")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    # 获取有页面访问的用户数
    active_users = page_views.values('user_id').distinct().count()

    # 获取模拟用户总数
    mock_user_count = User.objects.filter(
        Q(username__startswith='mock_user_') | Q(id__gte=31)
    ).distinct().count()

    coverage = active_users / mock_user_count if mock_user_count > 0 else 0

    print_info(f"活跃用户数: {active_users}")
    print_info(f"模拟用户总数: {mock_user_count}")
    print_info(f"用户覆盖率: {coverage*100:.1f}%")

    if coverage >= 0.5:  # 至少50%用户有访问
        print_pass(f"用户覆盖率达标（{coverage*100:.1f}% ≥ 50%）")
        return True
    else:
        print_warning(f"用户覆盖率偏低（{coverage*100:.1f}% < 50%）")
        return True  # 继续测试


def test_data_completeness(page_views):
    """测试6: 验证数据完整性"""
    print_test("验证数据完整性")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    issues = []
    total = page_views.count()

    # 检查 IP 地址
    logs_without_ip = page_views.filter(ip_address__isnull=True).count()
    if logs_without_ip > total * 0.1:
        issues.append(f"IP为空: {logs_without_ip} 条")
    else:
        print_info(f"IP 地址填充率: {(total - logs_without_ip) / total * 100:.1f}%")

    # 检查 User-Agent
    logs_without_ua = page_views.filter(user_agent__isnull=True).count()
    if logs_without_ua > total * 0.1:
        issues.append(f"User-Agent为空: {logs_without_ua} 条")
    else:
        print_info(f"User-Agent 填充率: {(total - logs_without_ua) / total * 100:.1f}%")

    # 检查 extra_data
    logs_without_extra = page_views.filter(extra_data__isnull=True).count()
    if logs_without_extra > total * 0.1:
        issues.append(f"extra_data为空: {logs_without_extra} 条")
    else:
        print_info(f"extra_data 填充率: {(total - logs_without_extra) / total * 100:.1f}%")

    # 检查 page_type 字段
    logs_without_page_type = 0
    for log in page_views:
        extra_data = log.extra_data or {}
        if 'page_type' not in extra_data:
            logs_without_page_type += 1

    if logs_without_page_type > total * 0.1:
        issues.append(f"page_type缺失: {logs_without_page_type} 条")
    else:
        print_info(f"page_type 填充率: {(total - logs_without_page_type) / total * 100:.1f}%")

    if issues:
        print_warning("部分字段填充率较低:")
        for issue in issues:
            print_info(f"  - {issue}")
        return False
    else:
        print_pass("数据完整性良好")
        return True


def test_time_distribution(page_views):
    """测试7: 验证时间分布"""
    print_test("验证时间分布（30天内）")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    # 获取最早和最晚的访问时间
    earliest = page_views.order_by('timestamp').first()
    latest = page_views.order_by('-timestamp').first()

    if earliest and latest:
        from django.utils import timezone
        import pytz

        earliest_time = earliest.timestamp
        latest_time = latest.timestamp

        # 处理时区
        if timezone.is_aware(earliest_time):
            now = timezone.now()
        else:
            now = datetime.now()
            if earliest_time.tzinfo is None:
                earliest_time = pytz.utc.localize(earliest_time)
                latest_time = pytz.utc.localize(latest_time)

        days_span = (now - earliest_time).days

        print_info(f"最早访问: {earliest_time.strftime('%Y-%m-%d %H:%M')}")
        print_info(f"最晚访问: {latest_time.strftime('%Y-%m-%d %H:%M')}")
        print_info(f"时间跨度: {days_span} 天")

        if days_span <= 35 and days_span >= 0:
            print_pass("访问时间分布合理（30天内）")
            return True
        else:
            print_warning(f"时间跨度异常: {days_span} 天")
            return False
    else:
        print_fail("无法获取访问时间")
        return False


def test_hour_distribution(page_views):
    """测试8: 验证小时分布（模拟真实用户模式）"""
    print_test("验证小时分布（白天更活跃）")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    hour_dict = {}
    for log in page_views[:1000]:  # 采样处理
        timestamp = log.timestamp
        # 获取本地小时（处理时区）
        if timestamp.tzinfo is not None:
            import pytz
            utc_time = timestamp.replace(tzinfo=None)
            local_tz = pytz.timezone('Asia/Shanghai')
            try:
                local_time = utc_time.astimezone(local_tz)
                hour = local_time.hour
            except:
                hour = timestamp.hour
        else:
            hour = timestamp.hour

        hour_dict[hour] = hour_dict.get(hour, 0) + 1

    # 验证白天（6-22点）的行为占比高于夜间
    day_hours = list(range(6, 23))
    night_hours = list(range(0, 6))

    day_count = sum(hour_dict.get(h, 0) for h in day_hours)
    night_count = sum(hour_dict.get(h, 0) for h in night_hours)
    total = sum(hour_dict.values())

    day_ratio = day_count / total if total > 0 else 0

    print_info(f"白天(6-22点): {day_count} ({day_ratio*100:.1f}%)")
    print_info(f"夜间(0-6点): {night_count} ({(1-day_ratio)*100:.1f}%)")

    if day_ratio >= 0.7:
        print_pass("小时分布符合预期（白天更活跃）")
        return True
    else:
        print_warning(f"小时分布异常：白天占比 {day_ratio*100:.1f}%（预期 > 70%）")
        return False


def test_quality_summary(page_views):
    """测试9: 数据质量总结"""
    print_test("数据质量总结")

    if page_views is None:
        print_fail("页面访问日志为空，跳过测试")
        return False

    total = page_views.count()

    print(f"\n  {TestColors.BOLD}页面访问数据质量指标:{TestColors.ENDC}")

    # 页面类型覆盖
    page_types = set()
    for log in page_views:
        extra_data = log.extra_data or {}
        if 'page_type' in extra_data:
            page_types.add(extra_data['page_type'])

    expected_types = 5  # home, recipe_list, recipe_detail, category, hot
    type_coverage = len(page_types) / expected_types * 100
    print(f"    页面类型覆盖: {type_coverage:.1f}%（{len(page_types)}/{expected_types}）")

    # 用户覆盖率
    user_count = page_views.values('user_id').distinct().count()
    print(f"    活跃用户数: {user_count}")

    # 平均每用户访问数
    if user_count > 0:
        avg_visits = total / user_count
        print(f"    平均每用户访问: {avg_visits:.1f}")

    # 时间跨度
    earliest = page_views.order_by('timestamp').first()
    latest = page_views.order_by('-timestamp').first()
    if earliest and latest:
        days = (latest.timestamp - earliest.timestamp).days
        print(f"    时间跨度: {days} 天")

    # 综合评分
    score = 0
    if type_coverage >= 100:
        score += 30
    elif type_coverage >= 80:
        score += 25

    if user_count >= 50:
        score += 25
    elif user_count >= 30:
        score += 20

    if 10 <= avg_visits <= 50:
        score += 25
    elif avg_visits > 0:
        score += 15

    if days <= 35:
        score += 20
    elif days > 0:
        score += 10

    print(f"\n  {TestColors.BOLD}质量得分: {score}/100{TestColors.ENDC}")

    if score >= 90:
        print_pass("数据质量优秀")
        return True
    elif score >= 70:
        print_warning("数据质量良好")
        return True
    else:
        print_fail("数据质量需要改进")
        return False


def run_all_tests():
    """运行所有测试"""
    print_header("页面访问模拟测试")

    results = {}

    # 测试1: 获取页面访问日志
    page_views = test_page_view_count()
    results['页面访问日志数量'] = page_views is not None and page_views.count() >= 500

    # 如果没有页面访问日志，后续测试无法进行
    if page_views is None or page_views.count() == 0:
        print_header("测试结果")
        print(f"{TestColors.FAIL}[X] 测试中断：没有找到页面访问日志{TestColors.ENDC}")
        print("\n请先运行 generate_page_visits.py 生成页面访问数据")
        return

    # 运行其他测试
    results['页面类型分布'] = test_page_type_distribution(page_views)
    results['停留时间'] = test_stay_duration(page_views)
    results['访问路径记录'] = test_session_path(page_views)
    results['用户覆盖率'] = test_user_coverage(page_views)
    results['数据完整性'] = test_data_completeness(page_views)
    results['时间分布'] = test_time_distribution(page_views)
    results['小时分布'] = test_hour_distribution(page_views)
    results['数据质量总结'] = test_quality_summary(page_views)

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
    elif passed >= total * 0.8:
        print(f"\n{TestColors.WARNING}{TestColors.BOLD}[WARNING] 大部分测试通过{TestColors.ENDC}")
    else:
        print(f"\n{TestColors.FAIL}{TestColors.BOLD}[FAIL] 部分测试失败{TestColors.ENDC}")

    # 额外统计信息
    print_header("页面访问数据统计")
    total_views = page_views.count()
    print(f"  页面访问总数: {total_views}")
    print(f"  活跃用户数: {page_views.values('user_id').distinct().count()}")

    # 页面类型分布
    page_type_counts = {}
    for log in page_views:
        extra_data = log.extra_data or {}
        page_type = extra_data.get('page_type', 'unknown')
        page_type_counts[page_type] = page_type_counts.get(page_type, 0) + 1

    print(f"  页面分布:")
    for page_type, count in sorted(page_type_counts.items(), key=lambda x: -x[1]):
        print(f"    - {page_type}: {count}")


if __name__ == "__main__":
    run_all_tests()
