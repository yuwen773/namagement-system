# Project Progress

## 2026-02-25

### Done
- Phase 1 (1.1~1.4): backend scaffold, MySQL, dependencies, bootstrap SQL.
- Phase 2 (2.1~2.3): auth, role permissions, JWT APIs, unified response/exception handling.
- Phase 3 (3.1~3.4): core data models + admin registration:
  - `Category`, `Region`
  - `HeritageItem`
  - `Inheritor` (unique: same `heritage_item` + same `name`)
  - `ImportJob`, `ImportError`

### Migration / Checks
- `python manage.py makemigrations categories regions heritage inheritors importer`: passed
- `python manage.py migrate`: passed
- `python manage.py check`: passed
- User-provided Phase 3 tests: passed

### Current status
- Phase 3 complete.
- Ready to start Phase 4 Step 4.1.
