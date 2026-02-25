from __future__ import annotations

from pathlib import Path
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Enhance demo data coverage for real-time power and building heatmap."

    def add_arguments(self, parser):
        parser.add_argument("--hours", type=int, default=72, help="how many recent hours to generate")
        parser.add_argument("--interval-minutes", type=int, default=15, help="sampling interval in minutes")
        parser.add_argument("--batch-size", type=int, default=2000, help="bulk insert batch size")

    def handle(self, *args, **options):
        repo_root = self._resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        from scripts.enhance_demo_data import enhance_demo_data

        result = enhance_demo_data(
            hours=int(options.get("hours") or 72),
            interval_minutes=int(options.get("interval_minutes") or 15),
            batch_size=int(options.get("batch_size") or 2000),
        )

        self.stdout.write(self.style.SUCCESS("enhance_demo_data completed"))
        self.stdout.write(
            f"created_floors={result.created_floors} "
            f"created_rooms={result.created_rooms} "
            f"created_devices={result.created_devices} "
            f"created_energy_rows={result.created_energy_rows} "
            f"updated_last_data_time={result.updated_last_data_time}"
        )

    @staticmethod
    def _resolve_repo_root() -> Path:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if parent.name == "backend":
                return parent.parent
        return current.parents[6]
