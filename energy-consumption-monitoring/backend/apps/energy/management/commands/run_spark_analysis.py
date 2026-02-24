from __future__ import annotations

from pathlib import Path
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run optional Spark offline analysis (falls back to Python if PySpark is unavailable)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-file",
            type=str,
            default="tmp/reports/spark_offline_analysis.json",
            help="output file path",
        )

    def handle(self, *args, **options):
        repo_root = self._resolve_repo_root()
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)

        from scripts.spark_offline_analysis import run_spark_offline_analysis

        result = run_spark_offline_analysis(output_file=options["output_file"])
        self.stdout.write(self.style.SUCCESS("spark analysis completed"))
        self.stdout.write(
            f"mode={result.mode} rows_written={result.rows_written} output_path={result.output_path}"
        )

    @staticmethod
    def _resolve_repo_root() -> Path:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if parent.name == "backend":
                return parent.parent
        return current.parents[6]
