# 架构设计

## 目录结构

```
backend/
├── config/         # settings, urls
├── apps/
│   ├── users/     # User, UserAddress
│   ├── products/  # Category, Product...
│   ├── orders/    # Order, OrderItem...
│   ├── marketing/ # Coupon, UserCoupon
│   ├── recommendations/
│   ├── content/   # ModificationCase, FAQ
│   └── system/    # SystemConfig, Message...
└── utils/         # response, exceptions, pagination
```

## 模型关系

```
User (1) ──► (N) UserAddress
User (1) ──► (N) Order
User (1) ──► (N) UserCoupon
Order (1) ──► (N) OrderItem
Product (1) ──► (N) ProductImage
Product (1) ──► (N) ProductAttribute
```

## 订单状态

```
pending_payment → pending_shipment → shipped → completed
                → cancelled (取消)
                → return_processing (退换货)
```

## API响应格式

```json
{"code": 200, "message": "操作成功", "data": {...}}
```

## API端点

| 模块 | 路径 |
|------|------|
| users | /api/users/ |
| products | /api/products/ |
| orders | /api/orders/ |
| marketing | /api/marketing/ |
| recommendations | /api/recommendations/ |
| content | /api/content/ |
| system | /api/system/ |
