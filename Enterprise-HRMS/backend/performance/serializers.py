from rest_framework import serializers
from .models import PerformanceReview


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
