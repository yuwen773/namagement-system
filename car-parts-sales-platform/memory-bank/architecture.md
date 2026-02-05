# 架构设计

## 技术栈

| 层 | 技术 |
|:---|:-----|
| 后端 | Python 3.12 + Django 6.0 + DRF 3.16 + JWT |
| 数据库 | MySQL 8.0 (utf8mb4) |
| 前端 | Vue 3 + Vite + Element Plus + Pinia |

## 目录结构

```
backend/
├── config/          # Django 配置
├── apps/
│   ├── users/       # 认证、用户、地址、浏览历史
│   ├── products/    # 商品、分类、评价、图片、属性
│   ├── orders/      # 订单、购物车、退换货
│   ├── marketing/   # 优惠券、促销、Banner
│   ├── recommendations/ # 推荐规则、商品
│   ├── content/     # 改装案例、FAQ
│   └── system/      # 配置、消息、日志
├── utils/           # 响应封装、分页、异常
└── scripts/         # 工具脚本

frontend/src/
├── api/modules/     # API 封装
├── stores/          # Pinia 状态
├── router/          # 路由
└── views/           # 页面
```

## 状态机

```
订单：pending_payment → pending_shipment → shipped → completed
        ↓                   ↓              ↓
     cancelled           cancelled     return_processing

商品：draft → pending → published → archived
```

## API 路由

```
/api/auth/           # 注册、登录、当前用户
/api/users/          # 用户、地址、浏览历史
/api/products/       # 商品、分类、评价
/api/orders/         # 订单、购物车、退换货
/api/marketing/      # 优惠券、促销、Banner
/api/recommendations/ # 推荐规则、商品
/api/content/        # 改装案例、FAQ
/api/system/         # 配置、消息、日志
```

## 关键设计

| 模式 | 说明 |
|:-----|:-----|
| 数据冗余 | OrderItem/CartItem 存储商品快照 |
| 分类 | 自关联实现无限级分类 |
| 购物车 | User 一对一，自动计算总数 |
| 优惠券 | 防止并发超领 |
| 推荐规则 | hot/new/personalized/category 四种类型 |

## API 响应格式

```json
{ "code": 200, "message": "操作成功", "data": {...} }
```

分页：`{ "count": 100, "page": 1, "page_size": 20, "results": [...] }`
