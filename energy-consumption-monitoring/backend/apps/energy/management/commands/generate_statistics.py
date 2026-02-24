from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Statistics command entrypoint reserved for phase 6.1 implementation."

    def add_arguments(self, parser):
        parser.add_argument("--start-date", type=str, default=None, help="optional start date")
        parser.add_argument("--end-date", type=str, default=None, help="optional end date")
        parser.add_argument("--dry-run", action="store_true", help="run command without writing data")

    def handle(self, *args, **options):
        self.stdout.write("generate_statistics command is available.")
        self.stdout.write(
            self.style.WARNING(
                "Phase 6.1 statistic aggregation logic has not started yet. "
                "This command currently provides command-line scaffolding only."
            )
        )
        self.stdout.write(
            f"received options: start_date={options.get('start_date')} "
            f"end_date={options.get('end_date')} dry_run={options.get('dry_run')}"
        )

