# Project Progress

## 2026-02-25

### Completed
- Phase 1 (1.1~1.4): backend scaffold, MySQL config, dependencies, bootstrap SQL.
- Phase 2 (2.1~2.3): auth/permission baseline and unified response format.

### Phase 2 details
- 2.1 User model and permissions
  - Added `UserProfile` (`role=admin|user`) and auto-create logic.
  - Added permission classes: `IsAdmin`, `IsAdminOrReadOnly`.
  - Added admin integration for role management.
- 2.2 JWT auth APIs
  - Added routes: `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`.
  - Added `GET /api/v1/auth/me` for authenticated profile checks.
  - Configured JWT lifetime: access 2h, refresh 7d.
- 2.3 Unified response and exception handling
  - Added response envelope helpers: `{ code, message, data, total? }`.
  - Added custom DRF exception handler and wired it in settings.

### Verification
- `python manage.py makemigrations users`: passed
- `python manage.py migrate`: passed
- `python manage.py check`: passed
- JWT login/refresh/logout/me smoke test: passed

### Current status
- Do not start Phase 3 Step 3.1 until further instruction.
