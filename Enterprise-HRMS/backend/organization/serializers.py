from rest_framework import serializers
from .models import Department, Post


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器 - 基础版，支持嵌套展示"""
    parent_name = serializers.CharField(source="parent.name", read_only=True, allow_null=True)
    full_path = serializers.CharField(read_only=True)
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            "id", "name", "code", "parent", "parent_name", "sort_order",
            "is_active", "full_path", "post_count", "created_at", "updated_at"
        ]
        extra_kwargs = {
            "parent": {"required": False, "allow_null": True}
        }

    def get_post_count(self, obj):
        """获取岗位数量"""
        return obj.posts.filter(is_active=True).count()


class DepartmentTreeSerializer(serializers.ModelSerializer):
    """部门树形结构序列化器 - 递归嵌套子部门"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "code", "sort_order", "is_active", "children"]

    def get_children(self, obj):
        """递归获取子部门"""
        children = obj.children.filter(is_active=True)
        if children.exists():
            return DepartmentTreeSerializer(children, many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    """岗位序列化器"""
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_code = serializers.CharField(source="department.code", read_only=True)
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "name", "code", "department", "department_name", "department_code",
            "description", "sort_order", "is_active", "employee_count",
            "created_at", "updated_at"
        ]
        extra_kwargs = {
            "department": {"required": True}
        }

    def get_employee_count(self, obj):
        """获取关联的员工数量"""
        # 从上下文获取 EmployeeProfile 模型来计算
        try:
            from employee.models import EmployeeProfile
            return EmployeeProfile.objects.filter(post=obj, status='active').count()
        except ImportError:
            return 0
