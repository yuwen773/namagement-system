# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Car Parts Sales & Recommendation Platform** (汽车改装件销售推荐平台) - A Django + Vue.js e-commerce platform focused on automotive modification parts with personalized recommendation features.

**Status:** Phase 5 (API Documentation) - Backend nearly complete, Frontend not started

**Key Documentation:**
- `memory-bank/PRD.md` - Product requirements document
- `memory-bank/architecture.md` - Database schema and business logic
- `memory-bank/IMPLEMENTATION_PLAN.md` - Phase-by-phase implementation plan
- `memory-bank/progress.md` - Current development status
- `memory-bank/dev-standards/backend-api-standards.md` - Backend coding standards
- `memory-bank/dev-standards/frontend-api-standards.md` - Frontend coding standards

## Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver              # Port 8000
python manage.py createsuperuser        # Create admin account
python scripts/seed_data.py             # Generate 1000+ products, users, orders
python scripts/verify_data.py           # Verify data integrity (14 checks)
python scripts/export_api_docs.py       # Export Swagger JSON/YAML docs
```

### Database
```bash
mysql -u root -p
CREATE DATABASE car_parts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### API Documentation (Development)
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Architecture

### Backend Structure (Django 6.0.2 + DRF 3.16.1)
```
backend/
├── config/              # Django project settings, urls, wsgi
├── apps/
│   ├── users/           # Authentication, User model (phone-based), UserAddress
│   ├── products/        # Category, Product, ProductImage, ProductAttribute, Review
│   ├── orders/          # Order, OrderItem, ReturnRequest, Cart, CartItem
│   ├── marketing/       # Coupon, UserCoupon
│   ├── recommendations/ # RecommendationRule, RecommendedProduct
│   ├── content/         # ModificationCase, FAQ
│   └── system/          # SystemConfig, Message, OperationLog
├── utils/
│   ├── response.py      # ApiResponse unified wrapper
│   ├── exceptions.py    # Custom exception classes
│   ├── pagination.py    # StandardPagination class
│   └── constants.py     # Constants
├── scripts/             # Data seeding and verification
└── docs/                # Exported API documentation
```

### Backend Apps Overview

| App | Key Models | Important Notes |
|-----|-----------|-----------------|
| `users` | User, UserAddress | Phone-based auth (username disabled), unique phone identifier |
| `products` | Category, Product, Review | Self-referential categories, product status workflow |
| `orders` | Order, OrderItem, Cart, CartItem | Order status machine, redundant data snapshots |
| `marketing` | Coupon, UserCoupon | Full reduction & discount types, per-user limits |
| `recommendations` | RecommendationRule | Rule types: hot/new/personalized/category |
| `content` | ModificationCase, FAQ | FAQ categories: order/payment/shipping/etc |
| `system` | SystemConfig, Message, OperationLog | Key-value config, broadcast messaging, audit logs |

### Frontend Structure (Planned - Not Implemented)
```
frontend/src/
├── api/
│   ├── request.ts      # Axios wrapper with interceptors
│   └── modules/        # auth.ts, user.ts, product.ts, order.ts, etc.
├── stores/             # Pinia stores (auth, cart, etc.)
├── router/             # Vue Router with role-based meta
├── views/              # Page components by module
└── utils/              # Utility functions
```

## API Response Format

All API responses use `ApiResponse` wrapper from `utils/response.py`:

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {...}
}
```

List endpoints use `StandardPagination`:
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "page": 1,
        "page_size": 20,
        "results": [...]
    }
}
```

Error responses:
```json
{
    "code": 400,
    "message": "错误信息",
    "data": null,
    "errors": {...}
}
```

## Key Patterns & Business Logic

### Authentication
- **JWT** via `djangorestframework-simplejwt`
- Access Token: 2 hours, Refresh Token: 7 days
- Phone-based login (username field disabled)
- Token stored in `localStorage`, sent as `Authorization: Bearer {token}`

### Status Machines

**Order Status:**
```
pending_payment → pending_shipment → shipped → completed
    ↓                    ↓               ↓
  cancelled           cancelled        return_processing
```

**Product Status:**
```
draft → pending → published → archived
```

### Important Model Behaviors

- **User.phone**: Unique identifier, used for authentication
- **Category**: Self-referential via `parent` foreign key, unlimited nesting
- **Order**: Auto-generated `order_no` (timestamp + 6 random digits)
- **OrderItem/CartItem**: Store redundant product snapshots (prevents data loss if product deleted)
- **UserAddress**: Auto-cancels previous default when setting new default
- **Cart**: One-to-one with user, auto-updates `total_items` and `total_price`
- **Review**: Linked to `order_item_id` (one review per order item)

### Permission Classes
- `IsAuthenticated` - Default for all endpoints
- `IsAdminUser` - Admin-only operations
- Custom `IsOwnerOrReadOnly` - For user resources

## Development Standards

**Before coding backend:** Read `memory-bank/dev-standards/backend-api-standards.md`
- Project structure conventions
- Unified API response format
- Exception handling patterns
- Pagination configuration
- Database optimization (select_related, prefetch_related)
- Security practices

**Before coding frontend:** Read `memory-bank/dev-standards/frontend-api-standards.md`
- Project directory structure
- Axios interceptors
- Error handling patterns
- Token management
- Route guards

## Data Seeding

`python scripts/seed_data.py` generates:
- 5 admin users (password: admin123)
- 20 regular users (password: 123456)
- 94 categories (3-level hierarchy)
- 1000 products (with images and attributes)
- 100 coupons
- Orders, cart items, reviews
- 50 modification cases, 30 FAQs
- System configs, messages, operation logs

## Important Notes

1. **Chinese Field Names**: Models use Chinese `verbose_name` for admin readability
2. **Database**: MySQL 8.0+, utf8mb4 charset, Asia/Shanghai timezone
3. **CORS**: Configured for `http://localhost:5173` frontend
4. **API Docs**: drf-yasg provides Swagger UI at `/swagger/`
5. **Password Storage**: Currently plaintext (development only)
6. **Module Order**: products → users → orders → marketing → recommendations → system
