"""
Analytics 模块 - 视图层

本模块提供数据分析相关的 API 接口，包括：
- 菜系分布分析
- 难度等级统计
- 口味偏好分析
- 食材使用频率统计
"""
from django.db.models import Count, Avg
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from utils.response import ApiResponse
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
