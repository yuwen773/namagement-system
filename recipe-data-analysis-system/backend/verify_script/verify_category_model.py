"""
分类模型验证脚本

验证内容：
1. categories 表是否已创建
2. 初始分类数据是否已插入
3. 各分类类型的数量是否正确

使用方法:
    python verify_category_model.py

预期结果:
    - categories 表存在
    - 共 27 条初始分类数据：
      - 8 个菜系
      - 7 个场景
      - 5 个人群
      - 7 个口味
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from categories.models import Category
from utils.constants import CategoryType


def print_section(title):
    """打印分隔符和标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def verify_table_exists():
    """验证 categories 表是否存在"""
    print_section("1. 验证 categories 表是否存在")

    try:
        # 尝试查询表，如果表不存在会抛出异常
        count = Category.objects.count()
        print(f"[OK] categories 表已创建")
        print(f"   当前记录数: {count} 条")
        return True
    except Exception as e:
        print(f"[ERROR] categories 表不存在或查询失败")
        print(f"   错误信息: {e}")
        return False


def verify_initial_data():
    """验证初始分类数据是否已插入"""
    print_section("2. 验证初始分类数据")

    # 预期的各类型数量
    expected_counts = {
        CategoryType.CUISINE: 8,   # 八大菜系
        CategoryType.SCENE: 7,     # 场景
        CategoryType.CROWD: 5,     # 人群
        CategoryType.TASTE: 7,     # 口味
    }

    total_count = 0
    all_correct = True

    for category_type, expected_count in expected_counts.items():
        actual_count = Category.objects.filter(type=category_type).count()
        total_count += actual_count

        type_name = dict(CategoryType.CHOICES).get(category_type, category_type)
        status = "[OK]" if actual_count == expected_count else "[ERROR]"

        print(f"{status} {type_name}: {actual_count}/{expected_count}")

        if actual_count != expected_count:
            all_correct = False

    print(f"\n总计: {total_count}/{sum(expected_counts.values())} 条")

    if all_correct:
        print("\n[OK] 所有分类数据数量正确！")
    else:
        print("\n[WARNING] 部分分类数据数量不符，请检查迁移是否正确执行")

    return all_correct


def display_all_categories():
    """显示所有分类数据"""
    print_section("3. 显示所有分类数据")

    categories = Category.objects.all().order_by('type', 'sort_order')

    if not categories.exists():
        print("[ERROR] 没有找到任何分类数据")
        return

    # 按类型分组显示
    for type_value, type_name in CategoryType.CHOICES:
        type_categories = [c for c in categories if c.type == type_value]
        if type_categories:
            print(f"\n【{type_name}】")
            for cat in type_categories:
                print(f"  - {cat.name} (排序: {cat.sort_order})")


def test_model_methods():
    """测试 Category 模型的辅助方法"""
    print_section("4. 测试 Category 模型方法")

    try:
        # 测试 get_cuisines 方法
        cuisines = Category.get_cuisines()
        print(f"[OK] get_cuisines(): 返回 {cuisines.count()} 个菜系")

        # 测试 get_scenes 方法
        scenes = Category.get_scenes()
        print(f"[OK] get_scenes(): 返回 {scenes.count()} 个场景")

        # 测试 get_crowds 方法
        crowds = Category.get_crowds()
        print(f"[OK] get_crowds(): 返回 {crowds.count()} 个人群")

        # 测试 get_tastes 方法
        tastes = Category.get_tastes()
        print(f"[OK] get_tastes(): 返回 {tastes.count()} 个口味")

        # 测试 get_by_type 方法
        all_cuisines = Category.get_by_type(CategoryType.CUISINE)
        print(f"[OK] get_by_type('cuisine'): 返回 {all_cuisines.count()} 个菜系")

        return True
    except Exception as e:
        print(f"[ERROR] 模型方法测试失败")
        print(f"   错误信息: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  分类模型验证脚本")
    print("=" * 60)

    results = []

    # 1. 验证表是否存在
    results.append(verify_table_exists())

    if not results[0]:
        print("\n[ERROR] categories 表不存在，请先运行迁移:")
        print("   python manage.py migrate categories")
        return

    # 2. 验证初始数据
    results.append(verify_initial_data())

    # 3. 显示所有分类
    display_all_categories()

    # 4. 测试模型方法
    results.append(test_model_methods())

    # 总结
    print_section("验证结果总结")

    if all(results):
        print("[OK] 所有验证通过！")
        print("\n统计信息:")
        print(f"   - 分类表: 已创建")
        print(f"   - 总记录数: {Category.objects.count()} 条")
        print(f"   - 菜系: {Category.get_cuisines().count()} 个")
        print(f"   - 场景: {Category.get_scenes().count()} 个")
        print(f"   - 人群: {Category.get_crowds().count()} 个")
        print(f"   - 口味: {Category.get_tastes().count()} 个")
        print("\n>>> 阶段二第6步（创建分类/标签表）已完成！")
    else:
        print("[WARNING] 部分验证失败，请检查上述错误信息")


if __name__ == '__main__':
    main()
