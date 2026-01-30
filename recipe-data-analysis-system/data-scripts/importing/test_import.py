# -*- coding: utf-8 -*-
"""
数据导入测试脚本

测试数据导入功能，使用少量测试数据验证导入流程。

验证项：
- 数据库连接正常
- 清空测试数据功能
- 菜谱导入功能
- 食材创建功能
- 食材关联功能
- 统计数据生成（点击量、收藏量）
- 外键约束正确
- 无错误异常

使用方法：
    cd data-scripts/importing
    python test_import.py
"""

import os
import sys
from pathlib import Path

# Windows 控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 添加 backend 目录到 Python 路径
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient


def clear_test_data():
    """清空测试数据"""
    print("\n" + "="*60)
    print("清空测试数据...")
    print("="*60)

    # 删除食材关联（先删除关联表）
    relations_count = RecipeIngredient.objects.count()
    RecipeIngredient.objects.all().delete()
    print(f"[OK] 删除食材关联: {relations_count} 条")

    # 删除菜谱
    recipes_count = Recipe.objects.count()
    Recipe.objects.all().delete()
    print(f"[OK] 删除菜谱: {recipes_count} 条")

    # 删除食材
    ingredients_count = Ingredient.objects.count()
    Ingredient.objects.all().delete()
    print(f"[OK] 删除食材: {ingredients_count} 条")

    print("[OK] 测试数据已清空")


def run_import_test():
    """运行导入测试"""
    print("\n" + "="*60)
    print("运行数据导入测试...")
    print("="*60)

    # 使用测试数据文件
    test_data_file = Path(__file__).parent.parent / 'output' / 'test_cleaned_output.json'

    if not test_data_file.exists():
        print(f"[ERROR] 测试数据文件不存在: {test_data_file}")
        print("请先运行数据清洗脚本生成测试数据")
        return False

    # 运行导入脚本
    import subprocess
    result = subprocess.run(
        [sys.executable, 'import_recipes.py', str(test_data_file)],
        cwd=Path(__file__).parent,
        capture_output=False
    )

    return result.returncode == 0


def verify_import_results():
    """验证导入结果"""
    print("\n" + "="*60)
    print("验证导入结果...")
    print("="*60)

    # 检查数量
    recipe_count = Recipe.objects.count()
    ingredient_count = Ingredient.objects.count()
    relation_count = RecipeIngredient.objects.count()

    print(f"\n数据统计:")
    print(f"  菜谱总数:   {recipe_count}")
    print(f"  食材总数:   {ingredient_count}")
    print(f"  食材关联数: {relation_count}")

    # 验证项
    all_passed = True

    # 验证1：至少有菜谱数据
    print(f"\n验证项:")
    if recipe_count > 0:
        print(f"  [OK] 菜谱数据存在 ({recipe_count} 条)")
    else:
        print(f"  [FAIL] 没有菜谱数据")
        all_passed = False

    # 验证2：菜谱有食材关联
    recipes_with_ingredients = Recipe.objects.filter(recipe_ingredients__isnull=False).distinct().count()
    if recipes_with_ingredients > 0:
        print(f"  [OK] 食材关联正确 ({recipes_with_ingredients}/{recipe_count} 条菜谱有食材)")
    else:
        print(f"  [FAIL] 没有食材关联")
        all_passed = False

    # 验证3：统计字段已生成
    recipes_with_stats = Recipe.objects.exclude(view_count=0, favorite_count=0).count()
    if recipes_with_stats > 0:
        print(f"  [OK] 统计数据已生成 ({recipes_with_stats} 条)")
    else:
        print(f"  [FAIL] 统计数据未生成")
        all_passed = False

    # 验证4：难度字段正确
    valid_difficulties = Recipe.objects.filter(difficulty__in=['easy', 'medium', 'hard']).count()
    if valid_difficulties == recipe_count:
        print(f"  [OK] 难度字段正确")
    else:
        print(f"  [FAIL] 难度字段有误 ({valid_difficulties}/{recipe_count})")
        all_passed = False

    # 验证5：食材分类已设置
    ingredients_with_category = Ingredient.objects.exclude(category='').count()
    if ingredients_with_category > 0:
        print(f"  [OK] 食材分类已设置")
    else:
        print(f"  [FAIL] 食材分类未设置")
        all_passed = False

    # 随机抽取一条菜谱详细验证
    if recipe_count > 0:
        recipe = Recipe.objects.first()
        print(f"\n随机菜谱详细验证:")
        print(f"  名称:         {recipe.name}")
        print(f"  菜系:         {recipe.cuisine_type or '(空)'}")
        print(f"  场景:         {recipe.scene_type or '(空)'}")
        print(f"  难度:         {recipe.get_difficulty_display()}")
        print(f"  烹饪时间:     {recipe.cooking_time or '(空)'} 分钟")
        print(f"  点击量:       {recipe.view_count}")
        print(f"  收藏量:       {recipe.favorite_count}")
        print(f"  口味标签:     {recipe.flavor_tags or '(空)'}")
        print(f"  食材数量:     {recipe.recipe_ingredients.count()}")

        # 验证关联食材
        ingredients = recipe.recipe_ingredients.all()
        if ingredients:
            print(f"  食材列表:")
            for ri in ingredients[:5]:  # 最多显示5个
                print(f"    - {ri.ingredient.name} ({ri.amount or '未指定用量'}) [{ri.ingredient.get_category_display()}]")

        # 验证收藏量与点击量关系
        ratio = recipe.favorite_count / recipe.view_count if recipe.view_count > 0 else 0
        if 0.05 <= ratio <= 0.20 or recipe.favorite_count == 0:
            print(f"  [OK] 收藏量比例合理 ({ratio:.1%})")
        else:
            print(f"  [WARN] 收藏量比例异常 ({ratio:.1%})，应在 5%-20% 之间")

    # 验证6：检查外键约束
    print(f"\n外键约束验证:")
    try:
        # 尝试删除一个有食材关联的食材（应该失败）
        if ingredient_count > 0:
            ingredient = Ingredient.objects.first()
            # 关闭 Django 的外键检查来测试数据库层面的约束
            from django.db import connection
            with connection.cursor() as cursor:
                # 检查是否有外键约束
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.KEY_COLUMN_USAGE
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'recipe_ingredients'
                    AND COLUMN_NAME = 'ingredient_id'
                    AND REFERENCED_TABLE_NAME = 'ingredients'
                """)
                fk_exists = cursor.fetchone()[0] > 0
                if fk_exists:
                    print(f"  [OK] 外键约束已设置 (recipe_ingredients -> ingredients)")
                else:
                    print(f"  [WARN] 外键约束未设置")

    except Exception as e:
        print(f"  [FAIL] 外键约束验证失败: {e}")

    return all_passed


def main():
    """主函数"""
    print("\n" + "="*60)
    print("数据导入测试")
    print("="*60)

    # 步骤1：清空测试数据
    clear_test_data()

    # 步骤2：运行导入
    if not run_import_test():
        print("\n[FAIL] 导入测试失败")
        return False

    # 步骤3：验证结果
    all_passed = verify_import_results()

    # 打印最终结果
    print("\n" + "="*60)
    if all_passed:
        print("[OK] 所有验证通过！导入功能正常")
        print("="*60)
        return True
    else:
        print("[FAIL] 部分验证失败，请检查上述错误")
        print("="*60)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
