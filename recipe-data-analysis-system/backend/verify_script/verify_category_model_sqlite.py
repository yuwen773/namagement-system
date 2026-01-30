"""
分类模型验证脚本 - SQLite 版本

用于在 MySQL 服务未运行时验证模型定义是否正确。

使用方法:
    python verify_category_model_sqlite.py
"""

import os
import sys

# 临时修改配置使用 SQLite
os.environ['DB_NAME'] = 'temp_test_db.sqlite3'

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.conf import settings

# 临时修改数据库配置为 SQLite
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'temp_test_db.sqlite3',
    }
}

django.setup()

from django.db import connection
from categories.models import Category
from utils.constants import CategoryType


def print_section(title):
    """打印分隔符和标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def create_tables():
    """创建数据库表"""
    print_section("创建数据库表")

    try:
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Category)
        print("[OK] categories 表创建成功")
        return True
    except Exception as e:
        print(f"[ERROR] 表创建失败: {e}")
        return False


def test_model_creation():
    """测试模型创建"""
    print_section("测试模型创建和数据插入")

    try:
        # 测试创建菜系
        cuisine = Category.objects.create(
            name='川菜',
            type=CategoryType.CUISINE,
            sort_order=1
        )
        print(f"[OK] 创建菜系: {cuisine.name}")

        # 测试创建场景
        scene = Category.objects.create(
            name='早餐',
            type=CategoryType.SCENE,
            sort_order=1
        )
        print(f"[OK] 创建场景: {scene.name}")

        # 测试创建人群
        crowd = Category.objects.create(
            name='儿童',
            type=CategoryType.CROWD,
            sort_order=1
        )
        print(f"[OK] 创建人群: {crowd.name}")

        # 测试创建口味
        taste = Category.objects.create(
            name='辣',
            type=CategoryType.TASTE,
            sort_order=1
        )
        print(f"[OK] 创建口味: {taste.name}")

        return True
    except Exception as e:
        print(f"[ERROR] 数据创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_methods():
    """测试模型方法"""
    print_section("测试模型方法")

    try:
        cuisines = Category.get_cuisines()
        print(f"[OK] get_cuisines(): 返回 {cuisines.count()} 个菜系")

        scenes = Category.get_scenes()
        print(f"[OK] get_scenes(): 返回 {scenes.count()} 个场景")

        crowds = Category.get_crowds()
        print(f"[OK] get_crowds(): 返回 {crowds.count()} 个人群")

        tastes = Category.get_tastes()
        print(f"[OK] get_tastes(): 返回 {tastes.count()} 个口味")

        return True
    except Exception as e:
        print(f"[ERROR] 模型方法测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def display_all_data():
    """显示所有数据"""
    print_section("显示所有分类数据")

    categories = Category.objects.all().order_by('type', 'sort_order')

    if not categories.exists():
        print("[ERROR] 没有找到任何分类数据")
        return

    for type_value, type_name in CategoryType.CHOICES:
        type_categories = [c for c in categories if c.type == type_value]
        if type_categories:
            print(f"\n【{type_name}】")
            for cat in type_categories:
                print(f"  - {cat.name} (排序: {cat.sort_order})")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  分类模型验证脚本 (SQLite)")
    print("=" * 60)

    results = []

    # 1. 创建表
    results.append(create_tables())

    # 2. 测试模型创建
    results.append(test_model_creation())

    # 3. 显示数据
    display_all_data()

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
        print("\n>>> 模型定义正确，可以在 MySQL 上运行迁移！")
    else:
        print("[WARNING] 部分验证失败")

    # 清理测试数据库
    try:
        os.remove('temp_test_db.sqlite3')
        print("\n[CLEAN] 测试数据库已清理")
    except:
        pass


if __name__ == '__main__':
    main()
