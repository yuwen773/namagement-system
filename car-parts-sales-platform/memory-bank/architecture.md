# 架构设计

## 目录结构

```
backend/
├── config/         # settings, urls
├── apps/
│   ├── users/       # User, UserAddress
│   ├── products/    # Category, Product...
│   ├── orders/      # Order, OrderItem...
│   ├── marketing/   # Coupon, UserCoupon
│   ├── recommendations/
│   ├── content/     # ModificationCase, FAQ
│   └── system/      # SystemConfig, Message...
└── utils/           # response, exceptions, pagination
```

## 模型关系

```
User (1) ──► (N) UserAddress
User (1) ──► (N) Order
User (1) ──► (N) UserCoupon
User (1) ──► (N) Review

Category (1) ──► (N) Category (parent, 自关联)
Category (1) ──► (N) Product

Product (1) ──► (N) ProductImage
Product (1) ──► (N) ProductAttribute
Product (1) ──► (N) OrderItem
Product (1) ──► (N) Review

Coupon (1) ──► (N) UserCoupon
RecommendationRule (1) ──► (N) RecommendedProduct
Order (1) ──► (N) OrderItem
Order (1) ──► (N) ReturnRequest
```

## 订单状态

```
pending_payment → pending_shipment → shipped → completed
    ↓                    ↓               ↓
  cancelled           cancelled        return_processing
```

## 模块概览

### users
- **模型**: User (扩展 AbstractUser), UserAddress
- **认证**: JWT (2h access, 7d refresh)

### products
- **模型**: Category (多级), Product, ProductImage, ProductAttribute, Review
- **状态**: draft/pending/published/archived

### orders
- **模型**: Order, OrderItem, ReturnRequest
- **字段**: order_no, amounts, status, express_info

### marketing
- **模型**: Coupon (满减/折扣), UserCoupon
- **限制**: total_quantity, per_user_limit

### recommendations
- **模型**: RecommendationRule, RecommendedProduct
- **类型**: hot/new/personalized/category

### content
- **模型**: ModificationCase (draft/published), FAQ
- **特性**: 浏览量统计, 分类筛选

### system
- **模型**: SystemConfig, Message, OperationLog
- **日志**: 操作审计, 只读不可删

## API 响应格式

```json
{"code": 200, "message": "操作成功", "data": {...}}
```

**分页**:
```json
{"code": 200, "message": "获取成功", "data": {"count": 100, "page": 1, "page_size": 20, "results": [...]}}
```

---

## products 模块文件说明

| 文件 | 作用 |
|------|------|
| `models.py` | 定义数据模型：Category(多级分类)、Product(商品)、ProductImage(商品图片)、ProductAttribute(商品属性)、Review(商品评价) |
| `serializers.py` | 序列化器：CategorySerializer、ProductSerializer、ReviewSerializer 等，负责 API 请求/响应的数据转换 |
| `views.py` | 视图集：CategoryViewSet、ProductViewSet、ReviewViewSet 等，实现 CRUD 逻辑和自定义 action |
| `urls.py` | URL 路由配置，使用 DRF Router 自动生成 RESTful 路由 |
| `admin.py` | Django Admin 后台注册和管理界面配置 |
| `apps.py` | Django App 配置类 |
| `migrations/` | 数据库迁移文件，记录模型结构变更历史 |
