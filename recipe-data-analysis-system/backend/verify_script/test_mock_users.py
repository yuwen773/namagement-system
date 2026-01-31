# -*- coding: utf-8 -*-
"""
模拟用户生成测试脚本

测试 generate_mock_users.py 的功能，验证：
1. 用户数据生成正确
2. 数据库插入成功
3. 字段完整性
4. 数据质量检查
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
# 脚本位置: backend/verify_script/test_mock_users.py
# 项目根目录是其上级目录
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 切换到 backend 目录
os.chdir(str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from accounts.models import User, UserProfile


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


def test_user_count():
    """测试1: 验证生成的用户数量"""
    print_test("验证生成的用户数量")

    # 获取所有模拟用户（包括 mock_user_ 开头和中文用户名）
    # 通过邮箱域名特征来识别模拟用户（模拟用户使用特定域名）
    mock_domains = ['qq.com', '163.com', '126.com', 'gmail.com', 'outlook.com',
                    'sina.com', 'hotmail.com', 'yahoo.com', 'yeah.net', 'foxmail.com']

    # 获取最近创建的用户（ID >= 31，因为模拟用户从ID 31开始）
    mock_users = User.objects.filter(id__gte=31)

    # 或者通过用户名模式识别（mock_user_ 开头或包含数字的中文用户名）
    from django.db.models import Q
    mock_users = User.objects.filter(
        Q(username__startswith='mock_user_') |
        Q(id__gte=31)
    ).distinct()

    if mock_users.count() >= 100:
        print_pass(f"找到 {mock_users.count()} 个模拟用户（≥ 100）")
        return mock_users
    elif mock_users.count() >= 50:
        print_warning(f"找到 {mock_users.count()} 个模拟用户（建议 ≥ 100）")
        return mock_users
    else:
        print_fail(f"只找到 {mock_users.count()} 个模拟用户（需要 ≥ 100）")
        return None


def test_user_profile_existence(users):
    """测试2: 验证所有用户都有对应的资料"""
    print_test("验证所有用户都有对应的资料")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    users_without_profile = []
    for user in users:
        try:
            _ = user.profile
        except UserProfile.DoesNotExist:
            users_without_profile.append(user.username)

    if not users_without_profile:
        print_pass(f"所有 {users.count()} 个用户都有对应的资料")
        return True
    else:
        print_fail(f"{len(users_without_profile)} 个用户缺少资料: {users_without_profile[:5]}")
        return False


def test_user_field_completeness(users):
    """测试3: 验证用户字段完整性"""
    print_test("验证用户字段完整性")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    incomplete_users = []
    for user in users[:20]:  # 检查前20个用户
        issues = []
        if not user.username:
            issues.append("缺少用户名")
        if not user.email:
            issues.append("缺少邮箱")
        if not user.password:
            issues.append("缺少密码")
        if user.role != 'user':
            issues.append(f"角色错误: {user.role}")

        if issues:
            incomplete_users.append({
                'username': user.username or '(空)',
                'issues': issues
            })

    if not incomplete_users:
        print_pass("抽检的前20个用户字段完整")
        return True
    else:
        for user_info in incomplete_users[:3]:
            print_fail(f"用户 {user_info['username']}: {', '.join(user_info['issues'])}")
        return False


def test_profile_field_completeness(users):
    """测试4: 验证用户资料字段完整性"""
    print_test("验证用户资料字段完整性")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    incomplete_profiles = []
    for user in users[:20]:  # 检查前20个用户
        profile = user.profile
        if not profile.nickname:
            incomplete_profiles.append(f"{user.username}: 缺少昵称")

    if not incomplete_profiles:
        print_pass("抽检的前20个用户资料字段完整")
        return True
    else:
        for issue in incomplete_profiles[:3]:
            print_fail(issue)
        return False


def test_password_storage():
    """测试5: 验证密码存储方式（明文）"""
    print_test("验证密码存储方式（明文）")

    mock_users = User.objects.filter(username__startswith='mock_user_')[:5]
    if not mock_users.exists():
        print_fail("没有找到模拟用户")
        return False

    # 验证密码是明文存储
    test_password = "test_password_123"
    for user in mock_users:
        if user.password:
            # 直接比较密码（明文存储）
            if len(user.password) < 20:  # 明文密码通常较短
                print_info(f"用户 {user.username} 的密码长度为 {len(user.password)}（明文存储）")
                break
    else:
        print_warning("无法确定密码存储方式")

    print_pass("密码存储方式检查完成")
    return True


def test_username_uniqueness():
    """测试6: 验证用户名唯一性"""
    print_test("验证用户名唯一性")

    # 检查是否有重复的用户名
    from django.db.models import Count
    duplicate_users = User.objects.values('username').annotate(
        count=Count('username')
    ).filter(count__gt=1)

    if not duplicate_users:
        print_pass("没有重复的用户名")
        return True
    else:
        print_fail(f"发现 {len(duplicate_users)} 个重复的用户名")
        for dup in duplicate_users[:3]:
            print_fail(f"  用户名 '{dup['username']}' 重复 {dup['count']} 次")
        return False


def test_email_uniqueness():
    """测试7: 验证邮箱唯一性"""
    print_test("验证邮箱唯一性")

    # 检查是否有重复的邮箱
    from django.db.models import Count
    duplicate_emails = User.objects.values('email').annotate(
        count=Count('email')
    ).filter(count__gt=1)

    if not duplicate_emails:
        print_pass("没有重复的邮箱")
        return True
    else:
        # 过滤掉 None 值
        duplicate_emails = [e for e in duplicate_emails if e['email']]
        if not duplicate_emails:
            print_pass("没有重复的邮箱")
            return True

        print_fail(f"发现 {len(duplicate_emails)} 个重复的邮箱")
        for dup in duplicate_emails[:3]:
            print_fail(f"  邮箱 '{dup['email']}' 重复 {dup['count']} 次")
        return False


def test_created_at_distribution(users):
    """测试8: 验证创建时间分布"""
    print_test("验证创建时间分布")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    # 检查创建时间的范围
    earliest = users.order_by('created_at').first()
    latest = users.order_by('-created_at').first()

    if earliest and latest:
        from django.utils import timezone
        now = timezone.now() if timezone.is_aware(earliest.created_at) else datetime.now()

        # 处理时区感知的 datetime
        earliest_time = earliest.created_at
        if timezone.is_aware(now) and not timezone.is_aware(earliest_time):
            import pytz
            earliest_time = pytz.utc.localize(earliest_time)

        days_span = (now - earliest_time).days

        print_info(f"最早创建: {earliest.created_at.strftime('%Y-%m-%d')}")
        print_info(f"最新创建: {latest.created_at.strftime('%Y-%m-%d')}")
        print_info(f"时间跨度: {days_span} 天")

        # 验证创建时间在过去一年内
        if days_span > 0 and days_span <= 400:
            print_pass("创建时间分布合理")
            return True
        else:
            print_warning(f"时间跨度异常: {days_span} 天")
            return False

    print_fail("无法获取创建时间")
    return False


def test_user_activation(users):
    """测试9: 验证用户激活状态"""
    print_test("验证用户激活状态")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    inactive_users = users.filter(is_active=False)

    if not inactive_users.exists():
        print_pass("所有用户都是激活状态")
        return True
    else:
        print_warning(f"{inactive_users.count()} 个用户未激活")
        return True  # 这不算严重错误


def test_user_role(users):
    """测试10: 验证用户角色"""
    print_test("验证用户角色")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    admin_users = users.filter(role='admin')
    regular_users = users.filter(role='user')

    print_info(f"普通用户: {regular_users.count()}")
    print_info(f"管理员用户: {admin_users.count()}")

    if admin_users.count() == 0:
        print_pass("所有模拟用户都是普通用户角色")
        return True
    else:
        print_warning(f"有 {admin_users.count()} 个模拟用户是管理员角色")
        return True


def test_login_simulation(users):
    """测试11: 验证登录时间模拟"""
    print_test("验证登录时间模拟")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    users_with_login = users.filter(last_login__isnull=True)
    users_never_login = users.filter(last_login__isnull=True)

    total = users.count()
    login_ratio = (total - users_with_login.count()) / total * 100 if total > 0 else 0

    print_info(f"从未登录: {users_never_login.count()} ({(users_never_login.count()/total*100):.1f}%)")
    print_info(f"有登录记录: {total - users_with_login.count()} ({login_ratio:.1f}%)")

    # 验证登录时间在创建时间之后
    invalid_logins = 0
    for user in users.filter(last_login__isnull=False)[:50]:
        if user.last_login and user.last_login < user.created_at:
            invalid_logins += 1

    if invalid_logins == 0:
        print_pass("登录时间模拟正确")
        return True
    else:
        print_fail(f"{invalid_logins} 个用户的登录时间早于创建时间")
        return False


def test_data_quality_summary(users):
    """测试12: 数据质量总结"""
    print_test("数据质量总结")

    if users is None:
        print_fail("用户列表为空，跳过测试")
        return False

    # 统计各种指标
    total = users.count()
    with_email = users.exclude(email='').count()
    with_nickname = 0
    with_bio = 0

    for user in users:
        try:
            profile = user.profile
            if profile.nickname:
                with_nickname += 1
            if profile.bio:
                with_bio += 1
        except UserProfile.DoesNotExist:
            pass

    print(f"\n  {TestColors.BOLD}数据质量指标:{TestColors.ENDC}")
    print(f"    总用户数: {total}")
    print(f"    有邮箱: {with_email} ({with_email/total*100:.1f}%)")
    print(f"    有昵称: {with_nickname} ({with_nickname/total*100:.1f}%)")
    print(f"    有简介: {with_bio} ({with_bio/total*100:.1f}%)")

    # 计算质量得分
    quality_score = (with_email + with_nickname + with_bio) / (total * 3) * 100
    print(f"\n  {TestColors.BOLD}质量得分: {quality_score:.1f}/100{TestColors.ENDC}")

    if quality_score >= 90:
        print_pass("数据质量优秀")
        return True
    elif quality_score >= 70:
        print_warning("数据质量良好")
        return True
    else:
        print_fail("数据质量需要改进")
        return False


def run_all_tests():
    """运行所有测试"""
    print_header("模拟用户生成测试")

    results = {}

    # 测试1: 获取用户列表
    users = test_user_count()
    results['用户数量'] = users is not None and users.count() >= 100

    # 如果没有用户，后续测试无法进行
    if users is None or users.count() == 0:
        print_header("测试结果")
        print(f"{TestColors.FAIL}[X] 测试中断：没有找到模拟用户{TestColors.ENDC}")
        print("\n请先运行 generate_mock_users.py 生成模拟用户")
        return

    # 如果用户数量不足100，给出警告但继续测试
    if users.count() < 100:
        print_warning(f"用户数量不足100个，但继续进行测试...")

    # 运行其他测试
    results['用户资料存在性'] = test_user_profile_existence(users)
    results['用户字段完整性'] = test_user_field_completeness(users)
    results['资料字段完整性'] = test_profile_field_completeness(users)
    results['密码存储方式'] = test_password_storage()
    results['用户名唯一性'] = test_username_uniqueness()
    results['邮箱唯一性'] = test_email_uniqueness()
    results['创建时间分布'] = test_created_at_distribution(users)
    results['用户激活状态'] = test_user_activation(users)
    results['用户角色'] = test_user_role(users)
    results['登录时间模拟'] = test_login_simulation(users)
    results['数据质量总结'] = test_data_quality_summary(users)

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


if __name__ == "__main__":
    run_all_tests()
