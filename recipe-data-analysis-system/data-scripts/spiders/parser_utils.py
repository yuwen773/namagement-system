# -*- coding: utf-8 -*-
"""
HTML解析工具模块

功能：
- 解析菜谱详情页
- 提取菜谱名称、食材、步骤、图片等
- 数据清洗和格式化
"""

import re
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup


class RecipeParser:
    """菜谱解析器"""

    # 难度关键词映射
    DIFFICULTY_KEYWORDS = {
        'easy': ['简单', '易做', '快手', '零失败', '新手', '入门'],
        'medium': ['普通', '一般', '适中', '家常'],
        'hard': ['困难', '复杂', '考验', '高级', '工艺']
    }

    # 菜系关键词
    CUISINE_KEYWORDS = {
        '川菜': ['川', '四川', '麻辣', '辣子'],
        '粤菜': ['粤', '广东', '广式', '港式'],
        '鲁菜': ['鲁', '山东'],
        '苏菜': ['苏', '江苏', '江南'],
        '浙菜': ['浙', '浙江'],
        '湘菜': ['湘', '湖南'],
        '徽菜': ['徽', '安徽'],
        '闽菜': ['闽', '福建'],
    }

    # 口味关键词
    FLAVOR_KEYWORDS = {
        '辣': ['辣', '麻辣', '香辣', '酸辣'],
        '甜': ['甜', '蜜汁', '糖醋'],
        '酸': ['酸', '糖醋', '酸辣'],
        '咸': ['咸', '酱香'],
        '鲜': ['鲜', '鲜美'],
        '清淡': ['清淡', '少油'],
        '麻': ['麻', '麻辣'],
    }

    @staticmethod
    def parse_recipe_detail(html: str) -> Dict[str, Any]:
        """
        解析菜谱详情页

        Args:
            html: HTML 内容

        Returns:
            解析后的菜谱数据字典
        """
        soup = BeautifulSoup(html, 'lxml')

        recipe_data = {
            'name': RecipeParser._parse_name(soup),
            'image_url': RecipeParser._parse_image_url(soup),
            'ingredients': RecipeParser._parse_ingredients(soup),
            'steps': RecipeParser._parse_steps(soup),
            'tips': RecipeParser._parse_tips(soup),
            'cooking_time': None,
            'difficulty': RecipeParser._analyze_difficulty(soup),
            'cuisine_type': None,
            'flavor_tags': [],
            'scene_type': '晚餐',  # 默认场景
        }

        # 根据名称分析菜系
        recipe_data['cuisine_type'] = RecipeParser._analyze_cuisine(
            recipe_data['name']
        )

        # 分析口味标签
        recipe_data['flavor_tags'] = RecipeParser._analyze_flavors(
            soup, recipe_data['name']
        )

        # 估算烹饪时间（基于步骤数量）
        recipe_data['cooking_time'] = RecipeParser._estimate_cooking_time(
            recipe_data['steps']
        )

        return recipe_data

    @staticmethod
    def _parse_name(soup: BeautifulSoup) -> Optional[str]:
        """解析菜谱名称"""
        try:
            # 尝试多种选择器
            selectors = [
                'h1.page-title',
                'h1.recipe-title',
                '.recipe-title h1',
                'h1',
            ]

            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    name = elem.get_text(strip=True)
                    if name:
                        return name
        except Exception as e:
            print(f"解析菜谱名称失败: {e}")

        return None

    @staticmethod
    def _parse_image_url(soup: BeautifulSoup) -> Optional[str]:
        """解析成品图片 URL"""
        try:
            # 尝试多种选择器
            selectors = [
                '.recipe-cover img',
                '.recipe-image img',
                'img.recipe-cover',
                '.detail-cover img',
            ]

            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    url = elem.get('src') or elem.get('data-src')
                    if url:
                        # 处理相对 URL
                        if url.startswith('//'):
                            return 'https:' + url
                        elif url.startswith('/'):
                            return 'https://www.xiachufang.com' + url
                        return url
        except Exception as e:
            print(f"解析图片 URL 失败: {e}")

        return None

    @staticmethod
    def _parse_ingredients(soup: BeautifulSoup) -> List[Dict[str, str]]:
        """解析食材列表"""
        ingredients = []

        try:
            # 尝试多种选择器
            selectors = [
                '.recipe-ingredients .ingredient',
                '.ingredients li',
                '.recipe-ingredient-item',
                '.ingredient-item',
            ]

            for selector in selectors:
                elems = soup.select(selector)
                if elems:
                    for elem in elems:
                        text = elem.get_text(strip=True)
                        if text:
                            # 解析食材和用量
                            ingredient = RecipeParser._parse_ingredient_text(text)
                            if ingredient:
                                ingredients.append(ingredient)
                    if ingredients:  # 如果找到食材，就不再尝试其他选择器
                        break

        except Exception as e:
            print(f"解析食材列表失败: {e}")

        return ingredients

    @staticmethod
    def _parse_ingredient_text(text: str) -> Optional[Dict[str, str]]:
        """
        解析单条食材文本

        Args:
            text: 食材文本，如 "猪肉 500g" 或 "鸡蛋：2个"

        Returns:
            {'name': '猪肉', 'amount': '500g'}
        """
        if not text:
            return None

        # 常见分隔符
        separators = [' ', '\t', '：', ':']

        for sep in separators:
            if sep in text:
                parts = text.split(sep, 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    amount = parts[1].strip()
                    if name and amount:
                        return {'name': name, 'amount': amount}

        # 如果没有分隔符，整个作为名称
        return {'name': text.strip(), 'amount': ''}

    @staticmethod
    def _parse_steps(soup: BeautifulSoup) -> List[str]:
        """解析制作步骤"""
        steps = []

        try:
            # 尝试多种选择器
            selectors = [
                '.recipe-steps .step',
                '.steps li',
                '.recipe-step-item',
                '.step-item',
                '.recipe-steps p',
            ]

            for selector in selectors:
                elems = soup.select(selector)
                if elems:
                    for elem in elems:
                        text = elem.get_text(strip=True)
                        # 去除序号
                        text = re.sub(r'^\d+[\.\、]\s*', '', text)
                        if text:
                            steps.append(text)
                    if steps:  # 如果找到步骤，就不再尝试其他选择器
                        break

        except Exception as e:
            print(f"解析制作步骤失败: {e}")

        return steps

    @staticmethod
    def _parse_tips(soup: BeautifulSoup) -> Optional[str]:
        """解析小贴士"""
        try:
            selectors = [
                '.recipe-tip',
                '.tip-content',
                '.tips',
            ]

            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    if text:
                        return text
        except Exception as e:
            print(f"解析小贴士失败: {e}")

        return None

    @staticmethod
    def _analyze_difficulty(soup: BeautifulSoup) -> str:
        """
        分析难度等级

        根据步骤数量、食材数量等判断
        """
        try:
            # 尝试从页面直接获取
            difficulty_elem = soup.select_one('.difficulty, .recipe-difficulty')
            if difficulty_elem:
                text = difficulty_elem.get_text(strip=True)
                for level, keywords in RecipeParser.DIFFICULTY_KEYWORDS.items():
                    if any(kw in text for kw in keywords):
                        return level

            # 根据步骤和食材数量估算
            steps_count = len(soup.select('.recipe-steps .step, .steps li'))
            ingredients_count = len(soup.select('.recipe-ingredients .ingredient, .ingredients li'))

            if steps_count <= 3 and ingredients_count <= 5:
                return 'easy'
            elif steps_count <= 8 and ingredients_count <= 12:
                return 'medium'
            else:
                return 'hard'

        except Exception:
            return 'medium'  # 默认中等

    @staticmethod
    def _analyze_cuisine(recipe_name: str) -> Optional[str]:
        """
        根据菜谱名称分析菜系
        """
        if not recipe_name:
            return '家常菜'  # 默认

        for cuisine, keywords in RecipeParser.CUISINE_KEYWORDS.items():
            if any(kw in recipe_name for kw in keywords):
                return cuisine

        return '家常菜'  # 默认

    @staticmethod
    def _analyze_flavors(soup: BeautifulSoup, recipe_name: Optional[str]) -> List[str]:
        """
        分析口味标签

        从页面和菜谱名称中提取口味信息
        """
        flavors = set()

        # 从菜谱名称分析（需要检查 recipe_name 是否为 None）
        if recipe_name:
            for flavor, keywords in RecipeParser.FLAVOR_KEYWORDS.items():
                if any(kw in recipe_name for kw in keywords):
                    flavors.add(flavor)

        # 尝试从页面获取口味标签
        try:
            flavor_elems = soup.select('.flavor-tag, .recipe-flavor, .tag')
            for elem in flavor_elems:
                text = elem.get_text(strip=True)
                for flavor, keywords in RecipeParser.FLAVOR_KEYWORDS.items():
                    if any(kw in text for kw in keywords):
                        flavors.add(flavor)
        except Exception:
            pass

        return list(flavors) if flavors else []

    @staticmethod
    def _estimate_cooking_time(steps: List[str]) -> Optional[int]:
        """
        估算烹饪时间（分钟）

        基于步骤数量
        """
        if not steps:
            return None

        # 每步约 5-10 分钟
        step_count = len(steps)
        if step_count <= 3:
            return 15
        elif step_count <= 5:
            return 30
        elif step_count <= 8:
            return 45
        else:
            return 60

    @staticmethod
    def parse_recipe_list(html: str) -> List[str]:
        """
        解析菜谱列表页，提取详情页链接

        Args:
            html: HTML 内容

        Returns:
            菜谱详情页 URL 列表
        """
        urls = []

        try:
            soup = BeautifulSoup(html, 'lxml')

            # 尝试多种选择器
            selectors = [
                'a.recipe-card',
                '.recipe-list a',
                '.recipe-item a',
                'a[href*="/recipe/"]',
            ]

            for selector in selectors:
                elems = soup.select(selector)
                if elems:
                    for elem in elems:
                        href = elem.get('href')
                        if href and '/recipe/' in href:
                            # 处理相对 URL
                            if href.startswith('/'):
                                href = 'https://www.xiachufang.com' + href
                            elif href.startswith('//'):
                                href = 'https:' + href

                            if href not in urls:
                                urls.append(href)
                    if urls:  # 如果找到链接，就不再尝试其他选择器
                        break

        except Exception as e:
            print(f"解析菜谱列表失败: {e}")

        return urls


def parse_recipe_detail(html: str) -> Dict[str, Any]:
    """便捷函数：解析菜谱详情"""
    return RecipeParser.parse_recipe_detail(html)


def parse_recipe_list(html: str) -> List[str]:
    """便捷函数：解析菜谱列表"""
    return RecipeParser.parse_recipe_list(html)
