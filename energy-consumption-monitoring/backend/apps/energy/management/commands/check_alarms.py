from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Alarm check command entrypoint reserved for phase 6.2 implementation."

    def add_arguments(self, parser):
        parser.add_argument("--device", type=str, default=None, help="optional device id/code filter")
        parser.add_argument("--dry-run", action="store_true", help="run command without writing alarm rows")

    def handle(self, *args, **options):
        self.stdout.write("check_alarms command is available.")
        self.stdout.write(
            self.style.WARNING(
                "Phase 6 alarm evaluation logic has not started yet. "
                "This command currently provides command-line scaffolding only."
            )
        )
        self.stdout.write(
            f"received options: device={options.get('device')} dry_run={options.get('dry_run')}"
        )

