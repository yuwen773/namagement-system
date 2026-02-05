# 架构设计

> 技术栈、目录结构和核心设计决策

## 技术栈

```
后端: Python 3.12 + Django 6.0 + DRF 3.16 + JWT
数据库: MySQL 8.0
前端: Vue 3 + Vite + Element Plus + Pinia + Vue Router 4
```

## 目录结构

```
backend/
├── config/          # Django 项目配置
├── apps/
│   ├── users/       # 认证、用户、地址、浏览历史
│   ├── products/    # 商品、分类、评价
│   ├── orders/      # 订单、购物车、退换货
│   ├── marketing/   # 优惠券
│   ├── recommendations/ # 推荐规则、推荐商品
│   ├── content/     # 改装案例、FAQ
│   └── system/      # 配置、消息、日志
├── utils/           # ApiResponse、分页、异常
└── scripts/         # 数据填充、验证

frontend/src/
├── api/modules/     # API 封装
├── components/layouts/  # 布局组件
├── views/admin/     # 管理端页面
├── stores/          # Pinia 状态管理
├── router/          # 路由配置
└── utils/           # 工具函数
```

## 状态机

```
订单: pending_payment → pending_shipment → shipped → completed
         ↓                 ↓              ↓
      cancelled        cancelled    return_processing

商品: draft → pending → published → archived

用户优惠券: unused → used / expired
```

## 认证机制

| 项 | 说明 |
|:---|:-----|
| Token 类型 | JWT (Access 2h, Refresh 7d) |
| 标识字段 | 手机号 (phone) |
| 传递方式 | `Authorization: Bearer {token}` |
| 存储位置 | localStorage |

## API 响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

## 关键设计决策

| 决策 | 说明 |
|:-----|:-----|
| 数据冗余 | OrderItem/CartItem 存储商品快照，防止商品删除后数据丢失 |
| 分类设计 | 自关联外键实现无限级分类 |
| 购物车 | Cart 与 User 一对一，自动计算 total_items/total_price |
| 默认地址 | 设置新默认地址时自动取消旧默认地址 |
| 优惠券 | 发放时检查 total_quantity 和 per_user_limit，防止并发超领 |
| 推荐规则 | 支持 hot/new/personalized/category 四种类型，优先级排序 |

## API 路由

```
/api/auth/           → 注册、登录、当前用户
/api/users/          → 用户管理、地址、浏览历史
/api/products/       → 商品、分类、评价
/api/orders/         → 订单、购物车、退换货
/api/marketing/      → 优惠券、用户优惠券
/api/recommendations/ → 推荐规则、推荐商品
/api/content/        → 改装案例、FAQ
/api/system/         → 系统配置、消息、日志
```

## 管理端组件组织

```
views/admin/
├── ProductManageView.vue  +  ProductEditDialog, CategoryManageDialog
├── UserManageView.vue     +  UserDetailDialog
├── OrderManageView.vue    +  OrderDetailDialog, ShipDialog
│                           +  ReturnDetailDialog, ReturnProcessDialog
├── MarketingManageView.vue +  CouponEditDialog
├── RecommendationManageView.vue  # 推荐规则、推荐商品
├── DashboardView.vue      # 交易统计、图表
├── ContentManageView.vue   # 改装案例、FAQ
└── SystemManageView.vue    # 配置、消息、日志
```

## 推荐管理架构

### 数据模型
```
RecommendationRule (推荐规则)
├── rule_type: hot | new | personalized | category
├── name: 规则名称
├── priority: 优先级 (0-999)
├── limit: 返回商品数量限制
├── config: JSON 配置 (销量/时间/权重)
├── is_active: 启用状态
└── product_count: 已配置商品数

RecommendedProduct (推荐商品)
├── rule: 关联规则
├── product: 关联商品
├── sort_order: 排序权重
└── remark: 备注
```

### 前端组件

| 文件 | 职责 |
|:-----|:-----|
| `RecommendationManageView.vue` | 主页面：规则管理、商品管理、统计监控 |
| `recommendation.js` | API 封装 |

### 功能清单

| 模块 | 功能 |
|:-----|:-----|
| 规则管理 | CRUD、启用/禁用、优先级排序 |
| 商品管理 | 添加/移除、排序权重调整 |
| 效果监控 | 规则统计、商品统计、类型分布 |

## 内容管理架构

### 数据模型
```
ModificationCase (改装案例)
├── title: 案例标题
├── summary: 案例摘要
├── content: 详细内容 (富文本)
├── cover_image: 封面图片
├── author: 作者
├── status: 状态 (draft | published)
├── sort_order: 排序值
├── published_at: 发布时间
├── view_count: 浏览次数
└── created_at: 创建时间

FAQ (常见问题)
├── question: 问题
├── answer: 答案
├── category: 分类 (order | payment | shipping | product | return | other)
├── sort_order: 排序值
├── is_active: 是否启用
└── created_at: 创建时间
```

### 前端组件

