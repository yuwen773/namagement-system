# Offline Data Import

This directory contains one-off import tooling that does not require any web UI.

## Command

Run from repository root:

```bash
python scripts/import_data.py --file <path> --type heritage --dry-run
python scripts/import_data.py --file <path> --type heritage --commit
python scripts/import_data.py --file <path> --type inheritor --commit
```

## Supported Input

- CSV (`.csv`)
- Excel (`.xls`, `.xlsx`)

## Key Options

- `--dry-run`: validate and report without writing business data.
- `--commit`: write data into database and record `ImportJob`/`ImportError`.
- `--default-level`: fallback level when source rows omit level.
- `--default-country`: fallback country when source rows omit country.
- `--user`: bind import job to an existing username.
- `--error-output`: explicit path for error report CSV.

The command prints a JSON summary including total rows, success/error counts, created/updated counts, and optional error report path.
