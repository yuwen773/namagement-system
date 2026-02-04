# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Car Parts Sales & Recommendation Platform** - A Django + Vue.js e-commerce platform focused on automotive modification parts with personalized recommendation features.

**Status:** Planning/Documentation Phase (No implementation code exists yet)

**Key Documentation:**
- `memory-bank/@PRD.md` - Product requirements document
- `memory-bank/@tech-stack.md` - Technology stack details
- `memory-bank/dev-standards/` - Development standards (backend & frontend)

## Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver        # Port 8000
python manage.py createsuperuser  # Create admin account
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # Development server (port 5173)
npm run build                     # Production build
```

### Database
```bash
mysql -u root -p < sql/init_db.sql    # Initialize with schema + test data
```

## API Response Format

All APIs return:
```json
{
    "code": 200,
    "message": "操作成功",
    "data": { ... }
}
```

List endpoints use `StandardPagination` with:
```json
{
    "results": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
}
```

## Architecture

### Backend Structure (Django 5.2 + DRF)
```
backend/
├── config/              # Django project settings, urls, wsgi
├── apps/
│   ├── users/           # Authentication, User model, UserAddress
│   ├── products/        # Category, Product, ProductImage, ProductAttribute
│   ├── orders/          # Order, OrderItem, ReturnRequest
│   ├── marketing/       # Coupon, UserCoupon, Promotion
│   ├── recommendations/ # RecommendationRule, RecommendedProduct
│   ├── content/         # ModificationCase, FAQ
│   └── system/          # SystemConfig, Message, OperationLog
└── utils/
    ├── response.py      # UnifiedResponse wrapper
    ├── exceptions.py    # Custom exceptions
    pagination.py        # StandardPagination
    └── constants.py     # Constants
```

### Frontend Structure (Vue 3 + Element Plus)
```
frontend/src/
├── api/
│   ├── request.ts      # Axios wrapper with interceptors
│   └── modules/        # auth.ts, user.ts, product.ts, order.ts, etc.
├── stores/             # Pinia stores (auth, cart, etc.)
├── router/             # Vue Router with role-based meta
└── views/              # Page components by module
```

### Module Implementation Order (Admin)
1. products → 2. users → 3. orders → 4. marketing → 5. recommendations → 6. system

## Key Patterns

- **Auth**: JWT via `djangorestframework-simplejwt` (Access: 2h, Refresh: 7d)
- **Permissions**: Custom classes - `IsAdmin`, `IsOwnerOrReadOnly`
- **ViewSets**: Use `get_serializer_class()` for dynamic serializers
- **Token**: Stored in `localStorage`, sent as `Authorization: Bearer {token}`

## Data Requirements

- **Products**: 1,000+ car modification parts with images and attributes
- **Users**: 20+ active accounts with browsing history, cart, orders, reviews
- **Admin**: 2-3 admin accounts for different modules

## Development Notes

- Read `memory-bank/dev-standards/backend-api-standards.md` before backend coding
- Read `memory-bank/dev-standards/frontend-api-standards.md` before frontend coding
- All Chinese field names in models: `real_name`, `phone`, `address`
- After major features, update `memory-bank/@architecture.md`
