from __future__ import annotations

import json
from pathlib import Path
import sys

from django.core.management.base import BaseCommand, CommandError


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "backend":
            return parent.parent
    return current.parents[5]


class Command(BaseCommand):
    help = "Import energy data from CSV/Excel/JSON with cleaning and chunked bulk import."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="source file path")
        parser.add_argument("--format", choices=["csv", "excel", "json"], default=None)
        parser.add_argument("--mode", choices=["orm", "api"], default="orm")
        parser.add_argument("--batch-size", type=int, default=None)
        parser.add_argument("--preview", type=int, default=None)
        parser.add_argument("--config", type=str, default=None)
        parser.add_argument("--api-base-url", type=str, default=None)
        parser.add_argument("--api-endpoint", type=str, default=None)
        parser.add_argument("--api-token", type=str, default=None)
        parser.add_argument("--checkpoint-file", type=str, default="tmp/import_checkpoint.json")
        parser.add_argument("--resume", action="store_true")
        parser.add_argument("--stop-on-error", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        repo_root = _resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        try:
            from scripts.data_importer import ImportExecutionOptions, run_import_job
        except Exception as exc:  # noqa: BLE001
            raise CommandError(f"Cannot import scripts.data_importer: {exc}") from exc

        source_path = Path(options["file_path"])
        if not source_path.exists():
            raise CommandError(f"file not found: {source_path}")

        execution_options = ImportExecutionOptions(
            file_path=source_path,
            file_format=options["format"],
            mode=options["mode"],
            batch_size=options["batch_size"],
            preview_rows=options["preview"],
            config_path=Path(options["config"]) if options["config"] else None,
            api_base_url=options["api_base_url"],
            api_endpoint=options["api_endpoint"],
            api_token=options["api_token"],
            checkpoint_file=Path(options["checkpoint_file"]),
            resume=bool(options["resume"]),
            continue_on_error=not bool(options["stop_on_error"]),
            dry_run=bool(options["dry_run"]),
        )

        clean_report, summary = run_import_job(execution_options)

        self.stdout.write(self.style.SUCCESS("import_energy_data finished"))
        self.stdout.write(f"clean_report={json.dumps(clean_report.to_dict(), ensure_ascii=False)}")
        self.stdout.write(f"summary={json.dumps(summary.to_dict(), ensure_ascii=False)}")

