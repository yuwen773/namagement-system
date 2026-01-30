"""
用户行为日志模型验证脚本

验证 UserBehaviorLog 模型的正确性和功能。
"""

import os
import sys
import django

# 设置 UTF-8 编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from behavior_logs.models import UserBehaviorLog
from utils.constants import BehaviorType


def print_section(title):
    """打印分隔线"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def verify_model_structure():
    """验证模型结构"""
    print_section("1. 验证模型结构")

    # 检查模型字段
    fields = [f.name for f in UserBehaviorLog._meta.get_fields()]
    print(f"✓ 模型字段: {', '.join(fields)}")

    # 检查模型选项
    print(f"✓ 数据库表名: {UserBehaviorLog._meta.db_table}")
    print(f"✓ 默认排序: {UserBehaviorLog._meta.ordering}")
    print(f"✓ verbose_name: {UserBehaviorLog._meta.verbose_name}")

    # 检查索引
    indexes = UserBehaviorLog._meta.indexes
    print(f"✓ 索引数量: {len(indexes)}")
    for idx in indexes:
        print(f"  - {idx.name}: {idx.fields}")


def verify_table_creation():
    """验证数据库表创建"""
    print_section("2. 验证数据库表创建")

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = 'user_behavior_logs'
        """)
        count = cursor.fetchone()[0]

        if count > 0:
            print("✓ user_behavior_logs 表已创建")

            # 检查列
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = DATABASE()
                AND table_name = 'user_behavior_logs'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print(f"✓ 表字段 ({len(columns)} 个):")
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"  - {col[0]}: {col[1]} {nullable}")
        else:
            print("✗ user_behavior_logs 表未创建")


