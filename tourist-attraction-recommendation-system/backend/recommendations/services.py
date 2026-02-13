"""
推荐算法服务模块

提供三种推荐策略：
1. 热门推荐 - 基于热度值排序
2. 个性化推荐 - 基于用户历史行为
3. 相似推荐 - 基于景点类别和地区

性能优化：使用 annotate 聚合查询替代循环，避免 N+1 问题
"""

from django.db.models import Avg, Count, Q, When, Case, FloatField, F
from django.db.models.functions import Coalesce
from attractions.models import Attraction
from comments.models import Comment, Favorite


def get_popular_attractions(limit: int = 10) -> list:
    """
    获取热门景点推荐（冷启动场景）

    用于新用户无历史数据时推荐热门景点

    热度公式: (浏览量 * 0.2) + (评论数 * 0.3) + (平均评分 * 浏览量 * 0.5)

    性能优化：使用 annotate 一次性计算所有景点的热度分数

    Args:
        limit: 返回数量限制

    Returns:
        热门景点列表（按热度排序）
    """
    # 使用聚合函数一次性计算所有景点的热度指标
    attractions = Attraction.objects.filter(
        is_deleted=False
    ).annotate(
        # 计算已审核且未删除的评论数
        comment_count=Count(
            Case(
                When(
                    comments__status='APPROVED',
                    comments__is_deleted=False,
                    then=1
                ),
                default=None,
                output_field=FloatField()
            ),
            distinct=True
        ),
        # 计算平均评分
        avg_rating=Coalesce(
            Avg(
                Case(
                    When(
                        comments__status='APPROVED',
                        comments__is_deleted=False,
                        comments__rating__isnull=False,
                        then='comments__rating'
                    ),
                    default=None,
                    output_field=FloatField()
                ),
                distinct=True
            ),
            0.0,
            output_field=FloatField()
        )
    ).annotate(
        # 计算热度分数: (浏览量 * 0.2) + (评论数 * 0.3) + (平均评分 * 浏览量 * 0.5)
        hot_score=(F('view_count') * 0.2) + (F('comment_count') * 0.3) + (F('avg_rating') * F('view_count') * 0.5)
    ).order_by('-hot_score')[:limit]

    # 转换为结果格式
    results = []
    for attraction in attractions:
        results.append({
            'attraction': attraction,
            'hot_score': round(attraction.hot_score, 2)
        })

    return results


def get_personalized_recommendations(user_id: int, limit: int = 10) -> list:
    """
    获取个性化推荐（基于用户历史行为）

    策略：推荐用户收藏过景点的同类景点

    性能优化：使用 annotate 和 prefetch_related 优化查询

    Args:
        user_id: 用户ID
        limit: 返回数量限制

    Returns:
        个性化推荐景点列表
    """
    from accounts.models import UserProfile

    try:
        user = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        return get_popular_attractions(limit)

    # 获取用户收藏的景点类别
    favorite_categories = Favorite.objects.filter(
        user=user,
        attraction__is_deleted=False
    ).values_list('attraction__category', flat=True).distinct()

    if not favorite_categories:
        # 无收藏记录，返回热门推荐
        return get_popular_attractions(limit)

    # 获取用户收藏的景点ID
    favorite_ids = set(Favorite.objects.filter(
        user=user,
        attraction__is_deleted=False
    ).values_list('attraction_id', flat=True))

    # 获取用户评分过的景点类别（评分 >= 4 视为喜欢）
    liked_categories = Comment.objects.filter(
        user=user,
        rating__gte=4,
        status='APPROVED',
        is_deleted=False
    ).values_list('attraction__category', flat=True).distinct()

    # 合并类别
    target_categories = set(favorite_categories) | set(liked_categories)

    # 使用聚合函数一次性计算推荐景点的热度分数
    recommendations = Attraction.objects.filter(
        category__in=target_categories,
        is_deleted=False
    ).exclude(
        id__in=favorite_ids
    ).annotate(
        comment_count=Count(
            Case(
                When(
                    comments__status='APPROVED',
                    comments__is_deleted=False,
                    then=1
                ),
                default=None,
                output_field=FloatField()
            ),
            distinct=True
        ),
        avg_rating=Coalesce(
            Avg(
                Case(
                    When(
                        comments__status='APPROVED',
                        comments__is_deleted=False,
                        comments__rating__isnull=False,
                        then='comments__rating'
                    ),
                    default=None,
                    output_field=FloatField()
                ),
                distinct=True
            ),
            0.0,
            output_field=FloatField()
        )
    ).annotate(
        hot_score=(F('view_count') * 0.2) + (F('comment_count') * 0.3) + (F('avg_rating') * F('view_count') * 0.5)
    ).order_by('-hot_score')[:limit]

    # 转换为结果格式
    results = []
    for attraction in recommendations:
        results.append({
            'attraction': attraction,
            'hot_score': round(attraction.hot_score, 2)
        })

    return results


def get_similar_attractions(attraction_id: int, limit: int = 6) -> list:
    """
    获取相似景点推荐（基于类别和地区）

    策略：推荐同类别的景点，优先同地区

    性能优化：使用 annotate 一次性计算热度分数和地区加成

    Args:
        attraction_id: 目标景点ID
        limit: 返回数量限制

    Returns:
        相似景点列表
    """
    try:
        target = Attraction.objects.get(pk=attraction_id, is_deleted=False)
    except Attraction.DoesNotExist:
        return []

    # 推荐同类景点，使用聚合函数计算热度分数
    # 同地区加 2 分
    similar = Attraction.objects.filter(
        category=target.category,
        is_deleted=False
    ).exclude(
        id=attraction_id
    ).annotate(
        comment_count=Count(
            Case(
                When(
                    comments__status='APPROVED',
                    comments__is_deleted=False,
                    then=1
                ),
                default=None,
                output_field=FloatField()
            ),
            distinct=True
        ),
        avg_rating=Coalesce(
            Avg(
                Case(
                    When(
                        comments__status='APPROVED',
                        comments__is_deleted=False,
                        comments__rating__isnull=False,
                        then='comments__rating'
                    ),
                    default=None,
                    output_field=FloatField()
                ),
                distinct=True
            ),
            0.0,
            output_field=FloatField()
        )
    ).annotate(
        hot_score=(F('view_count') * 0.2) + (F('comment_count') * 0.3) + (F('avg_rating') * F('view_count') * 0.5),
        # 同地区加 2 分
        region_bonus=Case(
            When(region=target.region, then=2),
            default=0,
            output_field=FloatField()
        ),
        # 总分 = 热度分数 + 地区分数
        total_score=F('hot_score') + F('region_bonus')
    ).order_by('-total_score')[:limit]

    # 转换为结果格式
    results = []
    for attraction in similar:
        results.append({
            'attraction': attraction,
            'hot_score': round(attraction.total_score, 2)
        })

    return results
