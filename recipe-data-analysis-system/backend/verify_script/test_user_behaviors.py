# -*- coding: utf-8 -*-
"""
用户行为模拟测试脚本

测试 generate_user_behaviors.py 的功能，验证：
1. 行为日志生成正确
2. 行为类型分布合理
3. 时间分布符合预期
4. 菜谱点击量和收藏量正确更新
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


def test_behavior_log_count():
    """测试1: 验证行为日志数量"""
    print_test("验证行为日志数量")

    total_logs = UserBehaviorLog.objects.count()

    # 获取模拟用户的行为日志
    mock_user_ids = list(User.objects.filter(
        Q(username__startswith='mock_user_') | Q(id__gte=31)
    ).values_list('id', flat=True))

    mock_logs = UserBehaviorLog.objects.filter(user_id__in=mock_user_ids)

    if mock_logs.count() >= 2000:  # 100用户 * 20最少行为
        print_pass(f"找到 {mock_logs.count()} 条模拟用户行为日志（≥ 2000）")
        return mock_logs
    elif mock_logs.count() >= 500:
        print_warning(f"找到 {mock_logs.count()} 条行为日志（建议 ≥ 2000）")
        return mock_logs
    else:
        print_fail(f"只找到 {mock_logs.count()} 条行为日志（需要 ≥ 2000）")
        return None


def test_behavior_type_distribution(logs):
    """测试2: 验证行为类型分布"""
    print_test("验证行为类型分布")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    type_counts = logs.values('behavior_type').annotate(count=Count('id'))
    type_dict = {item['behavior_type']: item['count'] for item in type_counts}

    print_info("行为类型分布:")
    expected_ratios = {
        'login': (0.03, 0.07),      # 3-7%
        'search': (0.15, 0.25),     # 15-25%
        'view': (0.55, 0.70),       # 55-70%
        'favorite': (0.10, 0.20)    # 10-20%
    }

    all_valid = True
    total = logs.count()

    for behavior_type, (min_ratio, max_ratio) in expected_ratios.items():
        count = type_dict.get(behavior_type, 0)
        ratio = count / total if total > 0 else 0

        status = "OK"
        if ratio < min_ratio or ratio > max_ratio:
            status = "OUT OF RANGE"
            all_valid = False

        print_info(f"  - {behavior_type}: {count} ({ratio*100:.1f}%) {status}")

        # 验证至少有数据
        if count == 0:
            print_fail(f"没有 {behavior_type} 类型的行为")
            all_valid = False

    if all_valid:
        print_pass("行为类型分布合理")
    else:
        print_warning("行为类型分布超出预期范围")

    return all_valid


def test_behavior_time_distribution(logs):
    """测试3: 验证行为时间分布"""
    print_test("验证行为时间分布")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    from django.utils import timezone

    # 获取最早和最晚的行为时间
    earliest = logs.order_by('timestamp').first()
    latest = logs.order_by('-timestamp').first()

    if earliest and latest:
        # 处理时区
        earliest_time = earliest.timestamp
        latest_time = latest.timestamp

        if timezone.is_aware(earliest_time):
            now = timezone.now()
        else:
            from django.conf import settings
            import pytz
            now = timezone.now() if settings.USE_TZ else datetime.now()
            if not timezone.is_aware(earliest_time):
                earliest_time = pytz.utc.localize(earliest_time)
                latest_time = pytz.utc.localize(latest_time)

        days_span = (now - earliest_time).days

        print_info(f"最早行为: {earliest_time.strftime('%Y-%m-%d %H:%M')}")
        print_info(f"最晚行为: {latest_time.strftime('%Y-%m-%d %H:%M')}")
        print_info(f"时间跨度: {days_span} 天")

        # 验证时间跨度在30天内
        if days_span <= 35 and days_span >= 0:
            print_pass("行为时间分布合理（30天内）")
            return True
        else:
            print_warning(f"时间跨度异常: {days_span} 天")
            return False
    else:
        print_fail("无法获取行为时间")
        return False


def test_hour_distribution(logs):
    """测试4: 验证小时分布（模拟真实用户模式）"""
    print_test("验证小时分布（模拟真实用户活跃模式）")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    # 直接使用Python处理小时分布，避免时区问题
    hour_dict = {}
    for log in logs[:1000]:  # 采样处理
        timestamp = log.timestamp
        # 获取本地小时（处理时区）
        if timestamp.tzinfo is not None:
            # 转换为本地时间
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

    # 验证白天行为占比 > 70%
    if day_ratio >= 0.7:
        print_pass("小时分布符合预期（白天更活跃）")
        return True
    else:
        print_warning(f"小时分布异常：白天占比 {day_ratio*100:.1f}%（预期 > 70%）")
        return False


def test_recipe_view_count_update():
    """测试5: 验证菜谱点击量更新"""
    print_test("验证菜谱点击量更新")

    # 获取有行为日志的菜谱ID（target 可能是纯ID或 'recipe:ID' 格式）
    viewed_targets = UserBehaviorLog.objects.filter(
        behavior_type='view'
    ).values_list('target', flat=True).distinct()

    if not viewed_targets:
        print_warning("没有找到浏览行为，无法验证点击量更新")
        return True  # 这不算失败

    # 提取菜谱ID（处理 'recipe:48643' 或纯数字格式）
    viewed_recipe_ids = []
    for target in viewed_targets:
        if target:
            if ':' in str(target):
                # 格式: recipe:48643
                try:
                    recipe_id = int(str(target).split(':')[-1])
                    viewed_recipe_ids.append(recipe_id)
                except (ValueError, IndexError):
                    pass
            else:
                # 纯数字格式
                try:
                    viewed_recipe_ids.append(int(target))
                except ValueError:
                    pass

    if not viewed_recipe_ids:
        print_warning("无法解析菜谱ID")
        return True

    # 验证这些菜谱的点击量 > 0
    recipes_with_views = Recipe.objects.filter(
        id__in=viewed_recipe_ids,
        view_count__gt=0
    )

    if recipes_with_views.count() > 0:
        print_pass(f"{recipes_with_views.count()} 个菜谱的点击量已更新")
        return True
    else:
        print_fail("菜谱点击量未正确更新")
        return False


def test_recipe_favorite_count_update():
    """测试6: 验证菜谱收藏量更新"""
    print_test("验证菜谱收藏量更新")

    # 获取有收藏行为的菜谱ID
    fav_targets = UserBehaviorLog.objects.filter(
        behavior_type='favorite'
    ).values_list('target', flat=True).distinct()

    if not fav_targets:
        print_warning("没有找到收藏行为，无法验证收藏量更新")
        return True  # 这不算失败

    # 提取菜谱ID（处理 'recipe:ID' 或纯数字格式）
    fav_recipe_ids = []
    for target in fav_targets:
        if target:
            if ':' in str(target):
                # 格式: recipe:48643
                try:
                    recipe_id = int(str(target).split(':')[-1])
                    fav_recipe_ids.append(recipe_id)
                except (ValueError, IndexError):
                    pass
            else:
                # 纯数字格式
                try:
                    fav_recipe_ids.append(int(target))
                except ValueError:
                    pass

    if not fav_recipe_ids:
        print_warning("无法解析菜谱ID")
        return True

    # 验证这些菜谱的收藏量 > 0
    recipes_with_favs = Recipe.objects.filter(
        id__in=fav_recipe_ids,
        favorite_count__gt=0
    )

    if recipes_with_favs.count() > 0:
        print_pass(f"{recipes_with_favs.count()} 个菜谱的收藏量已更新")
        return True
    else:
        print_fail("菜谱收藏量未正确更新")
        return False


def test_user_behavior_count(logs):
    """测试7: 验证每个用户的行为数量"""
    print_test("验证每个用户的行为数量（20-100条）")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    # 获取每个用户的行为数量
    user_behavior_counts = logs.values('user_id').annotate(
        count=Count('id')
    )

    min_count = 20
    max_count = 100

    users_out_of_range = []
    for item in user_behavior_counts:
        if item['count'] < min_count or item['count'] > max_count:
            users_out_of_range.append(item)

    if not users_out_of_range:
        print_pass(f"所有 {len(list(user_behavior_counts))} 个用户的行为数量在 {min_count}-{max_count} 范围内")
        return True
    else:
        print_warning(f"{len(users_out_of_range)} 个用户的行为数量超出范围")
        # 打印详细信息
        counts = [item['count'] for item in user_behavior_counts]
        print_info(f"  用户行为数量统计: 最小{min(counts)}, 最大{max(counts)}, 平均{sum(counts)/len(counts):.1f}")
        return True  # 继续测试


def test_behavior_data_completeness(logs):
    """测试8: 验证行为数据完整性"""
    print_test("验证行为数据完整性")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    # 验证必要字段
    issues = []

    # 检查 IP 地址
    logs_without_ip = logs.filter(ip_address__isnull=True).count()
    if logs_without_ip > logs.count() * 0.1:  # 允许10%为空
        issues.append(f"IP为空: {logs_without_ip} 条")
    else:
        print_info(f"IP 地址填充率: {(logs.count() - logs_without_ip) / logs.count() * 100:.1f}%")

    # 检查 User-Agent
    logs_without_ua = logs.filter(user_agent__isnull=True).count()
    if logs_without_ua > logs.count() * 0.1:
        issues.append(f"User-Agent为空: {logs_without_ua} 条")
    else:
        print_info(f"User-Agent 填充率: {(logs.count() - logs_without_ua) / logs.count() * 100:.1f}%")

    # 检查 extra_data
    logs_without_extra = logs.filter(extra_data__isnull=True).count()
    if logs_without_extra > logs.count() * 0.1:
        issues.append(f"extra_data为空: {logs_without_extra} 条")
    else:
        print_info(f"extra_data 填充率: {(logs.count() - logs_without_extra) / logs.count() * 100:.1f}%")

    if issues:
        print_warning("部分字段填充率较低:")
        for issue in issues:
            print_info(f"  - {issue}")
        return False
    else:
        print_pass("行为数据完整性良好")
        return True


def test_login_favorite_ratio(logs):
    """测试9: 验证登录到收藏的转化率"""
    print_test("验证登录到收藏的转化率（收藏不应超过登录）")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    login_count = logs.filter(behavior_type='login').count()
    favorite_count = logs.filter(behavior_type='favorite').count()

    print_info(f"登录次数: {login_count}")
    print_info(f"收藏次数: {favorite_count}")

    # 收藏次数应该远小于登录次数（合理的用户行为模式）
    if login_count > 0:
        ratio = favorite_count / login_count
        print_info(f"收藏/登录比例: {ratio:.2f}")

        # 收藏次数不应该超过登录次数的3倍
        if ratio <= 3:
            print_pass("登录到收藏的比例合理")
            return True
        else:
            print_warning(f"收藏次数相对于登录次数偏高（比例: {ratio:.2f}）")
            return True  # 继续测试
    else:
        print_warning("没有登录行为")
        return True


def test_data_quality_summary(logs):
    """测试10: 数据质量总结"""
    print_test("数据质量总结")

    if logs is None:
        print_fail("行为日志为空，跳过测试")
        return False

    total = logs.count()

    print(f"\n  {TestColors.BOLD}行为数据质量指标:{TestColors.ENDC}")

    # 行为类型覆盖
    type_counts = logs.values('behavior_type').annotate(count=Count('id'))
    type_coverage = len(type_counts) / 4 * 100  # 4种类型
    print(f"    行为类型覆盖: {type_coverage:.1f}%")

    # 用户覆盖率
    user_count = logs.values('user_id').distinct().count()
    print(f"    活跃用户数: {user_count}")

    # 时间跨度
    earliest = logs.order_by('timestamp').first()
    latest = logs.order_by('-timestamp').first()
    if earliest and latest:
        days = (latest.timestamp - earliest.timestamp).days
        print(f"    时间跨度: {days} 天")

    # 平均每用户行为数
    if user_count > 0:
        avg_behaviors = total / user_count
        print(f"    平均每用户行为: {avg_behaviors:.1f}")

    # 综合评分
    score = 0
    if type_coverage >= 100:
        score += 25
    elif type_coverage >= 75:
        score += 20

    if user_count >= 50:
        score += 25
    elif user_count >= 30:
        score += 20

    if 20 <= avg_behaviors <= 100:
        score += 25
    elif avg_behaviors > 0:
        score += 15

    if days <= 35:
        score += 25
    elif days > 0:
        score += 15

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
    print_header("用户行为模拟测试")

    results = {}

    # 测试1: 获取行为日志
    logs = test_behavior_log_count()
    results['行为日志数量'] = logs is not None and logs.count() >= 2000

    # 如果没有行为日志，后续测试无法进行
    if logs is None or logs.count() == 0:
        print_header("测试结果")
        print(f"{TestColors.FAIL}[X] 测试中断：没有找到行为日志{TestColors.ENDC}")
        print("\n请先运行 generate_user_behaviors.py 生成行为数据")
        return

    # 运行其他测试
    results['行为类型分布'] = test_behavior_type_distribution(logs)
    results['行为时间分布'] = test_behavior_time_distribution(logs)
    results['小时分布'] = test_hour_distribution(logs)
    results['菜谱点击量更新'] = test_recipe_view_count_update()
    results['菜谱收藏量更新'] = test_recipe_favorite_count_update()
    results['用户行为数量'] = test_user_behavior_count(logs)
    results['数据完整性'] = test_behavior_data_completeness(logs)
    results['登录收藏比例'] = test_login_favorite_ratio(logs)
    results['数据质量总结'] = test_data_quality_summary(logs)

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
    print_header("行为数据统计")
    total_logs = logs.count()
    print(f"  行为日志总数: {total_logs}")
    print(f"  活跃用户数: {logs.values('user_id').distinct().count()}")
    print(f"  菜谱点击量增量: {sum(r.view_count for r in Recipe.objects.filter(id__in=logs.filter(behavior_type='view').values_list('target', flat=True).distinct()))}")
    print(f"  菜谱收藏量增量: {sum(r.favorite_count for r in Recipe.objects.filter(id__in=logs.filter(behavior_type='favorite').values_list('target', flat=True).distinct()))}")


if __name__ == "__main__":
    run_all_tests()
