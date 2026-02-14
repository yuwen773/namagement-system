# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Campus Smart Energy Consumption Monitoring Visualization System** (校园智慧后勤能耗监测可视化系统)

A campus energy monitoring system that visualizes multi-source heterogeneous energy data (water, electricity, gas) using ECharts. Built with Django 5.2 + DRF backend and Vue 3 frontend, with optional Spark-based data analysis for large-scale datasets.

**Status**: Planning phase - implementation in progress according to `memory-bank/implementation-plan.md`

---

## Quick Reference

### Backend (Django + DRF)
```bash
cd backend
python manage.py runserver        # Default port 8000
python manage.py migrate
python manage.py createsuperuser
python manage.py import_energy_data <file_path>    # Import energy data from CSV
python manage.py generate_statistics               # Generate daily/monthly statistics
python manage.py check_alarms                      # Check and create alarm records
```

### Frontend (Vue 3 + Vite)
```bash
cd frontend
npm run dev                       # Development server on port 5173
npm run build                     # Production build
```

### Database
- **MySQL 8.0+** on default port 3306
- Database name: `energy_monitoring`
- Charset: UTF8MB4
- Init script: `sql/init_db.sql`

---

## Project Structure

```
energy-consumption-monitoring/
├── backend/                 # Django backend
│   ├── energy_monitoring/   # Project configuration
│   └── apps/                # Django applications
│       ├── accounts/        # User authentication, JWT
│       ├── buildings/       # Building/Floor/Room hierarchy
│       ├── devices/         # Device management, Energy types
│       ├── energy/          # Raw energy data, Statistics
│       ├── analysis/        # Data analysis APIs (dashboard, trends, rankings)
│       ├── alarms/          # Alarm rules and records
│       └── system/          # Bills, Notices, Operation logs
├── frontend/                # Vue 3 frontend
│   └── src/
│       ├── api/             # API modules (auth.js, building.js, etc.)
│       ├── views/
│       │   ├── admin/       # Admin portal pages (7 pages)
│       │   └── user/        # User portal pages (6 pages)
│       ├── layouts/         # AdminLayout, UserLayout
│       ├── stores/          # Pinia stores (user, building, energy)
│       └── router/          # Vue Router with role guards
├── sql/                     # Database init script
├── scripts/                 # Data import scripts (Pandas-based)
├── docs/                    # API documentation
└── memory-bank/             # Project documentation
```

---

## Key Architecture Patterns

### Backend (Django + DRF)

**App Structure**:
- Each app has `models.py`, `views.py`, `urls.py`, `serializers.py`
- Use `ModelViewSet` for CRUD operations
- Use `@action` decorator for custom endpoints

**Authentication**:
- JWT via `djangorestframework-simplejwt`
- Access Token: 2 hours, Refresh Token: 7 days
- Two roles: `ADMIN` (full access), `USER` (read-only personal data)

**Custom Permissions** (in `energy_monitoring/permissions.py`):
- `IsAdmin` - Admin only
- `IsAdminOrReadOnly` - Admin writes, others read
- `IsOwnerOrAdmin` - Resource owner or admin

**API Response Format**:
- Lists: `{ code: 0, data: [...], total: n }`
- Details: `{ code: 0, data: {...} }`
- Errors: `{ code: 1, message: "..." }`

**Database Models** (15 core tables):
- User management: `em_users`, `em_roles`
- Hierarchy: `em_buildings` → `em_floors` → `em_rooms`
- Devices: `em_energy_types`, `em_devices`
- Energy data: `em_energy_data` (raw), `em_energy_statistics` (aggregated)
- Alarms: `em_alarm_rules`, `em_alarms`
- System: `em_bills`, `em_recharge_records`, `em_notices`, `em_operation_logs`

### Frontend (Vue 3)

**State Management (Pinia)**:
- `useUserStore` - userInfo, token, role, login/logout
- `useBuildingStore` - buildingTree, currentBuilding
- `useEnergyStore` - selectedDevices, dateRange
- Use `pinia-plugin-persistedstate` for persistence

**Routing**:
- Admin prefix: `/admin/*` (7 pages)
- User prefix: `/user/*` (6 pages)
- Route guards: Check login status, redirect by role

**ECharts Best Practices**:
- Always dispose on unmount: `onUnmounted() { chart.dispose() }`
- Use `shallowRef` for chart instances to avoid deep reactivity
- Handle resize with `window.addEventListener('resize', ...)`

---

## Data Flow

1. **Import**: CSV/Excel → Pandas script → MySQL (`em_energy_data`)
2. **Processing**: Management commands → Aggregate to `em_energy_statistics`, detect `em_alarms`
3. **API**: Vue → DRF ViewSet → MySQL
4. **Visualization**: ECharts reads API response → render charts

---

## Important Conventions

### Field Naming
- **Database**: snake_case (`device_id`, `created_at`)
- **API Responses**: snake_case (consistent with DB)
- **Chinese for business fields**: `real_name`, `department`, `building_name`

### Energy Types
- `WATER` - 水
- `ELECTRICITY` - 电
- `GAS` - 气

### Alarm Status
- `PENDING` - 待处理
- `PROCESSED` - 已处理
- `IGNORED` - 已忽略

### Statistics Period Types
- `DAY` - 日统计
- `MONTH` - 月统计
- `YEAR` - 年统计

---

## Development Strategy

**Backend-First Approach**:
1. Complete all backend APIs and documentation first
2. Provide API specs to frontend team
3. Frontend development starts after backend is complete

**Reference**: Follow `memory-bank/implementation-plan.md` for step-by-step implementation with test validation for each step.

---

## API Documentation

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI spec: `docs/api-spec.json`

---

## Related Projects

This is part of a monorepo with 4 business management systems sharing similar Django + Vue architecture:
- `../Enterprise-HRMS/` - Human Resource Management System
- `../canteen-management-system/` - Canteen Management System
- `../recipe-data-analysis-system/` - Recipe Data Analysis System
- `../car-parts-sales-platform/` - Car Parts Sales Platform

Refer to these projects for implementation patterns and conventions.
