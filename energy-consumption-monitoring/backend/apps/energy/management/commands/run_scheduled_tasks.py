from __future__ import annotations

from pathlib import Path
import json
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run phase-6 scheduled tasks (hourly/daily/weekly), suitable for cron."

    def add_arguments(self, parser):
        parser.add_argument("--task", choices=["hourly", "daily", "weekly"], required=True)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        repo_root = self._resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        from scripts.scheduled_tasks import run_task

        result = run_task(task=options["task"], dry_run=bool(options.get("dry_run")))
        self.stdout.write(self.style.SUCCESS("scheduled task completed"))
        self.stdout.write(json.dumps({"task": result.task, "detail": result.detail}, ensure_ascii=False))

    @staticmethod
    def _resolve_repo_root() -> Path:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if parent.name == "backend":
                return parent.parent
        return current.parents[6]
