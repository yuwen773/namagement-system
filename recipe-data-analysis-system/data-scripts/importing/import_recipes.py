# -*- coding: utf-8 -*-
"""
数据导入脚本

将清洗后的菜谱数据导入到数据库中。

功能：
- 批量插入数据（使用 bulk_create）
- 处理食材关联
- 生成随机统计数据（点击量、收藏量）
- 进度显示
- 错误处理

使用方法：
    cd data-scripts/importing
    python import_recipes.py <input_file>

示例：
    # 导入清洗后的数据
    python import_recipes.py ../output/cleaned_recipes.json

    # 使用测试数据
    python import_recipes.py ../output/test_cleaned_output.json

数据生成规则：
- 点击量：100-50000 之间的随机数
- 收藏量：点击量的 5%-20%
- 难度分布：简单 40%、中等 40%、困难 20%（如果数据中没有难度）
"""

import os
import sys

# Windows 控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import json
import random
from pathlib import Path
from datetime import datetime

# 添加 backend 目录到 Python 路径
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import transaction
from django.utils import timezone
from tqdm import tqdm

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from utils.constants import IngredientCategory


# ===== 食材分类字典 =====
# 根据食材名称自动分类
INGREDIENT_CATEGORY_MAP = {
    # 蔬菜类
    '蔬菜': IngredientCategory.VEGETABLE,
    '青菜': IngredientCategory.VEGETABLE,
    '白菜': IngredientCategory.VEGETABLE,
    '菠菜': IngredientCategory.VEGETABLE,
    '芹菜': IngredientCategory.VEGETABLE,
    '生菜': IngredientCategory.VEGETABLE,
    '油菜': IngredientCategory.VEGETABLE,
    '韭菜': IngredientCategory.VEGETABLE,
    '西兰花': IngredientCategory.VEGETABLE,
    '花菜': IngredientCategory.VEGETABLE,
    '番茄': IngredientCategory.VEGETABLE,
    '西红柿': IngredientCategory.VEGETABLE,
    '黄瓜': IngredientCategory.VEGETABLE,
    '茄子': IngredientCategory.VEGETABLE,
    '辣椒': IngredientCategory.VEGETABLE,
    '青椒': IngredientCategory.VEGETABLE,
    '红椒': IngredientCategory.VEGETABLE,
    '土豆': IngredientCategory.VEGETABLE,
    '山药': IngredientCategory.VEGETABLE,
    '莲藕': IngredientCategory.VEGETABLE,
    '萝卜': IngredientCategory.VEGETABLE,
    '胡萝卜': IngredientCategory.VEGETABLE,
    '白萝卜': IngredientCategory.VEGETABLE,
    '冬瓜': IngredientCategory.VEGETABLE,
    '南瓜': IngredientCategory.VEGETABLE,
    '丝瓜': IngredientCategory.VEGETABLE,
    '苦瓜': IngredientCategory.VEGETABLE,
    '笋': IngredientCategory.VEGETABLE,
    '竹笋': IngredientCategory.VEGETABLE,
    '菌': IngredientCategory.VEGETABLE,
    '蘑菇': IngredientCategory.VEGETABLE,
    '香菇': IngredientCategory.VEGETABLE,
    '杏鲍菇': IngredientCategory.VEGETABLE,
    '金针菇': IngredientCategory.VEGETABLE,
    '木耳': IngredientCategory.VEGETABLE,
    '银耳': IngredientCategory.VEGETABLE,
    '豆芽': IngredientCategory.VEGETABLE,
    '豆腐': IngredientCategory.VEGETABLE,
    '豆干': IngredientCategory.VEGETABLE,
    '腐竹': IngredientCategory.VEGETABLE,

    # 肉类
    '猪肉': IngredientCategory.MEAT,
    '五花肉': IngredientCategory.MEAT,
    '排骨': IngredientCategory.MEAT,
    '肉': IngredientCategory.MEAT,
    '牛肉': IngredientCategory.MEAT,
    '牛腩': IngredientCategory.MEAT,
    '羊肉': IngredientCategory.MEAT,
    '鸡肉': IngredientCategory.MEAT,
    '鸡': IngredientCategory.MEAT,
    '鸡翅': IngredientCategory.MEAT,
    '鸡腿': IngredientCategory.MEAT,
    '鸡胸': IngredientCategory.MEAT,
    '鸭': IngredientCategory.MEAT,
    '鸭肉': IngredientCategory.MEAT,
    '鹅': IngredientCategory.MEAT,
    '火腿': IngredientCategory.MEAT,
    '香肠': IngredientCategory.MEAT,
    '培根': IngredientCategory.MEAT,

    # 海鲜类
    '鱼': IngredientCategory.SEAFOOD,
    '鲫鱼': IngredientCategory.SEAFOOD,
    '草鱼': IngredientCategory.SEAFOOD,
    '鲈鱼': IngredientCategory.SEAFOOD,
    '带鱼': IngredientCategory.SEAFOOD,
    '黄鱼': IngredientCategory.SEAFOOD,
    '虾': IngredientCategory.SEAFOOD,
    '虾仁': IngredientCategory.SEAFOOD,
    '蟹': IngredientCategory.SEAFOOD,
    '螃蟹': IngredientCategory.SEAFOOD,
    '蛤蜊': IngredientCategory.SEAFOOD,
    '蚌': IngredientCategory.SEAFOOD,
    '海参': IngredientCategory.SEAFOOD,
    '鲍鱼': IngredientCategory.SEAFOOD,
    '扇贝': IngredientCategory.SEAFOOD,
    '鱿鱼': IngredientCategory.SEAFOOD,
    '章鱼': IngredientCategory.SEAFOOD,
    '海带': IngredientCategory.SEAFOOD,
    '紫菜': IngredientCategory.SEAFOOD,

    # 调料类
    '盐': IngredientCategory.SEASONING,
    '糖': IngredientCategory.SEASONING,
    '冰糖': IngredientCategory.SEASONING,
    '酱油': IngredientCategory.SEASONING,
    '生抽': IngredientCategory.SEASONING,
    '老抽': IngredientCategory.SEASONING,
    '醋': IngredientCategory.SEASONING,
    '料酒': IngredientCategory.SEASONING,
    '蚝油': IngredientCategory.SEASONING,
    '豆瓣酱': IngredientCategory.SEASONING,
    '辣椒酱': IngredientCategory.SEASONING,
    '胡椒粉': IngredientCategory.SEASONING,
    '花椒粉': IngredientCategory.SEASONING,
    '孜然': IngredientCategory.SEASONING,
    '姜': IngredientCategory.SEASONING,
    '生姜': IngredientCategory.SEASONING,
    '蒜': IngredientCategory.SEASONING,
    '大蒜': IngredientCategory.SEASONING,
    '葱': IngredientCategory.SEASONING,
    '大葱': IngredientCategory.SEASONING,
    '小葱': IngredientCategory.SEASONING,
    '香菜': IngredientCategory.SEASONING,
    '八角': IngredientCategory.SEASONING,
    '桂皮': IngredientCategory.SEASONING,
    '香叶': IngredientCategory.SEASONING,
    '芝麻': IngredientCategory.SEASONING,
    '香油': IngredientCategory.SEASONING,
    '花椒': IngredientCategory.SEASONING,
    '豆瓣酱': IngredientCategory.SEASONING,

    # 谷物类
    '米': IngredientCategory.GRAIN,
    '大米': IngredientCategory.GRAIN,
    '小米': IngredientCategory.GRAIN,
    '面': IngredientCategory.GRAIN,
    '面粉': IngredientCategory.GRAIN,
    '面条': IngredientCategory.GRAIN,
    '面条': IngredientCategory.GRAIN,
    '粉丝': IngredientCategory.GRAIN,
    '粉条': IngredientCategory.GRAIN,

    # 水果类
    '苹果': IngredientCategory.FRUIT,
    '香蕉': IngredientCategory.FRUIT,
    '梨': IngredientCategory.FRUIT,
    '橙': IngredientCategory.FRUIT,
    '橘子': IngredientCategory.FRUIT,
    '柠檬': IngredientCategory.FRUIT,
    '西瓜': IngredientCategory.FRUIT,
    '葡萄': IngredientCategory.FRUIT,
    '草莓': IngredientCategory.FRUIT,
    '芒果': IngredientCategory.FRUIT,

    # 乳制品
    '牛奶': IngredientCategory.DAIRY,
    '酸奶': IngredientCategory.DAIRY,
    '奶酪': IngredientCategory.DAIRY,
    '黄油': IngredientCategory.DAIRY,
    '奶油': IngredientCategory.DAIRY,

    # 蛋类
    '鸡蛋': IngredientCategory.MEAT,
    '鸭蛋': IngredientCategory.MEAT,
    '鹌鹑蛋': IngredientCategory.MEAT,
}


