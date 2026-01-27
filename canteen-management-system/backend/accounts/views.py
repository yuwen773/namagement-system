from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import User
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    UserListSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户账号视图集
    提供用户登录、注册、列表、详情、更新、删除等接口
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        """
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        用户登录接口
        POST /api/accounts/login/
        请求体：{"username": "admin", "password": "admin123"}
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.verify_password(username, password)
            if user:
                user_data = UserSerializer(user).data
                return Response({
                    'code': 200,
                    'message': '登录成功',
                    'data': user_data
                }, status=status.HTTP_200_OK)

            return Response({
                'code': 401,
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'code': 400,
            'message': '请求参数错误',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        用户注册接口
        POST /api/accounts/register/
        请求体：{"username": "test_user", "password": "123456", "phone": "13800138000", "email": "test@example.com"}
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # 创建新用户，默认角色为 EMPLOYEE
            user = User.objects.create(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],  # 开发阶段明文存储
                role=User.Role.EMPLOYEE,
                status=User.Status.ENABLED
            )
            user_data = UserSerializer(user).data
            return Response({
                'code': 201,
                'message': '注册成功',
                'data': user_data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'code': 400,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        用户列表接口（仅管理员）
        GET /api/accounts/users/
        """
        # TODO: 添加权限验证，只允许管理员访问
        serializer = UserListSerializer(self.queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """
        用户详情接口
        GET /api/accounts/users/{id}/
        """
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        创建用户接口（管理员）
        POST /api/accounts/users/
        请求体：{"username": "new_user", "password": "123456", "role": "EMPLOYEE", "employee_id": 1}
        """
        # TODO: 添加权限验证，只允许管理员访问
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 201,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'code': 400,
            'message': '创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        更新用户接口
        PUT /api/accounts/users/{id}/
        """
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': serializer.data
            })

        return Response({
            'code': 400,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        删除用户接口
        DELETE /api/accounts/users/{id}/
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'code': 200,
            'message': '删除成功'
        })
