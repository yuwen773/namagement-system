# 架构设计

## 技术栈

### 后端
- Python 3.12.7 + Django 6.0.2 + DRF 3.16.1
- JWT 认证 (djangorestframework-simplejwt)
- MySQL 8.0+ (utf8mb4)

### 前端
- Vue 3 + Vite 7 + Element Plus
- Pinia 状态管理 + Vue Router 4
- Tailwind CSS + Axios

## 目录结构

```
backend/
├── config/              # Django 配置、路由
├── apps/
│   ├── users/           # User, UserAddress
│   ├── products/        # Category, Product, Review
│   ├── orders/          # Order, OrderItem, Cart, ReturnRequest
│   ├── marketing/       # Coupon, UserCoupon
│   ├── recommendations/ # RecommendationRule
│   ├── content/         # ModificationCase, FAQ
│   └── system/          # SystemConfig, Message, OperationLog
├── utils/               # ApiResponse, 分页, 异常
└── scripts/             # 数据填充、验证、导出

frontend/
├── src/
│   ├── api/             # 请求封装、API 模块
│   ├── components/      # 公共组件
│   │   ├── common/      # AppHeader, AppFooter, Breadcrumb
│   │   └── layouts/     # UserLayout, AdminLayout
│   ├── views/           # 页面组件
│   ├── stores/          # Pinia 状态管理
│   ├── router/          # 路由配置
│   └── utils/           # 工具函数
└── public/              # 静态资源
```

## 数据模型关系

```
User (1) ──► (N) UserAddress
User (1) ──► (N) Order
User (1) ──► (1) Cart ──► (N) CartItem
User (1) ──► (N) UserCoupon
User (1) ──► (N) Review

Category (1) ──► (N) Category (自关联)
Category (1) ──► (N) Product

Product (1) ──► (N) ProductImage
Product (1) ──► (N) ProductAttribute
Product (1) ──► (N) OrderItem
Product (1) ──► (N) Review

Coupon (1) ──► (N) UserCoupon
Order (1) ──► (N) OrderItem
Order (1) ──► (N) ReturnRequest
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
- 手机号唯一标识 (username 已禁用)
- Token 存储在 localStorage

### API 响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {...}
}
```

分页响应:
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

## 前端布局架构

### 用户端布局 (UserLayout)
- **文件**: `frontend/src/components/layouts/UserLayout.vue`
- **作用**: 包装所有用户端页面，提供统一的头部和底部
- **子组件**:
  - `AppHeader.vue` - 顶部导航栏
  - `AppFooter.vue` - 底部信息栏
- **特性**: 支持页面切换动画、返回顶部按钮

### 管理端布局 (AdminLayout)
- **文件**: `frontend/src/views/admin/AdminLayout.vue`
- **作用**: 管理后台专用布局
- **子组件**:
  - `AdminSidebar.vue` - 左侧导航菜单（可折叠）
  - `Breadcrumb.vue` - 面包屑导航
- **特性**: 支持侧边栏折叠、响应式适配

### AppHeader 组件
- **文件**: `frontend/src/components/common/AppHeader.vue`
- **功能**:
  - 顶部欢迎语 + 用户登录状态导航
  - Logo + 搜索框 + 购物车图标
  - 主导航菜单（首页、全部商品、分类、热销、新品、领券中心）
- **特性**:
  - 购物车数量角标
  - 消息中心未读数量提示
  - 响应式适配（移动端隐藏部分元素）

### AppFooter 组件
- **文件**: `frontend/src/components/common/AppFooter.vue`
- **功能**:
  - 新手指南、配送方式、售后服务、关于我们等链接
  - 客服热线和服务时间
  - 友情链接
  - 版权信息和备案号
- **特性**: 响应式三栏布局

### AdminSidebar 组件
- **文件**: `frontend/src/components/common/AdminSidebar.vue`
- **功能**:
  - Logo 区域 + 折叠按钮
  - 导航菜单（数据统计、商品/订单/用户/营销/内容/系统管理）
  - 底部快捷按钮（返回前台、退出登录）
- **特性**:
  - 折叠状态持久化到 localStorage
  - 与 AdminLayout 通过 storage 事件同步

### Breadcrumb 组件
- **文件**: `frontend/src/components/common/Breadcrumb.vue`
- **功能**: 自动生成面包屑导航
- **特性**:
  - 支持用户端和管理端路由
  - 自动识别详情页
  - 支持自定义右侧内容插槽

## 关键设计决策

### 数据冗余
- OrderItem/CartItem 存储商品快照 (名称、图片、价格)
- 防止商品删除/修改导致历史数据丢失

### 分类设计
- 自关联外键实现无限级分类
- 叶子分类 (无子分类) 用于关联商品

### 购物车
- Cart 与 User 一对一关系
- 自动计算 total_price 和 total_quantity

### 地址管理
- 设置新默认地址时自动取消旧默认地址

### 评价系统
- 每个订单商品只能评价一次
- 评价关联 order_item_id

### 前端路由设计
- 嵌套路由：用户端使用 UserLayout，管理端使用 AdminLayout
- 路由守卫：自动获取用户信息、检查登录状态、验证管理员权限
- 登录/注册页面独立布局（无头部底部）

## 前端设计系统

### 设计理念
**Industrial Performance Aesthetic** - 工业性能美学
- 体现汽车改装行业的专业性和技术感
- 深色主题配合玻璃态效果
- 橙色强调色 (#f97316) 体现性能感

### 设计规范文档
详见 `docs/frontend-design-system.md`，包含：
- 颜色系统（主色、中性色、功能色）
- 排版系统（字体家族、大小、字重）
- 间距系统（基于 4px 的 7 级体系）
- 组件规范（按钮、输入框、卡片、徽章等）
- 响应式设计（5 级断点）
- 动画与交互（过渡、缓动、悬停效果）
- 代码规范（Vue、CSS、TypeScript）

### 已实现页面
- HomeView.vue - 首页（动态渐变背景、分类导航、商品推荐）
- ProductListView.vue - 商品列表页（筛选侧边栏、搜索排序）
- ProductDetailView.vue - 商品详情页（图片画廊、评价系统）
- CartView.vue - 购物车页（商品列表、订单摘要）
- LoginView.vue - 登录页（分屏设计、品牌展示）

### 已实现组件
- AppHeader.vue - 深色玻璃态头部
- AppFooter.vue - 深色主题底部
- AdminSidebar.vue - 可折叠侧边栏
- Breadcrumb.vue - 自动生成面包屑
- UserLayout.vue - 用户端布局容器
- AdminLayout.vue - 管理端布局容器

## 前端路由设计
- 嵌套路由：用户端使用 UserLayout，管理端使用 AdminLayout
- 路由守卫：自动获取用户信息、检查登录状态、验证管理员权限
- 登录/注册页面独立布局（无头部底部）
