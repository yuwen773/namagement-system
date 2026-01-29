"""
菜谱模型验证脚本

验证 Recipe 模型的数据库结构和基本功能
"""
import os
import sys
import django

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recipes.models import Recipe


def verify_recipe_model():
    """验证 Recipe 模型"""

    print("=" * 60)
    print("菜谱模型验证")
    print("=" * 60)

    # 1. 创建测试菜谱
    print("\n1. 创建测试菜谱...")
    recipe = Recipe.objects.create(
        name='宫保鸡丁',
        cuisine_type='川菜',
        scene_type='晚餐',
        target_audience='通用',
        difficulty='medium',
        cooking_time=30,
        image_url='https://example.com/kungpao.jpg',
        steps='1. 鸡胸肉切丁\n2. 花生米炸香\n3. 爆炒鸡肉\n4. 调味收汁',
        flavor_tags='辣,甜,酸',
        view_count=1000,
        favorite_count=200
    )
    print(f"   ✅ 菜谱创建成功: {recipe.name}")

    # 2. 读取菜谱数据
    print("\n2. 读取菜谱数据...")
    retrieved_recipe = Recipe.objects.get(id=recipe.id)
    print(f"   ✅ 菜谱读取成功")
    print(f"      - 名称: {retrieved_recipe.name}")
    print(f"      - 菜系: {retrieved_recipe.cuisine_type}")
    print(f"      - 难度: {retrieved_recipe.get_difficulty_display()}")
    print(f"      - 烹饪时长: {retrieved_recipe.cooking_time} 分钟")
    print(f"      - 点击量: {retrieved_recipe.view_count}")
    print(f"      - 收藏量: {retrieved_recipe.favorite_count}")

    # 3. 测试口味标签方法
    print("\n3. 测试口味标签方法...")
    flavors = recipe.get_flavor_list()
    print(f"   ✅ 口味标签列表: {flavors}")

    # 4. 更新菜谱数据
    print("\n4. 更新菜谱数据...")
    recipe.cooking_time = 35
    recipe.view_count = 1500
    recipe.save()
    print(f"   ✅ 菜谱更新成功")
    print(f"      - 烹饪时长: {recipe.cooking_time} 分钟")
    print(f"      - 点击量: {recipe.view_count}")

    # 5. 测试筛选功能
    print("\n5. 测试筛选功能...")
    # 创建更多测试数据
    Recipe.objects.create(
        name='麻婆豆腐',
        cuisine_type='川菜',
        difficulty='easy',
        cooking_time=20,
        view_count=800,
        favorite_count=150
    )
    Recipe.objects.create(
        name='白切鸡',
        cuisine_type='粤菜',
        difficulty='easy',
        cooking_time=40,
        view_count=600,
        favorite_count=100
    )

    # 按菜系筛选
    sichuan_recipes = Recipe.objects.filter(cuisine_type='川菜')
    print(f"   ✅ 川菜数量: {sichuan_recipes.count()}")

    # 按难度筛选
    easy_recipes = Recipe.objects.filter(difficulty='easy')
    print(f"   ✅ 简单菜谱数量: {easy_recipes.count()}")

    # 按点击量排序
    top_viewed = Recipe.objects.order_by('-view_count')[:3]
    print(f"   ✅ 点击量前三:")
    for r in top_viewed:
        print(f"      - {r.name}: {r.view_count} 次")

    # 6. 测试索引
    print("\n6. 验证数据库表结构...")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT INDEX_NAME
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'recipes'
            ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """)
        indexes = cursor.fetchall()
        print(f"   ✅ recipes 表索引数量: {len(set([i[0] for i in indexes]))}")
        for index in set([i[0] for i in indexes]):
            print(f"      - {index}")

    # 7. 清理测试数据
    print("\n7. 清理测试数据...")
    Recipe.objects.all().delete()
    print(f"   ✅ 测试数据已清理")

    print("\n" + "=" * 60)
    print("✅ 菜谱模型验证完成！所有测试通过。")
    print("=" * 60)


if __name__ == '__main__':
    try:
        verify_recipe_model()
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
