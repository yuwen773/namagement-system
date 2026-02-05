# 架构设计

## 技术栈

**后端**: Python 3.12.7 + Django 6.0.2 + DRF 3.16.1 + JWT + MySQL 8.0+
**前端**: Vue 3 + Vite 7 + Element Plus + Pinia + Vue Router 4 + Tailwind CSS

## 目录结构

```
backend/
├── config/          # Django 配置
├── apps/
│   ├── users/       # User, UserAddress, BrowsingHistory
│   ├── products/    # Category, Product, Review
│   ├── orders/      # Order, OrderItem, Cart, ReturnRequest
│   ├── marketing/   # Coupon, UserCoupon
│   ├── recommendations/ # RecommendationRule
│   ├── content/     # ModificationCase, FAQ
│   └── system/      # SystemConfig, Message, OperationLog
├── utils/           # ApiResponse, 分页, 异常
└── scripts/         # 数据填充、验证

frontend/src/
├── api/             # API 封装
├── components/      # 公共组件
├── views/           # 页面组件
├── stores/          # Pinia 状态管理
├── router/          # 路由配置
└── utils/           # 工具函数
```

## 数据模型关系

```
User (1) ──► (N) UserAddress, Order, Cart, UserCoupon, Review, BrowsingHistory
Cart (1) ──► (N) CartItem
Order (1) ──► (N) OrderItem, ReturnRequest
Category (1) ──► (N) Category (自关联), Product
Product (1) ──► (N) ProductImage, ProductAttribute, Review
Coupon (1) ──► (N) UserCoupon
```

## 核心业务逻辑

### 订单状态机
```
pending_payment → pending_shipment → shipped → completed
    ↓                    ↓               ↓
  cancelled           cancelled        return_processing
```

### 商品状态流
```
draft → pending → published → archived
```

### 认证机制
- JWT Token: Access 2小时, Refresh 7天
- 手机号唯一标识
- 密码明文存储（开发环境）

### API 响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {...}
}
```

## 前端页面组件

| 页面 | 功能 |
|------|------|
| Home | 轮播图、分类导航、热门推荐、新品推荐 |
| ProductList | 分类筛选、价格筛选、排序、分页 |
| ProductDetail | 放大镜、属性展示、相关推荐、评价列表、浏览历史追踪 |
| Cart | 商品管理、优惠券选择、价格计算 |
| Checkout | 地址选择/新增、优惠券选择、商品清单、金额明细 |
| Payment | 订单信息、支付方式选择、支付结果、倒计时 |
| OrderList | 状态筛选、订单搜索、支付/取消/确认功能 |
| OrderDetail | 状态时间轴、物流信息、价格明细、退换货 |
| UserCenter | 个人资料、地址管理、积分、优惠券、评价、售后、消息 |
| BrowsingHistory | 按时间分组显示、快捷操作、清空历史 |

## 设计系统

**Industrial Performance Aesthetic** - 工业性能美学
- 深色主题 (#0f172a, #1e293b)
- 橙色强调色 (#f97316)
- 玻璃态效果 (backdrop-filter)

## 关键设计决策

| 决策 | 说明 |
|------|------|
| 数据冗余 | OrderItem/CartItem 存储商品快照，防止数据丢失 |
| 分类设计 | 自关联外键实现无限级分类 |
| 购物车 | Cart 与 User 一对一，自动计算总额 |
| 地址管理 | 设置新默认地址时自动取消旧默认地址 |
| 评价系统 | 每个订单商品只能评价一次 |
| 浏览历史 | 商品快照存储，自动去重，软关联设计 |

## API 路由

```
/api/auth/          → 认证 (register, login, me)
/api/users/         → 用户管理、地址、浏览历史
/api/products/      → 商品、分类、评价
/api/orders/        → 订单、购物车、退换货
/api/marketing/     → 优惠券
/api/recommendations/ → 推荐规则
/api/content/       → 改装案例、FAQ
/api/system/        → 系统配置、消息、日志
```

## 购物车架构

### 数据模型
- Cart: 与 User 一对一，存储 total_items、total_price
- CartItem: 存储商品快照防止数据丢失

### 优惠券计算
- 满减券: `selectedPrice >= min_purchase_amount` 时抵扣 `discount_amount`
- 折扣券: `selectedPrice × discount_percent / 100`

## 浏览历史架构

### BrowsingHistory 模型
```python
user: ForeignKey(User)
product_id: IntegerField
product_name: CharField  # 快照
product_image: URLField  # 快照
product_price: DecimalField  # 快照
viewed_at: DateTimeField
```

### 设计决策
- **商品快照**: 存储名称、图片、价格，防止商品删除后历史失效
- **自动去重**: 同一商品多次浏览只保留最新记录
- **软关联**: 使用 product_id 而非外键，允许商品删除后历史记录仍可展示

### 自动追踪
在 ProductDetailView 中，登录用户访问商品详情时自动记录浏览历史，静默失败不影响体验。
