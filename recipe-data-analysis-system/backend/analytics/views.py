"""
Analytics 模块 - 视图层

本模块提供数据分析相关的 API 接口，包括：
- 菜系分布分析
- 难度等级统计
- 口味偏好分析
- 食材使用频率统计
- 管理员专用深度分析
"""
from django.db.models import Count, Avg, Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.response import ApiResponse
from utils.permissions import IsAdminUser
from recipes.models import Recipe
from recipes.models import RecipeIngredient
from ingredients.models import Ingredient


# 难度等级中文映射
DIFFICULTY_LABELS = {
    'easy': '简单',
    'medium': '中等',
    'hard': '困难',
}


class CuisineDistributionView(APIView):
    """
    菜系分布分析接口

    GET /api/analytics/cuisines

    统计各菜系的菜谱数量和占比，用于数据可视化展示

    返回数据格式：
    [
        {
            "name": "川菜",
            "count": 3500,
            "percentage": 17.5
        },
        ...
    ]
    """

    def get(self, request):
        """
        获取菜系分布统计数据

        Returns:
            Response: 菜系分布数据，包含名称、数量和占比
        """
        # 按菜系分组统计
        cuisine_stats = (
            Recipe.objects
            .values('cuisine_type')
            .annotate(count=Count('id'))
            .exclude(cuisine_type='')
            .order_by('-count')
        )

        # 计算总菜谱数
        total_count = sum(item['count'] for item in cuisine_stats)

        # 构建返回数据
        result = []
        for item in cuisine_stats:
            cuisine_name = item['cuisine_type'] or '未分类'
            count = item['count']
            percentage = round((count / total_count * 100), 2) if total_count > 0 else 0

            result.append({
                'name': cuisine_name,
                'count': count,
                'percentage': percentage
            })

        return ApiResponse.success(
            data=result,
            message='获取菜系分布数据成功'
        )


class DifficultyStatsView(APIView):
    """
    难度等级统计接口

    GET /api/analytics/difficulty

    统计各难度等级的菜谱数量和占比，用于数据可视化展示

    返回数据格式：
    [
        {
            "name": "简单",
            "value": "easy",
            "count": 5000,
            "percentage": 25.0,
            "avg_cooking_time": 20
        },
        ...
    ]
    """

    def get(self, request):
        """
        获取难度等级统计数据

        Returns:
            Response: 难度等级统计数据，包含名称、值、数量、占比和平均烹饪时长
        """
        # 按难度分组统计，并计算平均烹饪时长
        difficulty_stats = (
            Recipe.objects
            .values('difficulty')
            .annotate(
                count=Count('id'),
                avg_cooking_time=Avg('cooking_time')
            )
            .order_by('-count')
        )

        # 计算总菜谱数
        total_count = sum(item['count'] for item in difficulty_stats)

        # 构建返回数据
        result = []
        for item in difficulty_stats:
            difficulty_value = item['difficulty']
            difficulty_name = DIFFICULTY_LABELS.get(difficulty_value, difficulty_value)
            count = item['count']
            percentage = round((count / total_count * 100), 2) if total_count > 0 else 0
            avg_cooking_time = round(item['avg_cooking_time'], 1) if item['avg_cooking_time'] else 0

            result.append({
                'name': difficulty_name,
                'value': difficulty_value,
                'count': count,
                'percentage': percentage,
                'avg_cooking_time': avg_cooking_time
            })

        return ApiResponse.success(
            data=result,
            message='获取难度统计数据成功'
        )


