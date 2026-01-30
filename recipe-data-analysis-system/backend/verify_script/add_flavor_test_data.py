"""
添加口味标签测试数据

为现有菜谱添加口味标签，以便测试口味偏好分析接口
"""
import os
import sys
import django

# 设置控制台输出编码为 UTF-8（兼容 Windows）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recipes.models import Recipe


def add_flavor_tags():
    """为菜谱添加口味标签"""
    # 常见口味标签
    common_flavors = ['辣', '甜', '酸', '咸', '鲜', '清淡', '麻']

    # 获取所有菜谱
    recipes = Recipe.objects.all()
    print(f"总菜谱数: {recipes.count()}")

    # 为每个菜谱随机分配 1-3 个口味标签
    import random
    updated_count = 0

    for recipe in recipes:
        # 随机选择 1-3 个口味标签
        num_flavors = random.randint(1, 3)
        flavors = random.sample(common_flavors, num_flavors)
        recipe.set_flavor_list(flavors)
        recipe.save()
        updated_count += 1
        print(f"更新菜谱: {recipe.name} -> 口味: {', '.join(flavors)}")

    print(f"\n成功更新 {updated_count} 条菜谱的口味标签")

    # 统计各口味的菜谱数量
    print("\n口味统计:")
    flavor_counts = {}
    for recipe in Recipe.objects.all():
        for flavor in recipe.get_flavor_list():
            flavor_counts[flavor] = flavor_counts.get(flavor, 0) + 1

    for flavor, count in sorted(flavor_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {flavor}: {count}")


if __name__ == '__main__':
    add_flavor_tags()
