# Repository Guidelines

## IMPORTANT (Agent Workflow)

- Before writing any code, read `memory-bank/architecture.md`, `memory-bank/PRD.md`, and `memory-bank/pre-prd.md`.
- When updating `memory-bank/architecture.md`, include the **entire database schema** (not partial snippets).
- After a major feature or milestone is completed, update `memory-bank/architecture.md` to reflect the new state.

## Project Structure & Module Organization

- `dataSource/`: Source datasets (CSV/XLS/XLSX). Treat these as **raw inputs**; avoid editing in-place.
- `memory-bank/`: Product/architecture documentation and the step-by-step build plan (see `memory-bank/implementation-plan.md` and `memory-bank/tech-stack.md`).

Planned (per `memory-bank/implementation-plan.md`):
- `backend/`: Django + Django REST Framework API, organized by apps under `backend/apps/` (e.g., `accounts/`, `airquality/`, `rules/`).
- `frontend/`: Vue 3 UI (Element Plus, ECharts, Tailwind CSS).

## Build, Test, and Development Commands

This repo currently contains data and design docs; application code may not exist yet. Once `backend/` and `frontend/` are added, prefer these conventions:

```powershell
# Backend (Django)
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

python manage.py migrate
python manage.py runserver

# Tests
python manage.py test
```

```powershell
# Frontend (Vue)
cd frontend
npm install
npm run dev
npm run build
```

## Coding Style & Naming Conventions

- Python: 4-space indentation; module/function names in `snake_case`.
- API/DB fields: use `snake_case` consistently (e.g., `is_deleted`).
- Files: keep dataset filenames stable; for derived data, use a suffix pattern like `*_clean.csv` or `*_processed.parquet` and add a short note in the PR.

## Testing Guidelines

- Backend: add tests alongside the relevant Django app (e.g., `backend/apps/airquality/tests/`).
- Minimum expectation: new endpoints, import/validation logic, and bug fixes must include a regression test.

## Commit & Pull Request Guidelines

- Commits follow a Conventional Commits-like pattern seen in history: `feat: ...`, `fix: ...`, `perf(backend): ...`, `refactor: ...`, `docs: ...`, `chore: ...`.
- PRs must include: purpose, affected paths (e.g., `dataSource/BeiJing/...`), and validation steps (commands run or data checks performed).
- Data changes: cite the source, explain transformations, and avoid committing database dumps or other large generated artifacts.

## Security & Configuration

- Do not commit secrets (DB passwords, API keys). Use environment variables or local-only config files.
- Any change to authentication or password handling must match the requirements captured in `memory-bank/implementation-plan.md`.
