from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from accounts.models import UserProfile
from attractions.models import Attraction
from comments.models import Comment
from .serializers import (
    HotAttractionSerializer,
    DashboardSerializer,
    MonthlyDataSerializer,
    UserManageSerializer,
    UserStatusSerializer
)
from accounts.permissions import IsAdmin


class AttractionHotView(APIView):
    """景点热度统计"""
    permission_classes = []

    @extend_schema(
        responses=HotAttractionSerializer(many=True)
    )
    def get(self, request):
        """获取热门景点排行 TOP 10"""
        attractions = Attraction.objects.filter(is_deleted=False)

        # 计算热度值并排序
        result = []
        for attr in attractions:
            view_count = attr.view_count
            comment_count = attr.comments.filter(status='APPROVED', is_deleted=False).count()
            comments = attr.comments.filter(status='APPROVED', is_deleted=False)
            avg_rating = comments.aggregate(avg=Avg('rating'))['avg'] or 0

            hot_score = (view_count * 0.2) + (comment_count * 0.3) + (avg_rating * view_count * 0.5)

            result.append({
                'id': attr.id,
                'name': attr.name,
                'cover_image': attr.cover_image.url if attr.cover_image else None,
                'category': attr.category,
                'region': attr.region,
                'view_count': view_count,
                'comment_count': comment_count,
                'avg_rating': round(avg_rating, 1),
                'hot_score': round(hot_score, 1)
            })

        # 按热度值降序排序，取前10
        result.sort(key=lambda x: x['hot_score'], reverse=True)
        result = result[:10]

        return Response({
            'code': 0,
            'data': result,
            'total': len(result)
        })


class MonthlyReportView(APIView):
    """月度数据统计"""
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        responses=MonthlyDataSerializer(many=True)
    )
    def get(self, request):
        """获取月度数据报告"""
        # 获取最近6个月的数据
        from datetime import timedelta

        now = timezone.now()
        months_data = []

        for i in range(5, -1, -1):
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if i > 0:
                month_start = month_start - timedelta(days=1)
                month_start = month_start.replace(day=1)

            month_end = month_start + timedelta(days=32)
            month_end = month_end.replace(day=1)

            month_name = month_start.strftime('%Y-%m')

            new_users = UserProfile.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()

            new_attractions = Attraction.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()

            new_comments = Comment.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()

            months_data.append({
                'month': month_name,
                'new_users': new_users,
                'new_attractions': new_attractions,
                'new_comments': new_comments
            })

        return Response({
            'code': 0,
            'data': months_data,
            'total': len(months_data)
        })


class DashboardView(APIView):
    """数据看板"""
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        responses=DashboardSerializer
    )
    def get(self, request):
        """获取看板数据汇总"""
        from datetime import timedelta

        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # 基础统计
        total_users = UserProfile.objects.filter(is_deleted=False).count()
        total_attractions = Attraction.objects.filter(is_deleted=False).count()
        total_comments = Comment.objects.filter(is_deleted=False).count()
        # 总浏览量（所有景点的浏览次数之和）
        total_views = Attraction.objects.filter(is_deleted=False).aggregate(
            total=Sum('view_count')
        )['total'] or 0

        # 本月新增
        monthly_new_users = UserProfile.objects.filter(
            created_at__gte=month_start
        ).count()
        monthly_new_attractions = Attraction.objects.filter(
            created_at__gte=month_start
        ).count()
        monthly_new_comments = Comment.objects.filter(
            created_at__gte=month_start
        ).count()

        data = {
            'total_users': total_users,
            'total_attractions': total_attractions,
            'total_comments': total_comments,
            'total_views': total_views,
            'monthly_new_users': monthly_new_users,
            'monthly_new_attractions': monthly_new_attractions,
            'monthly_new_comments': monthly_new_comments
        }

        return Response({
            'code': 0,
            'data': data
        })


class UserManageView(APIView):
    """用户管理列表"""
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        responses=UserManageSerializer(many=True)
    )
    def get(self, request):
        """获取所有用户列表（分页）"""
        queryset = UserProfile.objects.filter(is_deleted=False)

        # 搜索
        keyword = request.query_params.get('keyword', '')
        if keyword:
            queryset = queryset.filter(
                Q(username__icontains=keyword) |
                Q(real_name__icontains=keyword) |
                Q(email__icontains=keyword)
            )

        # 筛选
        role = request.query_params.get('role', '')
        if role:
            queryset = queryset.filter(role=role)

        is_active = request.query_params.get('is_active', '')
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')

        # 排序
        ordering = request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        users = queryset[start:end]

        serializer = UserManageSerializer(users, many=True)

        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total
        })


class UserStatusView(APIView):
    """用户状态管理"""
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=UserStatusSerializer,
        responses=UserManageSerializer
    )
    def put(self, request, user_id):
        """启用/禁用用户"""
        try:
            user = UserProfile.objects.get(id=user_id, is_deleted=False)
        except UserProfile.DoesNotExist:
            return Response({
                'code': -1,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.is_active = serializer.validated_data['is_active']
        user.save()

        return Response({
            'code': 0,
            'message': '用户状态更新成功',
            'data': UserManageSerializer(user).data
        })
