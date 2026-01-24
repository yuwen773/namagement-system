from rest_framework import serializers
from .models import Department, Post


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器 - 基础版，支持嵌套展示"""
    parent_name = serializers.CharField(source="parent.name", read_only=True, allow_null=True)
    full_path = serializers.CharField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "code", "parent", "parent_name", "sort_order", "is_active", "full_path", "created_at", "updated_at"]
        extra_kwargs = {
            "parent": {"required": False, "allow_null": True}
        }


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
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "name", "code", "description", "sort_order", "is_active", "employee_count", "created_at", "updated_at"]

    def get_employee_count(self, obj):
        """获取关联的员工数量（后续 Employee 模型创建后启用）"""
        return 0
