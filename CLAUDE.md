# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing **4 business management systems** built with modern web technologies. All projects follow a consistent Django + Vue.js full-stack architecture.

| Project | Status | Tech Stack |
|---------|--------|------------|
| [Enterprise-HRMS](./Enterprise-HRMS) | Active | Django 5.2 + DRF + Vue 3.5 + Element Plus |
| [Canteen Management](./canteen-management-system) | Active | Django 5.2 + DRF + Vue 3 + Element Plus |
| [Recipe Analysis](./recipe-data-analysis-system) | Active | Python + Vue 3 + ECharts |
| [Car Parts Sales](./car-parts-sales-platform) | Planning | Django 5.2 + DRF + Vue 3 + Element Plus |

## Critical Rules

1. **Always read subproject CLAUDE.md first** - Each subproject has its own detailed guidance in its root directory
2. **Read memory-bank documents before coding** - Each subproject has `memory-bank/architecture.md` with database schema and business rules
3. **Use Chinese for business logic** - Models and APIs use Chinese field names (`real_name`, `department`)
4. **API response format**: `{ code: 0, data: {...}, total: n }` for lists

## Common Commands

### Django Backend
```bash
cd <project>/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver        # Default port 8000
python manage.py createsuperuser  # Create admin account
```

### Vue Frontend
```bash
cd <project>/frontend
npm install
npm run dev                       # Development server
npm run build                     # Production build
```

### Database
```bash
mysql -u root -p < sql/init_db.sql    # Initialize with schema + test data
```

## Shared Architecture Patterns

### Backend (Django + DRF)
- **Apps structure**: `accounts`, `employees/organization`, `attendance`, `salary`, `approval`, `notice`
- **Auth**: JWT via `djangorestframework-simplejwt` (Access: 2h, Refresh: 7d)
- **Permissions**: Custom classes in `HRMS/permissions.py` or app-level
  - `IsAdmin` - Full admin access
  - `IsHROrAdmin` - HR/Admin sensitive operations
  - `IsEmployeeOrHROrAdmin` - Employee sees own data
- **ViewSets**: Use `get_serializer_class()` for dynamic serializers, `@action` for custom endpoints

### Frontend (Vue 3 + Element Plus)
- **State**: Pinia stores in `stores/`
- **Router**: `router/index.js` with `meta.roles` for route protection
- **API**: Centralized in `src/api/` directory
- **ECharts**: Must `onUnmounted() { chart.dispose() }` to prevent memory leaks

## Subproject Quick Reference

### Enterprise-HRMS
- **Port**: Backend 8000, Frontend 5173
- **DB**: MySQL 3307
- **Key**: Employee ID format `EMP{YYYYMM}{DEPT}{SEQ}`, Salary formula
- **Docs**: `memory-bank/architecture.md`, `memory-bank/PRD.md`

### Canteen Management
- **Theme**: Warm color scheme (orange/yellow/green)
- **Roles**: ADMIN (full access), EMPLOYEE (personal portal)
- **Key features**: Scheduling, certificate tracking, auto role-based redirect
- **Docs**: `memory-bank/PRD.md`, `memory-bank/architecture.md`

### Recipe Analysis
- **Focus**: Data visualization + crawler
- **API Standard**: `backend-api-standards.md` in memory-bank
- **Response**: `{ code: 200, message: "...", data: {} }`
- **Docs**: `memory-bank/architecture.md`, `memory-bank/PRD.md`

### Car Parts Sales
- **Status**: Planning phase - no implementation code yet
- **Docs**: `PRD.md`, `pre-prd.md`, `tech-stack.md` in memory-bank
- **Follow**: Module order in CLAUDE.md when implementing

## Database Conventions

- **MySQL**: 8.0+ on port 3306 or 3307
- **Engine**: InnoDB with UTF8MB4 charset
- **Init scripts**: `sql/init_db.sql` or `init.sql` in each project
- **Test data**: Included in initialization scripts (admin accounts, sample records)