| 文件 | 职责 |
|:-----|:-----|
| `ContentManageView.vue` | 主页面：案例管理、FAQ 管理、统计卡片 |
| `content.js` | API 封装 |

### 功能清单

| 模块 | 功能 |
|:-----|:-----|
| 案例管理 | CRUD、发布/草稿状态切换、封面图片、富文本内容 |
| FAQ 管理 | CRUD、分类管理、启用/禁用、排序 |
| 统计卡片 | 案例总数/已发布/草稿数、FAQ 总数/已启用/未启用数 |

## 系统管理架构

### 数据模型
```
SystemConfig (系统配置)
├── key: 配置键（唯一）
├── value: 配置值
├── description: 配置描述
├── category: 分类 (basic | seo | trade | other)
├── is_editable: 是否可编辑
├── created_at: 创建时间
└── updated_at: 更新时间

Message (消息通知)
├── recipient: 接收用户 ID（为空表示全员消息）
├── title: 消息标题
├── content: 消息内容
├── message_type: 消息类型 (announcement | notification | promotion | system)
├── status: 消息状态 (draft | sent | read)
├── sent_at: 发送时间
├── read_at: 阅读时间
└── created_at: 创建时间

OperationLog (操作日志)
├── operator: 操作人 ID
├── operator_name: 操作人昵称（只读）
├── action_type: 操作类型 (create | update | delete | login | logout | other)
├── object_type: 操作对象类型（表名）
├── object_id: 操作对象 ID
├── detail: 操作详情
├── ip_address: IP 地址
├── status: 操作状态 (success | failed)
├── error_message: 错误信息（失败时）
└── created_at: 操作时间
```

### 前端组件

| 文件 | 职责 |
|:-----|:-----|
| `SystemManageView.vue` | 主页面：系统配置、消息通知、操作日志（Tab 切换）|
| `system.js` | API 封装 |

### 功能清单

| 模块 | 功能 |
|:-----|:-----|
| 系统配置 | CRUD、分类管理、编辑权限控制、只读配置保护 |
| 消息通知 | 发送消息（全员/定向）、草稿编辑、查看详情、删除 |
| 操作日志 | 查看详情、筛选（操作类型、状态）、搜索 |
| 统计卡片 | 配置总数/可编辑/只读/基础、消息总数/草稿/已发送/已读、日志总数/成功/失败/今日 |

## 交易统计架构

### 数据源

```
后端统计接口
├── GET /api/orders/stats/
│   ├── sales_trend: 销售趋势数据（日期、金额）
│   ├── order_status_distribution: 订单状态分布
│   └── top_selling_products: 热销商品列表（商品ID、名称、销量、销售额）
│
└── GET /api/marketing/stats/
    ├── total_coupons: 优惠券总数
    ├── active_coupons: 启用中优惠券
    ├── total_issued: 已发放数量
    ├── total_used: 已使用数量
    └── usage_rate: 使用率
```

### 前端组件

| 文件 | 职责 |
|:-----|:-----|
| `DashboardView.vue` | 主页面：统计卡片、图表展示、数据筛选 |
| `order.js` | API 封装（getOrderStatsApi） |
| `marketing.js` | API 封装（getMarketingStatsApi） |

### 功能清单

| 模块 | 功能 |
|:-----|:-----|
| 统计卡片 | 总订单数、待处理订单、已完成订单、总销售额、趋势百分比 |
| 销售趋势图 | 日/周/月销售额折线图、双 Y 轴（销售额 + 订单数）、时间筛选 |
| 订单状态分布 | 饼图展示各状态订单占比、悬停显示详情 |
| 热销商品排行 | 按销量/金额切换、TOP10 水平条形图 |
| 优惠券核销统计 | 已使用/未使用/已过期饼图 |
| 时间筛选器 | 日期范围选择、数据自动刷新 |

### 数据处理

```javascript
// 前端按时间段分组订单数据
const groupOrdersByPeriod = (orders, period) => {
  // period: 'day' | 'week' | 'month'
  // 返回: { '2024-01-01': { amount: 10000, count: 5 }, ... }
}

// 订单状态映射
const orderStatusMap = {
  pending_payment: { label: '待付款', color: '#f59e0b' },
  pending_shipment: { label: '待发货', color: '#6b7280' },
  shipped: { label: '已发货', color: '#3b82f6' },
  completed: { label: '已完成', color: '#10b981' },
  cancelled: { label: '已取消', color: '#ef4444' },
  return_processing: { label: '退货中', color: '#f97316' }
}
```

### ECharts 配置

| 图表 | 类型 | 特性 |
|:-----|:-----|:-----|
| 销售趋势 | Line + Area | 双 Y 轴、渐变填充、平滑曲线 |
| 订单状态分布 | Pie (Donut) | 环形图、自定义颜色、悬停放大 |
| 热销商品 | Bar (Horizontal) | 水平条形、渐变色、数值标签 |
| 优惠券核销 | Pie (Donut) | 环形图、图例右侧显示 |
