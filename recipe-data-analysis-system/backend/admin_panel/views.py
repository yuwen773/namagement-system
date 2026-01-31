"""
Admin Panel 模块 - 视图层

本模块提供管理员仪表盘相关的 API 接口，包括：
- 数据总览接口（关键指标统计）
- 数据趋势接口
- 用户行为统计接口
"""
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.response import ApiResponse
from utils.permissions import IsAdminUser
from recipes.models import Recipe
from accounts.models import User
from favorites.models import UserFavorite


class DashboardOverviewView(APIView):
    """
    管理员 - 数据总览接口

    GET /api/admin/dashboard/overview

    提供平台关键指标统计，包括：
    - 总菜谱数
    - 总用户数
    - 今日新增菜谱数
    - 今日新增用户数
    - 今日活跃用户数
    - 总收藏数

    权限要求：仅管理员可访问

    返回数据格式：
    {
        "total_recipes": 20000,
        "total_users": 150,
        "today_new_recipes": 50,
        "today_new_users": 5,
        "today_active_users": 30,
        "total_favorites": 5000,
        "updated_at": "2026-01-31T12:00:00Z"
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取数据总览统计

        Args:
            request: 请求对象

        Returns:
            Response: 关键指标统计数据
        """
        # 获取当前时间（使用服务器时区）
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 1. 总菜谱数
        total_recipes = Recipe.objects.count()

        # 2. 总用户数
        total_users = User.objects.count()

        # 3. 今日新增菜谱数
        today_new_recipes = Recipe.objects.filter(
            created_at__gte=today_start,
            created_at__lt=today_end
        ).count()

        # 4. 今日新增用户数
        today_new_users = User.objects.filter(
            created_at__gte=today_start,
            created_at__lt=today_end
        ).count()

        # 5. 今日活跃用户数（今日有登录行为的用户）
        today_active_users = User.objects.filter(
            last_login__gte=today_start,
            last_login__lt=today_end
        ).count()

        # 6. 总收藏数
        total_favorites = UserFavorite.objects.count()

        # 构建返回数据
        result = {
            'total_recipes': total_recipes,
            'total_users': total_users,
            'today_new_recipes': today_new_recipes,
            'today_new_users': today_new_users,
            'today_active_users': today_active_users,
            'total_favorites': total_favorites,
            'updated_at': now.isoformat()
        }

        return ApiResponse.success(
            data=result,
            message='获取数据总览成功'
        )


class DashboardTrendsView(APIView):
    """
    管理员 - 数据趋势接口

    GET /api/admin/dashboard/trends

    提供平台数据增长趋势，包括：
    - 菜谱增长趋势
    - 用户增长趋势
    - 收藏趋势

    权限要求：仅管理员可访问

    查询参数：
    - period: 时间范围（day/week/month，默认 day）
    - days: 天数（1-90，默认 30）

    返回数据格式：
    {
        "period": "day",
        "days": 30,
        "data": {
            "dates": ["2026-01-01", "2026-01-02", ...],
            "recipe_counts": [100, 105, ...],
            "user_counts": [50, 52, ...],
            "favorite_counts": [200, 210, ...]
        }
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取数据趋势统计

        Args:
            request: 请求对象

        Returns:
            Response: 数据趋势统计
        """
        # 获取查询参数
        period = request.query_params.get('period', 'day')
        days = request.query_params.get('days', 30)

        # 参数验证
        if period not in ['day', 'week', 'month']:
            period = 'day'

        try:
            days = int(days)
            if days < 1:
                days = 1
            elif days > 90:
                days = 90
        except (ValueError, TypeError):
            days = 30

        # 计算时间范围
        now = timezone.now()
        if period == 'day':
            # 按天统计
            delta = timedelta(days=days)
            start_date = (now - delta).replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            # 按周统计
            delta = timedelta(weeks=days)
            start_date = (now - delta).replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # month
            # 按月统计
            start_date = (now - timedelta(days=days * 30)).replace(hour=0, minute=0, second=0, microsecond=0)

        # 生成日期列表
        dates = []
        date = start_date
        while date < now:
            dates.append(date.date().isoformat())
            if period == 'day':
                date += timedelta(days=1)
            elif period == 'week':
                date += timedelta(weeks=1)
            else:  # month
                # 简单处理：按30天为一个月
                date += timedelta(days=30)

        # 统计各时间点的累计数据
        recipe_counts = []
        user_counts = []
        favorite_counts = []

        for i, date_str in enumerate(dates):
            # 计算该日期的结束时间
            date_obj = datetime.fromisoformat(date_str)
            if period == 'day':
                period_end = date_obj + timedelta(days=1)
            elif period == 'week':
                period_end = date_obj + timedelta(weeks=1)
            else:  # month
                period_end = date_obj + timedelta(days=30)

            # 统计累计数据
            recipe_counts.append(
                Recipe.objects.filter(created_at__lt=period_end).count()
            )
            user_counts.append(
                User.objects.filter(created_at__lt=period_end).count()
            )
            favorite_counts.append(
                UserFavorite.objects.filter(created_at__lt=period_end).count()
            )

        # 构建返回数据
        result = {
            'period': period,
            'days': days,
            'data': {
                'dates': dates,
                'recipe_counts': recipe_counts,
                'user_counts': user_counts,
                'favorite_counts': favorite_counts
            }
        }

        return ApiResponse.success(
            data=result,
            message=f'获取数据趋势成功（最近 {days} 个{self._get_period_label(period)}）'
        )

    def _get_period_label(self, period):
        """获取时间范围中文名"""
        labels = {
            'day': '天',
            'week': '周',
            'month': '月'
        }
        return labels.get(period, '天')


