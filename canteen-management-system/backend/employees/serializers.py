from rest_framework import serializers
from .models import EmployeeProfile


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """
    员工档案详情序列化器
    用于创建、更新、详情展示
    """
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'name', 'gender', 'gender_display', 'phone', 'id_card', 'address',
            'position', 'position_display', 'entry_date', 'status', 'status_display',
            'health_certificate_no', 'health_certificate_expiry', 'health_certificate_url',
            'chef_certificate_level', 'created_at', 'updated_at'
        ]

    def validate_id_card(self, value):
        """
        验证身份证号唯一性（更新时排除当前记录）
        """
        if value:
            instance = self.instance
            queryset = EmployeeProfile.objects.filter(id_card=value)
            if instance:
                queryset = queryset.exclude(id=instance.id)
            if queryset.exists():
                raise serializers.ValidationError('该身份证号已存在')
        return value


class EmployeeProfileListSerializer(serializers.ModelSerializer):
    """
    员工档案列表序列化器（简化版）
    用于列表展示，不包含详细信息
    """
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'name', 'gender', 'gender_display', 'phone',
            'position', 'position_display', 'entry_date', 'status', 'status_display',
            'created_at'
        ]
