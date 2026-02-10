"""
推荐算法服务模块

提供三种推荐策略：
1. 热门推荐 - 基于热度值排序
2. 个性化推荐 - 基于用户历史行为
3. 相似推荐 - 基于景点类别和地区
"""

from django.db.models import Avg, Count, Q
from attractions.models import Attraction
from comments.models import Comment, Favorite


def calculate_hot_score(attraction: Attraction) -> float:
    """
    计算景点热度分数

    热度公式: (浏览量 * 0.2) + (评论数 * 0.3) + (平均评分 * 浏览量 * 0.5)
    """
    view_count = attraction.view_count
    comment_count = attraction.comments.filter(status='APPROVED', is_deleted=False).count()
    avg_rating = attraction.comments.filter(status='APPROVED', is_deleted=False).aggregate(
        avg=Avg('rating')
    )['avg'] or 0

    hot_score = (view_count * 0.2) + (comment_count * 0.3) + (avg_rating * view_count * 0.5)
    return round(hot_score, 2)


def get_popular_attractions(limit: int = 10) -> list:
    """
    获取热门景点推荐（冷启动场景）

    用于新用户无历史数据时推荐热门景点

    Args:
        limit: 返回数量限制

    Returns:
        热门景点列表（按热度排序）
    """
    attractions = Attraction.objects.filter(is_deleted=False)

    # 计算每个景点的热度分数
    results = []
    for attraction in attractions:
        hot_score = calculate_hot_score(attraction)
        results.append({
            'attraction': attraction,
            'hot_score': hot_score
        })

    # 按热度分数降序排序
    results.sort(key=lambda x: x['hot_score'], reverse=True)

    return results[:limit]


def get_personalized_recommendations(user_id: int, limit: int = 10) -> list:
    """
    获取个性化推荐（基于用户历史行为）

    策略：推荐用户收藏过景点的同类景点

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

    # 推荐同类景点（排除已收藏的）
    recommendations = Attraction.objects.filter(
        category__in=target_categories,
        is_deleted=False
    ).exclude(
        id__in=favorite_ids
    )

    # 计算热度分数并排序
    results = []
    for attraction in recommendations:
        hot_score = calculate_hot_score(attraction)
        results.append({
            'attraction': attraction,
            'hot_score': hot_score
        })

    results.sort(key=lambda x: x['hot_score'], reverse=True)

    return results[:limit]


def get_similar_attractions(attraction_id: int, limit: int = 6) -> list:
    """
    获取相似景点推荐（基于类别和地区）

    策略：推荐同类别的景点，优先同地区

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

    # 推荐同类景点
    similar = Attraction.objects.filter(
        category=target.category,
        is_deleted=False
    ).exclude(
        id=attraction_id
    )

    # 计算相似度分数（同地区优先）
    results = []
    for attraction in similar:
        # 同地区 +2 分
        region_bonus = 2 if attraction.region == target.region else 0
        hot_score = calculate_hot_score(attraction) + region_bonus
        results.append({
            'attraction': attraction,
            'hot_score': hot_score
        })

    results.sort(key=lambda x: x['hot_score'], reverse=True)

    return results[:limit]
