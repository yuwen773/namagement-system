from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import Comment, Favorite
from .serializers import CommentSerializer, CommentCreateSerializer, FavoriteSerializer
from accounts.permissions import IsAdmin


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_deleted=False)
        # 景点评论列表（只显示已审核）
        attraction_id = self.kwargs.get('attraction_id')
        if attraction_id:
            queryset = queryset.filter(attraction_id=attraction_id, status='APPROVED')
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request):
        """发表评论"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, status='PENDING')
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '评论已提交，等待审核'
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """删除评论（只能删除自己的）"""
        comment = self.get_object()
        if comment.user != request.user:
            return Response({
                'code': -1,
                'message': '只能删除自己的评论'
            }, status=status.HTTP_403_FORBIDDEN)
        comment.is_deleted = True
        comment.save()
        return Response({
            'code': 0,
            'message': '删除成功'
        })

    @action(detail=False, methods=['get'])
    def my(self, request):
        """我的评论"""
        queryset = Comment.objects.filter(user=request.user, is_deleted=False)
        serializer = CommentSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=False, methods=['get'], url_path='attraction/(?P<attraction_id>[^/.]+)')
    def attraction_list(self, request, attraction_id=None):
        """指定景点的评论列表"""
        queryset = Comment.objects.filter(
            attraction_id=attraction_id,
            status='APPROVED',
            is_deleted=False
        )
        serializer = CommentSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=True, methods=['put'])
    def review(self, request, pk=None):
        """审核评论（管理员）"""
        if not request.user.role == 'ADMIN':
            return Response({
                'code': -1,
                'message': '无权限'
            }, status=status.HTTP_403_FORBIDDEN)
        comment = self.get_object()
        action_type = request.data.get('action')
        if action_type == 'approve':
            comment.status = 'APPROVED'
        elif action_type == 'reject':
            comment.status = 'REJECTED'
        else:
            return Response({
                'code': -1,
                'message': '无效操作'
            }, status=status.HTTP_400_BAD_REQUEST)
        comment.save()
        return Response({
            'code': 0,
            'message': '审核成功'
        })


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request):
        """添加收藏"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=request.user)
        except Exception:
            return Response({
                'code': -1,
                'message': '已收藏该景点'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '收藏成功'
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """取消收藏"""
        favorite = self.get_object()
        favorite.delete()
        return Response({
            'code': 0,
            'message': '取消成功'
        })

    @action(detail=False, methods=['get'])
    def my(self, request):
        """我的收藏"""
        queryset = self.get_queryset()
        serializer = FavoriteSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })
