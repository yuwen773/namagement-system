from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from HRMS.permissions import IsHROrAdmin, IsEmployeeOrHROrAdmin
from .models import EmployeeProfile
from .serializers import (
    EmployeeListSerializer,
    EmployeeProfileSerializer,
    EmployeeProfileCreateSerializer,
    EmployeeProfileUpdateSerializer,
    BatchAssignSerializer,
)
from organization.models import Department


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    员工档案 ViewSet
    提供：list, retrieve, create, update, partial_update, destroy, pending, resign

    权限说明：
    - list, retrieve: 登录用户可访问（普通员工只能看自己）
    - create, update, partial_update, pending, resign: 仅 HR/Admin 可访问
    """
    queryset = EmployeeProfile.objects.select_related('user', 'department', 'post')
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsEmployeeOrHROrAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        if self.action == 'create':
            return EmployeeProfileCreateSerializer
        if self.action in ['update', 'partial_update']:
            return EmployeeProfileUpdateSerializer
        return EmployeeProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # 普通员工只能查看自己的记录
        if user.role == 'employee':
            queryset = queryset.filter(user=user)

        # 按状态筛选
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def check_permissions(self, request):
        """对敏感操作进行角色检查"""
        super().check_permissions(request)

        # 只有 HR/Admin 可以执行以下操作
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'pending', 'resign']:
            if request.user.role not in ['hr', 'admin']:
                self.permission_denied(request, message='权限不足，需要人事或管理员权限')

    def list(self, request, *args, **kwargs):
        """获取员工列表（支持分页和查询条件）"""
        # 普通员工只能查看自己
        if request.user.role == 'employee':
            queryset = self.get_queryset().filter(user=request.user)
        else:
            queryset = self.get_queryset()

        # 按状态筛选
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 按部门筛选
        department_id = request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        # 按岗位筛选
        post_id = request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        # 按关键词搜索（姓名/工号）
        keyword = request.query_params.get('keyword')
        if keyword:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(user__real_name__icontains=keyword) |
                Q(employee_no__icontains=keyword)
            )

        # 按入职日期范围筛选
        hire_date_start = request.query_params.get('hire_date_start')
        hire_date_end = request.query_params.get('hire_date_end')
        if hire_date_start:
            queryset = queryset.filter(hire_date__gte=hire_date_start)
        if hire_date_end:
            queryset = queryset.filter(hire_date__lte=hire_date_end)

        # 按待分配筛选（筛选待分配部门的员工）
        unassigned = request.query_params.get('unassigned')
        if unassigned in ['true', '1', 'yes']:
            queryset = queryset.filter(department__code='UNASSIGNED')

        # 分页
        total = queryset.count()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    def retrieve(self, request, *args, **kwargs):
        """获取员工详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """创建员工档案（入职办理）"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            'code': 0,
            'message': '入职办理成功',
            'data': EmployeeProfileSerializer(profile).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """更新员工档案"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 0,
            'message': '更新成功',
            'data': EmployeeProfileSerializer(instance).data
        })

    def destroy(self, request, *args, **kwargs):
        """删除员工档案（软删除，改为离职状态）"""
        instance = self.get_object()
        return Response({
            'code': 400,
            'message': '请使用离职接口处理员工离职'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """获取待入职用户列表（支持分页和查询条件）"""
        from accounts.models import User
        from django.db.models import Q

        # 查找没有 profile 的用户（排除管理员和人事账号）
        queryset = User.objects.filter(
            profile__isnull=True
        ).exclude(
            role__in=['admin', 'hr']
        ).order_by('-date_joined')

        # 按关键词搜索（姓名/用户名）
        keyword = request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(real_name__icontains=keyword) |
                Q(username__icontains=keyword)
            )

        # 按预期入职日期范围筛选（使用 date_joined 作为预期入职日期）
        hire_date_start = request.query_params.get('hire_date_start')
        hire_date_end = request.query_params.get('hire_date_end')
        if hire_date_start:
            queryset = queryset.filter(date_joined__date__gte=hire_date_start)
        if hire_date_end:
            queryset = queryset.filter(date_joined__date__lte=hire_date_end)

        # 分页
        total = queryset.count()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        return Response({
            'code': 0,
            'data': [{
                'id': user.id,
                'username': user.username,
                'real_name': user.real_name,
                'phone': user.phone,
                'email': user.email,
                'date_joined': user.date_joined,
            } for user in queryset],
            'total': total,
            'page': page,
            'page_size': page_size
        })

    @action(detail=True, methods=['post'])
    def resign(self, request, pk=None):
        """
        员工离职办理
        POST /api/employee/{id}/resign/
        请求体：{ resigned_date: '2024-01-31', resigned_reason: '个人原因' }
        """
        instance = self.get_object()

        # 验证员工状态
        if instance.status == 'resigned':
            return Response({
                'code': 400,
                'message': '该员工已离职'
            }, status=status.HTTP_400_BAD_REQUEST)

        resigned_date = request.data.get('resigned_date')
        resigned_reason = request.data.get('resigned_reason', '')

        if not resigned_date:
            return Response({
                'code': 400,
                'message': '请填写离职日期'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新员工状态
        instance.status = 'resigned'
        instance.resigned_date = resigned_date
        instance.resigned_reason = resigned_reason
        instance.save()

        # 禁用关联的用户账号
        instance.user.is_active = False
        instance.user.save()

        return Response({
            'code': 0,
            'message': '离职办理成功',
            'data': EmployeeProfileSerializer(instance).data
        })

    @action(detail=False, methods=['post'], permission_classes=[IsHROrAdmin])
    def batch_assign(self, request):
        """
        批量分配部门和岗位
        POST /api/employee/batch_assign/
        请求体：{
            "employee_ids": [1, 2, 3],
            "department_id": 5,
            "post_id": 10
        }
        """
        serializer = BatchAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee_ids = serializer.validated_data['employee_ids']
        department = serializer.validated_data['department_id']
        post = serializer.validated_data.get('post_id')

        with transaction.atomic():
            # 查询待分配员工
            employees = EmployeeProfile.objects.filter(
                id__in=employee_ids
            ).select_for_update()

            updated_count = 0
            failed_employees = []

            for emp in employees:
                try:
                    # 更新部门和岗位
                    emp.department = department
                    emp.post = post
                    # 重新生成工号
                    emp.employee_no = self._generate_employee_no(department)
                    emp.save()
                    updated_count += 1
                except Exception as e:
                    failed_employees.append({
                        'id': emp.id,
                        'name': emp.user.real_name,
                        'error': str(e)
                    })

            return Response({
                'code': 0,
                'message': f'成功分配 {updated_count} 名员工',
                'data': {
                    'updated_count': updated_count,
                    'failed_count': len(failed_employees),
                    'failed_employees': failed_employees
                }
            })

    def _generate_employee_no(self, department):
        """生成工号"""
        from django.utils import timezone
        year_month = timezone.now().strftime('%Y%m')
        dept_code = department.code.upper() if department.code else 'UNK'
        prefix = f"EMP{year_month}{dept_code}"

        existing = EmployeeProfile.objects.filter(
            employee_no__startswith=prefix
        ).order_by('-employee_no')

        first = existing.first()
        if first:
            last_seq = int(first.employee_no[-3:])
            new_seq = last_seq + 1
        else:
            new_seq = 1

        return f"{prefix}{new_seq:03d}"

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        获取当前用户的员工档案
        GET /api/employee/me/
        返回当前登录用户的员工档案信息（包含部门和岗位）
        """
        try:
            instance = EmployeeProfile.objects.select_related('user', 'department', 'post').get(
                user=request.user
            )
            serializer = self.get_serializer(instance)
            return Response({
                'code': 0,
                'data': serializer.data
            })
        except EmployeeProfile.DoesNotExist:
            return Response({
                'code': 404,
                'message': '暂无员工档案，请联系人事部门办理入职'
            }, status=status.HTTP_404_NOT_FOUND)
