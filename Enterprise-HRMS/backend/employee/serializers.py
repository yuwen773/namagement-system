from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

from .models import EmployeeProfile
from accounts.models import User
from organization.models import Department, Post


class EmployeeListSerializer(serializers.ModelSerializer):
    """员工列表序列化器（轻量版，仅显示关键字段）"""
    real_name = serializers.CharField(source='user.real_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    post_name = serializers.CharField(source='post.name', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'employee_no', 'real_name',
            'department_name', 'post_name',
            'hire_date', 'status'
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """员工档案详情序列化器"""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    real_name = serializers.CharField(source='user.real_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    post_name = serializers.CharField(source='post.name', read_only=True)
    department_path = serializers.CharField(source='get_full_path', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'user', 'user_id', 'username', 'real_name', 'phone', 'email',
            'employee_no', 'department', 'department_name', 'department_code',
            'post', 'post_name', 'department_path',
            'hire_date', 'salary_base', 'status',
            'resigned_date', 'resigned_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['employee_no', 'created_at', 'updated_at']


class EmployeeProfileCreateSerializer(serializers.ModelSerializer):
    """
    创建员工档案序列化器（入职办理）
    负责生成工号
    """
    user_id = serializers.IntegerField(write_only=True, required=True)
    user_real_name = serializers.CharField(source='user.real_name', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'user', 'user_id', 'user_real_name',
            'department', 'post', 'hire_date', 'salary_base',
            'status', 'resigned_date', 'resigned_reason'
        ]
        extra_kwargs = {
            'status': {'default': 'active'},
        }

    def validate_user(self, value):
        """验证用户存在且未关联档案"""
        if hasattr(value, 'profile'):
            raise serializers.ValidationError("该用户已关联员工档案")
        return value

    def validate_department(self, value):
        """验证部门存在且启用"""
        if not value.is_active:
            raise serializers.ValidationError("该部门已停用")
        return value

    def validate_post(self, value):
        """验证岗位存在且启用"""
        if not value.is_active:
            raise serializers.ValidationError("该岗位已停用")
        return value

    def validate_salary_base(self, value):
        """验证工资为正数"""
        if value < 0:
            raise serializers.ValidationError("基本工资不能为负数")
        return value

    def create(self, validated_data):
        """创建员工档案并生成工号"""
        with transaction.atomic():
            # 获取用户
            user_id = validated_data.pop('user_id')
            user = User.objects.get(id=user_id)

            # 生成工号：EMP{年月}{部门代码}{3位流水}
            employee_no = self._generate_employee_no(validated_data['department'])

            # 创建档案
            profile = EmployeeProfile.objects.create(
                user=user,
                employee_no=employee_no,
                **validated_data
            )

            return profile

    def _generate_employee_no(self, department):
        """
        生成唯一工号
        格式：EMP{年月}{部门代码}{3位流水}
        示例：EMP202401TECH001

        使用数据库事务 + SELECT FOR UPDATE 保证并发唯一
        """
        year_month = timezone.now().strftime('%Y%m')
        dept_code = department.code.upper() if department.code else 'UNK'
        prefix = f"EMP{year_month}{dept_code}"

        # 使用 SELECT FOR UPDATE 锁定行，保证并发安全
        existing_profiles = EmployeeProfile.objects.filter(
            employee_no__startswith=prefix
        ).select_for_update().order_by('-employee_no')

        first = existing_profiles.first()

        if first:
            # 提取现有最大流水号
            last_seq = int(first.employee_no[-3:])
            new_seq = last_seq + 1
        else:
            new_seq = 1

        return f"{prefix}{new_seq:03d}"
