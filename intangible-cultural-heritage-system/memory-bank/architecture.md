# System Architecture

## 1. Scope
- Intangible cultural heritage management + visualization system.
- Roles: `admin` (write/manage), `user` (read-only baseline).

## 2. Technical baseline
- Frontend: Vue 3 + TypeScript + Element Plus + ECharts + Tailwind CSS
- Backend: Django 5.2 + DRF + SimpleJWT
- Database: MySQL 8.0+
- API prefix: `/api/v1`

## 3. Core backend structure and file roles
- `backend/manage.py`: Django command entry.
- `backend/heritage_system/settings.py`: global config; DRF/JWT/CORS/DB.
- `backend/heritage_system/urls.py`: root routing; mounts `/api/v1/auth/*`.
- `backend/utils/response.py`: unified response helpers + DRF exception handler.
- `backend/apps/users/models.py`: `UserProfile` role model (`admin|user`) and role utilities.
- `backend/apps/users/permissions.py`: `IsAdmin`, `IsAdminOrReadOnly`.
- `backend/apps/users/serializers.py`: login/logout serialization and token packaging.
- `backend/apps/users/views.py`: login/refresh/logout/me endpoints.
- `backend/apps/users/urls.py`: auth route declarations.
- `backend/apps/users/admin.py`: admin integration for user-role visibility/management.
- `backend/apps/users/migrations/0001_initial.py`: creates `user_profiles`.
- `sql/init_db.sql`: DB bootstrap + seed baseline data.

## 4. Module boundaries (`backend/apps`)
- `users`: authentication, authorization, role model.
- `heritage`: heritage item domain (to be expanded in Phase 3+).
- `inheritors`: inheritor domain (to be expanded in Phase 3+).
- `categories`: taxonomy dictionary (Phase 3+).
- `regions`: geo normalization dictionary (Phase 3+).
- `importer`: import workflow and error trace (Phase 5+).
- `dashboard`: aggregated analytics APIs (Phase 6+).

## 5. Architecture decisions (implemented)
- API response envelope unified as `{ code, message, data, total? }`.
- Default API auth: JWT (`Bearer`).
- JWT lifetime: access 2 hours, refresh 7 days.
- Permission baseline: authenticated users by default; write actions restricted by role.

## 6. Current milestone
- Phase 1: completed.
- Phase 2 (2.1~2.3): completed and test-passed.
- Phase 3 Step 3.1: not started.

---
Last updated: 2026-02-25
