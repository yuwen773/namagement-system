# Repository Guidelines

## Project Structure & Module Organization
This repository currently contains planning and dataset assets for the Intangible Cultural Heritage system.

- `memory-bank/`: product and technical documents (`PRD.md`, import report, tech notes).
- `dataSource/`: raw source datasets (CSV/JSON/JSONL/SHP). Treat as input-only; do not edit in place.
- `.vscode/`: local editor settings.

When adding application code, keep a clear split:
- `backend/` for Django + DRF services.
- `frontend/` for Vue 3 + TypeScript UI.
- `scripts/` for one-off import/maintenance tooling.

## Build, Test, and Development Commands
Use project-local commands from each app directory.

- Backend setup: `cd backend && python -m venv .venv && pip install -r requirements.txt`
- Backend run: `cd backend && python manage.py runserver`
- Backend tests: `cd backend && pytest` (or `python manage.py test`)
- Frontend setup: `cd frontend && npm install`
- Frontend dev: `cd frontend && npm run dev`
- Frontend build/test: `cd frontend && npm run build && npm run test`

If a command is not available yet, add it in the relevant scaffold before opening a PR.

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indentation, `snake_case` for functions/modules, `PascalCase` for classes.
- TypeScript/Vue: 2-space indentation, `camelCase` for variables/functions, `PascalCase` for components (e.g., `HeritageTable.vue`).
- API routes should use kebab-case and versioning (e.g., `/api/v1/heritage-items`).
- Prefer small, focused modules; keep import pipelines deterministic and idempotent.

## Testing Guidelines
- Backend: pytest + Django test utilities; cover serializers, permissions, import validation, and dashboard aggregation.
- Frontend: component and page-flow tests for login, role-based routing, and dashboard rendering.
- Test file naming: `test_*.py` (backend), `*.spec.ts` (frontend).
- Add or update tests for every behavior change.

## Commit & Pull Request Guidelines
- Follow Conventional Commits as seen in history: `feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...`.
- Keep commits atomic; avoid mixing data updates with code refactors.
- PRs must include:
  - clear description of scope and affected paths,
  - linked issue/task (if any),
  - screenshots/GIFs for UI changes,
  - test evidence (commands + key results).

## Security & Data Handling
- Never commit secrets, `.env` files, or database dumps.
- Keep large raw files in `dataSource/`; store derived outputs in ignored directories (e.g., `exports/`, `tmp/`).
- Validate uploaded/imported files and log import errors with row-level context.
