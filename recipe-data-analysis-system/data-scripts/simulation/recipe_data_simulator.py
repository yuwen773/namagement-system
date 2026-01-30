# -*- coding: utf-8 -*-
"""
菜谱数据模拟器

作为爬虫的备选方案，生成模拟的菜谱数据
用于快速开发和测试
"""

import random
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class RecipeDataSimulator:
    """菜谱数据模拟器"""

    # 基础数据
    CUISINE_TYPES = ['川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '湘菜', '徽菜', '闽菜', '家常菜']
    SCENE_TYPES = ['早餐', '午餐', '晚餐', '下午茶', '夜宵', '快手菜', '宴客菜']
    DIFFICULTIES = ['easy', 'medium', 'hard']
    FLAVORS = ['辣', '甜', '酸', '咸', '鲜', '清淡', '麻']

    # 主料
    MAIN_INGREDIENTS = [
        '猪肉', '鸡肉', '牛肉', '羊肉', '鱼', '虾', '蟹', '鸡蛋', '豆腐',
        '土豆', '白菜', '萝卜', '西红柿', '黄瓜', '茄子', '青椒', '豆角'
    ]

    # 调料
    SEASONINGS = [
        '盐', '酱油', '醋', '料酒', '糖', '味精', '花椒', '辣椒', '姜', '蒜', '葱'
    ]

    # 菜谱名称模板
    RECIPE_NAME_PATTERNS = [
        "{method}{main}",
        "{flavor}{main}",
        "{cuisine}{method}{main}",
        "{main}{method}",
    ]

    COOKING_METHODS = [
        '红烧', '清蒸', '爆炒', '炖煮', '凉拌', '煎炸', '烤制', '涮', '焖'
    ]

    def __init__(self, output_dir: str = "output"):
        """初始化模拟器"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_ingredients(self) -> List[Dict[str, str]]:
        """生成食材列表"""
        # 3-6 种主料
        main_count = random.randint(3, 6)
        ingredients = []

        for _ in range(main_count):
            main = random.choice(self.MAIN_INGREDIENTS)
            amount = random.choice(['100g', '200g', '300g', '500g', '1个', '2个', '适量'])
            ingredients.append({'name': main, 'amount': amount})

        # 2-4 种调料
        for _ in range(random.randint(2, 4)):
            seasoning = random.choice(self.SEASONINGS)
            amount = random.choice(['少许', '适量', '1勺', '2勺'])
            ingredients.append({'name': seasoning, 'amount': amount})

        return ingredients

    def _generate_steps(self, difficulty: str) -> List[str]:
        """生成制作步骤"""
        step_templates = [
            "将{main}洗净，切成{size}。",
            "热锅凉油，下{seasoning}爆香。",
            "放入{main}，{method}至{state}。",
            "加入调料，{action}。",
            "出锅前撒上{seasoning}即可。",
            "盛入盘中，{extra}。"
        ]

        sizes = ['小块', '薄片', '丝', '段', '丁', '条']
        states = ['变色', '断生', '熟透', '软烂', '金黄']
        actions = ['翻炒均匀', '焖煮5分钟', '大火收汁', '小火慢炖']
        extras = ['趁热食用', '撒葱花点缀', '配米饭食用']

        steps = []
        step_count = {'easy': 3, 'medium': 5, 'hard': 8}[difficulty]

        for i in range(step_count):
            template = random.choice(step_templates)
            step = template.format(
                main=random.choice(self.MAIN_INGREDIENTS),
                size=random.choice(sizes),
                seasoning=random.choice(self.SEASONINGS),
                method=random.choice(self.COOKING_METHODS),
                state=random.choice(states),
                action=random.choice(actions),
                extra=random.choice(extras)
            )
            steps.append(f"{i+1}. {step}")

        return steps

    def generate_recipe(self, recipe_id: int) -> Dict[str, Any]:
        """生成单条菜谱数据"""
        # 选择基本属性
        cuisine = random.choice(self.CUISINE_TYPES)
        difficulty = random.choice(self.DIFFICULTIES)
        scene = random.choice(self.SCENE_TYPES)

        # 生成名称
        method = random.choice(self.COOKING_METHODS)
        main = random.choice(self.MAIN_INGREDIENTS)
        flavor = random.choice(random.sample(self.FLAVORS, 2))

        name_pattern = random.choice(self.RECIPE_NAME_PATTERNS)
        name = name_pattern.format(
            method=method,
            main=main,
            flavor=flavor,
            cuisine=cuisine
        )

        # 估算烹饪时间
        cooking_time = {'easy': 15, 'medium': 30, 'hard': 60}[difficulty]
        cooking_time += random.randint(-5, 10)

        # 生成其他数据
        ingredients = self._generate_ingredients()
        steps = self._generate_steps(difficulty)

        return {
            'recipe_id': recipe_id,
            'name': name,
            'cuisine_type': cuisine,
            'scene_type': scene,
            'difficulty': difficulty,
            'cooking_time': max(5, cooking_time),
            'flavor_tags': random.sample(self.FLAVORS, random.randint(1, 3)),
            'image_url': f'https://example.com/images/recipe_{recipe_id}.jpg',
            'ingredients': ingredients,
            'steps': steps,
            'tips': f"{name}的小贴士：注意火候控制，{random.choice(['保持食材鲜嫩', '收汁要浓', '不要煮太久'])}。",
            'source_url': f'https://www.xiachufang.com/recipe/{100000 + recipe_id}/',
            'crawled_at': datetime.now().isoformat(),
            # 模拟统计数据
            'view_count': random.randint(100, 50000),
            'favorite_count': random.randint(10, 5000),
        }

    def generate_recipes(self, count: int) -> List[Dict[str, Any]]:
        """批量生成菜谱数据"""
        recipes = []

        for i in range(1, count + 1):
            recipe = self.generate_recipe(i)
            recipes.append(recipe)

            if i % 100 == 0:
                print(f"已生成 {i} 条数据...")

        return recipes

    def save_data(self, recipes: List[Dict[str, Any]], filename: str = None) -> str:
        """保存数据到 JSON 文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulated_recipes_{timestamp}.json"

        save_path = self.output_dir / filename

        output_data = {
            'metadata': {
                'total': len(recipes),
                'generated_at': datetime.now().isoformat(),
                'source': 'simulator',
            },
            'recipes': recipes
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"数据已保存到: {save_path}")
        return str(save_path)


def main():
    """主函数"""
    print("=" * 50)
    print("菜谱数据模拟器")
    print("=" * 50)
    print("\n生成模拟菜谱数据（备选方案）")

    simulator = RecipeDataSimulator(output_dir="../output")

    # 生成 100 条测试数据
    count = 100
    print(f"\n开始生成 {count} 条模拟数据...")
    recipes = simulator.generate_recipes(count)

    # 保存数据
    simulator.save_data(recipes, "test_recipes_simulated.json")

    print("\n" + "=" * 50)
    print("模拟数据生成完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
