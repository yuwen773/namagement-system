from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import Comment, Favorite
from .serializers import CommentSerializer, CommentCreateSerializer, FavoriteSerializer, FavoriteCreateSerializer
from accounts.permissions import IsAdmin


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_deleted=False)
        attraction_id = self.kwargs.get('attraction_id')
        if attraction_id:
            queryset = queryset.filter(attraction_id=attraction_id, status='APPROVED')
        elif self.action == 'list' and self.request.user.role == 'ADMIN':
            status_filter = self.request.query_params.get('status')
            if status_filter and status_filter != 'all':
                queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, status='PENDING')
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '评论已提交，等待审核'
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
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
        queryset = Comment.objects.filter(user=request.user, is_deleted=False)
        serializer = CommentSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=False, methods=['get'], url_path='attraction/(?P<attraction_id>[^/.]+)')
    def attraction_list(self, request, attraction_id=None):
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
        if not request.user.role == 'ADMIN':
            return Response({
                'code': -1,
                'message': '无权限'
            }, status=status.HTTP_403_FORBIDDEN)
        comment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['APPROVED', 'REJECTED']:
            return Response({
                'code': -1,
                'message': '无效的状态'
            }, status=status.HTTP_400_BAD_REQUEST)
        comment.status = new_status
        comment.save()
        return Response({
            'code': 0,
            'message': '审核成功'
        })


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        queryset = self.get_queryset()
        serializer = FavoriteSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })
