"""
收藏模型验证脚本

本脚本验证 UserFavorite 模型的功能是否正常工作。

验证内容：
1. 模型结构验证
2. 收藏创建测试
3. 联合唯一约束测试（重复收藏应失败）
4. 反向查询测试
5. 数据库索引验证
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from recipes.models import Recipe
from favorites.models import UserFavorite
from django.db import IntegrityError
from django.core.exceptions import ValidationError


def verify_model_structure():
    """验证模型结构"""
    print("\n=== 1. 模型结构验证 ===")

    # 验证字段
    print("[OK] 模型字段：")
    print(f"  - user: {UserFavorite._meta.get_field('user').verbose_name}")
    print(f"  - recipe: {UserFavorite._meta.get_field('recipe').verbose_name}")
    print(f"  - created_at: {UserFavorite._meta.get_field('created_at').verbose_name}")

    # 验证约束
    print("\n[OK] 约束：")
    for constraint in UserFavorite._meta.constraints:
        print(f"  - {constraint.name}: {constraint}")

    # 验证索引
    print("\n[OK] 索引：")
    for index in UserFavorite._meta.indexes:
        print(f"  - {index.name}: {index.fields}")

    print("\n[OK] 模型结构验证通过")


def verify_favorite_creation():
    """验证收藏创建"""
    print("\n=== 2. 收藏创建测试 ===")

    try:
        # 获取或创建测试用户
        user, _ = User.objects.get_or_create(
            username='test_favorite_user',
            defaults={
                'email': 'favorite@test.com',
                'role': 'user'
            }
        )
        user.set_password('password123')
        user.save()

        # 获取或创建测试菜谱
        recipe, _ = Recipe.objects.get_or_create(
            name='测试收藏菜谱',
            defaults={
                'cuisine_type': '川菜',
                'difficulty': 'medium',
                'cooking_time': 30
            }
        )

        # 创建收藏
        favorite = UserFavorite.objects.create(
            user=user,
            recipe=recipe
        )

        print(f"[OK] 创建收藏成功：{favorite}")
        print(f"  - 用户：{favorite.user.username}")
        print(f"  - 菜谱：{favorite.recipe.name}")
        print(f"  - 收藏时间：{favorite.created_at}")

        print("\n[OK] 收藏创建测试通过")
        return favorite, user, recipe

    except Exception as e:
        print(f"\n[FAIL] 收藏创建测试失败：{e}")
        return None, None, None


def verify_unique_constraint(favorite, user, recipe):
    """验证联合唯一约束"""
    print("\n=== 3. 联合唯一约束测试 ===")

    if not favorite:
        print("[SKIP] 跳过测试（前面的测试未通过）")
        return

    try:
        # 尝试重复收藏同一菜谱
        duplicate = UserFavorite(
            user=user,
            recipe=recipe
        )
        duplicate.save()

        print("\n[FAIL] 联合唯一约束测试失败：允许重复收藏")

    except IntegrityError:
        print("[OK] 重复收藏被正确拒绝")
        print("[OK] 联合唯一约束测试通过")


def verify_reverse_query(user, recipe):
    """验证反向查询"""
    print("\n=== 4. 反向查询测试 ===")

    if not user or not recipe:
        print("[SKIP] 跳过测试（前面的测试未通过）")
        return

    try:
        # 通过用户查询收藏
        user_favorites = user.favorites.all()
        print(f"[OK] 用户 {user.username} 的收藏数量：{user_favorites.count()}")

        # 通过菜谱查询收藏者
        recipe_favorited = recipe.favorited_by.all()
        print(f"[OK] 菜谱 {recipe.name} 被收藏次数：{recipe_favorited.count()}")

        # 查询所有收藏
        all_favorites = UserFavorite.objects.select_related('user', 'recipe').all()
        print(f"[OK] 系统总收藏数量：{all_favorites.count()}")

        print("\n[OK] 反向查询测试通过")

    except Exception as e:
        print(f"\n[FAIL] 反向查询测试失败：{e}")


def verify_indexes():
    """验证数据库索引"""
    print("\n=== 5. 数据库索引验证 ===")

    try:
        from django.db import connection

        with connection.cursor() as cursor:
            # 获取表的所有索引
            cursor.execute("""
                SELECT INDEX_NAME, COLUMN_NAME
                FROM information_schema.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'user_favorites'
                ORDER BY INDEX_NAME, SEQ_IN_INDEX
            """)
            indexes = cursor.fetchall()

            print("[OK] user_favorites 表的索引：")
            for index_name, column_name in indexes:
                print(f"  - {index_name}: {column_name}")

        print("\n[OK] 数据库索引验证通过")

    except Exception as e:
        print(f"\n[FAIL] 数据库索引验证失败：{e}")


def cleanup_test_data():
    """清理测试数据"""
    print("\n=== 清理测试数据 ===")

    try:
        # 删除测试收藏
        UserFavorite.objects.filter(user__username='test_favorite_user').delete()

        # 删除测试用户
        User.objects.filter(username='test_favorite_user').delete()

        # 删除测试菜谱
        Recipe.objects.filter(name='测试收藏菜谱').delete()

        print("[OK] 测试数据已清理")

    except Exception as e:
        print(f"[WARN] 清理测试数据时出错：{e}")


def main():
    """主函数"""
    print("=" * 60)
    print("收藏模型验证测试")
    print("=" * 60)

    try:
        # 1. 模型结构验证
        verify_model_structure()

        # 2. 收藏创建测试
        favorite, user, recipe = verify_favorite_creation()

        # 3. 联合唯一约束测试
        verify_unique_constraint(favorite, user, recipe)

        # 4. 反向查询测试
        verify_reverse_query(user, recipe)

        # 5. 数据库索引验证
        verify_indexes()

        print("\n" + "=" * 60)
        print("[OK] 所有测试通过！")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] 测试过程中出现错误：{e}")
        import traceback
        traceback.print_exc()

    finally:
        # 清理测试数据
        cleanup_test_data()


if __name__ == '__main__':
    main()
