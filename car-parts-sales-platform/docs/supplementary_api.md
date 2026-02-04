# 后端补充接口文档

本文档详细描述了在初始实施计划基础之上，为满足完整业务需求而补充的后端 API 接口。

## 1. 认证与授权模块补充

### 1.1 密码重置接口

**接口规格：**
- **URL**: `POST /api/auth/password/reset/`
- **描述**: 用户忘记密码时，通过验证码重置密码。
- **请求体**:
  ```json
  {
      "username": "13800138000",
      "new_password": "new_password123",
      "code": "123456"  // 模拟验证码
  }
  ```
- **响应**:
  ```json
  {
      "code": 200,
      "message": "密码重置成功",
      "data": null
  }
  ```

## 2. 用户管理模块补充

### 2.1 管理员用户管理接口

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/users/users/` | 获取用户列表（支持搜索、分页） | 管理员 |
| `GET` | `/api/users/users/{id}/` | 获取特定用户详细信息（含积分、地址） | 管理员 |
| `PATCH` | `/api/users/users/{id}/status/` | 禁用/启用用户账号 | 管理员 |

**请求示例 (禁用用户):**
```json
// PATCH /api/users/users/1/status/
{
    "is_active": false
}
```

## 3. 商品管理模块补充

### 3.1 商品分类管理接口（管理员）

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/products/categories/` | 创建新分类 | 管理员 |
| `PUT` | `/api/products/categories/{id}/` | 更新分类信息 | 管理员 |
| `DELETE` | `/api/products/categories/{id}/` | 删除分类 | 管理员 |

## 4. 订单与售后模块补充

### 4.1 订单支付与售后操作

**接口规格：**

| 方法 | URL | 描述 | 说明 |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/orders/orders/{id}/pay/` | 模拟支付 | 开发测试用，支付后状态变更为 `pending_shipment` |
| `GET` | `/api/orders/returns/` | 售后申请列表 | 用户查看自己的退换货记录 |
| `GET` | `/api/orders/returns/{id}/` | 售后申请详情 | 查看处理进度和详情 |

### 4.2 管理员订单处理接口

**接口规格：**

| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| `GET` | `/api/orders/admin/orders/` | 管理员订单列表（支持多维度筛选） |
| `GET` | `/api/orders/admin/orders/{id}/` | 管理员订单详情 |
| `POST` | `/api/orders/returns/{id}/audit/` | 售后申请审核 |

**请求示例 (售后审核):**
```json
// POST /api/orders/returns/1/audit/
{
    "status": "approved", // 或 rejected
    "admin_note": "同意退货，请寄回..."
}
```

### 4.3 交易统计接口

**接口规格：**
- **URL**: `GET /api/orders/stats/`
- **描述**: 获取交易统计数据，用于后台仪表盘展示。
- **响应**:
  ```json
  {
      "code": 200,
      "data": {
          "sales_trend": [...], // 销售趋势图表数据
          "order_status_distribution": {...}, // 订单状态分布
          "top_selling_products": [...] // 热销商品排行
      }
  }
  ```

## 5. 营销管理模块补充

### 5.1 营销管理接口（管理员）

**接口规格：**

| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| `POST` | `/api/marketing/coupons/` | 创建优惠券 |
| `PUT` | `/api/marketing/coupons/{id}/` | 更新优惠券 |
| `DELETE` | `/api/marketing/coupons/{id}/` | 删除优惠券 |
| `GET` | `/api/marketing/stats/` | 优惠券发放与核销统计 |
| `POST` | `/api/marketing/promotions/` | 创建促销活动 |
| `GET` | `/api/marketing/promotions/` | 获取促销活动列表 |
| `POST` | `/api/marketing/banners/` | 上传/创建 Banner 轮播图 |
| `GET` | `/api/marketing/banners/` | 获取 Banner 列表（后台管理用） |

## 6. 用户评价模块补充

### 6.1 我的评价接口

**接口规格：**
- **URL**: `GET /api/products/reviews/me/`
- **描述**: 获取当前登录用户发表的所有评价记录。

## 7. 系统管理模块补充（新模块）

### 7.1 系统配置与日志接口

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/system/config/` | 获取系统配置（网站名称、SEO等） | 公开/管理员 |
| `POST` | `/api/system/config/` | 更新系统配置 | 管理员 |
| `POST` | `/api/system/messages/` | 发布站内信/通知 | 管理员 |
| `GET` | `/api/system/messages/` | 获取我的消息列表 | 登录用户 |
| `GET` | `/api/system/logs/` | 获取系统操作日志 | 管理员 |
