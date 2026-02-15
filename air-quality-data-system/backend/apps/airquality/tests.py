from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.airquality.models import AirQualityData, City, MonitoringStation, Province
from apps.logs.models import ImportTask


@override_settings(DATA_IMPORT_ASYNC=False)
class DataImportAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="admin",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )

    def test_upload_requires_admin(self):
        f = SimpleUploadedFile("provinces.csv", b"code,name,level\n110000,Beijing,PROVINCE\n")
        resp = self.client.post(
            "/api/admin/data-import/",
            data={"dataset_type": "provinces", "file": f},
            format="multipart",
        )
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.data["code"], 403)

    def test_upload_provinces_csv_success(self):
        self.client.force_authenticate(user=self.admin)
        f = SimpleUploadedFile("provinces.csv", b"code,name,level\n110000,Beijing,PROVINCE\n")
        resp = self.client.post(
            "/api/admin/data-import/",
            data={"dataset_type": "provinces", "file": f},
            format="multipart",
        )
        self.assertEqual(resp.status_code, 200)
        task_id = resp.data["data"]["task_id"]

        task = ImportTask.objects.get(task_id=task_id)
        self.assertEqual(task.status, ImportTask.Status.SUCCESS)
        self.assertEqual(task.total_count, 1)
        self.assertEqual(task.success_count, 1)
        self.assertEqual(task.failed_count, 0)
        self.assertEqual(Province.objects.count(), 1)

    def test_upload_air_quality_data_sets_quality_level(self):
        self.client.force_authenticate(user=self.admin)

        p = Province.objects.create(code="110000", name="Beijing", level="PROVINCE")
        c = City.objects.create(
            code="110100",
            name="Beijing City",
            province=p,
            longitude="116.407396",
            latitude="39.904200",
        )
        s = MonitoringStation.objects.create(
            code="S001",
            name="Station 1",
            city=c,
            address="Test address",
            station_type="URBAN",
        )

        csv = (
            "station_code,monitor_time,aqi,pm25\n"
            f"{s.code},2026-01-01 00:00:00,80,12.34\n"
        ).encode("utf-8")
        f = SimpleUploadedFile("airq.csv", csv)
        resp = self.client.post(
            "/api/admin/data-import/",
            data={"dataset_type": "air_quality_data", "file": f},
            format="multipart",
        )
        self.assertEqual(resp.status_code, 200)
        task_id = resp.data["data"]["task_id"]
        task = ImportTask.objects.get(task_id=task_id)
        self.assertEqual(task.status, ImportTask.Status.SUCCESS)

        rec = AirQualityData.objects.get(station=s)
        self.assertEqual(rec.aqi, 80)
        self.assertEqual(rec.quality_level, AirQualityData.QualityLevel.GOOD)
        self.assertTrue(timezone.is_aware(rec.monitor_time))


class UserAirQualityAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.province = Province.objects.create(code="110000", name="Beijing", level="PROVINCE")
        self.city_a = City.objects.create(
            code="110100",
            name="Beijing City",
            province=self.province,
            longitude="116.407396",
            latitude="39.904200",
        )
        self.city_b = City.objects.create(
            code="110200",
            name="Tianjin City",
            province=self.province,
            longitude="117.200000",
            latitude="39.133300",
        )
        self.station_a1 = MonitoringStation.objects.create(
            code="BJ001",
            name="Beijing Station 1",
            city=self.city_a,
            address="A1",
            station_type="URBAN",
        )
        self.station_a2 = MonitoringStation.objects.create(
            code="BJ002",
            name="Beijing Station 2",
            city=self.city_a,
            address="A2",
            station_type="URBAN",
        )
        self.station_b1 = MonitoringStation.objects.create(
            code="TJ001",
            name="Tianjin Station 1",
            city=self.city_b,
            address="B1",
            station_type="URBAN",
        )

        latest = timezone.now().replace(minute=0, second=0, microsecond=0)
        for i in range(24):
            monitor_time = latest - timedelta(hours=23 - i)
            AirQualityData.objects.create(
                station=self.station_a1,
                monitor_time=monitor_time,
                aqi=70 + i,
                pm25=30 + i,
                pm10=40 + i,
                so2=8 + i / 10,
                no2=20 + i / 2,
                co=1.2 + i / 100,
                o3=50 + i,
            )
            AirQualityData.objects.create(
                station=self.station_a2,
                monitor_time=monitor_time,
                aqi=60 + i,
                pm25=25 + i,
                pm10=35 + i,
                so2=7 + i / 10,
                no2=18 + i / 2,
                co=1.1 + i / 100,
                o3=48 + i,
            )
            AirQualityData.objects.create(
                station=self.station_b1,
                monitor_time=monitor_time,
                aqi=110 + i,
                pm25=60 + i,
                pm10=75 + i,
                so2=12 + i / 10,
                no2=30 + i / 2,
                co=1.6 + i / 100,
                o3=80 + i,
            )

    def test_overview_and_top_cities_api(self):
        overview_resp = self.client.get("/api/overview/")
        self.assertEqual(overview_resp.status_code, 200)
        self.assertEqual(overview_resp.data["code"], 200)
        self.assertIn("national", overview_resp.data["data"])
        self.assertGreaterEqual(overview_resp.data["data"]["city_count"], 2)

        top_resp = self.client.get("/api/overview/top-cities/?limit=2")
        self.assertEqual(top_resp.status_code, 200)
        self.assertEqual(len(top_resp.data["data"]["best"]), 2)
        self.assertEqual(len(top_resp.data["data"]["worst"]), 2)

    def test_city_and_station_detail_trend_api(self):
        city_resp = self.client.get(f"/api/cities/{self.city_a.code}/")
        self.assertEqual(city_resp.status_code, 200)
        self.assertEqual(city_resp.data["data"]["city_code"], self.city_a.code)
        self.assertIn("snapshot", city_resp.data["data"])

        city_trend_resp = self.client.get(f"/api/cities/{self.city_a.code}/trend/?hours=24")
        self.assertEqual(city_trend_resp.status_code, 200)
        self.assertGreaterEqual(len(city_trend_resp.data["data"]["trend"]), 1)

        station_resp = self.client.get(f"/api/stations/{self.station_a1.code}/")
        self.assertEqual(station_resp.status_code, 200)
        self.assertEqual(station_resp.data["data"]["station_code"], self.station_a1.code)

        station_trend_resp = self.client.get(f"/api/stations/{self.station_a1.code}/trend/?hours=24")
        self.assertEqual(station_trend_resp.status_code, 200)
        self.assertGreaterEqual(len(station_trend_resp.data["data"]["trend"]), 1)

        invalid_city_resp = self.client.get("/api/cities/999999/")
        self.assertEqual(invalid_city_resp.status_code, 404)
        invalid_station_resp = self.client.get("/api/stations/UNKNOWN/")
        self.assertEqual(invalid_station_resp.status_code, 404)

    def test_historical_data_and_analysis_api(self):
        history_resp = self.client.get(f"/api/historical-data/?city_code={self.city_a.code}&page=1&page_size=20")
        self.assertEqual(history_resp.status_code, 200)
        self.assertEqual(history_resp.data["code"], 200)
        self.assertIn("total", history_resp.data)

        export_resp = self.client.get(f"/api/historical-data/export/?city_code={self.city_a.code}&format=csv")
        self.assertEqual(export_resp.status_code, 200)
        self.assertIn("attachment;", export_resp["Content-Disposition"])

        compare_resp = self.client.post(
            "/api/analysis/compare/",
            data={"city_codes": [self.city_a.code, self.city_b.code], "hours": 24},
            format="json",
        )
        self.assertEqual(compare_resp.status_code, 200)
        self.assertEqual(len(compare_resp.data["data"]["series"]), 2)

        corr_resp = self.client.get(
            f"/api/analysis/correlation/?city_code={self.city_a.code}&pollutant_x=pm25&pollutant_y=pm10"
        )
        self.assertEqual(corr_resp.status_code, 200)
        self.assertIn("correlation", corr_resp.data["data"])

        distribution_resp = self.client.get(f"/api/analysis/distribution/?city_code={self.city_a.code}")
        self.assertEqual(distribution_resp.status_code, 200)
        self.assertIn("distribution", distribution_resp.data["data"])


class AdminDashboardAndAirQualityManageAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.admin = User.objects.create_user(
            username="admin_manage",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )
        self.user_active = User.objects.create_user(
            username="active_user",
            password="123456",
            is_staff=False,
            is_superuser=False,
        )
        self.user_deleted = User.objects.create_user(
            username="deleted_user",
            password="123456",
            is_staff=False,
            is_superuser=False,
            is_deleted=True,
            status=False,
        )
        now = timezone.now()
        User.objects.filter(id=self.user_active.id).update(last_login=now)
        User.objects.filter(id=self.user_deleted.id).update(last_login=now)

        self.province = Province.objects.create(code="120000", name="Tianjin", level="PROVINCE")
        self.city = City.objects.create(
            code="120100",
            name="Tianjin City",
            province=self.province,
            longitude="117.200000",
            latitude="39.133300",
        )
        self.station = MonitoringStation.objects.create(
            code="TJ-MANAGE-001",
            name="Manage Station",
            city=self.city,
            address="test",
            station_type="URBAN",
        )
        base_time = timezone.now().replace(minute=0, second=0, microsecond=0)
        self.record_1 = AirQualityData.objects.create(
            station=self.station,
            monitor_time=base_time - timedelta(hours=2),
            aqi=90,
            pm25=20,
            pm10=30,
            so2=4,
            no2=5,
            co=1,
            o3=45,
        )
        self.record_2 = AirQualityData.objects.create(
            station=self.station,
            monitor_time=base_time - timedelta(hours=1),
            aqi=110,
            pm25=21,
            pm10=31,
            so2=4,
            no2=5,
            co=1,
            o3=46,
        )
        self.record_3 = AirQualityData.objects.create(
            station=self.station,
            monitor_time=base_time,
            aqi=120,
            pm25=22,
            pm10=32,
            so2=4,
            no2=5,
            co=1,
            o3=47,
        )

        ImportTask.objects.create(
            task_id="task-dashboard-001",
            file_name="sample.csv",
            file_type="air_quality_data",
            status=ImportTask.Status.SUCCESS,
            total_count=100,
            success_count=100,
            failed_count=0,
            initiator=self.admin,
        )

        self.client.force_authenticate(user=self.admin)

    def test_admin_dashboard_api(self):
        resp = self.client.get("/api/admin/dashboard/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["code"], 200)
        self.assertEqual(resp.data["data"]["data_summary"]["total_data_count"], 3)
        self.assertEqual(resp.data["data"]["data_summary"]["covered_city_count"], 1)
        self.assertGreaterEqual(resp.data["data"]["user_summary"]["today_active_user_count"], 1)
        self.assertEqual(
            resp.data["data"]["latest_import_task"]["task_id"],
            "task-dashboard-001",
        )

    def test_air_quality_manage_list_update_and_delete(self):
        list_resp = self.client.get("/api/admin/air-quality/?page=1&page_size=20")
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(list_resp.data["total"], 3)

        update_resp = self.client.put(
            "/api/admin/air-quality/",
            data={"id": self.record_1.id, "aqi": 180, "pm25": 55.5},
            format="json",
        )
        self.assertEqual(update_resp.status_code, 200)
        self.record_1.refresh_from_db()
        self.assertEqual(self.record_1.aqi, 180)
        self.assertEqual(self.record_1.quality_level, AirQualityData.QualityLevel.MODERATE_POLLUTION)

        delete_resp = self.client.delete(
            "/api/admin/air-quality/",
            data={"id": self.record_2.id},
            format="json",
        )
        self.assertEqual(delete_resp.status_code, 200)
        self.assertFalse(AirQualityData.objects.filter(id=self.record_2.id).exists())

        batch_resp = self.client.delete(
            "/api/admin/air-quality/",
            data={"ids": [self.record_1.id, self.record_3.id]},
            format="json",
        )
        self.assertEqual(batch_resp.status_code, 200)
        self.assertEqual(AirQualityData.objects.count(), 0)
