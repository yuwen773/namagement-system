# -*- coding: utf-8 -*-
"""
菜谱数据清洗脚本

功能：
1. 去除重复数据
2. 补全缺失字段
3. 统一数据格式（难度、时长、单位等）
4. 提取和标准化食材列表
5. 验证数据完整性
6. 生成清洗报告
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, field

# Windows 控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


@dataclass
class CleaningStats:
    """清洗统计数据"""
    total_input: int = 0
    total_output: int = 0
    duplicates_removed: int = 0
    missing_fields_filled: int = 0
    invalid_records_removed: int = 0
    formats_normalized: int = 0
    ingredients_extracted: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class RecipeCleaner:
    """菜谱数据清洗器"""

    # 有效的难度等级
    VALID_DIFFICULTIES = {'easy', 'medium', 'hard'}

    # 难度中文映射
    DIFFICULTY_MAP = {
        '简单': 'easy',
        '初级': 'easy',
        '容易': 'easy',
        '1': 'easy',
        '中等': 'medium',
        '中级': 'medium',
        '普通': 'medium',
        '2': 'medium',
        '困难': 'hard',
        '高级': 'hard',
        '复杂': 'hard',
        '3': 'hard',
    }

    # 菜系列表（用于标准化）
    VALID_CUISINES = {
        '川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '湘菜', '徽菜', '闽菜', '家常菜'
    }

    # 场景列表
    VALID_SCENES = {
        '早餐', '午餐', '晚餐', '下午茶', '夜宵', '快手菜', '宴客菜'
    }

    # 口味标签
    VALID_FLAVORS = {
        '辣', '甜', '酸', '咸', '鲜', '清淡', '麻'
    }

    # 食材单位标准化
    UNIT_NORMALIZATION = {
        '克': 'g', 'g': 'g',
        '毫升': 'ml', 'ml': 'ml',
        '个': '个', '只': '个',
        '勺': '勺', '汤匙': '勺', '茶匙': '勺',
        '适量': '适量', '少许': '少许',
    }

    def __init__(self):
        """初始化清洗器"""
        self.stats = CleaningStats()
        self.seen_names: Set[str] = set()
        self.seen_ids: Set[int] = set()

    def _normalize_text(self, text: Any) -> str:
        """
        标准化文本

        Args:
            text: 输入文本

        Returns:
            标准化后的文本
        """
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        # 去除首尾空格和特殊字符
        return text.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    def _normalize_difficulty(self, difficulty: Any) -> str:
        """
        标准化难度等级

        Args:
            difficulty: 原始难度值

        Returns:
            标准化后的难度值 (easy/medium/hard)
        """
        if not difficulty:
            return 'medium'  # 默认中等

        difficulty_str = str(difficulty).strip()

        # 如果已经是有效值
        if difficulty_str in self.VALID_DIFFICULTIES:
            return difficulty_str

        # 使用映射表转换
        for key, value in self.DIFFICULTY_MAP.items():
            if key in difficulty_str:
                return value

        # 无法识别，返回默认值
        self.stats.warnings.append(f"无法识别难度值: {difficulty}, 使用默认值 medium")
        return 'medium'

    def _normalize_cooking_time(self, cooking_time: Any) -> int:
        """
        标准化烹饪时间

        Args:
            cooking_time: 原始烹饪时间（可能是数字或字符串）

        Returns:
            标准化后的分钟数
        """
        if cooking_time is None:
            return 30  # 默认30分钟

        if isinstance(cooking_time, (int, float)):
            return max(1, int(cooking_time))

        if isinstance(cooking_time, str):
            # 尝试提取数字
            import re
            match = re.search(r'(\d+)', cooking_time)
            if match:
                return max(1, int(match.group(1)))

        return 30  # 默认值

    def _normalize_flavor_tags(self, flavors: Any) -> List[str]:
        """
        标准化口味标签

        Args:
            flavors: 原始口味标签（可能是列表或逗号分隔的字符串）

        Returns:
            标准化后的口味标签列表
        """
        if not flavors:
            return []

        # 如果是字符串，按逗号分隔
        if isinstance(flavors, str):
            flavors = [f.strip() for f in flavors.split(',')]

        # 过滤出有效的口味标签
        valid_tags = []
        for flavor in flavors:
            flavor_str = str(flavor).strip()
            if flavor_str in self.VALID_FLAVORS:
                valid_tags.append(flavor_str)

        return valid_tags

    def _normalize_ingredients(self, ingredients: Any) -> List[Dict[str, str]]:
        """
        标准化食材列表

        Args:
            ingredients: 原始食材数据

        Returns:
            标准化后的食材列表
        """
        if not ingredients:
            return []

        normalized = []

        if isinstance(ingredients, list):
            for item in ingredients:
                if isinstance(item, dict):
                    name = self._normalize_text(item.get('name', ''))
                    amount = self._normalize_text(item.get('amount', '适量'))

                    if name:  # 食材名称不能为空
                        normalized.append({'name': name, 'amount': amount})

        elif isinstance(ingredients, str):
            # 如果是字符串，尝试按行分割
            lines = ingredients.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    # 简单的食材提取（假设格式为 "食材名 用量"）
                    parts = line.split(maxsplit=1)
                    name = parts[0] if parts else ''
                    amount = parts[1] if len(parts) > 1 else '适量'
                    if name:
                        normalized.append({'name': name, 'amount': amount})

        return normalized

    def _normalize_steps(self, steps: Any) -> List[str]:
        """
        标准化制作步骤

        Args:
            steps: 原始步骤数据

        Returns:
            标准化后的步骤列表
        """
        if not steps:
            return []

        normalized = []

        if isinstance(steps, list):
            for step in steps:
                step_text = self._normalize_text(step)
                if step_text:
                    # 确保步骤有编号
                    if not step_text[0].isdigit():
                        step_text = f"{len(normalized) + 1}. {step_text}"
                    normalized.append(step_text)

        elif isinstance(steps, str):
            # 按行分割
            lines = steps.split('\n')
            for i, line in enumerate(lines, 1):
                step_text = line.strip()
                if step_text:
                    normalized.append(step_text)

        return normalized

    def _normalize_image_url(self, image_url: Any) -> str:
        """
        标准化图片 URL

        Args:
            image_url: 原始图片 URL

        Returns:
            标准化后的 URL 或空字符串
        """
        if not image_url:
            return ""

        url = str(image_url).strip()

        # 检查是否是有效 URL
        if url.startswith('http://') or url.startswith('https://'):
            return url

        # 如果是本地路径，保持原样
        if url.startswith('/') or url.startswith('./'):
            return url

        return ""

    def _generate_name_hash(self, name: str) -> str:
        """
        生成菜谱名称哈希值（用于去重）

        Args:
            name: 菜谱名称

        Returns:
            MD5 哈希值
        """
        return hashlib.md5(name.encode('utf-8')).hexdigest()

    def _is_duplicate(self, recipe: Dict[str, Any]) -> bool:
        """
        检查是否是重复记录

        Args:
            recipe: 菜谱数据

        Returns:
            是否重复
        """
        # 优先使用 recipe_id
        recipe_id = recipe.get('recipe_id')
        if recipe_id and recipe_id in self.seen_ids:
            return True

        # 其次使用名称哈希
        name = recipe.get('name', '')
        if name:
            name_hash = self._generate_name_hash(name)
            if name_hash in self.seen_names:
                return True
            self.seen_names.add(name_hash)

        # 记录 recipe_id
        if recipe_id:
            self.seen_ids.add(recipe_id)

        return False

    def _validate_recipe(self, recipe: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        验证菜谱数据的完整性

        Args:
            recipe: 菜谱数据

        Returns:
            (是否有效, 错误信息)
        """
        # 必填字段检查
        if not recipe.get('name'):
            return False, "缺少菜谱名称"

        # 食材检查
        ingredients = recipe.get('ingredients', [])
        if not ingredients or len(ingredients) == 0:
            return False, "缺少食材信息"

        # 步骤检查
        steps = recipe.get('steps', [])
        if not steps or len(steps) == 0:
            return False, "缺少制作步骤"

        return True, None

    def _fill_missing_fields(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """
        补全缺失字段

        Args:
            recipe: 菜谱数据

        Returns:
            补全后的菜谱数据
        """
        # 补全菜系
        if not recipe.get('cuisine_type'):
            recipe['cuisine_type'] = '家常菜'
            self.stats.missing_fields_filled += 1

        # 补全场景
        if not recipe.get('scene_type'):
            recipe['scene_type'] = '晚餐'
            self.stats.missing_fields_filled += 1

        # 补全难度（已标准化）
        if not recipe.get('difficulty'):
            recipe['difficulty'] = 'medium'
            self.stats.missing_fields_filled += 1

        # 补全烹饪时间（已标准化）
        if not recipe.get('cooking_time'):
            recipe['cooking_time'] = 30
            self.stats.missing_fields_filled += 1

        # 补全统计数据
        if not recipe.get('view_count'):
            recipe['view_count'] = 0
            self.stats.missing_fields_filled += 1

        if not recipe.get('favorite_count'):
            recipe['favorite_count'] = 0
            self.stats.missing_fields_filled += 1

        return recipe

    def clean_recipe(self, recipe: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        清洗单条菜谱记录

        Args:
            recipe: 原始菜谱数据

        Returns:
            清洗后的菜谱数据，如果数据无效则返回 None
        """
        # 检查重复
        if self._is_duplicate(recipe):
            self.stats.duplicates_removed += 1
            return None

        # 标准化文本字段
        recipe['name'] = self._normalize_text(recipe.get('name', ''))

        # 标准化菜系
        cuisine = recipe.get('cuisine_type', '')
        if cuisine and isinstance(cuisine, str):
            cuisine = cuisine.strip()
            # 如果菜系不在有效列表中，使用默认值
            if cuisine not in self.VALID_CUISINES:
                self.stats.warnings.append(f"菜系 '{cuisine}' 不在标准列表中")
                # 尝试模糊匹配
                for valid_cuisine in self.VALID_CUISINES:
                    if valid_cuisine in cuisine or cuisine in valid_cuisine:
                        cuisine = valid_cuisine
                        break
                else:
                    cuisine = '家常菜'
        recipe['cuisine_type'] = cuisine or '家常菜'

        # 标准化场景
        scene = recipe.get('scene_type', '')
        if scene and isinstance(scene, str):
            scene = scene.strip()
            if scene not in self.VALID_SCENES:
                scene = '晚餐'
        recipe['scene_type'] = scene or '晚餐'

        # 标准化难度
        recipe['difficulty'] = self._normalize_difficulty(recipe.get('difficulty'))

        # 标准化烹饪时间
        recipe['cooking_time'] = self._normalize_cooking_time(recipe.get('cooking_time'))

        # 标准化口味标签
        recipe['flavor_tags'] = self._normalize_flavor_tags(recipe.get('flavor_tags', []))

        # 标准化食材
        recipe['ingredients'] = self._normalize_ingredients(recipe.get('ingredients', []))
        if recipe['ingredients']:
            self.stats.ingredients_extracted += len(recipe['ingredients'])

        # 标准化步骤
        recipe['steps'] = self._normalize_steps(recipe.get('steps', []))

        # 标准化图片 URL
        recipe['image_url'] = self._normalize_image_url(recipe.get('image_url'))

        # 补全缺失字段
        recipe = self._fill_missing_fields(recipe)

        # 验证数据完整性
        is_valid, error_msg = self._validate_recipe(recipe)
        if not is_valid:
            self.stats.invalid_records_removed += 1
            self.stats.errors.append(f"无效记录: {recipe.get('name', '未知')} - {error_msg}")
            return None

        self.stats.formats_normalized += 1
        return recipe

    def clean_recipes(self, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量清洗菜谱数据

        Args:
            recipes: 原始菜谱数据列表

        Returns:
            清洗后的菜谱数据列表
        """
        self.stats.total_input = len(recipes)
        cleaned_recipes = []

        print(f"\n开始清洗 {self.stats.total_input} 条菜谱数据...")
        print("=" * 60)

        for i, recipe in enumerate(recipes, 1):
            print(f"[{i}/{self.stats.total_input}] 清洗: {recipe.get('name', '未知')}...")

            cleaned_recipe = self.clean_recipe(recipe)
            if cleaned_recipe:
                cleaned_recipes.append(cleaned_recipe)

        self.stats.total_output = len(cleaned_recipes)

        print("=" * 60)
        print(f"清洗完成！输入: {self.stats.total_input}, 输出: {self.stats.total_output}")

        return cleaned_recipes

    def print_report(self):
        """打印清洗报告"""
        print("\n" + "=" * 60)
        print("数据清洗报告")
        print("=" * 60)
        print(f"输入记录数:      {self.stats.total_input}")
        print(f"输出记录数:      {self.stats.total_output}")
        print(f"去除重复:        {self.stats.duplicates_removed}")
        print(f"补全缺失字段:    {self.stats.missing_fields_filled}")
        print(f"移除无效记录:    {self.stats.invalid_records_removed}")
        print(f"格式标准化:      {self.stats.formats_normalized}")
        print(f"提取食材数量:    {self.stats.ingredients_extracted}")
        print(f"警告数量:        {len(self.stats.warnings)}")
        print(f"错误数量:        {len(self.stats.errors)}")

        if self.stats.warnings:
            print("\n警告详情:")
            for warning in self.stats.warnings[:10]:  # 只显示前10条
                print(f"  - {warning}")
            if len(self.stats.warnings) > 10:
                print(f"  ... 还有 {len(self.stats.warnings) - 10} 条警告")

        if self.stats.errors:
            print("\n错误详情:")
            for error in self.stats.errors[:10]:  # 只显示前10条
                print(f"  - {error}")
            if len(self.stats.errors) > 10:
                print(f"  ... 还有 {len(self.stats.errors) - 10} 条错误")

        print("=" * 60)

    def get_report_dict(self) -> Dict[str, Any]:
        """获取清洗报告字典"""
        return {
            'input_count': self.stats.total_input,
            'output_count': self.stats.total_output,
            'duplicates_removed': self.stats.duplicates_removed,
            'missing_fields_filled': self.stats.missing_fields_filled,
            'invalid_records_removed': self.stats.invalid_records_removed,
            'formats_normalized': self.stats.formats_normalized,
            'ingredients_extracted': self.stats.ingredients_extracted,
            'warnings_count': len(self.stats.warnings),
            'errors_count': len(self.stats.errors),
            'warnings_sample': self.stats.warnings[:10],
            'errors_sample': self.stats.errors[:10],
        }


def load_input_file(input_path: str) -> List[Dict[str, Any]]:
    """
    加载输入文件

    Args:
        input_path: 输入文件路径

    Returns:
        菜谱数据列表
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 支持两种格式：直接是数组，或者包含 recipes 字段
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and 'recipes' in data:
        return data['recipes']
    else:
        raise ValueError("不支持的文件格式，需要 JSON 数组或包含 recipes 字段的对象")


def save_output_file(
    recipes: List[Dict[str, Any]],
    output_path: str,
    report: Dict[str, Any]
) -> None:
    """
    保存清洗后的数据

    Args:
        recipes: 清洗后的菜谱数据
        output_path: 输出文件路径
        report: 清洗报告
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        'metadata': {
            'total': len(recipes),
            'cleaned_at': datetime.now().isoformat(),
            'cleaning_report': report,
        },
        'recipes': recipes
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n清洗后的数据已保存到: {output_path}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='菜谱数据清洗脚本')
    parser.add_argument(
        'input',
        nargs='?',
        default='../output/test_recipes_simulated.json',
        help='输入文件路径（JSON 格式）'
    )
    parser.add_argument(
        'output',
        nargs='?',
        default='../output/cleaned_recipes.json',
        help='输出文件路径（JSON 格式）'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("菜谱数据清洗脚本")
    print("=" * 60)
    print(f"输入文件: {args.input}")
    print(f"输出文件: {args.output}")

    try:
        # 加载数据
        recipes = load_input_file(args.input)
        print(f"成功加载 {len(recipes)} 条记录")

        # 清洗数据
        cleaner = RecipeCleaner()
        cleaned_recipes = cleaner.clean_recipes(recipes)

        # 打印报告
        cleaner.print_report()

        # 保存结果
        report = cleaner.get_report_dict()
        save_output_file(cleaned_recipes, args.output, report)

        # 保存清洗报告
        report_path = Path(args.output).parent / 'cleaning_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"清洗报告已保存到: {report_path}")

        print("\n" + "=" * 60)
        print("清洗完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
