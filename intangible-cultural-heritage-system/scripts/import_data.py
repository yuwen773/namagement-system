from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _bootstrap_django() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]
    backend_path = repo_root / "backend"

    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "heritage_system.settings")

    import django

    django.setup()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Offline data import for heritage/inheritor datasets."
    )
    parser.add_argument("--file", required=True, help="CSV/XLS/XLSX file path.")
    parser.add_argument(
        "--type",
        required=True,
        choices=["heritage", "inheritor"],
        help="Dataset type.",
    )
    parser.add_argument(
        "--default-level",
        help="Fallback level when source row has no level value.",
    )
    parser.add_argument(
        "--default-country",
        help="Fallback country name when source row has no country value.",
    )
    parser.add_argument(
        "--user",
        help="Existing username for ImportJob.created_by (commit mode only).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for error persistence (default: 100).",
    )
    parser.add_argument(
        "--error-output",
        help="Optional path for row-level error CSV report.",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--dry-run", action="store_true", help="Validate only.")
    mode_group.add_argument("--commit", action="store_true", help="Write data to DB.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    _bootstrap_django()

    from django.contrib.auth import get_user_model

    from apps.importer.services import OfflineImporterService

    created_by = None
    if args.user:
        user_model = get_user_model()
        created_by = user_model.objects.filter(username=args.user).first()
        if created_by is None:
            print(f"Unknown user: {args.user}", file=sys.stderr)
            return 2

    importer = OfflineImporterService(
        file_path=args.file,
        dataset_type=args.type,
        commit=args.commit,
        created_by=created_by,
        default_level=args.default_level,
        default_country=args.default_country,
        batch_size=args.batch_size,
        error_output=args.error_output,
    )

    try:
        result = importer.run()
    except Exception as error:
        print(f"Import failed: {error}", file=sys.stderr)
        return 1

    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
