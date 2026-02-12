from rest_framework import serializers
from django.db.models import Avg
from accounts.models import UserProfile
from attractions.models import Attraction
from comments.models import Comment


class HotAttractionSerializer(serializers.ModelSerializer):
    """热门景点序列化器"""
    comment_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    hot_score = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = ['id', 'name', 'cover_image', 'category', 'region',
                  'view_count', 'comment_count', 'avg_rating', 'hot_score']

    def get_comment_count(self, obj):
        return obj.comments.filter(status='APPROVED', is_deleted=False).count()

    def get_avg_rating(self, obj):
        comments = obj.comments.filter(status='APPROVED', is_deleted=False)
        if comments.exists():
            return round(comments.aggregate(avg=Avg('rating'))['avg'], 1)
        return 0

    def get_hot_score(self, obj):
        """计算热度值: (浏览量 * 0.2) + (评论数 * 0.3) + (平均评分 * 浏览量 * 0.5)"""
        view_count = obj.view_count
        comment_count = obj.comments.filter(status='APPROVED', is_deleted=False).count()
        avg_rating = self.get_avg_rating(obj)
        hot_score = (view_count * 0.2) + (comment_count * 0.3) + (avg_rating * view_count * 0.5)
        return round(hot_score, 1)


class DashboardSerializer(serializers.Serializer):
    """数据看板序列化器"""
    total_users = serializers.IntegerField()
    total_attractions = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    monthly_new_users = serializers.IntegerField()
    monthly_new_attractions = serializers.IntegerField()
    monthly_new_comments = serializers.IntegerField()


class MonthlyDataSerializer(serializers.Serializer):
    """月度数据序列化器"""
    month = serializers.CharField()
    new_users = serializers.IntegerField()
    new_attractions = serializers.IntegerField()
    new_comments = serializers.IntegerField()


class UserManageSerializer(serializers.ModelSerializer):
    """用户管理列表序列化器"""

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'real_name', 'email', 'phone',
                  'role', 'is_active', 'created_at']


class UserStatusSerializer(serializers.Serializer):
    """用户状态更新序列化器"""
    is_active = serializers.BooleanField(required=True)