def guess_ingredient_category(ingredient_name):
    """
    根据食材名称猜测分类

    Args:
        ingredient_name: 食材名称

    Returns:
        str: 食材分类
    """
    name = ingredient_name.strip()

    # 查找精确匹配
    for key, category in INGREDIENT_CATEGORY_MAP.items():
        if key in name:
            return category

    # 默认返回其他
    return IngredientCategory.OTHER


def generate_random_stats(existing_view=None, existing_fav=None):
    """
    生成随机统计数据

    如果数据中已有统计数据，则使用原值；否则生成随机值。

    Args:
        existing_view: 已有的点击量
        existing_fav: 已有的收藏量

    Returns:
        tuple: (view_count, favorite_count)
    """
    # 如果已有数据，使用原值
    if existing_view is not None and existing_view > 0:
        view_count = existing_view
    else:
        # 生成点击量：100-50000
        view_count = random.randint(100, 50000)

    # 如果已有收藏量，使用原值
    if existing_fav is not None and existing_fav > 0:
        favorite_count = existing_fav
    else:
        # 收藏量为点击量的 5%-20%
        favorite_count = int(view_count * random.uniform(0.05, 0.20))

    return view_count, favorite_count


def assign_difficulty_if_missing(difficulty):
    """
    如果数据中没有难度，根据分布分配难度

    分布：简单 40%、中等 40%、困难 20%

    Args:
        difficulty: 已有的难度值

    Returns:
        str: 难度值（easy/medium/hard）
    """
    if difficulty and difficulty in ['easy', 'medium', 'hard']:
        return difficulty

    # 随机分配难度
    rand = random.random()
    if rand < 0.4:
        return 'easy'
    elif rand < 0.8:
        return 'medium'
    else:
        return 'hard'


