# -*- coding: utf-8 -*-
"""
大数据集清洗脚本 - 流式处理 1.8G JSON 文件

功能：
1. 流式读取大 JSON 文件，避免内存溢出
2. 逐条清洗验证，只保留完整数据
3. 达到目标数量（默认 20,000 条）后停止
4. 生成详细清洗报告
"""

import os
import sys
import json
import hashlib
import gc
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

# Windows 控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 尝试导入 ijson，如果没有则使用备用方案
try:
    import ijson
    HAS_IJSON = True
except ImportError:
    HAS_IJSON = False
    print("警告: 未安装 ijson 库，将使用备用方案（可能较慢）")
    print("建议安装: pip install ijson")


@dataclass
class CleaningStats:
    """清洗统计数据"""
    total_input: int = 0
    total_output: int = 0
    target_count: int = 20000
    duplicates_removed: int = 0
    missing_fields_filled: int = 0
    invalid_records_removed: int = 0
    formats_normalized: int = 0
    ingredients_extracted: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    field_missing_stats: Dict[str, int] = field(default_factory=lambda: defaultdict(int))


class LargeDatasetCleaner:
    """大数据集清洗器 - 流式处理"""

    # 有效的难度等级
    VALID_DIFFICULTIES = {'easy', 'medium', 'hard'}

    # 难度中文映射
    DIFFICULTY_MAP = {
        '简单': 'easy', '初级': 'easy', '容易': 'easy', '1': 'easy',
        '中等': 'medium', '中级': 'medium', '普通': 'medium', '2': 'medium',
        '困难': 'hard', '高级': 'hard', '复杂': 'hard', '3': 'hard',
    }

    # 菜系列表
    VALID_CUISINES = {
        '川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '湘菜', '徽菜', '闽菜', '家常菜'
    }

    # 场景列表
    VALID_SCENES = {
        '早餐', '午餐', '晚餐', '下午茶', '夜宵', '快手菜', '宴客菜'
    }

    # 口味标签
    VALID_FLAVORS = {'辣', '甜', '酸', '咸', '鲜', '清淡', '麻'}

    # 数据库必需字段
    REQUIRED_FIELDS = {
        'name': '菜谱名称',
        'ingredients': '食材列表',
        'steps': '制作步骤',
    }

    def __init__(self, target_count: int = 20000, batch_size: int = 1000):
        """
        初始化清洗器

        Args:
            target_count: 目标数据条数
            batch_size: 批量保存的批次大小
        """
        self.target_count = target_count
        self.batch_size = batch_size
        self.stats = CleaningStats(target_count=target_count)
        self.seen_names: Set[str] = set()
        self.seen_ids: Set[int] = set()
        self.cleaned_recipes: List[Dict[str, Any]] = []

    def _normalize_text(self, text: Any) -> str:
        """标准化文本"""
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        return text.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    def _normalize_difficulty(self, difficulty: Any) -> str:
        """标准化难度等级"""
        if not difficulty:
            return 'medium'

        difficulty_str = str(difficulty).strip()

        if difficulty_str in self.VALID_DIFFICULTIES:
            return difficulty_str

        for key, value in self.DIFFICULTY_MAP.items():
            if key in difficulty_str:
                return value

        return 'medium'

    def _normalize_cooking_time(self, cooking_time: Any) -> int:
        """标准化烹饪时间"""
        if cooking_time is None:
            return 30

        if isinstance(cooking_time, (int, float)):
            return max(1, int(cooking_time))

        if isinstance(cooking_time, str):
            import re
            match = re.search(r'(\d+)', cooking_time)
            if match:
                return max(1, int(match.group(1)))

        return 30

    def _normalize_ingredients(self, ingredients: Any) -> List[Dict[str, str]]:
        """标准化食材列表"""
        if not ingredients:
            return []

        normalized = []

        if isinstance(ingredients, list):
            for item in ingredients:
                if isinstance(item, dict):
                    name = self._normalize_text(item.get('name', ''))
                    amount = self._normalize_text(item.get('amount', '适量'))

                    if name:
                        normalized.append({'name': name, 'amount': amount})
                elif isinstance(item, str):
                    name = self._normalize_text(item)
                    if name:
                        normalized.append({'name': name, 'amount': '适量'})

        elif isinstance(ingredients, str):
            # 尝试解析字符串格式
            lines = ingredients.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(maxsplit=1)
                    name = parts[0] if parts else ''
                    amount = parts[1] if len(parts) > 1 else '适量'
                    if name:
                        normalized.append({'name': name, 'amount': amount})

        return normalized

    def _extract_ingredients_from_recipe(self, recipe: Dict[str, Any]) -> List[Dict[str, str]]:
        """从菜谱数据中提取食材（支持多种字段名）"""
        # 尝试多种可能的字段名
        ingredients = recipe.get('ingredients') or recipe.get('recipeIngredient') or recipe.get('recipe_ingredients') or []
        return self._normalize_ingredients(ingredients)

    def _extract_steps_from_recipe(self, recipe: Dict[str, Any]) -> List[str]:
        """从菜谱数据中提取步骤（支持多种字段名）"""
        # 尝试多种可能的字段名
        steps = recipe.get('steps') or recipe.get('recipeInstructions') or recipe.get('recipe_instructions') or recipe.get('instructions') or []
        return self._normalize_steps(steps)

    def _normalize_steps(self, steps: Any) -> List[str]:
        """标准化制作步骤"""
        if not steps:
            return []

        normalized = []

        if isinstance(steps, list):
            for step in steps:
                step_text = self._normalize_text(step)
                if step_text:
                    if not step_text[0].isdigit():
                        step_text = f"{len(normalized) + 1}. {step_text}"
                    normalized.append(step_text)

        elif isinstance(steps, str):
            lines = steps.split('\n')
            for i, line in enumerate(lines, 1):
                step_text = line.strip()
                if step_text:
                    normalized.append(step_text)

        return normalized

    def _normalize_image_url(self, image_url: Any) -> str:
        """标准化图片 URL"""
        if not image_url:
            return ""

        url = str(image_url).strip()

        if url.startswith('http://') or url.startswith('https://'):
            return url

        return ""

    def _generate_name_hash(self, name: str) -> str:
        """生成菜谱名称哈希值"""
        return hashlib.md5(name.encode('utf-8')).hexdigest()

    def _is_duplicate(self, recipe: Dict[str, Any]) -> bool:
        """检查是否是重复记录"""
        recipe_id = recipe.get('id') or recipe.get('recipe_id')
        if recipe_id and recipe_id in self.seen_ids:
            return True

        name = recipe.get('name', '')
        if name:
            name_hash = self._generate_name_hash(name)
            if name_hash in self.seen_names:
                return True
            self.seen_names.add(name_hash)

        if recipe_id:
            self.seen_ids.add(recipe_id)

        return False

    def _validate_recipe(self, recipe: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        验证菜谱数据的完整性

        数据库必需字段：
        - name: 菜谱名称
        - ingredients: 食材列表（至少 1 条）
        - steps: 制作步骤（至少 1 步）
        """
        # 检查菜谱名称
        if not recipe.get('name'):
            self.stats.field_missing_stats['name'] += 1
            return False, "缺少菜谱名称"

        # 检查食材（支持多种字段名）
        ingredients = self._extract_ingredients_from_recipe(recipe)
        if not ingredients or len(ingredients) == 0:
            self.stats.field_missing_stats['ingredients'] += 1
            return False, "缺少食材信息"

        # 检查步骤（支持多种字段名）
        steps = self._extract_steps_from_recipe(recipe)
        if not steps or len(steps) == 0:
            self.stats.field_missing_stats['steps'] += 1
            return False, "缺少制作步骤"

        return True, None

    def _fill_missing_fields(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """补全缺失字段"""
        if not recipe.get('cuisine_type'):
            recipe['cuisine_type'] = '家常菜'
            self.stats.missing_fields_filled += 1

        if not recipe.get('scene_type'):
            recipe['scene_type'] = '晚餐'
            self.stats.missing_fields_filled += 1

        if not recipe.get('difficulty'):
            recipe['difficulty'] = 'medium'
            self.stats.missing_fields_filled += 1

        if not recipe.get('cooking_time'):
            recipe['cooking_time'] = 30
            self.stats.missing_fields_filled += 1

        if not recipe.get('view_count'):
            recipe['view_count'] = 0

        if not recipe.get('favorite_count'):
            recipe['favorite_count'] = 0

        return recipe

    def clean_recipe(self, recipe: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """清洗单条菜谱记录"""
        self.stats.total_input += 1

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
            if cuisine not in self.VALID_CUISINES:
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

        # 标准化食材（支持多种字段名）
        recipe['ingredients'] = self._extract_ingredients_from_recipe(recipe)

        # 标准化步骤（支持多种字段名）
        recipe['steps'] = self._extract_steps_from_recipe(recipe)

        # 标准化图片 URL
        recipe['image_url'] = self._normalize_image_url(recipe.get('image_url') or recipe.get('img'))

        # 补全缺失字段
        recipe = self._fill_missing_fields(recipe)

        # 验证数据完整性
        is_valid, error_msg = self._validate_recipe(recipe)
        if not is_valid:
            self.stats.invalid_records_removed += 1
            if self.stats.total_input % 1000 == 0:
                self.stats.errors.append(f"记录 #{self.stats.total_input}: {error_msg}")
            return None

        self.stats.formats_normalized += 1
        self.stats.ingredients_extracted += len(recipe.get('ingredients', []))

        return recipe

    def process_json_lines(self, input_path: str) -> List[Dict[str, Any]]:
        """处理 JSON Lines 格式文件（每行一个 JSON 对象）"""
        print(f"使用 JSON Lines 方式读取文件: {input_path}")

        line_count = 0
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if len(self.cleaned_recipes) >= self.target_count:
                    print(f"\n已达到目标数量 {self.target_count}，停止处理")
                    break

                line_count += 1
                line = line.strip()
                if not line:
                    continue

                try:
                    recipe = json.loads(line)
                    cleaned = self.clean_recipe(recipe)
                    if cleaned:
                        self.cleaned_recipes.append(cleaned)
                        self.stats.total_output = len(self.cleaned_recipes)

                        # 显示进度
                        if self.stats.total_output % 100 == 0:
                            success_rate = self.stats.total_output / self.stats.total_input * 100
                            print(f"已清洗: {self.stats.total_output}/{self.target_count} | "
                                  f"已处理: {self.stats.total_input} 行 | "
                                  f"有效率: {success_rate:.1f}%")

                except json.JSONDecodeError as e:
                    self.stats.errors.append(f"第 {line_count} 行 JSON 解析错误: {str(e)[:100]}")
                    continue
                except Exception as e:
                    self.stats.errors.append(f"第 {line_count} 行处理错误: {str(e)[:100]}")
                    continue

        return self.cleaned_recipes

    def process_with_ijson(self, input_path: str) -> List[Dict[str, Any]]:
        """使用 ijson 流式处理标准 JSON 数组文件"""
        print(f"使用 ijson 流式读取文件: {input_path}")

        with open(input_path, 'rb') as f:
            # 尝试不同的解析方式
            try:
                # 方式1: 直接解析数组
                recipes = ijson.items(f, 'item')
                for recipe in recipes:
                    if len(self.cleaned_recipes) >= self.target_count:
                        print(f"\n已达到目标数量 {self.target_count}，停止处理")
                        break

                    cleaned = self.clean_recipe(recipe)
                    if cleaned:
                        self.cleaned_recipes.append(cleaned)
                        self.stats.total_output = len(self.cleaned_recipes)

                        # 显示进度
                        if self.stats.total_output % 100 == 0:
                            success_rate = self.stats.total_output / self.stats.total_input * 100 if self.stats.total_input > 0 else 0
                            print(f"已清洗: {self.stats.total_output}/{self.target_count} | "
                                  f"已处理: {self.stats.total_input} | "
                                  f"有效率: {success_rate:.1f}%")

            except Exception as e:
                # 方式2: 尝试解析包含 recipes 字段的对象
                f.seek(0)
                try:
                    recipes = ijson.items(f, 'recipes.item')
                    for recipe in recipes:
                        if len(self.cleaned_recipes) >= self.target_count:
                            break

                        cleaned = self.clean_recipe(recipe)
                        if cleaned:
                            self.cleaned_recipes.append(cleaned)
                            self.stats.total_output = len(self.cleaned_recipes)

                            if self.stats.total_output % 100 == 0:
                                print(f"已清洗: {self.stats.total_output}/{self.target_count} | "
                                      f"已处理: {self.stats.total_input}")
                except Exception as e2:
                    print(f"ijson 解析失败: {e2}")
                    print("尝试使用 JSON Lines 方式...")
                    return self.process_json_lines(input_path)

        return self.cleaned_recipes

    def clean_dataset(self, input_path: str) -> List[Dict[str, Any]]:
        """
        清洗数据集

        Args:
            input_path: 输入文件路径

        Returns:
            清洗后的菜谱数据列表
        """
        print("=" * 60)
        print("大数据集清洗脚本")
        print("=" * 60)
        print(f"输入文件: {input_path}")
        print(f"目标数量: {self.target_count}")
        print(f"批次大小: {self.batch_size}")
        print("=" * 60)

        # 检测文件格式并选择处理方式
        print("\n检测文件格式...")
        file_type = self._detect_file_format(input_path)
        print(f"检测到格式: {file_type}")

        if file_type == "json_lines":
            self.process_json_lines(input_path)
        elif file_type == "json_array" and HAS_IJSON:
            self.process_with_ijson(input_path)
        else:
            print("\n无法使用 ijson，尝试使用 JSON Lines 方式...")
            self.process_json_lines(input_path)

        print("\n" + "=" * 60)
        print(f"清洗完成！")
        print(f"输入记录数:      {self.stats.total_input}")
        print(f"输出记录数:      {self.stats.total_output}")
        print(f"去除重复:        {self.stats.duplicates_removed}")
        print(f"移除无效记录:    {self.stats.invalid_records_removed}")
        if self.stats.total_input > 0:
            print(f"有效率:          {self.stats.total_output/self.stats.total_input*100:.2f}%")
        print("=" * 60)

        return self.cleaned_recipes

    def _detect_file_format(self, input_path: str) -> str:
        """
        检测文件格式

        Returns:
            'json_lines' 或 'json_array'
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            first_char = f.read(1).strip()
            if first_char == '[':
                return "json_array"
            else:
                return "json_lines"

    def print_report(self):
        """打印清洗报告"""
        print("\n" + "=" * 60)
        print("数据清洗报告")
        print("=" * 60)
        print(f"目标数量:        {self.stats.target_count}")
        print(f"输入记录数:      {self.stats.total_input}")
        print(f"输出记录数:      {self.stats.total_output}")
        print(f"去除重复:        {self.stats.duplicates_removed}")
        print(f"补全缺失字段:    {self.stats.missing_fields_filled}")
        print(f"移除无效记录:    {self.stats.invalid_records_removed}")
        print(f"格式标准化:      {self.stats.formats_normalized}")
        print(f"提取食材数量:    {self.stats.ingredients_extracted}")
        print(f"警告数量:        {len(self.stats.warnings)}")
        print(f"错误数量:        {len(self.stats.errors)}")

        if self.stats.field_missing_stats:
            print("\n缺失字段统计:")
            for field, count in self.stats.field_missing_stats.items():
                print(f"  - {field}: {count} 条")

        print("=" * 60)

    def save_output(self, output_path: str):
        """保存清洗后的数据"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        output_data = {
            'metadata': {
                'total': len(self.cleaned_recipes),
                'cleaned_at': datetime.now().isoformat(),
                'target_count': self.target_count,
                'success_rate': f"{len(self.cleaned_recipes)/self.stats.total_input*100:.2f}%",
            },
            'recipes': self.cleaned_recipes
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\n清洗后的数据已保存到: {output_path}")

    def get_report_dict(self) -> Dict[str, Any]:
        """获取清洗报告字典"""
        return {
            'target_count': self.stats.target_count,
            'input_count': self.stats.total_input,
            'output_count': self.stats.total_output,
            'duplicates_removed': self.stats.duplicates_removed,
            'missing_fields_filled': self.stats.missing_fields_filled,
            'invalid_records_removed': self.stats.invalid_records_removed,
            'formats_normalized': self.stats.formats_normalized,
            'ingredients_extracted': self.stats.ingredients_extracted,
            'warnings_count': len(self.stats.warnings),
            'errors_count': len(self.stats.errors),
            'field_missing_stats': dict(self.stats.field_missing_stats),
            'success_rate': f"{self.stats.total_output/self.stats.total_input*100:.2f}%" if self.stats.total_input > 0 else "0%",
        }


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='大数据集清洗脚本 - 流式处理大 JSON 文件')
    parser.add_argument(
        'input',
        nargs='?',
        default='../dataset/recipe_corpus_full.json',
        help='输入文件路径（JSON 格式）'
    )
    parser.add_argument(
        'output',
        nargs='?',
        default='../output/cleaned_20k_recipes.json',
        help='输出文件路径（JSON 格式）'
    )
    parser.add_argument(
        '--target', '-t',
        type=int,
        default=20000,
        help='目标数据条数（默认: 20000）'
    )
    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=1000,
        help='批量保存的批次大小（默认: 1000）'
    )

    args = parser.parse_args()

    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {args.input}")
        print("\n提示: 请将数据集放在 data-scripts/dataset/ 目录下")
        sys.exit(1)

    try:
        # 清洗数据
        cleaner = LargeDatasetCleaner(target_count=args.target, batch_size=args.batch_size)
        cleaner.clean_dataset(str(input_path))

        # 打印报告
        cleaner.print_report()

        # 保存结果
        cleaner.save_output(args.output)

        # 保存清洗报告
        report_path = Path(args.output).parent / 'cleaning_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(cleaner.get_report_dict(), f, ensure_ascii=False, indent=2)
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
