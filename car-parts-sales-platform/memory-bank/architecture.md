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
User (1) ──► (N) Review (商品评价，待实现)

Category (1) ──► (N) Category (parent，自关联)
Category (1) ──► (N) Product

Product (1) ──► (N) ProductImage
Product (1) ──► (N) ProductAttribute
Product (1) ──► (N) OrderItem
Product (1) ──► (N) Review (待实现)

Coupon (1) ──► (N) UserCoupon
RecommendationRule (1) ──► (N) RecommendedProduct
RecommendedProduct (N) ──► (1) Product
Order (1) ──► (N) OrderItem
Order (1) ──► (N) ReturnRequest
Order (1) ──► (1) UserCoupon (used_order，反向)
Order (1) ──► (1) Coupon (通过UserCoupon，可选)

Category: 支持多级分类（parent自关联）
Coupon: 定义优惠券规则（满减/折扣、门槛、有效期）
UserCoupon: 用户领取的优惠券（关联User和Coupon，状态跟踪）
RecommendationRule: 推荐规则（热门推荐、新品推荐、个性化推荐）
RecommendedProduct: 手动配置的推荐商品（关联规则和商品）
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

### products 模块
| 文件 | 作用 |
|------|------|
| `models.py` | Category (分类)、Product (商品)、ProductImage (图片)、ProductAttribute (属性) |
| `serializers.py` | 商品相关序列化器 |
| `views.py` | ProductViewSet、CategoryViewSet |
| `admin.py` | 商品管理后台配置 |
| `urls.py` | /api/products/ 路由 |

**Category 模型字段**：
- `parent`: 自关联外键，支持多级分类
- `sort_order`: 排序权重
- `is_active`: 是否启用
- `full_path`: 属性方法，获取完整分类路径

**Product 模型字段**：
- `status`: draft/pending/published/archived
- `price/original_price`: 销售价/原价
- `stock_quantity`: 库存数量
- `sales_count/view_count`: 销量/浏览量
- `is_featured/is_new`: 是否推荐/新品
- `history`: django-simple-history 历史记录

**ProductImage 模型字段**：
- `product`: 关联商品
- `image_url`: 图片URL
- `sort_order`: 排序

**ProductAttribute 模型字段**：
- `product`: 关联商品
- `attr_name/attr_value`: 属性名/值（如"适配车型"、"材质"）

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
- `issued_quantity`: 已发放数量（统计用，防止超发）

**UserCoupon 模型字段**：
- `status`: unused/used/expired
- `used_order`: 使用的订单（关联 Order）
- `obtained_at/used_at`: 领取/使用时间

**业务逻辑设计**：
- 优惠券与用户通过 `UserCoupon` 中间表关联（支持一人多券）
- `issued_quantity` 字段用于防止超额发放
- `used_order` 关联到 `orders.Order`，支持订单与优惠券的双向查询
- 优惠券状态转换：unused → used（订单支付时）或 unused → expired（过期）

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

### recommendations 模块
| 文件 | 作用 |
|------|------|
| `models.py` | RecommendationRule (推荐规则)、RecommendedProduct (推荐商品) |
| `serializers.py` | 推荐规则和商品序列化器 |
| `views.py` | RecommendationRuleViewSet、RecommendedProductViewSet |
| `admin.py` | 推荐管理后台配置 |
| `urls.py` | /api/recommendations/ 路由 |
| `router.py` | DRF Router 配置 |

**RecommendationRule 模型字段**：
- `rule_type`: hot (热门推荐) / new (新品推荐) / personalized (个性化推荐) / category (分类推荐)
- `config`: JSON 配置参数（如最小销量、天数等）
- `priority`: 优先级（数字越大越优先）
- `limit`: 限制数量（该规则最多返回多少个商品）
- `is_active`: 是否启用

**RecommendedProduct 模型字段**：
- `rule`: 关联推荐规则
- `product`: 关联商品
- `sort_order`: 排序权重（数字越大越靠前）
- `remark`: 备注（管理员可记录推荐理由）

**业务逻辑设计**：
- 支持多种推荐类型：热门推荐（基于销量）、新品推荐（基于时间）、个性化推荐（基于用户行为）
- `config` 字段使用 JSON 存储，灵活配置规则参数
- 管理员可手动配置推荐商品（通过 RecommendedProduct）
- `priority` 字段控制规则优先级，高优先级规则先执行
- `unique_together` 确保同一规则下商品不重复

**RecommendationRuleViewSet 自定义 Action**：
- `active`: 获取启用的推荐规则

### content 模块
| 文件 | 作用 |
|------|------|
| `models.py` | ModificationCase (改装案例)、FAQ (常见问题) |
| `serializers.py` | 改装案例和 FAQ 序列化器 |
| `views.py` | ModificationCaseViewSet、FAQViewSet |
| `admin.py` | 内容管理后台配置 |
| `urls.py` | /api/content/ 路由 |

**ModificationCase 模型字段**：
- `title`: 标题
- `summary`: 摘要
- `content`: 内容
- `cover_image`: 封面图片URL
- `author`: 作者
- `status`: draft/published（草稿/发布）
- `view_count`: 浏览量
- `sort_order`: 排序权重
- `published_at`: 发布时间

**FAQ 模型字段**：
- `question`: 问题
- `answer`: 答案
- `category`: 分类（order/payment/shipping/product/return/account/other）
- `sort_order`: 排序
- `is_active`: 是否启用

**业务逻辑设计**：
- 改装案例分为草稿和发布两种状态
- 普通用户只能查看已发布的案例
- FAQ 支持按分类筛选，只显示启用的 FAQ
- 案例详情页自动增加浏览量

### system 模块
| 文件 | 作用 |
|------|------|
| `models.py` | SystemConfig (系统配置)、Message (站内消息)、OperationLog (操作日志) |
| `serializers.py` | 系统管理序列化器 |
| `views.py` | SystemConfigViewSet、MessageViewSet、OperationLogViewSet |
| `admin.py` | 系统管理后台配置 |
| `urls.py` | /api/system/ 路由 |

**SystemConfig 模型字段**：
- `key`: 配置键（唯一）
- `value`: 配置值
- `description`: 描述
- `category`: 分类（basic/seo/trade/other）
- `is_editable`: 是否可编辑

**Message 模型字段**：
- `recipient`: 接收用户（可为空表示全员）
- `title`: 标题
- `content`: 内容
- `message_type`: 消息类型（announcement/notification/promotion/system）
- `status`: 状态（draft/sent/read）
- `sent_at`: 发送时间
- `read_at`: 阅读时间

**OperationLog 模型字段**：
- `operator`: 操作人
- `action_type`: 操作类型（create/update/delete/login/logout/other）
- `object_type`: 操作对象类型
- `object_id`: 操作对象ID
- `detail`: 操作详情
- `ip_address`: IP地址
- `status`: 状态（success/failed）

**业务逻辑设计**：
- SystemConfig 用于存储平台运行配置，支持分类管理
- Message 支持发送给指定用户或全员，消息有类型和状态区分
- OperationLog 记录所有管理员操作，便于审计
- 操作日志只允许管理员查看，不可修改或删除

**MessageViewSet 自定义 Action**：
- `my-messages`: 获取当前用户的消息
- `mark-read`: 标记消息已读

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
