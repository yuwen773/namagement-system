# 后端补充接口文档

本文档详细描述了在初始实施计划基础之上，为满足完整业务需求而补充的后端 API 接口。

## 1. 认证与授权模块补充

### 1.1 密码重置接口   ✔️已完成

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

## 2. 用户管理模块补充 ✔️已完成

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

## 3. 商品管理模块补充 ✔️已完成

### 3.1 商品分类管理接口（管理员）

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/products/categories/` | 创建新分类 | 管理员 |
| `PUT` | `/api/products/categories/{id}/` | 更新分类信息 | 管理员 |
| `DELETE` | `/api/products/categories/{id}/` | 删除分类 | 管理员 |

## 4. 订单与售后模块补充

### 4.1 订单支付与售后操作 ✔️已完成

**接口规格：**

| 方法 | URL | 描述 | 说明 |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/orders/orders/{id}/pay/` | 模拟支付 | 开发测试用，支付后状态变更为 `pending_shipment` |
| `GET` | `/api/orders/returns/` | 售后申请列表 | 用户查看自己的退换货记录 |
| `GET` | `/api/orders/returns/{id}/` | 售后申请详情 | 查看处理进度和详情 |

### 4.2 管理员订单处理接口  ✔️已完成

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

### 4.3 交易统计接口 ✔️已完成

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

### 5.1 营销管理接口（管理员） ✔️已完成

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

#### 7.1.1 系统配置接口 (SystemConfig)

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/system/configs/` | 获取系统配置列表 | 公开/管理员 |
| `GET` | `/api/system/configs/{id}/` | 获取配置详情 | 公开/管理员 |
| `POST` | `/api/system/configs/` | 创建系统配置 | 管理员 |
| `PUT` | `/api/system/configs/{id}/` | 更新系统配置 | 管理员 |
| `PATCH` | `/api/system/configs/{id}/` | 部分更新配置 | 管理员 |
| `DELETE` | `/api/system/configs/{id}/` | 删除系统配置 | 管理员 |

**查询参数：**
- `category`: 分类筛选 (basic/seo/trade/other)
- `is_editable`: 是否可编辑筛选 (true/false)
- `search`: 搜索关键词（配置键或描述）
- `ordering`: 排序字段 (category/key/created_at)
- `page`: 页码
- `page_size`: 每页数量

**响应示例 (列表)：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 10,
        "page": 1,
        "page_size": 20,
        "results": [
            {
                "id": 1,
                "key": "site_name",
                "value": "汽车改装件销售平台",
                "description": "网站名称",
                "category": "basic",
                "is_editable": true
            }
        ]
    }
}
```

**请求示例 (创建/更新)：**
```json
{
    "key": "site_name",
    "value": "汽车改装件销售平台",
    "description": "网站名称",
    "category": "basic",
    "is_editable": true
}
```

#### 7.1.2 站内消息接口 (Message)

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/system/messages/` | 获取消息列表 | 登录用户 |
| `GET` | `/api/system/messages/{id}/` | 获取消息详情（自动标记已读） | 登录用户 |
| `POST` | `/api/system/messages/` | 发送消息 | 管理员 |
| `PUT` | `/api/system/messages/{id}/` | 更新消息 | 管理员 |
| `DELETE` | `/api/system/messages/{id}/` | 删除消息 | 管理员 |
| `GET` | `/api/system/messages/my-messages/` | 获取我的消息 | 登录用户 |
| `POST` | `/api/system/messages/{id}/mark-read/` | 标记消息已读 | 登录用户 |

**查询参数：**
- `message_type`: 消息类型筛选 (announcement/notification/promotion/system)
- `status`: 状态筛选 (draft/sent/read)
- `search`: 搜索关键词（标题或内容）
- `ordering`: 排序字段
- `page`: 页码
- `page_size`: 每页数量

**响应示例 (列表)：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 5,
        "page": 1,
        "page_size": 20,
        "results": [
            {
                "id": 1,
                "recipient": 10,
                "recipient_name": "张三",
                "title": "系统维护通知",
                "content": "系统将于今晚进行维护...",
                "message_type": "announcement",
                "status": "sent",
                "sent_at": "2024-01-15T10:00:00Z",
                "read_at": null,
                "created_at": "2024-01-15T09:00:00Z"
            }
        ]
    }
}
```

**请求示例 (发送消息)：**
```json
{
    "recipient": null,
    "title": "系统维护通知",
    "content": "系统将于今晚进行维护...",
    "message_type": "announcement"
}
```
> 注：`recipient` 为 `null` 表示全员消息

#### 7.1.3 操作日志接口 (OperationLog)

**接口规格：**

| 方法 | URL | 描述 | 权限 |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/system/logs/` | 获取操作日志列表 | 管理员 |
| `GET` | `/api/system/logs/{id}/` | 获取日志详情 | 管理员 |

**查询参数：**
- `action_type`: 操作类型筛选 (create/update/delete/login/logout/other)
- `object_type`: 对象类型筛选
- `status`: 状态筛选 (success/failed)
- `search`: 搜索关键词（操作详情或对象）
- `ordering`: 排序字段
- `page`: 页码
- `page_size`: 每页数量

**响应示例 (列表)：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "page": 1,
        "page_size": 20,
        "results": [
            {
                "id": 1,
                "operator": 1,
                "operator_name": "管理员",
                "action_type": "create",
                "action_type_display": "创建",
                "object_type": "Product",
                "object_id": "123",
                "detail": "创建商品: 汽车保险杠",
                "ip_address": "192.168.1.100",
                "status": "success",
                "status_display": "成功",
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    }
}
```

#### 7.1.4 字段说明

**系统配置分类 (category)：**
- `basic`: 基础配置（网站名称、LOGO等）
- `seo`: SEO配置（关键词、描述等）
- `trade`: 交易配置（订单超时时间等）
- `other`: 其他配置

**消息类型 (message_type)：**
- `announcement`: 系统公告
- `notification`: 订单通知
- `promotion`: 促销通知
- `system`: 系统通知

**消息状态 (status)：**
- `draft`: 草稿
- `sent`: 已发送
- `read`: 已读

**操作类型 (action_type)：**
- `create`: 创建
- `update`: 更新
- `delete`: 删除
- `login`: 登录
- `logout`: 登出
- `other`: 其他
