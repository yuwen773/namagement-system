"""
数据导入测试脚本 (SQLite 版本)

使用 SQLite 数据库快速测试数据导入功能。

注意：这只是临时测试脚本，用于验证导入逻辑是否正确。
正式环境请使用 MySQL 版本的 test_import.py
"""

import os
import sys
import json
from pathlib import Path

# Windows 控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 添加 backend 目录到 Python 路径
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# 临时使用 SQLite 进行测试
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
# 临时修改数据库配置为 SQLite
from django.conf import settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

django.setup()

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from django.db import connection
from tqdm import tqdm


def setup_database():
    """创建数据库表"""
    from django.core.management import call_command
    print("创建数据库表...")
    call_command('migrate', '--run-syncdb', verbosity=0)
    print("✓ 数据库表创建完成")


def clear_test_data():
    """清空测试数据"""
    print("\n清空测试数据...")
    RecipeIngredient.objects.all().delete()
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()
    print("✓ 测试数据已清空")


def load_test_data():
    """加载测试数据"""
    test_data_file = Path(__file__).parent.parent / 'output' / 'test_cleaned_output.json'

    if not test_data_file.exists():
        raise FileNotFoundError(f"测试数据文件不存在: {test_data_file}")

    with open(test_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get('recipes', [])


def guess_ingredient_category(ingredient_name):
    """根据食材名称猜测分类"""
    from utils.constants import IngredientCategory

    name = ingredient_name.strip().lower()

    # 简化的分类规则
    if any(x in name for x in ['菜', '蔬', '瓜', '豆', '笋', '菇', '菌', '木耳', '银耳', '豆腐']):
        return IngredientCategory.VEGETABLE
    elif any(x in name for x in ['肉', '鸡', '鸭', '猪', '牛', '羊', '火腿', '香肠', '蛋']):
        return IngredientCategory.MEAT
    elif any(x in name for x in ['鱼', '虾', '蟹', '蛤', '海参', '鱿鱼', '海带', '紫菜']):
        return IngredientCategory.SEAFOOD
    elif any(x in name for x in ['盐', '糖', '油', '酱', '醋', '酒', '椒', '粉', '姜', '蒜', '葱']):
        return IngredientCategory.SEASONING
    elif any(x in name for x in ['果', '梨', '蕉', '萄', '莓']):
        return IngredientCategory.FRUIT
    elif any(x in name for x in ['米', '面', '粉']):
        return IngredientCategory.GRAIN
    else:
        return IngredientCategory.OTHER


def generate_random_stats(existing_view=None, existing_fav=None):
    """生成随机统计数据"""
    import random

    if existing_view and existing_view > 0:
        view_count = existing_view
    else:
        view_count = random.randint(100, 50000)

    if existing_fav and existing_fav > 0:
        favorite_count = existing_fav
    else:
        favorite_count = int(view_count * random.uniform(0.05, 0.20))

    return view_count, favorite_count


def import_recipes(recipes):
    """导入菜谱数据"""
    from django.db import transaction
    import random

    recipes_to_create = []
    ingredient_cache = {}
    relations_to_create = []

    print("\n导入菜谱数据...")

    for recipe_data in tqdm(recipes, desc="处理菜谱"):
        # 验证必填字段
        if not recipe_data.get('name'):
            continue
        if not recipe_data.get('ingredients'):
            continue

        # 处理统计数据
        view_count, favorite_count = generate_random_stats(
            recipe_data.get('view_count'),
            recipe_data.get('favorite_count')
        )

        # 处理难度
        difficulty = recipe_data.get('difficulty', 'medium')
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = random.choice(['easy', 'medium', 'hard'])

        # 处理口味标签
        flavor_tags_list = recipe_data.get('flavor_tags', [])
        if isinstance(flavor_tags_list, list):
            flavor_tags = ','.join(flavor_tags_list)
        else:
            flavor_tags = flavor_tags_list

        # 处理步骤
        steps_list = recipe_data.get('steps', [])
        if isinstance(steps_list, list):
            steps = '\n'.join(steps_list)
        else:
            steps = steps_list

        # 创建菜谱
        recipe = Recipe(
            name=recipe_data.get('name'),
            cuisine_type=recipe_data.get('cuisine_type', ''),
            scene_type=recipe_data.get('scene_type', ''),
            difficulty=difficulty,
            cooking_time=recipe_data.get('cooking_time'),
            image_url=recipe_data.get('image_url', ''),
            steps=steps,
            flavor_tags=flavor_tags,
            view_count=view_count,
            favorite_count=favorite_count
        )
        recipes_to_create.append(recipe)
        recipe._ingredients_data = recipe_data.get('ingredients', [])

    # 批量插入菜谱
    created_recipes = Recipe.objects.bulk_create(recipes_to_create, batch_size=100)
    print(f"✓ 成功插入 {len(created_recipes)} 条菜谱")

    # 处理食材关联
    print("\n处理食材关联...")

    for recipe in tqdm(created_recipes, desc="创建食材关联"):
        for idx, ing_data in enumerate(recipe._ingredients_data):
            ingredient_name = ing_data.get('name')
            if not ingredient_name:
                continue

            # 获取或创建食材
            if ingredient_name not in ingredient_cache:
                category = guess_ingredient_category(ingredient_name)
                try:
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient.objects.create(
                        name=ingredient_name,
                        category=category
                    )
                ingredient_cache[ingredient_name] = ingredient

            ingredient = ingredient_cache[ingredient_name]

            relation = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=ing_data.get('amount', ''),
                sort_order=idx
            )
            relations_to_create.append(relation)

    # 批量插入关联
    RecipeIngredient.objects.bulk_create(relations_to_create, batch_size=100)
    print(f"✓ 成功创建 {len(relations_to_create)} 条食材关联")