class FlavorPreferenceView(APIView):
    """
    口味偏好分析接口

    GET /api/analytics/flavors

    统计各口味标签的菜谱数量，用于数据可视化展示

    返回数据格式：
    [
        {
            "name": "辣",
            "count": 8000,
            "percentage": 40.0
        },
        ...
    ]
    """

    def get(self, request):
        """
        获取口味偏好统计数据

        Returns:
            Response: 口味偏好统计数据，包含名称、数量和占比
        """
        # 获取所有有口味标签的菜谱
        recipes = Recipe.objects.exclude(flavor_tags='').exclude(flavor_tags__isnull=True)

        # 统计各口味标签的菜谱数量
        flavor_counts = {}
        total_tag_count = 0

        for recipe in recipes:
            flavor_list = recipe.get_flavor_list()
            for flavor in flavor_list:
                flavor_counts[flavor] = flavor_counts.get(flavor, 0) + 1
                total_tag_count += 1

        # 转换为列表并按数量降序排列
        result = []
        for flavor, count in sorted(flavor_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = round((count / total_tag_count * 100), 2) if total_tag_count > 0 else 0
            result.append({
                'name': flavor,
                'count': count,
                'percentage': percentage
            })

        return ApiResponse.success(
            data=result,
            message='获取口味偏好数据成功'
        )


class IngredientFrequencyView(APIView):
    """
    食材使用频率统计接口

    GET /api/analytics/ingredients

    统计各食材被使用的菜谱数量，用于数据可视化展示

    查询参数：
    - limit: 返回数量（可选，1-100，默认20）

    返回数据格式：
    [
        {
            "id": 1,
            "name": "鸡蛋",
            "count": 5000,
            "category": "other"
        },
        ...
    ]
    """

    def get(self, request):
        """
        获取食材使用频率统计数据

        Returns:
            Response: 食材使用频率统计数据，包含食材ID、名称、使用次数和分类
        """
        # 获取查询参数
        limit = request.query_params.get('limit', 20)

        # 参数验证
        try:
            limit = int(limit)
            if limit < 1:
                limit = 1
            elif limit > 100:
                limit = 100
        except (ValueError, TypeError):
            limit = 20

        # 统计各食材被使用的菜谱数量（通过 RecipeIngredient 关联表）
        ingredient_stats = (
            RecipeIngredient.objects
            .values('ingredient__id', 'ingredient__name', 'ingredient__category')
            .annotate(recipe_count=Count('recipe', distinct=True))
            .order_by('-recipe_count')[:limit]
        )

        # 构建返回数据
        result = []
        for item in ingredient_stats:
            result.append({
                'id': item['ingredient__id'],
                'name': item['ingredient__name'],
                'count': item['recipe_count'],
                'category': item['ingredient__category']
            })

        return ApiResponse.success(
            data=result,
            message=f'获取食材使用频率数据成功（Top {len(result)}）'
        )


# ==================== 管理员专用深度分析接口 ====================

class AdminCuisineAnalysisView(APIView):
    """
    管理员 - 菜系深度分析接口

    GET /api/admin/analytics/cuisines

    提供各菜系的详细分析数据，包括：
    - 各菜系数量和占比
    - 各菜系的平均点击量
    - 各菜系的平均收藏量
    - 各菜系的难度分布

    权限要求：仅管理员可访问

    返回数据格式：
    {
        "summary": {
            "total_recipes": 20000,
            "total_cuisines": 10
        },
        "cuisines": [
            {
                "name": "川菜",
                "count": 3500,
                "percentage": 17.5,
                "avg_view_count": 5200.5,
                "avg_favorite_count": 850.3,
                "avg_cooking_time": 35.2,
                "difficulty_distribution": {
                    "easy": 800,
                    "medium": 1800,
                    "hard": 900
                }
            },
            ...
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取菜系深度分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 菜系深度分析数据
        """
        # 按菜系分组统计基础数据
        cuisine_stats = (
            Recipe.objects
            .values('cuisine_type')
            .annotate(
                count=Count('id'),
                avg_view_count=Avg('view_count'),
                avg_favorite_count=Avg('favorite_count'),
                avg_cooking_time=Avg('cooking_time')
            )
            .exclude(cuisine_type='')
            .order_by('-count')
        )

        # 计算总菜谱数
        total_recipes = Recipe.objects.count()
        total_cuisines = cuisine_stats.count()

        # 构建返回数据
        cuisines = []
        for item in cuisine_stats:
            cuisine_name = item['cuisine_type'] or '未分类'
            count = item['count']
            percentage = round((count / total_recipes * 100), 2) if total_recipes > 0 else 0

            # 获取该菜系的难度分布
            difficulty_distribution = self._get_difficulty_distribution(cuisine_name)

            cuisines.append({
                'name': cuisine_name,
                'count': count,
                'percentage': percentage,
                'avg_view_count': round(item['avg_view_count'], 2) if item['avg_view_count'] else 0,
                'avg_favorite_count': round(item['avg_favorite_count'], 2) if item['avg_favorite_count'] else 0,
                'avg_cooking_time': round(item['avg_cooking_time'], 1) if item['avg_cooking_time'] else 0,
                'difficulty_distribution': difficulty_distribution
            })

        result = {
            'summary': {
                'total_recipes': total_recipes,
                'total_cuisines': total_cuisines
            },
            'cuisines': cuisines
        }

        return ApiResponse.success(
            data=result,
            message='获取菜系深度分析数据成功'
        )

    def _get_difficulty_distribution(self, cuisine_type):
        """
        获取指定菜系的难度分布

        Args:
            cuisine_type: 菜系类型

        Returns:
            dict: 难度分布数据
        """
        difficulty_stats = (
            Recipe.objects
            .filter(cuisine_type=cuisine_type)
            .values('difficulty')
            .annotate(count=Count('id'))
        )

        distribution = {
            'easy': 0,
            'medium': 0,
            'hard': 0
        }

        for item in difficulty_stats:
            difficulty = item['difficulty']
            if difficulty in distribution:
                distribution[difficulty] = item['count']

        return distribution


class AdminDifficultyAnalysisView(APIView):
    """
    管理员 - 难度深度分析接口

    GET /api/admin/analytics/difficulty

    提供各难度等级的详细分析数据，包括：
    - 各难度等级数量和占比
    - 各难度等级的平均烹饪时长
    - 各难度等级的平均点击量
    - 各难度等级的平均收藏量

    权限要求：仅管理员可访问

    返回数据格式：
    {
        "summary": {
            "total_recipes": 20000,
            "total_difficulty_levels": 3
        },
        "difficulties": [
            {
                "name": "简单",
                "value": "easy",
                "count": 5000,
                "percentage": 25.0,
                "avg_cooking_time": 20,
                "avg_view_count": 3200.5,
                "avg_favorite_count": 480.2
            },
            ...
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取难度深度分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 难度深度分析数据
        """
        # 按难度分组统计基础数据
        difficulty_stats = (
            Recipe.objects
            .values('difficulty')
            .annotate(
                count=Count('id'),
                avg_cooking_time=Avg('cooking_time'),
                avg_view_count=Avg('view_count'),
                avg_favorite_count=Avg('favorite_count')
            )
            .order_by('-count')
        )

        # 计算总菜谱数
        total_recipes = Recipe.objects.count()
        total_difficulty_levels = difficulty_stats.count()

        # 构建返回数据
        difficulties = []
        for item in difficulty_stats:
            difficulty_value = item['difficulty']
            difficulty_name = DIFFICULTY_LABELS.get(difficulty_value, difficulty_value)
            count = item['count']
            percentage = round((count / total_recipes * 100), 2) if total_recipes > 0 else 0

            difficulties.append({
                'name': difficulty_name,
                'value': difficulty_value,
                'count': count,
                'percentage': percentage,
                'avg_cooking_time': round(item['avg_cooking_time'], 1) if item['avg_cooking_time'] else 0,
                'avg_view_count': round(item['avg_view_count'], 2) if item['avg_view_count'] else 0,
                'avg_favorite_count': round(item['avg_favorite_count'], 2) if item['avg_favorite_count'] else 0,
            })

        result = {
            'summary': {
                'total_recipes': total_recipes,
                'total_difficulty_levels': total_difficulty_levels
            },
            'difficulties': difficulties
        }

        return ApiResponse.success(
            data=result,
            message='获取难度深度分析数据成功'
        )


class AdminHotRecipeAnalysisView(APIView):
    """
    管理员 - 热门菜谱分析接口

    GET /api/admin/analytics/hot

    提供热门菜谱的详细分析数据，包括：
    - Top 菜谱列表（可按点击量或收藏量排序）
    - 点击量趋势统计
    - 收藏量趋势统计
    - 收藏转化率分析（收藏量/点击量）

    权限要求：仅管理员可访问

    查询参数：
    - sort_by: 排序方式（view_count/favorite_count，默认 view_count）
    - limit: 返回数量（1-100，默认 50）

    返回数据格式：
    {
        "summary": {
            "total_recipes": 20000,
            "sort_by": "view_count",
            "limit": 50
        },
        "trends": {
            "avg_view_count": 25000.5,
            "avg_favorite_count": 3200.8,
            "avg_conversion_rate": 12.8
        },
        "recipes": [
            {
                "id": 1,
                "name": "宫保鸡丁",
                "cuisine_type": "川菜",
                "difficulty": "medium",
                "view_count": 50000,
                "favorite_count": 8000,
                "conversion_rate": 16.0
            },
            ...
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取热门菜谱分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 热门菜谱分析数据
        """
        # 获取查询参数
        sort_by = request.query_params.get('sort_by', 'view_count')
        limit = request.query_params.get('limit', 50)

        # 参数验证
        if sort_by not in ['view_count', 'favorite_count']:
            sort_by = 'view_count'

        try:
            limit = int(limit)
            if limit < 1:
                limit = 1
            elif limit > 100:
                limit = 100
        except (ValueError, TypeError):
            limit = 50

        # 获取总菜谱数
        total_recipes = Recipe.objects.count()

        # 按 sort_by 排序获取 Top 菜谱
        order_field = f'-{sort_by}'
        hot_recipes = Recipe.objects.order_by(order_field)[:limit]

        # 计算平均点击量、平均收藏量、平均转化率
        all_recipes = Recipe.objects.all()
        avg_view_count = all_recipes.aggregate(avg=Avg('view_count'))['avg'] or 0
        avg_favorite_count = all_recipes.aggregate(avg=Avg('favorite_count'))['avg'] or 0
        avg_conversion_rate = (avg_favorite_count / avg_view_count * 100) if avg_view_count > 0 else 0

        # 构建 Top 菜谱列表数据
        recipes = []
        for recipe in hot_recipes:
            view_count = recipe.view_count or 0
            favorite_count = recipe.favorite_count or 0
            conversion_rate = (favorite_count / view_count * 100) if view_count > 0 else 0

            recipes.append({
                'id': recipe.id,
                'name': recipe.name,
                'cuisine_type': recipe.cuisine_type or '未分类',
                'difficulty': recipe.difficulty or 'medium',
                'view_count': view_count,
                'favorite_count': favorite_count,
                'conversion_rate': round(conversion_rate, 2)
            })

        # 获取排序方式中文名
        sort_by_label = '点击量' if sort_by == 'view_count' else '收藏量'

        result = {
            'summary': {
                'total_recipes': total_recipes,
                'sort_by': sort_by,
                'sort_by_label': sort_by_label,
                'limit': limit
            },
            'trends': {
                'avg_view_count': round(avg_view_count, 2),
                'avg_favorite_count': round(avg_favorite_count, 2),
                'avg_conversion_rate': round(avg_conversion_rate, 2)
            },
            'recipes': recipes
        }

        return ApiResponse.success(
            data=result,
            message=f'获取热门菜谱分析数据成功（Top {len(recipes)}，按{sort_by_label}排序）'
        )


class AdminIngredientPairsAnalysisView(APIView):
    """
    管理员 - 食材关联分析接口

    GET /api/admin/analytics/ingredient-pairs

    分析食材共现频率，发现常见食材搭配组合。

    权限要求：仅管理员可访问

    查询参数：
    - limit: 返回数量（1-100，默认 50）
    - min_count: 最小共现次数（1-1000，默认 10）
    - category: 食材分类筛选（可选）

    返回数据格式：
    {
        "summary": {
            "total_recipes": 20000,
            "total_pairs": 1500,
            "min_count": 10,
            "limit": 50
        },
        "pairs": [
            {
                "ingredient_1": {
                    "id": 1,
                    "name": "鸡蛋"
                },
                "ingredient_2": {
                    "id": 2,
                    "name": "番茄"
                },
                "count": 1500,
                "percentage": 7.5
            },
            ...
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取食材关联分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 食材关联分析数据
        """
        # 获取查询参数
        limit = request.query_params.get('limit', 50)
        min_count = request.query_params.get('min_count', 10)
        category = request.query_params.get('category', None)

        # 参数验证
        try:
            limit = int(limit)
            if limit < 1:
                limit = 1
            elif limit > 100:
                limit = 100
        except (ValueError, TypeError):
            limit = 50

        try:
            min_count = int(min_count)
            if min_count < 1:
                min_count = 1
            elif min_count > 1000:
                min_count = 1000
        except (ValueError, TypeError):
            min_count = 10

        # 获取总菜谱数
        total_recipes = Recipe.objects.count()

        # 获取所有菜谱的食材组合
        from collections import defaultdict

        pair_counts = defaultdict(int)
        ingredient_names = {}
        ingredient_categories = {}

        # 构建食材到菜谱的映射
        recipe_ingredients = defaultdict(list)
        for ri in RecipeIngredient.objects.select_related('recipe', 'ingredient').all():
            recipe_id = ri.recipe_id
            ingredient_id = ri.ingredient_id
            recipe_ingredients[recipe_id].append(ingredient_id)
            ingredient_names[ingredient_id] = ri.ingredient.name
            ingredient_categories[ingredient_id] = ri.ingredient.category

        # 统计食材配对出现次数
        for recipe_id, ingredient_list in recipe_ingredients.items():
            # 按ID排序，确保 (A, B) 和 (B, A) 被视为同一对
            sorted_ingredients = sorted(ingredient_list)
            # 生成所有可能的配对
            for i in range(len(sorted_ingredients)):
                for j in range(i + 1, len(sorted_ingredients)):
                    pair = (sorted_ingredients[i], sorted_ingredients[j])
                    pair_counts[pair] += 1

        # 应用分类筛选
        if category:
            pair_counts = {
                pair: count for pair, count in pair_counts.items()
                if ingredient_categories.get(pair[0]) == category and
                   ingredient_categories.get(pair[1]) == category
            }

        # 应用最小共现次数筛选
        pair_counts = {
            pair: count for pair, count in pair_counts.items()
            if count >= min_count
        }

        # 按共现次数降序排列
        sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

        # 构建返回数据
        pairs = []
        for (ing_id_1, ing_id_2), count in sorted_pairs:
            percentage = round((count / total_recipes * 100), 2) if total_recipes > 0 else 0
            pairs.append({
                'ingredient_1': {
                    'id': ing_id_1,
                    'name': ingredient_names.get(ing_id_1, f'食材{ing_id_1}'),
                    'category': ingredient_categories.get(ing_id_1, 'other')
                },
                'ingredient_2': {
                    'id': ing_id_2,
                    'name': ingredient_names.get(ing_id_2, f'食材{ing_id_2}'),
                    'category': ingredient_categories.get(ing_id_2, 'other')
                },
                'count': count,
                'percentage': percentage
            })

        result = {
            'summary': {
                'total_recipes': total_recipes,
                'total_pairs': len(pair_counts),
                'min_count': min_count,
                'limit': limit,
                'category_filter': category or '全部'
            },
            'pairs': pairs
        }

        return ApiResponse.success(
            data=result,
            message=f'获取食材关联分析数据成功（Top {len(pairs)}，最小共现次数≥{min_count}）'
        )