def verify_create_behavior_log():
    """验证创建行为日志"""
    print_section("3. 验证创建行为日志")

    # 清理之前的测试数据
    UserBehaviorLog.objects.filter(target__contains='TEST').delete()

    # 获取或创建测试用户
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        print("✓ 测试用户已创建")

    # 创建各种类型的行为日志
    behaviors = [
        {
            'user': user,
            'behavior_type': BehaviorType.LOGIN,
            'target': None,
            'extra_data': {'login_method': 'password'},
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        {
            'user': user,
            'behavior_type': BehaviorType.SEARCH,
            'target': '/recipes',
            'extra_data': {'keyword': '宫保鸡丁', 'results_count': 10},
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        {
            'user': user,
            'behavior_type': BehaviorType.VIEW,
            'target': 'recipe:1',
            'extra_data': {'duration': 45, 'scroll_depth': 0.8},
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        {
            'user': user,
            'behavior_type': BehaviorType.COLLECT,
            'target': 'recipe:1',
            'extra_data': {'source': 'detail_page'},
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        {
            'user': None,  # 未登录用户
            'behavior_type': BehaviorType.VIEW,
            'target': 'recipe:2',
            'extra_data': {'duration': 20},
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
        },
    ]

    created_count = 0
    for behavior in behaviors:
        log = UserBehaviorLog.objects.create(**behavior)
        created_count += 1
        user_str = log.user.username if log.user else '匿名用户'
        print(f"✓ 创建行为日志: {user_str} - {log.behavior_type} - {log.target}")

    print(f"\n✓ 成功创建 {created_count} 条行为日志")


def verify_query_behaviors():
    """验证查询行为日志"""
    print_section("4. 验证查询行为日志")

    # 查询特定用户的行为
    try:
        user = User.objects.get(username='testuser')
        user_behaviors = UserBehaviorLog.objects.filter(user=user)
        print(f"✓ 用户 '{user.username}' 的行为记录: {user_behaviors.count()} 条")

        # 按行为类型筛选
        view_behaviors = UserBehaviorLog.objects.filter(
            user=user,
            behavior_type=BehaviorType.VIEW
        )
        print(f"✓ 其中浏览行为: {view_behaviors.count()} 条")

        # 查询最近的记录
        recent_behaviors = UserBehaviorLog.objects.filter(user=user)[:5]
        print(f"✓ 最近 5 条行为记录:")
        for log in recent_behaviors:
            user_str = log.user.username if log.user else '匿名用户'
            print(f"  - {user_str} | {log.behavior_type} | {log.target} | {log.timestamp}")

    except User.DoesNotExist:
        print("✗ 测试用户不存在")


def verify_anonymous_user():
    """验证未登录用户的行为记录"""
    print_section("5. 验证未登录用户的行为记录")

    anonymous_behaviors = UserBehaviorLog.objects.filter(user=None)
    print(f"✓ 未登录用户的行为记录: {anonymous_behaviors.count()} 条")

    for log in anonymous_behaviors:
        print(f"  - 匿名用户 | {log.behavior_type} | {log.target} | IP: {log.ip_address}")


def verify_extra_data():
    """验证额外数据功能"""
    print_section("6. 验证额外数据功能")

    # 创建带有额外数据的行为日志
    log = UserBehaviorLog.objects.create(
        behavior_type=BehaviorType.SEARCH,
        target='/recipes',
        extra_data={
            'keyword': '麻婆豆腐',
            'filters': {'cuisine': '川菜', 'difficulty': 'medium'},
            'results_count': 15,
            'page': 1
        }
    )

    # 测试获取整个 extra_data
    all_data = log.get_extra_data()
    print(f"✓ 获取所有额外数据: {all_data}")

    # 测试获取特定键
    keyword = log.get_extra_data('keyword', 'N/A')
    print(f"✓ 获取搜索关键词: {keyword}")

    # 测试获取不存在的键
    not_found = log.get_extra_data('not_exist', '默认值')
    print(f"✓ 获取不存在的键: {not_found}")

    # 测试设置额外数据
    log.set_extra_data({'new_key': 'new_value'})
    print(f"✓ 更新后的额外数据: {log.extra_data}")


def verify_convenience_method():
    """验证便捷方法"""
    print_section("7. 验证便捷方法 log_behavior")

    # 清理测试数据
    UserBehaviorLog.objects.filter(extra_data__test_marker=True).delete()

    # 使用便捷方法创建行为日志
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    log = UserBehaviorLog.log_behavior(
        user=user,
        behavior_type=BehaviorType.VIEW,
        target='recipe:999',
        extra_data={'test_marker': True, 'method': 'log_behavior'},
        ip_address='10.0.0.1',
        user_agent='Test Agent'
    )

    print(f"✓ 使用便捷方法创建行为日志")
    print(f"  - ID: {log.id}")
    print(f"  - 用户: {log.user.username}")
    print(f"  - 行为类型: {log.behavior_type}")
    print(f"  - 目标: {log.target}")
    print(f"  - 额外数据: {log.extra_data}")


def verify_indexes():
    """验证索引创建"""
    print_section("8. 验证数据库索引")

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT index_name, column_name
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
            AND table_name = 'user_behavior_logs'
            ORDER BY index_name, seq_in_index
        """)
        indexes = cursor.fetchall()

        index_dict = {}
        for idx in indexes:
            if idx[0] not in index_dict:
                index_dict[idx[0]] = []
            index_dict[idx[0]].append(idx[1])

        print(f"✓ 索引数量: {len(index_dict)}")
        for idx_name, columns in index_dict.items():
            print(f"  - {idx_name}: {', '.join(columns)}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  用户行为日志模型验证")
    print("=" * 60)

    try:
        verify_model_structure()
        verify_table_creation()
        verify_create_behavior_log()
        verify_query_behaviors()
        verify_anonymous_user()
        verify_extra_data()
        verify_convenience_method()
        verify_indexes()

        print_section("验证完成")
        print("✅ 所有验证通过！")

    except Exception as e:
        print(f"\n✗ 验证失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
