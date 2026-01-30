"""
验证食材模型脚本

本脚本用于验证食材模型和菜谱-食材关联模型的正确性
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 设置 UTF-8 输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient


def verify_ingredient_model():
    """验证食材模型"""
    print("=" * 60)
    print("1. 验证 Ingredient 模型")
    print("=" * 60)

    # 测试创建食材
    print("\n1.1 测试创建食材...")
    ingredients_data = [
        {'name': '鸡肉', 'category': 'meat'},
        {'name': '土豆', 'category': 'vegetable'},
        {'name': '生抽', 'category': 'seasoning'},
        {'name': '花生', 'category': 'other'},
    ]

    created_ingredients = []
    for data in ingredients_data:
        ingredient, created = Ingredient.objects.get_or_create(
            name=data['name'],
            defaults={'category': data['category']}
        )
        if created:
            print(f"  [OK] 创建食材: {ingredient.name} ({ingredient.get_category_display()})")
        else:
            print(f"  - 食材已存在: {ingredient.name}")
        created_ingredients.append(ingredient)

    print(f"\n1.2 验证食材数量...")
    count = Ingredient.objects.count()
    print(f"  [OK] 当前食材总数: {count}")

    print(f"\n1.3 测试查询食材...")
    meats = Ingredient.objects.filter(category='meat')
    print(f"  [OK] 肉类食材数量: {meats.count()}")
    for meat in meats:
        print(f"    - {meat.name}")

    print(f"\n1.4 测试食材排序...")
    sorted_ingredients = Ingredient.objects.all()[:5]
    print(f"  [OK] 前5个食材（按分类和名称排序）:")
    for ing in sorted_ingredients:
        print(f"    - {ing}")

    return created_ingredients


def verify_recipe_ingredient_model(ingredients):
    """验证菜谱-食材关联模型"""
    print("\n" + "=" * 60)
    print("2. 验证 RecipeIngredient 模型")
    print("=" * 60)

    # 获取或创建测试菜谱
    print("\n2.1 获取测试菜谱...")
    recipe, created = Recipe.objects.get_or_create(
        name='宫保鸡丁',
        defaults={
            'cuisine_type': '川菜',
            'difficulty': 'medium',
            'cooking_time': 30,
        }
    )
    if created:
        print(f"  [OK] 创建菜谱: {recipe.name}")
    else:
        print(f"  - 菜谱已存在: {recipe.name}")

    # 清理旧的关联数据
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    print(f"  [OK] 清理旧的关联数据")

    # 测试创建食材关联
    print("\n2.2 测试创建食材关联...")
    ingredient_links = [
        {'ingredient': ingredients[0], 'amount': '300g', 'sort_order': 1},  # 鸡肉
        {'ingredient': ingredients[1], 'amount': '2个', 'sort_order': 2},   # 土豆
        {'ingredient': ingredients[2], 'amount': '2勺', 'sort_order': 3},   # 生抽
    ]

    for link_data in ingredient_links:
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=link_data['ingredient'],
            amount=link_data['amount'],
            sort_order=link_data['sort_order']
        )
        print(f"  [OK] 添加食材: {recipe_ingredient.ingredient.name} ({recipe_ingredient.amount})")

    # 测试反向查询
    print(f"\n2.3 测试反向查询...")
    print(f"  [OK] 菜谱 '{recipe.name}' 的食材列表:")
    for ri in recipe.recipe_ingredients.all():
        print(f"    {ri.sort_order}. {ri.ingredient.name}: {ri.amount}")

    # 测试联合唯一约束
    print(f"\n2.4 测试联合唯一约束...")
    try:
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredients[0],  # 鸡肉
            amount='100g',
            sort_order=10
        )
        print(f"  [X] 错误：应该抛出唯一约束异常")
        return False
    except Exception as e:
        print(f"  [OK] 正确抛出唯一约束异常: {type(e).__name__}")

    # 测试食材反向查询
    print(f"\n2.5 测试食材反向查询...")
    chicken = ingredients[0]
    recipes_with_chicken = chicken.recipe_ingredients.all()
    print(f"  [OK] 使用 '{chicken.name}' 的菜谱数量: {recipes_with_chicken.count()}")
    for ri in recipes_with_chicken:
        print(f"    - {ri.recipe.name}")

    return True


def verify_database_indexes():
    """验证数据库索引"""
    print("\n" + "=" * 60)
    print("3. 验证数据库索引")
    print("=" * 60)

    # 检查 ingredients 表索引
    print("\n3.1 检查 ingredients 表索引...")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT INDEX_NAME, COLUMN_NAME
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'ingredients'
            ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """)
        indexes = cursor.fetchall()
        print(f"  [OK] ingredients 表索引数量: {len(set([i[0] for i in indexes]))}")
        for index_name, column_name in indexes:
            print(f"    - {index_name}: {column_name}")

    # 检查 recipe_ingredients 表索引
    print("\n3.2 检查 recipe_ingredients 表索引...")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT INDEX_NAME, COLUMN_NAME
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'recipe_ingredients'
            ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """)
        indexes = cursor.fetchall()
        print(f"  [OK] recipe_ingredients 表索引数量: {len(set([i[0] for i in indexes]))}")
        for index_name, column_name in indexes:
            print(f"    - {index_name}: {column_name}")

    # 检查约束
    print("\n3.3 检查 recipe_ingredients 表约束...")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'recipe_ingredients'
        """)
        constraints = cursor.fetchall()
        print(f"  [OK] recipe_ingredients 表约束数量: {len(constraints)}")
        for constraint_name, constraint_type in constraints:
            print(f"    - {constraint_name}: {constraint_type}")

    return True


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("食材模型验证脚本")
    print("=" * 60)

    try:
        # 验证食材模型
        ingredients = verify_ingredient_model()

        # 验证菜谱-食材关联模型
        verify_recipe_ingredient_model(ingredients)

        # 验证数据库索引
        verify_database_indexes()

        print("\n" + "=" * 60)
        print("[PASS] 所有验证测试通过！")
        print("=" * 60)

        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"[FAIL] 验证失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
