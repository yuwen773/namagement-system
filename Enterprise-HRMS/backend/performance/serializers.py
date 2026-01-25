from rest_framework import serializers
from .models import PerformanceReview, PerformanceTemplate


class PerformanceReviewSerializer(serializers.ModelSerializer):
    """绩效评估详情序列化器"""
    employee_name = serializers.CharField(source='employee.real_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.real_name', read_only=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            'id', 'employee', 'employee_name', 'review_period',
            'reviewer', 'reviewer_name', 'score', 'strengths',
            'improvements', 'goals', 'status', 'status_text',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PerformanceReviewListSerializer(serializers.ModelSerializer):
    """绩效评估列表序列化器（轻量版）"""
    employee_name = serializers.CharField(source='employee.real_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.real_name', read_only=True, allow_null=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)
    # 截取内容显示
    strengths_short = serializers.CharField(source='strengths', read_only=True)
    improvements_short = serializers.CharField(source='improvements', read_only=True)
    goals_short = serializers.CharField(source='goals', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            'id', 'employee_name', 'review_period', 'reviewer_name',
            'score', 'status', 'status_text', 'created_at',
            'strengths_short', 'improvements_short', 'goals_short'
        ]


class PerformanceReviewCreateSerializer(serializers.ModelSerializer):
    """创建绩效评估序列化器"""

    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'review_period', 'score',
            'strengths', 'improvements', 'goals', 'status'
        ]

    def validate(self, attrs):
        # 检查同一员工同一评估周期是否已存在记录
        employee = attrs.get('employee')
        review_period = attrs.get('review_period')

        # 更新场景：如果存在重复则排除当前实例
        if self.instance:
            exists = PerformanceReview.objects.filter(
                employee=employee,
                review_period=review_period
            ).exclude(pk=self.instance.pk).exists()
        else:
            exists = PerformanceReview.objects.filter(
                employee=employee,
                review_period=review_period
            ).exists()

        if exists:
            raise serializers.ValidationError({
                'non_field_errors': [f'员工 {employee.real_name} 在周期 {review_period} 已存在绩效评估记录']
            })

        return attrs


class PerformanceReviewUpdateSerializer(serializers.ModelSerializer):
    """更新绩效评估序列化器（仅允许修改特定字段）"""

    class Meta:
        model = PerformanceReview
        fields = ['score', 'strengths', 'improvements', 'goals', 'status']


# ==================== PerformanceTemplate 序列化器 ====================

class PerformanceTemplateSerializer(serializers.ModelSerializer):
    """绩效模板详情序列化器"""
    total_weight = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceTemplate
        fields = [
            'id', 'name', 'description', 'is_active',
            'items', 'total_weight', 'items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_weight(self, obj):
        return obj.get_total_weight()

    def get_items_count(self, obj):
        return len(obj.items) if obj.items else 0


class PerformanceTemplateListSerializer(serializers.ModelSerializer):
    """绩效模板列表序列化器（轻量版）"""
    total_weight = serializers.SerializerMethodField()
    active_status = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceTemplate
        fields = [
            'id', 'name', 'description', 'is_active', 'active_status',
            'total_weight', 'created_at'
        ]

    def get_total_weight(self, obj):
        return obj.get_total_weight()

    def get_active_status(self, obj):
        return '启用' if obj.is_active else '停用'


class PerformanceTemplateCreateUpdateSerializer(serializers.ModelSerializer):
    """创建/更新绩效模板序列化器"""

    class Meta:
        model = PerformanceTemplate
        fields = ['name', 'description', 'is_active', 'items']

    def validate_items(self, value):
        """验证考核项权重总和不超过100"""
        total_weight = sum(item.get('weight', 0) for item in value)
        if total_weight > 100:
            raise serializers.ValidationError('考核项权重总和不能超过100')
        if total_weight < 100:
            # 给出警告但不阻止
            pass
        return value
