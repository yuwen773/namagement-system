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
Order (1) ──► (N) ReturnRequest
Product (1) ──► (N) ProductImage
Product (1) ──► (N) ProductAttribute
UserCoupon (N) ──► (1) Order (used_order)
```

## 订单状态

```
pending_payment (待付款)
    ↓
pending_shipment (待发货)
    ↓
shipped (已发货)
    ↓
completed (已完成)
    ↓
return_processing (退换货) → ReturnRequest

cancelled (已取消) - 任意可取消状态
```

## 已实现模块详解

### users 模块
| 文件 | 作用 |
|------|------|
| `models.py` | User (扩展 AbstractUser)、UserAddress |
| `serializers.py` | 用户注册、登录、地址管理序列化器 |
| `views.py` | 认证视图集（register, login, me） |
| `permissions.py` | IsOwnerOrAdmin 权限类 |
| `urls.py` | /api/users/ 路由 |

### marketing 模块
| 文件 | 作用 |
|------|------|
| `models.py` | Coupon (优惠券)、UserCoupon (用户优惠券) |
| `admin.py` | 优惠券管理后台配置 |

**Coupon 模型字段**：
- `discount_type`: full_reduction (满减) / discount (折扣)
- `min_amount`: 使用门槛
- `valid_from/until`: 有效期
- `total_quantity/per_user_limit`: 发放限制

**UserCoupon 模型字段**：
- `status`: unused/used/expired
- `used_order`: 使用的订单（关联 Order）

### orders 模块
| 文件 | 作用 |
|------|------|
| `models.py` | Order、OrderItem、ReturnRequest |
| `serializers.py` | 订单和退换货的序列化器 |
| `views.py` | OrderViewSet、ReturnRequestViewSet |
| `admin.py` | Django Admin 配置 |
| `urls.py` | /api/orders/ 路由 |

**Order 模型字段**：
- `order_no`: 自动生成（日期+随机数）
- `user`: 关联用户
- `recipient_*`: 收货地址信息（冗余存储）
- `total_amount/discount_amount/shipping_fee/pay_amount`: 金额信息
- `status`: 订单状态
- `express_company/tracking_number`: 物流信息
- `coupon`: 使用的优惠券（关联 UserCoupon，related_name='+' 避免冲突）

**OrderItem 模型字段**：
- `order`: 关联订单
- `product`: 关联商品
- `product_name/image/price`: 冗余商品信息
- `quantity`: 购买数量
- `subtotal`: 小计（自动计算）

**ReturnRequest 模型字段**：
- `request_type`: return (退货) / exchange (换货)
- `reason`: 退换货原因
- `evidence_images`: 凭证图片URL列表（JSON）
- `status`: pending/approved/rejected/completed

**OrderViewSet 自定义 Action**：
- `cancel`: 取消订单（待付款/待发货）
- `confirm`: 确认收货（已发货）
- `ship`: 订单发货（管理员，待发货）
- `my-orders`: 我的订单列表

**ReturnRequestViewSet 自定义 Action**：
- `process`: 处理退换货申请（管理员）

## API响应格式

```json
{"code": 200, "message": "操作成功", "data": {...}}
```

**分页响应**：
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
