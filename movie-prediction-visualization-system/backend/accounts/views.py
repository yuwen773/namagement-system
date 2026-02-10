from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsAdmin, IsUserOrAdmin


class RegisterView(APIView):
    """用户注册接口"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'code': 0,
                'message': '注册成功',
                'data': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录接口"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 0,
                'message': '登录成功',
                'data': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': UserSerializer(user).data
                }
            })
        return Response({
            'code': -1,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """获取/更新当前用户信息"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取当前用户信息"""
        serializer = UserProfileSerializer(request.user)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def put(self, request):
        """更新当前用户信息"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 0,
                'message': '信息更新成功',
                'data': serializer.data
            })
        return Response({
            'code': -1,
            'message': '信息更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """修改密码接口"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not request.user.check_password(old_password):
                return Response({
                    'code': -1,
                    'message': '原密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)

            request.user.set_password(new_password)
            request.user.save()
            return Response({
                'code': 0,
                'message': '密码修改成功'
            })
        return Response({
            'code': -1,
            'message': '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集（管理员专用）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        """获取用户列表"""
        queryset = self.get_queryset()
        # 支持按用户名搜索
        username = request.query_params.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)
        # 支持按角色筛选
        role = request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        # 支持按状态筛选
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        """禁用用户"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 已禁用'
        })

    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        """启用用户"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 已启用'
        })

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        user = self.get_object()
        new_password = request.data.get('new_password', '123456')
        user.set_password(new_password)
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 密码已重置为: {new_password}'
        })
