"""
Analytics 模块 - 视图层

本模块提供数据分析相关的 API 接口，包括：
- 菜系分布分析
- 难度等级统计
- 口味偏好分析
- 食材使用频率统计
- 管理员专用深度分析
- 用户行为分析
"""
from django.db.models import Count, Avg, Q, F, Sum
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.response import ApiResponse
from utils.permissions import IsAdminUser
from recipes.models import Recipe
from recipes.models import RecipeIngredient
from ingredients.models import Ingredient
from behavior_logs.models import UserBehaviorLog
from utils.constants import BehaviorType


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


# ==================== 用户行为分析接口 ====================

class ClickStreamAnalysisView(APIView):
    """
    管理员 - 点击流分析接口

    GET /api/admin/analytics/clickstream

    分析用户访问路径和点击流模式，包括：
    - 用户访问路径统计
    - 常见路径模式
    - 转化率分析（浏览到收藏）
    - 页面跳转漏斗分析

    权限要求：仅管理员可访问

    查询参数：
    - days: 分析时间范围天数（1-90，默认 30）
    - limit_path: 返回路径数量（1-50，默认 20）

    返回数据格式：
    {
        "summary": {
            "total_logs": 10000,
            "days": 30,
            "unique_users": 500
        },
        "path_patterns": [
            {
                "path": "首页 -> 菜谱列表 -> 菜谱详情",
                "count": 1500,
                "percentage": 15.0,
                "conversion_rate": 12.5
            }
        ],
        "conversion_funnel": {
            "login": 1000,
            "view_recipe": 2500,
            "collect": 500,
            "conversion_rate": 20.0
        },
        "behavior_distribution": {
            "login": 500,
            "search": 800,
            "view": 3000,
            "collect": 600
        }
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取点击流分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 点击流分析数据
        """
        # 获取查询参数
        days = request.query_params.get('days', 30)
        limit_path = request.query_params.get('limit_path', 20)

        # 参数验证
        try:
            days = int(days)
            if days < 1:
                days = 1
            elif days > 90:
                days = 90
        except (ValueError, TypeError):
            days = 30

        try:
            limit_path = int(limit_path)
            if limit_path < 1:
                limit_path = 1
            elif limit_path > 50:
                limit_path = 50
        except (ValueError, TypeError):
            limit_path = 20

        # 计算时间范围
        end_time = timezone.now()
        start_time = end_time - timedelta(days=days)

        # 获取时间范围内的行为日志
        behavior_logs = UserBehaviorLog.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time
        ).select_related('user')

        # 总行为日志数
        total_logs = behavior_logs.count()

        # 独立用户数
        unique_users = behavior_logs.filter(user__isnull=False).values('user').distinct().count()

        # 行为类型分布
        behavior_distribution = self._get_behavior_distribution(behavior_logs)

        # 转化漏斗分析
        conversion_funnel = self._get_conversion_funnel(behavior_logs)

        # 路径模式分析
        path_patterns = self._get_path_patterns(behavior_logs, limit_path)

        result = {
            'summary': {
                'total_logs': total_logs,
                'days': days,
                'unique_users': unique_users
            },
            'behavior_distribution': behavior_distribution,
            'conversion_funnel': conversion_funnel,
            'path_patterns': path_patterns
        }

        return ApiResponse.success(
            data=result,
            message=f'获取点击流分析数据成功（{days}天数据，共{total_logs}条记录）'
        )

    def _get_behavior_distribution(self, behavior_logs):
        """
        获取行为类型分布

        Args:
            behavior_logs: 行为日志查询集

        Returns:
            dict: 行为类型分布数据
        """
        distribution = behavior_logs.values('behavior_type').annotate(
            count=Count('id')
        ).order_by('-count')

        result = {}
        total = 0

        for item in distribution:
            behavior_type = item['behavior_type']
            count = item['count']
            result[behavior_type] = count
            total += count

        # 计算百分比
        for key in list(result.keys()):
            percentage = round((result[key] / total * 100), 2) if total > 0 else 0
            result[f'{key}_percentage'] = percentage

        return result

    def _get_conversion_funnel(self, behavior_logs):
        """
        获取转化漏斗数据

        Args:
            behavior_logs: 行为日志查询集

        Returns:
            dict: 转化漏斗数据
        """
        # 获取各行为类型的用户数（独立用户）
        login_users = behavior_logs.filter(
            behavior_type=BehaviorType.LOGIN
        ).values('user').distinct().count()

        view_users = behavior_logs.filter(
            behavior_type=BehaviorType.VIEW
        ).values('user').distinct().count()

        collect_users = behavior_logs.filter(
            behavior_type=BehaviorType.COLLECT
        ).values('user').distinct().count()

        # 计算转化率
        login_to_view_rate = round((view_users / login_users * 100), 2) if login_users > 0 else 0
        view_to_collect_rate = round((collect_users / view_users * 100), 2) if view_users > 0 else 0
        overall_conversion = round((collect_users / login_users * 100), 2) if login_users > 0 else 0

        return {
            'login_users': login_users,
            'view_users': view_users,
            'collect_users': collect_users,
            'login_to_view_rate': login_to_view_rate,
            'view_to_collect_rate': view_to_collect_rate,
            'overall_conversion_rate': overall_conversion
        }

    def _get_path_patterns(self, behavior_logs, limit):
        """
        获取常见路径模式

        Args:
            behavior_logs: 行为日志查询集
            limit: 返回数量

        Returns:
            list: 路径模式列表
        """
        # 页面路径映射
        path_mapping = {
            'home': '首页',
            '/': '首页',
            'recipe_list': '菜谱列表',
            '/recipes': '菜谱列表',
            'recipe_detail': '菜谱详情',
            'category': '分类页',
            '/category': '分类页',
            'hot': '热门页',
            '/hot': '热门页',
            'search': '搜索页',
            '/search': '搜索页',
            'analytics': '数据页',
            '/analytics': '数据页',
            'profile': '个人中心',
            '/profile': '个人中心',
            'favorite': '收藏页',
            '/favorites': '收藏页',
        }

        # 按用户和时间分组，提取访问路径
        user_sessions = defaultdict(list)

        for log in behavior_logs.order_by('user_id', 'timestamp'):
            if log.user_id:
                target = log.target or ''

                # 映射页面路径
                page_name = path_mapping.get(target, target)

                # 提取菜谱详情页
                if target and target.startswith('recipe:'):
                    page_name = '菜谱详情'

                user_sessions[log.user_id].append({
                    'type': log.behavior_type,
                    'page': page_name,
                    'timestamp': log.timestamp
                })

        # 统计路径模式
        path_counts = defaultdict(int)
        path_to_views = defaultdict(int)
        path_to_collects = defaultdict(int)

        for user_id, sessions in user_sessions.items():
            if len(sessions) < 2:
                continue

            # 构建访问序列
            path_sequence = []
            for session in sessions:
                if session['page'] not in path_sequence:
                    path_sequence.append(session['page'])

            # 生成路径模式字符串
            path_str = ' -> '.join(path_sequence[:4])  # 只取前4个页面
            if len(path_sequence) > 4:
                path_str += ' -> ...'

            path_counts[path_str] += 1

            # 统计该路径下的浏览和收藏行为
            for session in sessions:
                if session['type'] == BehaviorType.VIEW:
                    path_to_views[path_str] += 1
                elif session['type'] == BehaviorType.COLLECT:
                    path_to_collects[path_str] += 1

        # 计算总路径数
        total_paths = sum(path_counts.values())

        # 按访问次数排序并限制返回数量
        sorted_paths = sorted(path_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

        # 构建返回数据
        result = []
        for path_str, count in sorted_paths:
            percentage = round((count / total_paths * 100), 2) if total_paths > 0 else 0
            views = path_to_views.get(path_str, 0)
            collects = path_to_collects.get(path_str, 0)
            conversion_rate = round((collects / views * 100), 2) if views > 0 else 0

            result.append({
                'path': path_str,
                'count': count,
                'percentage': percentage,
                'views': views,
                'collects': collects,
                'conversion_rate': conversion_rate
            })

        return result


# ==================== 活跃用户分析接口 ====================

class ActiveUsersAnalysisView(APIView):
    """
    管理员 - 活跃用户分析接口

    GET /api/admin/analytics/active-users

    分析用户活跃度指标，包括：
    - DAU（日活跃用户数）
    - WAU（周活跃用户数）
    - MAU（月活跃用户数）
    - 活跃用户趋势（按天/周/月）
    - 用户活跃时段分布

    权限要求：仅管理员可访问

    查询参数：
    - days: 分析时间范围天数（7-90，默认 30）
    - trend_by: 趋势聚合方式（day/week/month，默认 day）
    - include_trend: 是否返回趋势数据（true/false，默认 true）

    返回数据格式：
    {
        "summary": {
            "total_users": 100,
            "active_today": 45,
            "active_week": 78,
            "active_month": 95
        },
        "dau": {
            "today": 45,
            "yesterday": 42,
            "change_rate": 7.14
        },
        "wau": {
            "current": 78,
            "previous": 72,
            "change_rate": 8.33
        },
        "mau": {
            "current": 95,
            "previous": 88,
            "change_rate": 7.95
        },
        "stickiness": {
            "dau_mau_ratio": 47.37
        },
        "trend": [
            {
                "date": "2026-01-01",
                "dau": 40,
                "wau": 75,
                "mau": 90
            }
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取活跃用户分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 活跃用户分析数据
        """
        # 获取查询参数
        days = request.query_params.get('days', 30)
        trend_by = request.query_params.get('trend_by', 'day')
        include_trend = request.query_params.get('include_trend', 'true')

        # 参数验证
        try:
            days = int(days)
            if days < 7:
                days = 7
            elif days > 90:
                days = 90
        except (ValueError, TypeError):
            days = 30

        if trend_by not in ['day', 'week', 'month']:
            trend_by = 'day'

        include_trend = include_trend.lower() == 'true'

        # 计算时间范围
        end_time = timezone.now()
        start_time = end_time - timedelta(days=days)

        # 获取总用户数
        from accounts.models import User
        total_users = User.objects.count()

        # 计算日活跃用户（今天和昨天）
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        yesterday_end = today_start

        dau_today = UserBehaviorLog.objects.filter(
            timestamp__gte=today_start,
            user__isnull=False
        ).values('user').distinct().count()

        dau_yesterday = UserBehaviorLog.objects.filter(
            timestamp__gte=yesterday_start,
            timestamp__lt=yesterday_end,
            user__isnull=False
        ).values('user').distinct().count()

        # 计算周活跃用户（本周和上周）
        week_start = end_time - timedelta(days=end_time.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        last_week_start = week_start - timedelta(days=7)
        last_week_end = week_start

        wau_current = UserBehaviorLog.objects.filter(
            timestamp__gte=week_start,
            user__isnull=False
        ).values('user').distinct().count()

        wau_previous = UserBehaviorLog.objects.filter(
            timestamp__gte=last_week_start,
            timestamp__lt=last_week_end,
            user__isnull=False
        ).values('user').distinct().count()

        # 计算月活跃用户（本月和上月）
        month_start = end_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)

        mau_current = UserBehaviorLog.objects.filter(
            timestamp__gte=month_start,
            user__isnull=False
        ).values('user').distinct().count()

        mau_previous = UserBehaviorLog.objects.filter(
            timestamp__gte=last_month_start,
            timestamp__lt=month_start,
            user__isnull=False
        ).values('user').distinct().count()

        # 计算变化率
        def calc_change_rate(current, previous):
            if previous == 0:
                return 100.0 if current > 0 else 0.0
            return round(((current - previous) / previous * 100), 2)

        dau_change = calc_change_rate(dau_today, dau_yesterday)
        wau_change = calc_change_rate(wau_current, wau_previous)
        mau_change = calc_change_rate(mau_current, mau_previous)

        # 计算留存率（DAU/MAU）
        dau_mau_ratio = round((dau_today / mau_current * 100), 2) if mau_current > 0 else 0

        # 构建基础统计
        result = {
            'summary': {
                'total_users': total_users,
                'active_today': dau_today,
                'active_week': wau_current,
                'active_month': mau_current
            },
            'dau': {
                'today': dau_today,
                'yesterday': dau_yesterday,
                'change_rate': dau_change
            },
            'wau': {
                'current': wau_current,
                'previous': wau_previous,
                'change_rate': wau_change
            },
            'mau': {
                'current': mau_current,
                'previous': mau_previous,
                'change_rate': mau_change
            },
            'stickiness': {
                'dau_mau_ratio': dau_mau_ratio
            }
        }

        # 添加趋势数据
        if include_trend:
            trend_data = self._get_trend_data(start_time, end_time, trend_by, days)
            result['trend'] = trend_data

        return ApiResponse.success(
            data=result,
            message=f'获取活跃用户分析数据成功（{days}天数据）'
        )

    def _get_trend_data(self, start_time, end_time, trend_by, total_days):
        """
        获取活跃用户趋势数据

        Args:
            start_time: 开始时间
            end_time: 结束时间
            trend_by: 聚合方式（day/week/month）
            total_days: 总天数

        Returns:
            list: 趋势数据列表
        """
        trend_data = []

        if trend_by == 'day':
            # 按天聚合
            for i in range(total_days):
                date = (end_time - timedelta(days=total_days - i - 1)).date()
                day_start = timezone.make_aware(
                    timezone.datetime.combine(date, timezone.datetime.min.time())
                )
                day_end = day_start + timedelta(days=1)

                dau = UserBehaviorLog.objects.filter(
                    timestamp__gte=day_start,
                    timestamp__lt=day_end,
                    user__isnull=False
                ).values('user').distinct().count()

                # 计算周活跃（该天往前7天）
                week_start = day_start - timedelta(days=6)
                wau = UserBehaviorLog.objects.filter(
                    timestamp__gte=week_start,
                    timestamp__lt=day_end,
                    user__isnull=False
                ).values('user').distinct().count()

                # 计算月活跃（该天往前30天）
                month_start = day_start - timedelta(days=29)
                mau = UserBehaviorLog.objects.filter(
                    timestamp__gte=month_start,
                    timestamp__lt=day_end,
                    user__isnull=False
                ).values('user').distinct().count()

                trend_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'dau': dau,
                    'wau': wau,
                    'mau': mau
                })

        elif trend_by == 'week':
            # 按周聚合
            week_count = total_days // 7
            for i in range(week_count):
                week_end = end_time - timedelta(days=i * 7)
                week_start = week_end - timedelta(days=6)

                dau = UserBehaviorLog.objects.filter(
                    timestamp__gte=week_start,
                    timestamp__lte=week_end,
                    user__isnull=False
                ).values('user').distinct().count()

                # 周内平均DAU
                total_dau = 0
                for j in range(7):
                    day = week_end - timedelta(days=j)
                    day_dau = UserBehaviorLog.objects.filter(
                        timestamp__date=day.date(),
                        user__isnull=False
                    ).values('user').distinct().count()
                    total_dau += day_dau
                avg_dau = round(total_dau / 7, 1)

                trend_data.append({
                    'date': f"{week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}",
                    'avg_dau': avg_dau,
                    'wau': dau
                })

        elif trend_by == 'month':
            # 按月聚合
            current_date = end_time.date()
            for i in range(min(6, total_days // 30 + 1)):
                month_end = current_date - timedelta(days=i * 30)
                month_start = (month_end - timedelta(days=29)).replace(day=1)

                if i == 0:
                    # 当前月，使用实际日期
                    month_end = current_date

                dau = UserBehaviorLog.objects.filter(
                    timestamp__gte=month_start,
                    timestamp__lte=month_end,
                    user__isnull=False
                ).values('user').distinct().count()

                trend_data.append({
                    'date': month_start.strftime('%Y-%m'),
                    'mau': dau
                })

        return trend_data


# ==================== 登录频次分析接口 ====================

class LoginFrequencyAnalysisView(APIView):
    """
    管理员 - 登录频次分析接口

    GET /api/admin/analytics/login-frequency

    分析用户登录频次和登录时间分布，包括：
    - 用户登录次数分布（高频/中频/低频/沉默用户）
    - 登录时间段分布（24小时分布）
    - 每日登录次数趋势
    - 新用户与老用户登录对比

    权限要求：仅管理员可访问

    查询参数：
    - days: 分析时间范围天数（1-90，默认 30）

    返回数据格式：
    {
        "summary": {
            "total_logs": 5000,
            "days": 30,
            "total_users": 100
        },
        "login_frequency_distribution": {
            "high_frequency": 20,
            "medium_frequency": 35,
            "low_frequency": 30,
            "silent": 15
        },
        "hourly_distribution": {
            "0-6": 50,
            "6-12": 800,
            "12-18": 1200,
            "18-24": 2950
        },
        "daily_trend": [
            {
                "date": "2026-01-01",
                "login_count": 150,
                "login_users": 80
            }
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取登录频次分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 登录频次分析数据
        """
        # 获取查询参数
        days = request.query_params.get('days', 30)

        # 参数验证
        try:
            days = int(days)
            if days < 1:
                days = 1
            elif days > 90:
                days = 90
        except (ValueError, TypeError):
            days = 30

        # 计算时间范围
        end_time = timezone.now()
        start_time = end_time - timedelta(days=days)

        # 获取总用户数
        from accounts.models import User
        total_users = User.objects.count()

        # 获取登录行为日志
        login_logs = UserBehaviorLog.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time,
            behavior_type=BehaviorType.LOGIN,
            user__isnull=False
        ).select_related('user')

        total_logs = login_logs.count()

        # 登录次数分布统计
        login_frequency_distribution = self._get_frequency_distribution(login_logs, total_users)

        # 登录时间段分布
        hourly_distribution = self._get_hourly_distribution(login_logs)

        # 每日登录趋势
        daily_trend = self._get_daily_trend(login_logs, start_time, end_time)

        result = {
            'summary': {
                'total_logs': total_logs,
                'days': days,
                'total_users': total_users
            },
            'login_frequency_distribution': login_frequency_distribution,
            'hourly_distribution': hourly_distribution,
            'daily_trend': daily_trend
        }

        return ApiResponse.success(
            data=result,
            message=f'获取登录频次分析数据成功（{days}天数据，共{total_logs}次登录）'
        )

    def _get_frequency_distribution(self, login_logs, total_users):
        """
        获取用户登录频率分布

        Args:
            login_logs: 登录日志查询集
            total_users: 总用户数

        Returns:
            dict: 登录频率分布数据
        """
        # 统计每个用户的登录次数
        user_login_counts = login_logs.values('user_id').annotate(
            login_count=Count('id')
        )

        # 按登录次数分组
        high_frequency = 0   # 高频用户：登录次数 >= 20
        medium_frequency = 0 # 中频用户：登录次数 5-19
        low_frequency = 0    # 低频用户：登录次数 1-4
        silent = 0           # 沉默用户：登录次数 0

        for item in user_login_counts:
            count = item['login_count']
            if count >= 20:
                high_frequency += 1
            elif count >= 5:
                medium_frequency += 1
            else:
                low_frequency += 1

        # 计算沉默用户数（登录次数为0的用户）
        active_user_ids = set(item['user_id'] for item in user_login_counts)
        silent = total_users - len(active_user_ids)

        return {
            'high_frequency': high_frequency,
            'medium_frequency': medium_frequency,
            'low_frequency': low_frequency,
            'silent': silent,
            'high_percentage': round((high_frequency / total_users * 100), 2) if total_users > 0 else 0,
            'medium_percentage': round((medium_frequency / total_users * 100), 2) if total_users > 0 else 0,
            'low_percentage': round((low_frequency / total_users * 100), 2) if total_users > 0 else 0,
            'silent_percentage': round((silent / total_users * 100), 2) if total_users > 0 else 0
        }

    def _get_hourly_distribution(self, login_logs):
        """
        获取登录时间段分布（24小时）

        Args:
            login_logs: 登录日志查询集

        Returns:
            dict: 24小时分布数据
        """
        # 初始化24小时分布
        hourly_counts = {i: 0 for i in range(24)}

        # 统计每小时登录次数
        for log in login_logs:
            hour = log.timestamp.hour
            hourly_counts[hour] += 1

        # 合并为4个时段
        return {
            '0-6': sum(hourly_counts[h] for h in range(0, 6)),
            '6-12': sum(hourly_counts[h] for h in range(6, 12)),
            '12-18': sum(hourly_counts[h] for h in range(12, 18)),
            '18-24': sum(hourly_counts[h] for h in range(18, 24)),
            'detail': {
                str(h): hourly_counts[h] for h in range(24)
            }
        }

    def _get_daily_trend(self, login_logs, start_time, end_time):
        """
        获取每日登录趋势

        Args:
            login_logs: 登录日志查询集
            start_time: 开始时间
            end_time: 结束时间

        Returns:
            list: 每日趋势数据
        """
        # 获取日期范围内的所有日期
        daily_data = login_logs.extra(
            {'date': "DATE(timestamp)"}
        ).values('date').annotate(
            login_count=Count('id'),
            login_users=Count('user_id', distinct=True)
        ).order_by('date')

        # 转换为日期字符串格式
        trend = []
        for item in daily_data:
            trend.append({
                'date': item['date'].strftime('%Y-%m-%d') if hasattr(item['date'], 'strftime') else str(item['date']),
                'login_count': item['login_count'],
                'login_users': item['login_users']
            })

        return trend


# ==================== 页面停留分析接口 ====================

class PageDurationAnalysisView(APIView):
    """
    管理员 - 页面停留分析接口

    GET /api/admin/analytics/page-duration

    分析用户在各个页面的停留时间，包括：
    - 各页面的平均停留时间
    - 停留时长分布（短/中/长）
    - 停留时间趋势
    - 页面对比分析

    权限要求：仅管理员可访问

    查询参数：
    - days: 分析时间范围天数（1-90，默认 30）
    - page: 页面类型筛选（可选）

    返回数据格式：
    {
        "summary": {
            "total_logs": 5000,
            "days": 30,
            "total_pages": 8
        },
        "page_statistics": [
            {
                "page": "菜谱详情",
                "avg_duration": 120.5,
                "total_visits": 2500,
                "min_duration": 5,
                "max_duration": 1800,
                "median_duration": 90.0
            }
        ],
        "duration_distribution": {
            "short": 1000,
            "medium": 1500,
            "long": 500
        },
        "trend": [
            {
                "date": "2026-01-01",
                "avg_duration": 115.2
            }
        ]
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    # 页面路径中文映射
    PAGE_LABELS = {
        'home': '首页',
        '/': '首页',
        'recipe_list': '菜谱列表',
        '/recipes': '菜谱列表',
        'recipe_detail': '菜谱详情',
        'category': '分类页',
        '/category': '分类页',
        'hot': '热门页',
        '/hot': '热门页',
        'search': '搜索页',
        '/search': '搜索页',
        'analytics': '数据页',
        '/analytics': '数据页',
        'profile': '个人中心',
        '/profile': '个人中心',
        'favorite': '收藏页',
        '/favorites': '收藏页',
    }

    def get(self, request):
        """
        获取页面停留分析数据

        Args:
            request: 请求对象

        Returns:
            Response: 页面停留分析数据
        """
        # 获取查询参数
        days = request.query_params.get('days', 30)
        page_filter = request.query_params.get('page', None)

        # 参数验证
        try:
            days = int(days)
            if days < 1:
                days = 1
            elif days > 90:
                days = 90
        except (ValueError, TypeError):
            days = 30

        # 计算时间范围
        end_time = timezone.now()
        start_time = end_time - timedelta(days=days)

        # 获取时间范围内的页面访问日志
        behavior_logs = UserBehaviorLog.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time,
            behavior_type='page_view',
            user__isnull=False
        ).select_related('user')

        total_logs = behavior_logs.count()

        # 页面停留数据统计
        page_statistics = self._get_page_statistics(behavior_logs, page_filter)

        # 停留时长分布
        duration_distribution = self._get_duration_distribution(behavior_logs)

        # 每日趋势
        trend = self._get_duration_trend(behavior_logs, start_time, end_time)

        result = {
            'summary': {
                'total_logs': total_logs,
                'days': days,
                'total_pages': len(page_statistics),
                'page_filter': page_filter or '全部'
            },
            'page_statistics': page_statistics,
            'duration_distribution': duration_distribution,
            'trend': trend
        }

        return ApiResponse.success(
            data=result,
            message=f'获取页面停留分析数据成功（{days}天数据，共{total_logs}条记录）'
        )

    def _get_page_statistics(self, behavior_logs, page_filter):
        """
        获取各页面停留时间统计

        Args:
            behavior_logs: 行为日志查询集
            page_filter: 页面类型筛选

        Returns:
            list: 页面统计数据列表
        """
        # 初始化页面统计
        page_stats = defaultdict(lambda: {
            'durations': [],
            'count': 0
        })

        for log in behavior_logs:
            target = log.target or ''

            # 映射页面名称
            page_name = self._get_page_name(target)

            # 应用筛选
            if page_filter and page_filter.lower() != page_name.lower():
                continue

            # 提取停留时长
            duration = self._get_duration_from_log(log)
            if duration is not None:
                page_stats[page_name]['durations'].append(duration)
                page_stats[page_name]['count'] += 1

        # 构建返回数据
        result = []
        for page_name, stats in sorted(page_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            durations = stats['durations']
            count = stats['count']

            if not durations:
                continue

            # 计算统计数据
            avg_duration = sum(durations) / count if count > 0 else 0
            min_duration = min(durations) if durations else 0
            max_duration = max(durations) if durations else 0
            median_duration = self._calculate_median(durations)

            result.append({
                'page': page_name,
                'avg_duration': round(avg_duration, 2),
                'total_visits': count,
                'min_duration': min_duration,
                'max_duration': max_duration,
                'median_duration': round(median_duration, 2)
            })

        return result

    def _get_page_name(self, target):
        """
        获取页面中文名称

        Args:
            target: 页面路径

        Returns:
            str: 中文页面名称
        """
        # 菜谱详情页特殊处理
        if target and target.startswith('recipe:'):
            return '菜谱详情'

        return self.PAGE_LABELS.get(target, target)

    def _get_duration_from_log(self, log):
        """
        从日志中提取停留时长

        Args:
            log: 行为日志

        Returns:
            float: 停留时长（秒），None 表示无效数据
        """
        if not log.extra_data:
            return None

        duration = log.extra_data.get('duration')
        if duration is None:
            return None

        try:
            duration = float(duration)
            # 过滤异常值：停留时间在 1秒 到 1小时（3600秒）之间
            if 1 <= duration <= 3600:
                return duration
            return None
        except (ValueError, TypeError):
            return None

    def _calculate_median(self, values):
        """
        计算中位数

        Args:
            values: 数值列表

        Returns:
            float: 中位数
        """
        if not values:
            return 0

        sorted_values = sorted(values)
        n = len(sorted_values)

        if n % 2 == 0:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        else:
            return sorted_values[n // 2]

    def _get_duration_distribution(self, behavior_logs):
        """
        获取停留时长分布

        Args:
            behavior_logs: 行为日志查询集

        Returns:
            dict: 停留时长分布数据
        """
        short_count = 0   # 短停留：< 30秒
        medium_count = 0  # 中停留：30-120秒
        long_count = 0    # 长停留：> 120秒

        for log in behavior_logs:
            duration = self._get_duration_from_log(log)
            if duration is None:
                continue

            if duration < 30:
                short_count += 1
            elif duration < 120:
                medium_count += 1
            else:
                long_count += 1

        total = short_count + medium_count + long_count

        return {
            'short': short_count,
            'medium': medium_count,
            'long': long_count,
            'short_percentage': round((short_count / total * 100), 2) if total > 0 else 0,
            'medium_percentage': round((medium_count / total * 100), 2) if total > 0 else 0,
            'long_percentage': round((long_count / total * 100), 2) if total > 0 else 0
        }

    def _get_duration_trend(self, behavior_logs, start_time, end_time):
        """
        获取每日平均停留时间趋势

        Args:
            behavior_logs: 行为日志查询集
            start_time: 开始时间
            end_time: 结束时间

        Returns:
            list: 每日趋势数据
        """
        # 按日期分组收集停留时间数据
        from collections import defaultdict

        daily_durations = defaultdict(list)

        for log in behavior_logs:
            duration = self._get_duration_from_log(log)
            if duration is not None:
                date_key = log.timestamp.strftime('%Y-%m-%d')
                daily_durations[date_key].append(duration)

        # 构建趋势数据
        trend = []
        for date_key in sorted(daily_durations.keys()):
            durations = daily_durations[date_key]
            count = len(durations)

            if count > 0:
                avg_duration = sum(durations) / count
            else:
                avg_duration = 0

            trend.append({
                'date': date_key,
                'avg_duration': round(avg_duration, 2),
                'visit_count': count
            })

        return trend