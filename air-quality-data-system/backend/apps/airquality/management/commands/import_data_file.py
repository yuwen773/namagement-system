import os
import uuid
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.logs.models import ImportTask
from utils.data_importer import run_import_task


class Command(BaseCommand):
    help = "Import a CSV/Excel file into the database using the Phase 1.3 importer."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Path to the file to import")
        parser.add_argument(
            "--dataset-type",
            default="air_quality_data",
            choices=["provinces", "cities", "stations", "air_quality_data"],
            help="Dataset type template to apply",
        )
        parser.add_argument(
            "--username",
            default="",
            help="Initiator username (defaults to the first superuser if omitted)",
        )

    def handle(self, *args, **options):
        file_path = Path(options["file"]).expanduser().resolve()
        if not file_path.exists():
            self.stderr.write(f"File not found: {file_path}")
            return 1

        dataset_type = options["dataset_type"]
        username = (options["username"] or "").strip()

        User = get_user_model()
        if username:
            initiator = User.objects.filter(username=username).first()
        else:
            initiator = User.objects.filter(is_superuser=True).order_by("id").first()
        if not initiator:
            self.stderr.write("No initiator user found (create a superuser first).")
            return 1

        task_id = uuid.uuid4().hex
        ImportTask.objects.create(
            task_id=task_id,
            file_name=os.path.basename(str(file_path)),
            file_type=dataset_type,
            status=ImportTask.Status.PENDING,
            total_count=0,
            success_count=0,
            failed_count=0,
            initiator=initiator,
            end_time=None,
        )

        self.stdout.write(f"Starting import task: {task_id} ({dataset_type})")
        run_import_task(task_id=task_id, dataset_type=dataset_type, file_path=str(file_path))
        task = ImportTask.objects.get(task_id=task_id)
        self.stdout.write(
            f"Done. status={task.status} total={task.total_count} success={task.success_count} failed={task.failed_count}"
        )
        return 0

