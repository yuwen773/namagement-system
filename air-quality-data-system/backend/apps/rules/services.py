from __future__ import annotations

from apps.rules.models import ProtectionRule


class RuleMatcherService:
    default_messages = {
        ProtectionRule.PopulationType.GENERAL: "空气质量变化较快，请减少不必要户外活动并关注后续预警。",
        ProtectionRule.PopulationType.CHILDREN: "儿童建议减少户外活动，外出时佩戴防护口罩。",
        ProtectionRule.PopulationType.ELDERLY: "老年人建议避免剧烈活动，外出注意防护。",
        ProtectionRule.PopulationType.PATIENTS: "呼吸道疾病患者建议尽量居家，按医嘱做好健康管理。",
        ProtectionRule.PopulationType.SENSITIVE: "敏感人群建议减少外出并加强个人防护。",
    }

    def match(self, aqi: int, population_type: str) -> str:
        rule = (
            ProtectionRule.objects.filter(
                is_enabled=True,
                population_type=population_type,
                min_aqi__lte=aqi,
                max_aqi__gte=aqi,
            )
            .order_by("min_aqi", "id")
            .first()
        )
        if rule:
            return rule.advice
        return self.default_messages.get(
            population_type, "暂无匹配规则，请参考通用健康防护建议。"
        )