def verify_import():
    """验证导入结果"""
    print("\n" + "="*60)
    print("验证导入结果")
    print("="*60)

    recipe_count = Recipe.objects.count()
    ingredient_count = Ingredient.objects.count()
    relation_count = RecipeIngredient.objects.count()

    print(f"\n数据统计:")
    print(f"  菜谱总数:   {recipe_count}")
    print(f"  食材总数:   {ingredient_count}")
    print(f"  食材关联数: {relation_count}")

    # 随机抽取一条菜谱验证
    if recipe_count > 0:
        recipe = Recipe.objects.first()
        print(f"\n随机菜谱验证:")
        print(f"  名称:       {recipe.name}")
        print(f"  菜系:       {recipe.cuisine_type or '(空)'}")
        print(f"  难度:       {recipe.get_difficulty_display()}")
        print(f"  点击量:     {recipe.view_count}")
        print(f"  收藏量:     {recipe.favorite_count}")
        print(f"  食材数量:   {recipe.recipe_ingredients.count()}")

        ingredients = recipe.recipe_ingredients.all()
        if ingredients:
            print(f"  食材列表:")
            for ri in ingredients[:5]:
                print(f"    - {ri.ingredient.name} ({ri.amount or '未指定'})")


def main():
    """主函数"""
    print("="*60)
    print("数据导入测试 (SQLite 版本)")
    print("="*60)

    try:
        # 创建数据库
        setup_database()

        # 清空数据
        clear_test_data()

        # 加载测试数据
        print("\n加载测试数据...")
        recipes = load_test_data()
        print(f"✓ 加载 {len(recipes)} 条菜谱数据")

        # 导入数据
        import_recipes(recipes)

        # 验证结果
        verify_import()

        print("\n" + "="*60)
        print("✓ 导入测试完成！")
        print("="*60)
        print("\n注意：此测试使用 SQLite 内存数据库。")
        print("正式环境请使用 MySQL 配置。")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
