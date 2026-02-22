from rest_framework import serializers

from .models import ProtectionRule


class ProtectionRuleSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(
        max_length=100,
        error_messages={
            "required": "请输入规则名称",
            "blank": "规则名称不能为空",
            "max_length": "规则名称长度不能超过100字"
        }
    )
    min_aqi = serializers.IntegerField(
        error_messages={
            "required": "请输入AQI最小值",
            "invalid": "AQI最小值格式错误，请输入整数"
        }
    )
    max_aqi = serializers.IntegerField(
        error_messages={
            "required": "请输入AQI最大值",
            "invalid": "AQI最大值格式错误，请输入整数"
        }
    )
    population_type = serializers.ChoiceField(
        choices=ProtectionRule.PopulationType.choices,
        error_messages={
            "required": "请选择人群类型",
            "invalid_choice": "人群类型无效，可选值：GENERAL、CHILDREN、ELDERLY、PATIENTS、SENSITIVE"
        }
    )
    advice = serializers.CharField(
        error_messages={"required": "请输入防护建议", "blank": "防护建议不能为空"}
    )
    is_enabled = serializers.BooleanField(
        required=False,
        error_messages={"invalid": "启用状态格式错误"}
    )

    class Meta:
        model = ProtectionRule
        fields = [
            "id",
            "rule_name",
            "min_aqi",
            "max_aqi",
            "population_type",
            "advice",
            "is_enabled",
        ]
