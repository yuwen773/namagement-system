from rest_framework import serializers
from .models import ApprovalRequest


class ApprovalRequestSerializer(serializers.ModelSerializer):
    """审批请求详情序列化器"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    approver_name = serializers.CharField(source='approver.real_name', read_only=True)
    request_type_display = serializers.CharField(source='get_request_type_display', read_only=True)
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = [
            'id', 'user', 'user_name', 'request_type', 'request_type_display',
            'leave_type', 'leave_type_display', 'start_time', 'end_time',
            'reason', 'hours', 'status', 'status_display',
            'approver', 'approver_name', 'approver_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'approver', 'approver_reason', 'created_at', 'updated_at']


class ApprovalRequestListSerializer(serializers.ModelSerializer):
    """审批请求列表序列化器（轻量版）"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    request_type_display = serializers.CharField(source='get_request_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.real_name', read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = [
            'id', 'user', 'user_name', 'request_type', 'request_type_display',
            'leave_type', 'start_time', 'end_time', 'hours',
            'reason', 'status', 'status_display',
            'approver', 'approver_name', 'approver_reason',
            'created_at', 'updated_at'
        ]


class ApprovalRequestCreateSerializer(serializers.ModelSerializer):
    """创建审批请求序列化器"""

    class Meta:
        model = ApprovalRequest
        fields = [
            'request_type', 'leave_type', 'start_time', 'end_time',
            'reason', 'hours'
        ]

    def validate(self, data):
        """验证数据"""
        request_type = data.get('request_type')
        leave_type = data.get('leave_type')
        hours = data.get('hours')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # 请假申请必须选择请假类型
        if request_type == 'leave' and not leave_type:
            raise serializers.ValidationError({
                'leave_type': '请假申请必须选择请假类型'
            })

        # 加班申请必须填写加班时长
        if request_type == 'overtime' and not hours:
            raise serializers.ValidationError({
                'hours': '加班申请必须填写加班时长'
            })

        # 加班时长必须为正数
        if request_type == 'overtime' and hours and float(hours) <= 0:
            raise serializers.ValidationError({
                'hours': '加班时长必须大于 0'
            })

        # 结束时间必须晚于开始时间
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({
                'end_time': '结束时间必须晚于开始时间'
            })

        return data

    def create(self, validated_data):
        """创建时自动设置申请人为当前用户"""
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class ApprovalActionSerializer(serializers.Serializer):
    """审批操作序列化器"""
    approver_reason = serializers.CharField(required=False, allow_blank=True)
