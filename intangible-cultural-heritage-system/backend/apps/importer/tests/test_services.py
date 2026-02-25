import csv
import tempfile
from pathlib import Path

from django.test import TestCase

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.importer.models import ImportError, ImportJob
from apps.importer.services import OfflineImporterService
from apps.inheritors.models import Inheritor
from apps.regions.models import Region


class OfflineImporterServiceTests(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp_dir.name)

        self.category = Category.objects.create(
            name="Traditional Opera",
            code="CAT001",
            level=Category.LEVEL_NATIONAL,
        )
        self.region = Region.objects.create(
            country_code="CN",
            country_name="China",
            latitude="35.861700",
            longitude="104.195400",
            continent="Asia",
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def _write_csv(self, file_name, headers, rows):
        file_path = self.tmp_path / file_name
        with file_path.open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(headers)
            writer.writerows(rows)
        return file_path

    def test_heritage_dry_run_keeps_database_unchanged(self):
        csv_file = self._write_csv(
            "heritage_dry_run.csv",
            ["Name", "Category", "Level", "Country", "Description"],
            [
                ["Beijing Opera", "Traditional Opera", "national", "China", "A classic art"],
                ["Invalid Row", "", "national", "China", "missing category"],
            ],
        )
        error_file = self.tmp_path / "dry_run_errors.csv"

        result = OfflineImporterService(
            file_path=csv_file,
            dataset_type="heritage",
            commit=False,
            error_output=error_file,
        ).run()

        self.assertEqual(result.total_rows, 2)
        self.assertEqual(result.success_count, 1)
        self.assertEqual(result.error_count, 1)
        self.assertEqual(result.created_count, 1)
        self.assertEqual(result.updated_count, 0)
        self.assertEqual(HeritageItem.objects.count(), 0)
        self.assertTrue(error_file.exists())

    def test_heritage_commit_creates_job_data_and_error_log(self):
        csv_file = self._write_csv(
            "heritage_commit.csv",
            ["Name", "Category", "Level", "Country"],
            [
                ["Beijing Opera", "Traditional Opera", "national", "China"],
                ["Broken Heritage", "Traditional Opera", "national", ""],
            ],
        )
        error_file = self.tmp_path / "commit_errors.csv"

        result = OfflineImporterService(
            file_path=csv_file,
            dataset_type="heritage",
            commit=True,
            error_output=error_file,
        ).run()

        self.assertEqual(result.success_count, 1)
        self.assertEqual(result.error_count, 1)
        self.assertEqual(HeritageItem.objects.count(), 1)
        self.assertEqual(ImportJob.objects.count(), 1)
        self.assertEqual(ImportError.objects.count(), 1)
        self.assertEqual(ImportJob.objects.first().status, ImportJob.STATUS_COMPLETED)
        self.assertTrue(error_file.exists())

        rerun_file = self._write_csv(
            "heritage_rerun.csv",
            ["Name", "Category", "Level", "Country", "Description"],
            [["Beijing Opera", "Traditional Opera", "national", "China", "Updated description"]],
        )
        rerun_result = OfflineImporterService(
            file_path=rerun_file,
            dataset_type="heritage",
            commit=True,
        ).run()

        self.assertEqual(rerun_result.created_count, 0)
        self.assertEqual(rerun_result.updated_count, 1)
        self.assertEqual(HeritageItem.objects.count(), 1)

    def test_inheritor_commit_is_idempotent(self):
        heritage_item = HeritageItem.objects.create(
            name="Shadow Puppetry",
            category=self.category,
            level=HeritageItem.LEVEL_NATIONAL,
            region=self.region,
        )

        csv_file = self._write_csv(
            "inheritor_commit.csv",
            ["Name", "Heritage Name", "Country", "Gender", "Level"],
            [
                ["Li Ming", "Shadow Puppetry", "China", "male", "national"],
                ["Unknown", "Missing Heritage", "China", "male", "national"],
            ],
        )

        first_result = OfflineImporterService(
            file_path=csv_file,
            dataset_type="inheritor",
            commit=True,
        ).run()
        self.assertEqual(first_result.success_count, 1)
        self.assertEqual(first_result.error_count, 1)
        self.assertEqual(Inheritor.objects.count(), 1)
        self.assertEqual(Inheritor.objects.first().heritage_item, heritage_item)

        rerun_file = self._write_csv(
            "inheritor_rerun.csv",
            ["Name", "Heritage Name", "Country", "Gender", "Level", "Area"],
            [["Li Ming", "Shadow Puppetry", "China", "male", "national", "Sichuan"]],
        )
        second_result = OfflineImporterService(
            file_path=rerun_file,
            dataset_type="inheritor",
            commit=True,
        ).run()
        self.assertEqual(second_result.created_count, 0)
        self.assertEqual(second_result.updated_count, 1)
        self.assertEqual(Inheritor.objects.count(), 1)
        self.assertEqual(Inheritor.objects.first().area, "Sichuan")
