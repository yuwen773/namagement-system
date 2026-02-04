# 开发进度

## 阶段状态

| 阶段 | 状态 | 完成内容 |
|------|------|----------|
| 一：项目初始化 | ✅ | 后端结构、JWT认证、统一响应、分页 |
| 二：数据库设计 | 🔄 | users、marketing、orders 模块已完成 |
| 三：后端API | 🔄 | users、orders、marketing API 已完成 |
| 四：模拟数据 | ⏳ | - |
| 五：前端开发 | ⏳ | - |
| 六：测试部署 | ⏳ | - |

## 已完成模块

### users 模块 (2026-02-04)
- `models.py`: User、UserAddress 模型
- `serializers.py`: 用户相关序列化器
- `views.py`: 认证视图集（注册、登录、获取当前用户）
- `admin.py`: Django Admin 配置
- `urls.py`: 用户路由配置

### marketing 模块 (2026-02-04)
- `models.py`: Coupon、UserCoupon 模型
- `admin.py`: Django Admin 配置
- `migrations/0001_initial.py`: 数据库迁移

### orders 模块 (2026-02-04)
- `models.py`: Order、OrderItem、ReturnRequest 模型
  - Order: 订单号、用户、收货地址、金额、状态、物流、时间戳
  - OrderItem: 订单商品（冗余商品信息）
  - ReturnRequest: 退换货申请（类型、原因、凭证、状态）
- `serializers.py`: 订单相关序列化器
  - OrderListSerializer: 订单列表
  - OrderDetailSerializer: 订单详情
  - OrderCreateSerializer: 创建订单
  - ReturnRequestListSerializer/DetailSerializer: 退换货
- `views.py`: 订单视图集
  - OrderViewSet: CRUD + cancel/confirm/ship/my-orders
  - ReturnRequestViewSet: CRUD + process
- `admin.py`: Django Admin 配置
- `urls.py`: 订单路由配置

## 待办

- products模块：Category、Product、ProductImage、ProductAttribute
- recommendations模块：RecommendationRule、RecommendedProduct
- content模块：ModificationCase、FAQ
- system模块：SystemConfig、Message、OperationLog

## API 端点

### 订单模块 (`/api/orders/`)
| 端点 | 方法 | 描述 |
|------|------|------|
| `/orders/` | GET | 订单列表 |
| `/orders/` | POST | 创建订单 |
| `/orders/{id}/` | GET | 订单详情 |
| `/orders/{id}/` | PUT/PATCH | 更新订单 |
| `/orders/{id}/` | DELETE | 删除订单 |
| `/orders/{id}/cancel/` | POST | 取消订单 |
| `/orders/{id}/confirm/` | POST | 确认收货 |
| `/orders/{id}/ship/` | POST | 订单发货（管理员） |
| `/orders/my-orders/` | GET | 我的订单 |
| `/returns/` | GET | 退换货列表 |
| `/returns/` | POST | 创建退换货申请 |
| `/returns/{id}/process/` | POST | 处理退换货（管理员） |

## 版本

- Python: 3.12.7
- Django: 6.0.2
- DRF: 3.16.1
