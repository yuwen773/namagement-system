from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate day/month/year energy statistics into em_energy_statistics."

    def add_arguments(self, parser):
        parser.add_argument("--start-date", type=str, default=None, help="optional start date (YYYY-MM-DD)")
        parser.add_argument("--end-date", type=str, default=None, help="optional end date (YYYY-MM-DD)")
        parser.add_argument(
            "--period-types",
            type=str,
            default="DAY,MONTH,YEAR",
            help="comma separated period types: DAY,MONTH,YEAR",
        )
        parser.add_argument("--dry-run", action="store_true", help="run command without writing data")

    def handle(self, *args, **options):
        repo_root = self._resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        from scripts.generate_statistics import generate_statistics

        start_date = self._parse_date(options.get("start_date"))
        end_date = self._parse_date(options.get("end_date"))
        period_types = [
            token.strip().upper()
            for token in str(options.get("period_types") or "").split(",")
            if token.strip()
        ]
        if not period_types:
            period_types = ["DAY", "MONTH", "YEAR"]

        result = generate_statistics(
            start_date=start_date,
            end_date=end_date,
            dry_run=bool(options.get("dry_run")),
            period_types=period_types,
        )
        self.stdout.write(self.style.SUCCESS("generate_statistics completed"))
        self.stdout.write(
            f"scanned_groups={result.scanned_groups} created={result.created_count} "
            f"updated={result.updated_count} skipped={result.skipped_count}"
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
