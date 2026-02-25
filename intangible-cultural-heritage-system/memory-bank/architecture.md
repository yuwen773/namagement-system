# Architecture

## Scope
- System: intangible cultural heritage management + visualization.
- Roles: `admin` (write/manage), `user` (read-only).
- API prefix: `/api/v1`.

## Tech Stack
- Backend: Django 5.2, DRF, SimpleJWT, MySQL 8+.
- Frontend (planned): Vue 3 + TypeScript + Element Plus + ECharts.

## File Responsibilities
- Core
  - `backend/manage.py`: Django command entry.
  - `backend/heritage_system/settings.py`: app registry, DB, auth, middleware, CORS.
  - `backend/heritage_system/urls.py`: root routing for versioned API modules.
- Shared utils
  - `backend/utils/response.py`: unified response `{code, message, data, total?}` and exception mapping.
  - `backend/utils/pagination.py`: unified list pagination (`page_size=20`).
- Auth (`users`)
  - `backend/apps/users/models.py`: `UserProfile` and role helpers.
  - `backend/apps/users/permissions.py`: `IsAdmin`, `IsAdminOrReadOnly`.
  - `backend/apps/users/serializers.py`: auth serializers.
  - `backend/apps/users/views.py`: login/refresh/logout/me endpoints.
  - `backend/apps/users/urls.py`: auth routes.
  - `backend/apps/users/admin.py`: user/profile admin config.
- Heritage items (`heritage`)
  - `backend/apps/heritage/models.py`: `HeritageItem` model.
  - `backend/apps/heritage/serializers.py`: read/write serializers.
  - `backend/apps/heritage/views.py`: CRUD + filters + pagination + permission.
  - `backend/apps/heritage/urls.py`: heritage routes.
  - `backend/apps/heritage/admin.py`: admin config.
- Inheritors (`inheritors`)
  - `backend/apps/inheritors/models.py`: `Inheritor` model.
  - `backend/apps/inheritors/serializers.py`: read/write serializers and heritage brief fields.
  - `backend/apps/inheritors/views.py`: CRUD + filters + pagination + permission.
  - `backend/apps/inheritors/urls.py`: inheritor routes.
  - `backend/apps/inheritors/admin.py`: admin config.
- Categories (`categories`)
  - `backend/apps/categories/models.py`: category dictionary with parent-child structure.
  - `backend/apps/categories/serializers.py`: read/write serializers and parent brief fields.
  - `backend/apps/categories/views.py`: CRUD + `tree` action + filters + permission.
  - `backend/apps/categories/urls.py`: category routes.
  - `backend/apps/categories/admin.py`: admin config.
- Regions (`regions`)
  - `backend/apps/regions/models.py`: region model (ISO code, name, coordinates, continent).
  - `backend/apps/regions/serializers.py`: read/write serializers.
  - `backend/apps/regions/views.py`: CRUD + `search` (name/code) + permission.
  - `backend/apps/regions/urls.py`: region routes.
  - `backend/apps/regions/admin.py`: admin config.
- Import (`importer`)
  - `backend/apps/importer/models.py`: `ImportJob`, `ImportError`.
  - `backend/apps/importer/admin.py`: import job/error admin inspection.
- DB lifecycle
  - `backend/apps/*/migrations/*.py`: schema evolution history.
  - `sql/init_db.sql`: initial DB bootstrap data/script.

## Data Model Relationships
- `Category` 1:N `HeritageItem`
- `Region` 1:N `HeritageItem`
- `HeritageItem` 1:N `Inheritor`
- `Region` 1:N `Inheritor`
- `ImportJob` 1:N `ImportError`
- `User` 1:N `ImportJob`

## Architecture Insights
- API contract is unified, so frontend only handles one success/error envelope shape.
- Permission model is centralized (`IsAdminOrReadOnly`) and reused across resource apps.
- Resource APIs follow one implementation pattern (ModelViewSet + filters + pagination), reducing maintenance cost.
- Category tree endpoint keeps hierarchical reads simple without changing relational schema.

---
Last updated: 2026-02-25
