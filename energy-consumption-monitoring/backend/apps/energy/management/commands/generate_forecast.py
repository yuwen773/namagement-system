from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate 7/30 day energy forecasts into em_energy_forecasts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--horizons",
            type=str,
            default="7,30",
            help="comma separated horizons in days, default: 7,30",
        )
        parser.add_argument("--end-date", type=str, default=None, help="anchor end date (YYYY-MM-DD)")
        parser.add_argument("--model-version", type=str, default="linear-v1")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        repo_root = self._resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        from scripts.generate_forecast import generate_forecast

        horizon_values = tuple(
            sorted(
                {
                    int(item.strip())
                    for item in str(options.get("horizons") or "").split(",")
                    if item.strip().isdigit()
                }
            )
        )
        if not horizon_values:
            horizon_values = (7, 30)

        end_date = self._parse_date(options.get("end_date"))
        result = generate_forecast(
            horizons=horizon_values,
            end_date=end_date,
            model_version=str(options.get("model_version") or "linear-v1"),
            dry_run=bool(options.get("dry_run")),
        )
        self.stdout.write(self.style.SUCCESS("generate_forecast completed"))
        self.stdout.write(
            f"target_groups={result.target_groups} "
            f"generated_points={result.generated_points} skipped_groups={result.skipped_groups}"
        )

    @staticmethod
    def _resolve_repo_root() -> Path:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if parent.name == "backend":
                return parent.parent
        return current.parents[6]

    @staticmethod
    def _parse_date(raw: str | None) -> date | None:
        if not raw:
            return None
        return date.fromisoformat(raw)