class RecipeImporter:
    """菜谱数据导入器"""

    def __init__(self, input_file, batch_size=100):
        """
        初始化导入器

        Args:
            input_file: 输入JSON文件路径
            batch_size: 批量插入的批次大小
        """
        self.input_file = Path(input_file)
        self.batch_size = batch_size

        # 统计信息
        self.stats = {
            'total': 0,
            'recipes_imported': 0,
            'ingredients_imported': 0,
            'relations_imported': 0,
            'errors': [],
            'skipped': 0
        }

        # 食材缓存（避免重复查询）
        self.ingredient_cache = {}

    def load_data(self):
        """加载JSON数据"""
        print(f"\n{'='*60}")
        print(f"加载数据文件: {self.input_file}")
        print(f"{'='*60}")

        if not self.input_file.exists():
            raise FileNotFoundError(f"文件不存在: {self.input_file}")

        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        recipes = data.get('recipes', [])
        self.stats['total'] = len(recipes)

        print(f"[OK] 加载成功，共 {len(recipes)} 条菜谱数据")
        return recipes

    def normalize_ingredient_name(self, name):
        """
        标准化食材名称

        - 截断超过100字符的名称
        - 移除括号内的详细用量说明（保留主要名称）

        Args:
            name: 原始食材名称

        Returns:
            str: 标准化后的食材名称
        """
        if not name:
            return name

        # 如果超过100字符，需要截断
        if len(name) > 100:
            # 尝试提取括号前的主名称
            import re
            # 匹配第一个左括号之前的内容
            match = re.match(r'^([^\\(（]+)', name)
            if match:
                main_name = match.group(1).strip()
                # 如果主名称在合理长度内，使用它
                if 0 < len(main_name) <= 100:
                    return main_name
            # 直接截断到100字符
            return name[:100].strip()

        return name

    def get_or_create_ingredient(self, name):
        """
        获取或创建食材

        Args:
            name: 食材名称

        Returns:
            Ingredient: 食材对象
        """
        # 标准化食材名称
        normalized_name = self.normalize_ingredient_name(name)

        # 检查缓存（使用标准化后的名称）
        if normalized_name in self.ingredient_cache:
            return self.ingredient_cache[normalized_name]

        # 尝试获取
        try:
            ingredient = Ingredient.objects.get(name=normalized_name)
            self.ingredient_cache[normalized_name] = ingredient
            return ingredient
        except Ingredient.DoesNotExist:
            # 创建新食材
            category = guess_ingredient_category(normalized_name)
            ingredient = Ingredient.objects.create(
                name=normalized_name,
                category=category
            )
            self.stats['ingredients_imported'] += 1
            self.ingredient_cache[normalized_name] = ingredient
            return ingredient

    def import_recipes(self, recipes):
        """
        导入菜谱数据

        Args:
            recipes: 菜谱数据列表
        """
        print(f"\n{'='*60}")
        print("开始导入数据...")
        print(f"{'='*60}\n")

        # 准备批量插入的数据
        recipes_to_create = []
        ingredients_relations_to_create = []

        # 使用进度条
        for recipe_data in tqdm(recipes, desc="处理菜谱数据"):
            try:
                # 验证必填字段
                if not recipe_data.get('name'):
                    self.stats['skipped'] += 1
                    self.stats['errors'].append(f"跳过：菜谱缺少名称")
                    continue

                if not recipe_data.get('ingredients'):
                    self.stats['skipped'] += 1
                    self.stats['errors'].append(f"跳过：{recipe_data.get('name')} - 缺少食材信息")
                    continue

                # 处理统计数据
                existing_view = recipe_data.get('view_count')
                existing_fav = recipe_data.get('favorite_count')
                view_count, favorite_count = generate_random_stats(existing_view, existing_fav)

                # 处理难度
                difficulty = assign_difficulty_if_missing(recipe_data.get('difficulty'))

                # 处理口味标签（列表转逗号分隔字符串）
                flavor_tags_list = recipe_data.get('flavor_tags', [])
                if isinstance(flavor_tags_list, list):
                    flavor_tags = ','.join(flavor_tags_list)
                else:
                    flavor_tags = flavor_tags_list

                # 处理步骤（列表转字符串）
                steps_list = recipe_data.get('steps', [])
                if isinstance(steps_list, list):
                    steps = '\n'.join(steps_list)
                else:
                    steps = steps_list

                # 创建菜谱对象
                recipe = Recipe(
                    name=recipe_data.get('name'),
                    cuisine_type=recipe_data.get('cuisine_type', ''),
                    scene_type=recipe_data.get('scene_type', ''),
                    target_audience=recipe_data.get('target_audience', ''),
                    difficulty=difficulty,
                    cooking_time=recipe_data.get('cooking_time'),
                    image_url=recipe_data.get('image_url', ''),
                    steps=steps,
                    flavor_tags=flavor_tags,
                    view_count=view_count,
                    favorite_count=favorite_count
                )
                recipes_to_create.append(recipe)

                # 暂时保存食材关联数据（需要菜谱ID后才能创建）
                recipe._ingredients_data = recipe_data.get('ingredients', [])

            except Exception as e:
                self.stats['skipped'] += 1
                self.stats['errors'].append(f"处理失败: {recipe_data.get('name', 'Unknown')} - {str(e)}")

        # 批量插入菜谱
        if recipes_to_create:
            print(f"\n批量插入菜谱...")

            # 保存菜谱名称到食材数据的映射（用于后续创建关联）
            recipe_ingredients_map = {}
            for r in recipes_to_create:
                recipe_ingredients_map[r.name] = r._ingredients_data

            # 批量插入菜谱
            created_recipes = Recipe.objects.bulk_create(
                recipes_to_create,
                batch_size=self.batch_size
            )
            self.stats['recipes_imported'] = len(created_recipes)
            print(f"[OK] 成功插入 {len(created_recipes)} 条菜谱")

            # 创建食材关联
            print(f"\n处理食材关联...")

            # 从数据库重新获取菜谱（确保有主键ID）
            recipe_names = list(recipe_ingredients_map.keys())
            recipes_from_db = Recipe.objects.filter(name__in=recipe_names)

            # 为每个创建的菜谱处理食材关联
            for recipe in tqdm(recipes_from_db, desc="创建食材关联"):
                # 获取该菜谱的食材数据
                ingredients_data = recipe_ingredients_map.get(recipe.name, [])

                # 去重：同一菜谱中相同食材只保留第一个
                seen_ingredients = set()
                unique_ingredients = []
                for ing_data in ingredients_data:
                    ingredient_name = ing_data.get('name')
                    if not ingredient_name:
                        continue
                    # 标准化食材名称（用于去重比较）
                    normalized_name = self.normalize_ingredient_name(ingredient_name)
                    if normalized_name not in seen_ingredients:
                        seen_ingredients.add(normalized_name)
                        unique_ingredients.append((ing_data, len(seen_ingredients) - 1))

                for idx, (ing_data, sort_order) in enumerate(unique_ingredients):
                    ingredient_name = ing_data.get('name')

                    try:
                        ingredient = self.get_or_create_ingredient(ingredient_name)

                        relation = RecipeIngredient(
                            recipe=recipe,  # 使用从数据库获取的 recipe 对象（有主键）
                            ingredient=ingredient,
                            amount=ing_data.get('amount', ''),
                            sort_order=sort_order
                        )
                        ingredients_relations_to_create.append(relation)
                    except Exception as e:
                        self.stats['errors'].append(f"创建食材关联失败: {ingredient_name} - {str(e)}")

            # 批量插入食材关联
            if ingredients_relations_to_create:
                print(f"\n批量插入食材关联...")
                RecipeIngredient.objects.bulk_create(ingredients_relations_to_create, batch_size=self.batch_size)
                self.stats['relations_imported'] = len(ingredients_relations_to_create)
                print(f"[OK] 成功创建 {len(ingredients_relations_to_create)} 条食材关联")

    def print_summary(self):
        """打印导入摘要"""
        print(f"\n{'='*60}")
        print("导入完成！")
        print(f"{'='*60}")
        print(f"原始数据:     {self.stats['total']} 条")
        print(f"成功导入菜谱: {self.stats['recipes_imported']} 条")
        print(f"新增食材:     {self.stats['ingredients_imported']} 种")
        print(f"食材关联:     {self.stats['relations_imported']} 条")
        print(f"跳过记录:     {self.stats['skipped']} 条")

        if self.stats['errors']:
            print(f"\n错误信息 (最多显示10条):")
            for error in self.stats['errors'][:10]:
                print(f"  - {error}")
            if len(self.stats['errors']) > 10:
                print(f"  ... 还有 {len(self.stats['errors']) - 10} 条错误")

        print(f"{'='*60}\n")

    def verify_import(self):
        """验证导入结果"""
        print("验证导入结果...")

        recipe_count = Recipe.objects.count()
        ingredient_count = Ingredient.objects.count()
        relation_count = RecipeIngredient.objects.count()

        print(f"  数据库中菜谱总数: {recipe_count}")
        print(f"  数据库中食材总数: {ingredient_count}")
        print(f"  食材关联总数:     {relation_count}")

        # 随机抽取一条菜谱验证
        if recipe_count > 0:
            recipe = Recipe.objects.first()
            print(f"\n随机验证菜谱:")
            print(f"  名称: {recipe.name}")
            print(f"  菜系: {recipe.cuisine_type or '未设置'}")
            print(f"  难度: {recipe.get_difficulty_display()}")
            print(f"  食材数: {recipe.recipe_ingredients.count()}")
            print(f"  点击量: {recipe.view_count}")
            print(f"  收藏量: {recipe.favorite_count}")

    def run(self):
        """执行导入"""
        try:
            # 加载数据
            recipes = self.load_data()

            # 导入数据（使用事务）
            with transaction.atomic():
                self.import_recipes(recipes)

            # 打印摘要
            self.print_summary()

            # 验证导入
            self.verify_import()

        except Exception as e:
            print(f"\n[FAIL] 导入失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python import_recipes.py <input_file>")
        print("\n示例:")
        print("  python import_recipes.py ../output/cleaned_recipes.json")
        print("  python import_recipes.py ../output/test_cleaned_output.json")
        sys.exit(1)

    input_file = sys.argv[1]

    # 创建导入器并执行
    importer = RecipeImporter(input_file)
    success = importer.run()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