class DashboardBehaviorsView(APIView):
    """
    管理员 - 用户行为统计接口

    GET /api/admin/dashboard/behaviors

    提供用户行为分析数据，包括：
    - 各类行为数量分布
    - 活跃用户分布
    - 页面访问量统计

    权限要求：仅管理员可访问

    返回数据格式：
    {
        "behavior_distribution": {
            "login": 100,
            "search": 200,
            "view": 500,
            "favorite": 50
        },
        "active_user_distribution": {
            "dau": 30,
            "wau": 80,
            "mau": 120
        },
        "page_views": {
            "home": 1000,
            "recipe_list": 2000,
            "recipe_detail": 1500,
            "category": 500,
            "hot": 300
        }
    }
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        获取用户行为统计

        Args:
            request: 请求对象

        Returns:
            Response: 用户行为统计数据
        """
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # 1. 日活跃用户（DAU）
        dau = User.objects.filter(
            last_login__gte=today_start
        ).count()

        # 2. 周活跃用户（WAU）
        week_start = today_start - timedelta(days=7)
        wau = User.objects.filter(
            last_login__gte=week_start
        ).count()

        # 3. 月活跃用户（MAU）
        month_start = today_start - timedelta(days=30)
        mau = User.objects.filter(
            last_login__gte=month_start
        ).count()

        # 4. 行为分布（基于现有数据模型进行估算）
        # 由于当前没有行为日志表，这里使用收藏数据作为参考
        total_favorites = UserFavorite.objects.count()
        today_favorites = UserFavorite.objects.filter(
            created_at__gte=today_start
        ).count()

        # 5. 页面访问量（基于菜谱浏览量的估算）
        # 使用菜谱的 view_count 作为页面访问量的参考
        total_views = Recipe.objects.aggregate(
            total=Count('view_count')
        )['total'] or 0

        # 构建返回数据
        result = {
            'behavior_distribution': {
                'login': dau,  # 今日登录用户数
                'favorite': today_favorites,  # 今日收藏数
                'view': total_views,  # 总浏览量（基于菜谱点击量）
            },
            'active_user_distribution': {
                'dau': dau,  # 日活跃用户
                'wau': wau,  # 周活跃用户
                'mau': mau,  # 月活跃用户
            },
            'page_views': {
                'recipe_detail': total_views,  # 菜谱详情页访问量
            },
            'updated_at': now.isoformat()
        }

        return ApiResponse.success(
            data=result,
            message='获取用户行为统计成功'
        )
