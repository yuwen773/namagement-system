from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.airquality.models import AirQualityData, City, MonitoringStation, Province
from apps.rules.models import ProtectionRule


class ProtectionGuideAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        province = Province.objects.create(code="310000", name="Shanghai", level="PROVINCE")
        self.city = City.objects.create(
            code="310100",
            name="Shanghai City",
            province=province,
            longitude="121.473700",
            latitude="31.230400",
        )
        station = MonitoringStation.objects.create(
            code="SH001",
            name="Shanghai Station",
            city=self.city,
            address="SH",
            station_type="URBAN",
        )

        latest = timezone.now().replace(minute=0, second=0, microsecond=0)
        for idx in range(24):
            AirQualityData.objects.create(
                station=station,
                monitor_time=latest - timedelta(hours=23 - idx),
                aqi=80 + idx,
                pm25=40 + idx,
                pm10=60 + idx,
                so2=8 + idx / 10,
                no2=18 + idx / 10,
                co=1.0 + idx / 100,
                o3=70 + idx,
            )

        ProtectionRule.objects.create(
            rule_name="General 101-150",
            min_aqi=101,
            max_aqi=150,
            population_type=ProtectionRule.PopulationType.GENERAL,
            advice="普通人群建议减少户外运动。",
            is_enabled=True,
        )
        ProtectionRule.objects.create(
            rule_name="Sensitive 101-150",
            min_aqi=101,
            max_aqi=150,
            population_type=ProtectionRule.PopulationType.SENSITIVE,
            advice="敏感人群建议避免外出。",
            is_enabled=True,
        )
        ProtectionRule.objects.create(
            rule_name="Children 101-150",
            min_aqi=101,
            max_aqi=150,
            population_type=ProtectionRule.PopulationType.CHILDREN,
            advice="儿童建议佩戴口罩并减少户外活动。",
            is_enabled=True,
        )
        ProtectionRule.objects.create(
            rule_name="Elderly 101-150",
            min_aqi=101,
            max_aqi=150,
            population_type=ProtectionRule.PopulationType.ELDERLY,
            advice="老年人建议避免高强度活动。",
            is_enabled=True,
        )
        ProtectionRule.objects.create(
            rule_name="Patients 101-150",
            min_aqi=101,
            max_aqi=150,
            population_type=ProtectionRule.PopulationType.PATIENTS,
            advice="呼吸道患者建议尽量居家。",
            is_enabled=True,
        )

    def test_protection_guide_returns_current_advice_and_forecast(self):
        resp = self.client.get(f"/api/protection-guide/?city_code={self.city.code}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["code"], 200)
        self.assertEqual(resp.data["data"]["city"]["city_code"], self.city.code)
        self.assertIn("advice", resp.data["data"])
        self.assertIn("forecast", resp.data["data"])
        self.assertIn(resp.data["data"]["forecast"]["trend"], {"RISING", "FALLING", "STABLE"})

    def test_protection_guide_invalid_city_returns_404(self):
        resp = self.client.get("/api/protection-guide/?city_code=999999")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data["code"], 404)


class ProtectionRuleManageAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="rule_admin",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=self.admin)
        self.rule = ProtectionRule.objects.create(
            rule_name="General 0-50",
            min_aqi=0,
            max_aqi=50,
            population_type=ProtectionRule.PopulationType.GENERAL,
            advice="空气质量优，正常活动。",
            is_enabled=True,
        )
        self.rule_2 = ProtectionRule.objects.create(
            rule_name="General 51-100",
            min_aqi=51,
            max_aqi=100,
            population_type=ProtectionRule.PopulationType.GENERAL,
            advice="空气质量良，适量活动。",
            is_enabled=True,
        )

    def test_rule_manage_crud_and_batch_enable(self):
        list_resp = self.client.get("/api/admin/rules/")
        self.assertEqual(list_resp.status_code, 200)
        self.assertGreaterEqual(len(list_resp.data["data"]), 2)

        create_resp = self.client.post(
            "/api/admin/rules/",
            data={
                "rule_name": "Sensitive 0-50",
                "min_aqi": 0,
                "max_aqi": 50,
                "population_type": ProtectionRule.PopulationType.SENSITIVE,
                "advice": "敏感人群可正常活动。",
                "is_enabled": True,
            },
            format="json",
        )
        self.assertEqual(create_resp.status_code, 200)
        created_id = create_resp.data["data"]["id"]

        update_resp = self.client.put(
            "/api/admin/rules/",
            data={"id": created_id, "advice": "敏感人群建议减少户外停留。"},
            format="json",
        )
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.data["data"]["advice"], "敏感人群建议减少户外停留。")

        batch_resp = self.client.put(
            "/api/admin/rules/",
            data={"ids": [self.rule.id, self.rule_2.id], "is_enabled": False},
            format="json",
        )
        self.assertEqual(batch_resp.status_code, 200)
        self.rule.refresh_from_db()
        self.rule_2.refresh_from_db()
        self.assertFalse(self.rule.is_enabled)
        self.assertFalse(self.rule_2.is_enabled)

        delete_resp = self.client.delete(
            "/api/admin/rules/",
            data={"id": created_id},
            format="json",
        )
        self.assertEqual(delete_resp.status_code, 200)
        self.assertFalse(ProtectionRule.objects.filter(id=created_id).exists())
