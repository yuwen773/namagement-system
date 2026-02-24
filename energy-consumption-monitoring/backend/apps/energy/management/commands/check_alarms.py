from __future__ import annotations

from pathlib import Path
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Evaluate alarm rules and create threshold/mutation/offline alarms."

    def add_arguments(self, parser):
        parser.add_argument("--device", type=str, default=None, help="optional device id/code filter")
        parser.add_argument(
            "--offline-minutes",
            type=int,
            default=120,
            help="offline window (minutes), default 120",
        )
        parser.add_argument(
            "--dedup-hours",
            type=int,
            default=6,
            help="duplicate suppression window (hours), default 6",
        )
        parser.add_argument("--dry-run", action="store_true", help="run command without writing alarm rows")

    def handle(self, *args, **options):
        repo_root = self._resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        from scripts.check_alarms import check_alarms

        result = check_alarms(
            device_filter=options.get("device"),
            dry_run=bool(options.get("dry_run")),
            offline_minutes=int(options.get("offline_minutes") or 120),
            dedup_window_hours=int(options.get("dedup_hours") or 6),
        )
        self.stdout.write(self.style.SUCCESS("check_alarms completed"))
        self.stdout.write(
            f"threshold={result.threshold_created} mutation={result.mutation_created} "
            f"offline={result.offline_created} skipped_duplicates={result.skipped_duplicates}"
        )

    @staticmethod
    def _resolve_repo_root() -> Path:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if parent.name == "backend":
                return parent.parent
        return current.parents[6]
