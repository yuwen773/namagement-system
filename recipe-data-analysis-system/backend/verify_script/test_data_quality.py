# -*- coding: utf-8 -*-
"""
数据质量验证脚本（阶段十七第4步）

综合验证模拟数据的质量，检查：
1. 行为记录数量是否符合预期
2. 行为时间分布是否合理
3. 点击量和收藏量是否更新
4. 是否存在异常数据
5. 生成完整的数据质量报告
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 切换到 backend 目录
os.chdir(str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db.models import Count, Q, Sum
from django.utils import timezone
import pytz

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


class QualityReport:
    """数据质量报告"""

    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.summary = {
            'total_users': 0,
            'total_behaviors': 0,
            'total_page_views': 0,
            'recipes_with_views': 0,
            'recipes_with_favorites': 0,
            'quality_score': 0,
            'issues': [],
            'warnings': []
        }
        self.details = {}

    def add_issue(self, issue: str):
        self.summary['issues'].append(issue)

    def add_warning(self, warning: str):
        self.summary['warnings'].append(warning)

    def to_dict(self):
        return {
            'report_time': self.timestamp,
            'summary': self.summary,
            'details': self.details
        }

    def print_summary(self):
        print(f"\n{TestColors.HEADER}{TestColors.BOLD}")
        print("=" * 70)
        print("                        数据质量报告")
        print("=" * 70)
        print(f"{TestColors.ENDC}\n")

        print(f"  报告生成时间: {self.timestamp}")
        print(f"  总用户数: {self.summary['total_users']}")
        print(f"  行为日志总数: {self.summary['total_behaviors']}")
        print(f"  页面访问总数: {self.summary['total_page_views']}")
        print(f"  有点击量的菜谱: {self.summary['recipes_with_views']}")
        print(f"  有收藏量的菜谱: {self.summary['recipes_with_favorites']}")
        print(f"\n  {TestColors.BOLD}质量得分: {self.summary['quality_score']}/100{TestColors.ENDC}")

        if self.summary['issues']:
            print(f"\n  {TestColors.FAIL}问题列表:{TestColors.ENDC}")
            for issue in self.summary['issues'][:10]:
                print(f"    - {issue}")

        if self.summary['warnings']:
            print(f"\n  {TestColors.WARNING}警告列表:{TestColors.ENDC}")
            for warning in self.summary['warnings'][:10]:
                print(f"    - {warning}")


def print_header(text: str):
    """打印标题"""
    print(f"\n{TestColors.HEADER}{TestColors.BOLD}{'=' * 60}{TestColors.ENDC}")
    print(f"{TestColors.HEADER}{TestColors.BOLD}{text:^60}{TestColors.ENDC}")
    print(f"{TestColors.HEADER}{TestColors.BOLD}{'=' * 60}{TestColors.ENDC}\n")


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


# ============================================================================
# 1. 用户数据验证
# ============================================================================

def validate_user_data(report: QualityReport):
    """验证用户数据"""
    print_header("1. 用户数据验证")

    # 获取模拟用户
    mock_users = User.objects.filter(
        Q(username__startswith='mock_user_') | Q(id__gte=31)
    ).distinct()

    user_count = mock_users.count()
    report.summary['total_users'] = user_count
    report.details['users'] = {
        'mock_user_count': user_count,
        'with_profiles': 0,
        'with_nickname': 0,
        'with_bio': 0,
        'is_active': 0
    }

    print_info(f"模拟用户数量: {user_count}")

    # 验证用户数量
    if user_count >= 100:
        print_pass(f"用户数量达标（≥ 100，实际: {user_count}）")
    elif user_count >= 50:
        print_warning(f"用户数量偏少（≥ 50，实际: {user_count}）")
        report.add_warning(f"用户数量偏少: {user_count}（建议 ≥ 100）")
    else:
        print_fail(f"用户数量不足（实际: {user_count}，需要 ≥ 100）")
        report.add_issue(f"用户数量不足: {user_count}（需要 ≥ 100）")

    # 验证资料完整性
    users_with_profiles = 0
    users_with_nickname = 0
    users_with_bio = 0
    users_active = 0

    for user in mock_users:
        try:
            _ = user.profile
            users_with_profiles += 1
            if user.profile.nickname:
                users_with_nickname += 1
            if user.profile.bio:
                users_with_bio += 1
        except:
            pass
        if user.is_active:
            users_active += 1

    report.details['users']['with_profiles'] = users_with_profiles
    report.details['users']['with_nickname'] = users_with_nickname
    report.details['users']['with_bio'] = users_with_bio
    report.details['users']['is_active'] = users_active

    print_info(f"有资料的用户: {users_with_profiles} ({users_with_profiles/user_count*100:.1f}%)")
    print_info(f"有昵称的用户: {users_with_nickname} ({users_with_nickname/user_count*100:.1f}%)")
    print_info(f"有简介的用户: {users_with_bio} ({users_with_bio/user_count*100:.1f}%)")
    print_info(f"激活的用户: {users_active} ({users_active/user_count*100:.1f}%)")

    # 验证用户名唯一性
    duplicate_users = User.objects.values('username').annotate(
        count=Count('username')
    ).filter(count__gt=1)

    if not duplicate_users:
        print_pass("用户名唯一性验证通过")
    else:
        dup_count = len(list(duplicate_users))
        print_fail(f"发现 {dup_count} 个重复用户名")
        report.add_issue(f"发现 {dup_count} 个重复用户名")

    # 验证邮箱唯一性
    duplicate_emails = User.objects.values('email').annotate(
        count=Count('email')
    ).filter(count__gt=1)

    duplicate_emails = [e for e in duplicate_emails if e['email']]
    if not duplicate_emails:
        print_pass("邮箱唯一性验证通过")
    else:
        dup_count = len(duplicate_emails)
        print_fail(f"发现 {dup_count} 个重复邮箱")
        report.add_issue(f"发现 {dup_count} 个重复邮箱")

    return mock_users


# ============================================================================
# 2. 行为记录数量验证
# ============================================================================

def validate_behavior_count(report: QualityReport, mock_users):
    """验证行为记录数量"""
    print_header("2. 行为记录数量验证")

    # 获取模拟用户的行为日志
    mock_user_ids = list(mock_users.values_list('id', flat=True))

    # 所有行为日志
    all_behaviors = UserBehaviorLog.objects.filter(user_id__in=mock_user_ids)
    behavior_count = all_behaviors.count()
    report.summary['total_behaviors'] = behavior_count

    # 页面访问日志
    page_views = all_behaviors.filter(behavior_type='page_view')
    page_view_count = page_views.count()
    report.summary['total_page_views'] = page_view_count

    print_info(f"行为日志总数: {behavior_count}")
    print_info(f"页面访问日志: {page_view_count}")

    # 验证行为数量
    expected_min_behaviors = 2000  # 100用户 * 20条

    if behavior_count >= expected_min_behaviors:
        print_pass(f"行为数量达标（≥ {expected_min_behaviors}，实际: {behavior_count}）")
    elif behavior_count >= 500:
        print_warning(f"行为数量偏少（≥ 500，实际: {behavior_count}）")
        report.add_warning(f"行为数量偏少: {behavior_count}（建议 ≥ {expected_min_behaviors}）")
    else:
        print_fail(f"行为数量不足（实际: {behavior_count}，需要 ≥ {expected_min_behaviors}）")
        report.add_issue(f"行为数量不足: {behavior_count}（需要 ≥ {expected_min_behaviors}）")

    # 验证页面访问数量
    expected_min_page_views = 500
    if page_view_count >= expected_min_page_views:
        print_pass(f"页面访问数量达标（≥ {expected_min_page_views}，实际: {page_view_count}）")
    elif page_view_count >= 100:
        print_warning(f"页面访问数量偏少（≥ 100，实际: {page_view_count}）")
    else:
        print_fail(f"页面访问数量不足（实际: {page_view_count}，需要 ≥ {expected_min_page_views}）")
        report.add_issue(f"页面访问数量不足: {page_view_count}（需要 ≥ {expected_min_page_views}）")

    # 按类型统计
    type_counts = all_behaviors.values('behavior_type').annotate(count=Count('id'))
    report.details['behavior_types'] = {item['behavior_type']: item['count'] for item in type_counts}

    print_info("\n行为类型分布:")
    for item in type_counts:
        behavior_type = item['behavior_type']
        count = item['count']
        ratio = count / behavior_count * 100 if behavior_count > 0 else 0
        print_info(f"  - {behavior_type}: {count} ({ratio:.1f}%)")

    return all_behaviors, page_views


# ============================================================================
# 3. 行为类型分布验证
# ============================================================================

def validate_behavior_distribution(report: QualityReport, behaviors):
    """验证行为类型分布"""
    print_header("3. 行为类型分布验证")

    type_counts = behaviors.values('behavior_type').annotate(count=Count('id'))
    type_dict = {item['behavior_type']: item['count'] for item in type_counts}
    total = behaviors.count()

    # 预期比例范围
    expected_ratios = {
        'login': (0.03, 0.07),      # 3-7%
        'search': (0.15, 0.25),     # 15-25%
        'view': (0.50, 0.70),       # 50-70%
        'favorite': (0.10, 0.20),   # 10-20%
        'page_view': (0.01, 0.10)   # 1-10%
    }

    report.details['expected_ratios'] = expected_ratios
    report.details['actual_ratios'] = {}

    all_valid = True
    print_info("行为类型比例验证:")

    for behavior_type, (min_ratio, max_ratio) in expected_ratios.items():
        count = type_dict.get(behavior_type, 0)
        ratio = count / total if total > 0 else 0
        actual_ratio = round(ratio * 100, 1)
        expected_range = f"{min_ratio*100:.0f}-{max_ratio*100:.0f}%"

        report.details['actual_ratios'][behavior_type] = {
            'count': count,
            'ratio': actual_ratio,
            'expected': expected_range
        }

        if count == 0:
            print_fail(f"  - {behavior_type}: 无数据（预期 {expected_range}）")
            all_valid = False
            report.add_issue(f"缺少 {behavior_type} 类型的行为数据")
        elif ratio < min_ratio or ratio > max_ratio:
            print_warning(f"  - {behavior_type}: {actual_ratio}%（预期 {expected_range}）")
            report.add_warning(f"{behavior_type} 比例异常: {actual_ratio}%（预期 {expected_range}）")
        else:
            print_pass(f"  - {behavior_type}: {actual_ratio}%（预期 {expected_range}）")

    return all_valid


# ============================================================================
# 4. 时间分布验证
# ============================================================================

def validate_time_distribution(report: QualityReport, behaviors):
    """验证时间分布"""
    print_header("4. 时间分布验证")

    # 获取最早和最晚的行为时间
    earliest = behaviors.order_by('timestamp').first()
    latest = behaviors.order_by('-timestamp').first()

    if earliest and latest:
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

        print_info(f"最早行为: {earliest_time.strftime('%Y-%m-%d %H:%M')}")
        print_info(f"最晚行为: {latest_time.strftime('%Y-%m-%d %H:%M')}")
        print_info(f"时间跨度: {days_span} 天")

        report.details['time_range'] = {
            'earliest': earliest_time.strftime('%Y-%m-%d %H:%M'),
            'latest': latest_time.strftime('%Y-%m-%d %H:%M'),
            'days_span': days_span
        }

        # 验证时间跨度
        if days_span <= 35 and days_span >= 0:
            print_pass(f"时间跨度合理（{days_span} 天，预期 1-35 天）")
        elif days_span > 35:
            print_warning(f"时间跨度偏大（{days_span} 天，建议 ≤ 35 天）")
            report.add_warning(f"时间跨度偏大: {days_span} 天（建议 ≤ 35 天）")
        else:
            print_fail(f"时间跨度异常: {days_span} 天")
            report.add_issue(f"时间跨度异常: {days_span} 天")
    else:
        print_fail("无法获取行为时间")
        report.add_issue("无法获取行为时间")

    # 验证小时分布（白天更活跃）
    print_info("\n小时分布验证（白天6-22点应更活跃）:")

    hour_dict = {}
    sample_size = min(behaviors.count(), 1000)

    for log in behaviors[:sample_size]:
        timestamp = log.timestamp
        if timestamp.tzinfo is not None:
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

    day_hours = list(range(6, 23))
    night_hours = list(range(0, 6))

    day_count = sum(hour_dict.get(h, 0) for h in day_hours)
    night_count = sum(hour_dict.get(h, 0) for h in night_hours)
    total = sum(hour_dict.values())

    day_ratio = day_count / total if total > 0 else 0

    print_info(f"  白天(6-22点): {day_count} ({day_ratio*100:.1f}%)")
    print_info(f"  夜间(0-6点): {night_count} ({(1-day_ratio)*100:.1f}%)")

    report.details['hour_distribution'] = {
        'day_ratio': round(day_ratio * 100, 1),
        'sample_size': sample_size
    }

    if day_ratio >= 0.7:
        print_pass("小时分布符合预期（白天更活跃）")
    elif day_ratio >= 0.5:
        print_warning(f"小时分布偏均匀（白天占比 {day_ratio*100:.1f}%，预期 > 70%）")
        report.add_warning(f"小时分布偏均匀: {day_ratio*100:.1f}%")
    else:
        print_fail(f"小时分布异常（白天占比 {day_ratio*100:.1f}%，预期 > 70%）")
        report.add_issue(f"小时分布异常: {day_ratio*100:.1f}%")


# ============================================================================
# 5. 菜谱点击量和收藏量验证
# ============================================================================

def validate_recipe_stats(report: QualityReport, behaviors):
    """验证菜谱点击量和收藏量"""
    print_header("5. 菜谱点击量和收藏量验证")

    # 获取有浏览行为的菜谱ID
    view_targets = behaviors.filter(
        behavior_type='view'
    ).values_list('target', flat=True).distinct()

    # 提取菜谱ID
    view_recipe_ids = []
    for target in view_targets:
        if target:
            if ':' in str(target):
                try:
                    recipe_id = int(str(target).split(':')[-1])
                    view_recipe_ids.append(recipe_id)
                except (ValueError, IndexError):
                    pass
            else:
                try:
                    view_recipe_ids.append(int(target))
                except ValueError:
                    pass

    # 获取有收藏行为的菜谱ID
    fav_targets = behaviors.filter(
        behavior_type='favorite'
    ).values_list('target', flat=True).distinct()

    fav_recipe_ids = []
    for target in fav_targets:
        if target:
            if ':' in str(target):
                try:
                    recipe_id = int(str(target).split(':')[-1])
                    fav_recipe_ids.append(recipe_id)
                except (ValueError, IndexError):
                    pass
            else:
                try:
                    fav_recipe_ids.append(int(target))
                except ValueError:
                    pass

    # 验证点击量
    recipes_with_views = Recipe.objects.filter(
        id__in=view_recipe_ids,
        view_count__gt=0
    ).count()
    report.summary['recipes_with_views'] = recipes_with_views

    total_recipes = Recipe.objects.count()
    print_info(f"总菜谱数: {total_recipes}")
    print_info(f"有点击量的菜谱: {recipes_with_views}")

    if recipes_with_views > 0:
        print_pass(f"菜谱点击量已更新（{recipes_with_views} 个菜谱）")
    else:
        print_fail("菜谱点击量未更新")
        report.add_issue("菜谱点击量未更新")

    # 验证收藏量
    recipes_with_favorites = Recipe.objects.filter(
        id__in=fav_recipe_ids,
        favorite_count__gt=0
    ).count()
    report.summary['recipes_with_favorites'] = recipes_with_favorites

    print_info(f"有收藏量的菜谱: {recipes_with_favorites}")

    if recipes_with_favorites > 0:
        print_pass(f"菜谱收藏量已更新（{recipes_with_favorites} 个菜谱）")
    else:
        print_fail("菜谱收藏量未更新")
        report.add_issue("菜谱收藏量未更新")

    # 验证数据合理性：收藏量不应超过点击量
    unreasonable = 0
    recipes_checked = 0

    for recipe in Recipe.objects.filter(id__in=set(view_recipe_ids + fav_recipe_ids)):
        if recipe.view_count > 0 and recipe.favorite_count > recipe.view_count:
            unreasonable += 1
        recipes_checked += 1

    if unreasonable == 0:
        print_pass("收藏量/点击量比例合理")
    else:
        print_warning(f"{unreasonable} 个菜谱收藏量超过点击量")
        report.add_warning(f"{unreasonable} 个菜谱收藏量超过点击量")

    report.details['recipe_stats'] = {
        'total_recipes': total_recipes,
        'recipes_with_views': recipes_with_views,
        'recipes_with_favorites': recipes_with_favorites,
        'unreasonable_count': unreasonable
    }


# ============================================================================
# 6. 数据完整性验证
# ============================================================================

def validate_data_completeness(report: QualityReport, behaviors, page_views):
    """验证数据完整性"""
    print_header("6. 数据完整性验证")

    total = behaviors.count()
    page_total = page_views.count() if page_views else 0

    report.details['completeness'] = {}

    # 验证必要字段
    checks = [
        ('IP 地址', behaviors.filter(ip_address__isnull=True).count(), total, 0.1),
        ('User-Agent', behaviors.filter(user_agent__isnull=True).count(), total, 0.1),
        ('extra_data', behaviors.filter(extra_data__isnull=True).count(), total, 0.1),
    ]

    if page_views:
        checks.extend([
            ('page_view IP', page_views.filter(ip_address__isnull=True).count(), page_total, 0.1),
            ('page_view User-Agent', page_views.filter(user_agent__isnull=True).count(), page_total, 0.1),
        ])

    all_complete = True
    print_info("字段填充率验证:")

    for field_name, null_count, total_count, max_null_ratio in checks:
        fill_rate = (total_count - null_count) / total_count * 100 if total_count > 0 else 0
        is_valid = null_count <= total_count * max_null_ratio

        report.details['completeness'][field_name] = {
            'fill_rate': round(fill_rate, 1),
            'null_count': null_count
        }

        if is_valid:
            print_pass(f"  {field_name}: {fill_rate:.1f}%")
        else:
            print_fail(f"  {field_name}: {fill_rate:.1f}%（低于 {(1-max_null_ratio)*100:.0f}% 标准）")
            all_complete = False
            report.add_issue(f"{field_name} 填充率过低: {fill_rate:.1f}%")

    # 验证 page_type 字段
    if page_views:
        page_type_issues = 0
        for log in page_views:
            extra_data = log.extra_data or {}
            if 'page_type' not in extra_data:
                page_type_issues += 1

        page_type_fill_rate = (page_total - page_type_issues) / page_total * 100 if page_total > 0 else 0
        report.details['completeness']['page_type'] = {
            'fill_rate': round(page_type_fill_rate, 1),
            'null_count': page_type_issues
        }

        if page_type_issues <= page_total * 0.1:
            print_pass(f"  page_type: {page_type_fill_rate:.1f}%")
        else:
            print_fail(f"  page_type: {page_type_fill_rate:.1f}%")
            all_complete = False
            report.add_issue(f"page_type 填充率过低: {page_type_fill_rate:.1f}%")

    return all_complete


# ============================================================================
# 7. 用户行为覆盖验证
# ============================================================================

def validate_user_coverage(report: QualityReport, behaviors, page_views, mock_users):
    """验证用户行为覆盖"""
    print_header("7. 用户行为覆盖验证")

    # 有行为记录的用户数
    active_users = behaviors.values('user_id').distinct().count()
    total_users = mock_users.count()
    user_coverage = active_users / total_users if total_users > 0 else 0

    print_info(f"活跃用户数: {active_users}")
    print_info(f"总用户数: {total_users}")
    print_info(f"用户覆盖率: {user_coverage*100:.1f}%")

    report.details['user_coverage'] = {
        'active_users': active_users,
        'total_users': total_users,
        'coverage': round(user_coverage * 100, 1)
    }

    if user_coverage >= 0.8:
        print_pass(f"用户覆盖率高（{user_coverage*100:.1f}% ≥ 80%）")
    elif user_coverage >= 0.5:
        print_warning(f"用户覆盖率中等（{user_coverage*100:.1f}%，建议 ≥ 80%）")
        report.add_warning(f"用户覆盖率中等: {user_coverage*100:.1f}%")
    else:
        print_fail(f"用户覆盖率偏低（{user_coverage*100:.1f}% < 50%）")
        report.add_issue(f"用户覆盖率偏低: {user_coverage*100:.1f}%")

    # 每用户平均行为数
    avg_behaviors = behaviors.count() / active_users if active_users > 0 else 0
    print_info(f"\n平均每用户行为数: {avg_behaviors:.1f}")

    if 20 <= avg_behaviors <= 100:
        print_pass(f"每用户行为数合理（{avg_behaviors:.1f}，预期 20-100）")
    elif avg_behaviors < 20:
        print_warning(f"每用户行为数偏少（{avg_behaviors:.1f}，建议 ≥ 20）")
        report.add_warning(f"每用户行为数偏少: {avg_behaviors:.1f}")
    else:
        print_warning(f"每用户行为数偏多（{avg_behaviors:.1f}，建议 ≤ 100）")

    report.details['avg_behaviors_per_user'] = round(avg_behaviors, 1)


# ============================================================================
# 8. 异常数据检测
# ============================================================================

def detect_anomalies(report: QualityReport, behaviors, page_views):
    """检测异常数据"""
    print_header("8. 异常数据检测")

    anomalies = []

    # 检测1: 检查是否有同一用户在极短时间内产生大量行为
    print_info("检测同一用户短时间内大量行为...")

    user_counts = behaviors.values('user_id').annotate(count=Count('id'))
    extreme_counts = [u for u in user_counts if u['count'] > 500]

    if extreme_counts:
        print_warning(f"发现 {len(extreme_counts)} 个用户有超过500条行为记录")
        for u in extreme_counts[:3]:
            anomalies.append(f"用户 {u['user_id']} 有 {u['count']} 条行为记录")
            report.add_warning(f"用户 {u['user_id']} 行为过多: {u['count']} 条")
    else:
        print_pass("未发现用户行为数量异常")

    # 检测2: 检查行为时间是否在未来
    print_info("\n检测未来时间的行为...")

    from django.utils import timezone
    future_behaviors = behaviors.filter(timestamp__gt=timezone.now())

    if future_behaviors.exists():
        count = future_behaviors.count()
        print_fail(f"发现 {count} 条未来时间的行为记录")
        anomalies.append(f"{count} 条行为记录时间在未来")
        report.add_issue(f"发现 {count} 条未来时间的行为记录")
    else:
        print_pass("未发现未来时间的行为")

    # 检测3: 检查是否有空的用户ID（非匿名用户）
    print_info("\n检测无效用户ID...")

    # 排除匿名用户（user_id 为 NULL）的情况
    invalid_users = behaviors.filter(user_id__isnull=True).exclude(
        behavior_type__in=['page_view', 'view']
    )

    if invalid_users.exists():
        count = invalid_users.count()
        print_warning(f"发现 {count} 条非浏览行为的匿名记录")
        anomalies.append(f"{count} 条非浏览行为的匿名记录")
    else:
        print_pass("未发现无效用户ID")

    # 检测4: 检查页面访问的停留时间
    print_info("\n检测异常停留时间...")

    abnormal_durations = 0
    checked = 0

    for log in page_views[:500]:
        extra_data = log.extra_data or {}
        stay_duration = extra_data.get('stay_duration', 0)

        if stay_duration < 0 or stay_duration > 3600:  # 负数或超过1小时
            abnormal_durations += 1
        checked += 1

    if abnormal_durations > checked * 0.1:
        print_warning(f"发现 {abnormal_durations} 条异常停留时间记录")
        anomalies.append(f"{abnormal_durations} 条停留时间异常")
        report.add_warning(f"{abnormal_durations} 条停留时间异常")
    else:
        print_pass("停留时间基本正常")

    report.details['anomalies'] = {
        'count': len(anomalies),
        'details': anomalies[:10]
    }

    return len(anomalies) == 0


# ============================================================================
# 9. 生成综合质量得分
# ============================================================================

def calculate_quality_score(report: QualityReport):
    """计算综合质量得分"""
    print_header("9. 质量得分计算")

    score = 0
    max_score = 100

    # 用户数据（20分）
    if report.summary['total_users'] >= 100:
        score += 20
    elif report.summary['total_users'] >= 50:
        score += 15
    elif report.summary['total_users'] > 0:
        score += 10

    # 行为数据（30分）
    if report.summary['total_behaviors'] >= 2000:
        score += 30
    elif report.summary['total_behaviors'] >= 500:
        score += 20
    elif report.summary['total_behaviors'] > 0:
        score += 10

    # 菜谱统计（20分）
    if report.summary['recipes_with_views'] > 0:
        score += 10
    if report.summary['recipes_with_favorites'] > 0:
        score += 10

    # 用户覆盖率（15分）
    coverage = report.details.get('user_coverage', {}).get('coverage', 0)
    if coverage >= 80:
        score += 15
    elif coverage >= 50:
        score += 10
    elif coverage > 0:
        score += 5

    # 时间分布（15分）
    days_span = report.details.get('time_range', {}).get('days_span', 0)
    if 1 <= days_span <= 35:
        score += 15
    elif days_span > 0:
        score += 10

    report.summary['quality_score'] = score

    print(f"\n  {TestColors.BOLD}得分明细:{TestColors.ENDC}")
    print(f"    用户数据: {min(20, report.summary['total_users'] > 0 and 20 or (report.summary['total_users'] >= 50 and 15 or 10))} / 20")
    print(f"    行为数据: {min(30, report.summary['total_behaviors'] >= 2000 and 30 or (report.summary['total_behaviors'] >= 500 and 20 or 10))} / 30")
    print(f"    菜谱统计: {min(20, (report.summary['recipes_with_views'] > 0 and 10 or 0) + (report.summary['recipes_with_favorites'] > 0 and 10 or 0))} / 20")
    print(f"    用户覆盖: {min(15, coverage >= 80 and 15 or (coverage >= 50 and 10 or 5))} / 15")
    print(f"    时间分布: {min(15, days_span >= 1 and days_span <= 35 and 15 or 10)} / 15")

    print(f"\n  {TestColors.BOLD}综合得分: {score} / {max_score}{TestColors.ENDC}")

    if score >= 90:
        print_pass("数据质量优秀")
        return True
    elif score >= 70:
        print_warning("数据质量良好")
        return True
    else:
        print_fail("数据质量需要改进")
        return False


# ============================================================================
# 主函数
# ============================================================================

def run_validation():
    """运行完整的质量验证"""
    print_header("模拟数据质量验证（阶段十七第4步）")

    report = QualityReport()

    # 1. 验证用户数据
    mock_users = validate_user_data(report)

    # 检查是否有用户
    if mock_users.count() == 0:
        print_fail("没有找到模拟用户，请先运行 generate_mock_users.py")
        report.add_issue("没有模拟用户数据")
        report.print_summary()
        return report

    # 2. 验证行为记录数量
    behaviors, page_views = validate_behavior_count(report, mock_users)

    # 3. 验证行为类型分布
    validate_behavior_distribution(report, behaviors)

    # 4. 验证时间分布
    validate_time_distribution(report, behaviors)

    # 5. 验证菜谱点击量和收藏量
    validate_recipe_stats(report, behaviors)

    # 6. 验证数据完整性
    validate_data_completeness(report, behaviors, page_views)

    # 7. 验证用户覆盖
    validate_user_coverage(report, behaviors, page_views, mock_users)

    # 8. 检测异常数据
    detect_anomalies(report, behaviors, page_views)

    # 9. 计算质量得分
    is_quality_ok = calculate_quality_score(report)

    # 打印最终报告
    report.print_summary()

    # 保存报告到文件
    report_file = project_root / 'data-quality-report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2, default=str)

    print(f"\n报告已保存到: {report_file}")

    # 返回验证结果
    print_header("验证结果")
    if is_quality_ok and not report.summary['issues']:
        print(f"{TestColors.OKGREEN}{TestColors.BOLD}[SUCCESS] 数据质量验证通过！{TestColors.ENDC}")
        return True
    else:
        print(f"{TestColors.WARNING}{TestColors.BOLD}[WARNING] 数据质量存在一些问题，建议检查{TestColors.ENDC}")
        return False


if __name__ == "__main__":
    result = run_validation()
    sys.exit(0 if result else 1)
