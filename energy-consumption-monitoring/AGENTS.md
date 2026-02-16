# Repository Guidelines

## Project Structure & Module Organization
This repository is currently documentation-and-data first.
- `memory-bank/`: core product/architecture docs (`PRD.md`, `architecture.md`, `implementation-plan.md`, `tech-stack.md`).
- `dataSource/`: CSV datasets used for import and analysis (for example `building_consumption.csv`, `events.csv`).
- `CLAUDE.md`: implementation conventions and target architecture.

Planned runtime modules (per project docs): `backend/` (Django + DRF), `frontend/` (Vue 3 + Vite), `sql/` (schema/init scripts), and `scripts/` (data import/processing).

## Build, Test, and Development Commands
Use these once app modules are present:
- `cd backend && python manage.py runserver`: start Django API locally.
- `cd backend && python manage.py migrate`: apply DB migrations.
- `cd backend && python manage.py createsuperuser`: create admin account.
- `cd frontend && npm run dev`: start Vue dev server.
- `cd frontend && npm run build`: create production frontend build.

Data workflow examples:
- `python manage.py import_energy_data <file_path>`
- `python manage.py generate_statistics`

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indentation, `snake_case` for functions/fields/modules.
- Vue/JS: `camelCase` for variables/functions, `PascalCase` for components (for example `AdminLayout.vue`).
- API and DB fields should remain `snake_case` for consistency.
- Keep app boundaries clear (`accounts`, `buildings`, `devices`, `energy`, `analysis`, `alarms`, `system`).

## Testing Guidelines
- Backend: `pytest` + `pytest-django`.
- Frontend: `vitest` for unit tests; `playwright` or `cypress` for key E2E flows.
- Recommended baseline: backend coverage >= 80%, plus passing E2E for login, import, analysis, and alarm handling.

## Commit & Pull Request Guidelines
Follow Conventional Commits, as used in history: `feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `chore:`.
Examples:
- `feat: add energy statistics endpoint`
- `fix: correct building tree filter`

PRs should include:
- Clear scope and affected modules.
- Linked issue/task.
- Test evidence (command output or screenshots for UI/API).
- Migration/DB impact notes when schema or import logic changes.

## Security & Configuration Tips
- Never commit secrets, `.env` files, or production dumps.
- Validate large CSV inputs before import.
- Keep MySQL charset as `utf8mb4` and document any config changes in `memory-bank/progress.md`.

## Agent-Specific Instructions
- Backend implementation work must use the `python-data-analysis-backend` skill.
