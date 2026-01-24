from rest_framework import serializers


class DepartmentStatsSerializer(serializers.Serializer):
    """部门统计序列化器"""
    department_id = serializers.IntegerField()
    department_name = serializers.CharField()
    employee_count = serializers.IntegerField()


class MonthlyTrendSerializer(serializers.Serializer):
    """月度趋势序列化器"""
    month = serializers.CharField()
    count = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class DashboardStatsSerializer(serializers.Serializer):
    """仪表盘统计数据序列化器"""

    # 核心指标
    total_employees = serializers.IntegerField(
        label="在职员工总数",
        help_text="当前状态为 active 的员工总数"
    )
    new_hires_this_month = serializers.IntegerField(
        label="本月入职人数",
        help_text="本月新入职的员工数量"
    )
    resigned_this_month = serializers.IntegerField(
        label="本月离职人数",
        help_text="本月办理离职的员工数量"
    )
    total_salary_this_month = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        label="本月薪资总额",
        help_text="本月已发布薪资记录的总和"
    )

    # 分布数据
    department_distribution = DepartmentStatsSerializer(
        many=True,
        label="部门人数分布",
        help_text="各部门在职员工数量"
    )

    # 趋势数据
    salary_trend = MonthlyTrendSerializer(
        many=True,
        label="近6月薪资趋势",
        help_text="最近6个月的薪资发放趋势"
    )
