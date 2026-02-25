# Progress

## 2026-02-25

### Completed
- Phase 1 (1.1~1.4): backend scaffold, MySQL config, dependencies, bootstrap SQL.
- Phase 2 (2.1~2.3): JWT auth, role permissions, unified response/exception handling.
- Phase 3 (3.1~3.4): core models and admin registration (`Category`, `Region`, `HeritageItem`, `Inheritor`, `ImportJob`, `ImportError`).
- Phase 4.1: heritage CRUD (`/api/v1/heritage/`) with filters, pagination, admin-write/user-read.
- Phase 4.2: inheritor CRUD (`/api/v1/inheritors/`) with filters, pagination, related heritage brief.
- Phase 4.3: category CRUD (`/api/v1/categories/`) and tree endpoint (`/api/v1/categories/tree/`).
- Phase 4.4: region CRUD (`/api/v1/regions/`) and search (`?search=<country name/code>`).

### Validation
- `python manage.py check`: passed.
- User validation: Phase 4.1~4.4 passed.

### Current Status
- Phase 4 is complete and verified.
- Phase 5.1 is the next planned step.
