from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .models import UserProfile
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)


class RegisterView(APIView):
    """用户注册接口"""
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserProfileSerializer}
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'code': 0,
                'message': '注册成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'real_name': user.real_name,
                    'phone': user.phone,
                    'email': user.email,
                    'role': user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录接口"""
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: None}
    )
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
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'real_name': user.real_name,
                        'phone': user.phone,
                        'email': user.email,
                        'role': user.role,
                    }
                }
            })
        return Response({
            'code': -1,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """个人信息接口"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserProfileSerializer
    )
    def get(self, request):
        """获取当前用户信息"""
        serializer = UserProfileSerializer(request.user)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        request=UserUpdateSerializer,
        responses=UserProfileSerializer
    )
    def put(self, request):
        """更新当前用户信息"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 0,
                'message': '更新成功',
                'data': UserProfileSerializer(request.user).data
            })
        return Response({
            'code': -1,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """修改密码接口"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: None}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # 验证旧密码
            if not request.user.check_password(old_password):
                return Response({
                    'code': -1,
                    'message': '原密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 更新密码
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


class DeleteAccountView(APIView):
    """账号注销接口"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: None}
    )
    def delete(self, request):
        """逻辑删除当前用户"""
        user = request.user
        user.is_deleted = True
        user.is_active = False
        user.save()

        return Response({
            'code': 0,
            'message': '账号注销成功'
        })
