# System Architecture

## 1. Goal
- Intangible cultural heritage management + visualization system.
- Roles: `admin` (CRUD/manage) and `user` (read-only).

## 2. Stack
- Backend: Django 5.2 + DRF + SimpleJWT + MySQL 8.0+
- Frontend (planned): Vue 3 + TypeScript + Element Plus + ECharts + Tailwind CSS
- API base: `/api/v1`

## 3. Backend file map (what each file does)
- `backend/manage.py`: Django command entry.
- `backend/heritage_system/settings.py`: app registration, DB, DRF/JWT/CORS, global defaults.
- `backend/heritage_system/urls.py`: root URL routing, mounts versioned APIs.
- `backend/utils/response.py`: unified response envelope + DRF exception handler.
- `backend/apps/users/models.py`: `UserProfile` and role utilities (`admin|user`).
- `backend/apps/users/permissions.py`: `IsAdmin`, `IsAdminOrReadOnly`.
- `backend/apps/users/serializers.py`: auth request/response serialization.
- `backend/apps/users/views.py`: login/refresh/logout/me endpoints.
- `backend/apps/users/urls.py`: auth route table.
- `backend/apps/users/admin.py`: admin-side role management.
- `backend/apps/categories/models.py`: `Category` tree dictionary (`parent`, `level`, `code`).
- `backend/apps/categories/admin.py`: category admin list/filter/search.
- `backend/apps/regions/models.py`: `Region` with ISO code, country name, lat/lon, continent.
- `backend/apps/regions/admin.py`: region admin list/filter/search.
- `backend/apps/heritage/models.py`: `HeritageItem` core domain model.
- `backend/apps/heritage/admin.py`: heritage item admin management.
- `backend/apps/inheritors/models.py`: `Inheritor` model, linked to heritage + region, unique per item/name.
- `backend/apps/inheritors/admin.py`: inheritor admin management.
- `backend/apps/importer/models.py`: `ImportJob` + `ImportError` for import tracking.
- `backend/apps/importer/admin.py`: import job/error inspection in admin.
- `backend/apps/*/migrations/0001_initial.py`: schema snapshots for each domain.
- `sql/init_db.sql`: base DB bootstrap and seed script.

## 4. Current data-model relationships
- `Category` 1:N `HeritageItem`
- `Region` 1:N `HeritageItem`
- `HeritageItem` 1:N `Inheritor`
- `Region` 1:N `Inheritor`
- `ImportJob` 1:N `ImportError`
- `User` 1:N `ImportJob` (`created_by`)

## 5. Current architecture decisions
- Unified response format: `{ code, message, data, total? }`
- Default auth: JWT Bearer
- Permission baseline: authenticated by default; write operations role-restricted
- Domain integrity: FK constraints + practical indexes + uniqueness for key business rule

## 6. Milestone
- Phase 1: done
- Phase 2: done
- Phase 3 (3.1~3.4): done and test-passed
- Next: Phase 4.1 (heritage CRUD APIs)

---
Last updated: 2026-02-25
