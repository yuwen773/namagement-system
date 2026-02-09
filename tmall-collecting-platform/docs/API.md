# 天猫潮玩电商数据采集系统 - API 接口文档

## 文档概述

本文档描述了天猫潮玩电商数据采集系统的所有 RESTful API 接口。

- **基础路径**: `http://localhost:8000/api`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

---

## API 响应格式规范

### 成功响应

```json
{
    "code": 0,
    "message": "操作成功",
    "data": { ... },
    "total": 100
}
```

### 错误响应

```json
{
    "code": -1,
    "message": "错误描述",
    "data": null
}
```

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 202 | 异步任务已接受 |
| 400 | 请求参数错误 |
| 401 | 未认证（缺少或无效的Token） |
| 403 | 无权限（非管理员） |
| 404 | 资源不存在 |
| 409 | 资源冲突（如已有运行中的任务） |
| 500 | 服务器内部错误 |

---

## 认证说明

### Token 使用方式

所有需要认证的接口必须在请求头中携带 Token：

```http
Authorization: Bearer <access_token>
```

### Token 获取

通过登录接口获取 `access_token`，有效期为 2 小时。

---

## 1. 用户认证模块

### 1.1 用户注册

无需 Token 即可访问。

**接口**: `POST /api/users/register/`

**请求体**:

```json
{
    "username": "test_user",
    "password": "123456",
    "email": "test@example.com"
}
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，唯一 |
| password | string | 是 | 密码，最少6位 |
| email | string | 否 | 邮箱地址 |

**成功响应** (201):

```json
{
    "code": 0,
    "message": "注册成功",
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "test_user",
        "email": "test@example.com",
        "role": "user",
        "status": "active",
        "created_at": "2026-02-07T10:00:00Z"
    }
}
```

**错误响应** (400):

```json
{
    "code": -1,
    "message": "用户名已存在"
}
```

---

### 1.2 用户登录

无需 Token 即可访问。

**接口**: `POST /api/users/login/`

**请求体**:

```json
{
    "username": "test_user",
    "password": "123456"
}
```

**成功响应** (200):

```json
{
    "code": 0,
    "message": "登录成功",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "username": "test_user",
            "email": "test@example.com",
            "role": "user",
            "role_display": "普通用户",
            "status": "active",
            "status_display": "正常",
            "avatar": null,
            "phone": null
        }
    }
}
```

**错误响应** (401):

```json
{
    "code": -1,
    "message": "用户名或密码错误"
}
```

或（账户被冻结）

```json
{
    "code": -1,
    "message": "账户已被冻结，请联系管理员"
}
```

---

### 1.3 获取当前用户信息

**接口**: `GET /api/users/profile/`

**请求头**:

```http
Authorization: Bearer <access_token>
```

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "test_user",
        "email": "test@example.com",
        "role": "user",
        "role_display": "普通用户",
        "status": "active",
        "status_display": "正常",
        "avatar": null,
        "phone": null,
        "created_at": "2026-02-07T10:00:00Z",
        "updated_at": "2026-02-07T10:00:00Z"
    }
}
```

---

### 1.4 修改密码

**接口**: `POST /api/users/change-password/`

**请求头**:

```http
Authorization: Bearer <access_token>
```

**请求体**:

```json
{
    "old_password": "123456",
    "new_password": "654321"
}
```

**成功响应** (200):

```json
{
    "code": 0,
    "message": "密码修改成功"
}
```

**错误响应** (400):

```json
{
    "code": -1,
    "message": "原密码错误"
}
```

---

## 2. 用户管理模块（管理员）

> 以下接口仅管理员可访问

### 2.1 获取用户列表

**接口**: `GET /api/users/`

**请求头**:

```http
Authorization: Bearer <access_token>
```

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| role | string | 否 | 角色筛选: admin/user |
| status | string | 否 | 状态筛选: active/frozen |
| search | string | 否 | 搜索用户名 |

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "username": "test_user",
            "email": "test@example.com",
            "role": "user",
            "role_display": "普通用户",
            "status": "active",
            "status_display": "正常",
            "avatar": null,
            "phone": null,
            "created_at": "2026-02-07T10:00:00Z",
            "updated_at": "2026-02-07T10:00:00Z"
        }
    ],
    "total": 100
}
```

---

### 2.2 获取用户详情

**接口**: `GET /api/users/{id}/`

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | uuid | 用户ID |

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "test_user",
        "email": "test@example.com",
        "role": "user",
        "role_display": "普通用户",
        "status": "active",
        "status_display": "正常",
        "avatar": null,
        "phone": null,
        "created_at": "2026-02-07T10:00:00Z",
        "updated_at": "2026-02-07T10:00:00Z"
    }
}
```

---

### 2.3 更新用户信息

**接口**: `PUT /api/users/{id}/`

**请求体**:

```json
{
    "email": "newemail@example.com",
    "avatar": "https://example.com/avatar.jpg",
    "phone": "13800138000"
}
```

**成功响应** (200):

```json
{
    "code": 0,
    "message": "用户信息更新成功",
    "data": { ... }
}
```

---

### 2.4 删除用户

**接口**: `DELETE /api/users/{id}/`

**成功响应** (200):

```json
{
    "code": 0,
    "message": "用户删除成功"
}
```

---

### 2.5 修改用户状态（冻结/解冻）

**接口**: `POST /api/users/{id}/status/`

**请求体**:

```json
{
    "status": "frozen"
}
```

**状态值**: `active`（正常） | `frozen`（冻结）

**成功响应** (200):

```json
{
    "code": 0,
    "message": "用户状态已更新"
}
```

---

### 2.6 重置用户密码

**接口**: `POST /api/users/{id}/reset-password/`

**请求体**:

```json
{
    "new_password": "123456"
}
```

**成功响应** (200):

```json
{
    "code": 0,
    "message": "密码重置成功"
}
```

---

## 3. 商品管理模块

### 3.1 获取商品列表

**接口**: `GET /api/`

**请求头**:

```http
Authorization: Bearer <access_token>
```

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| search | string | 否 | 搜索标题关键字 |
| min_price | decimal | 否 | 最低价格 |
| max_price | decimal | 否 | 最高价格 |
| shop | string | 否 | 店铺名称筛选 |
| brand | string | 否 | 品牌筛选 |
| ordering | string | 否 | 排序: price, -price, sales, -sales, -crawl_time |

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "高达模型 RX-78-2 1/60",
            "price": "299.00",
            "sales": 5000,
            "shop": "万代官方旗舰店",
            "image_url": "https://example.com/image.jpg",
            "brand": "万代",
            "crawl_time": "2026-02-07T10:00:00Z"
        }
    ],
    "total": 10000
}
```

---

### 3.2 获取商品详情

**接口**: `GET /api/{id}/`

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | uuid | 商品ID |

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "高达模型 RX-78-2 1/60",
        "price": "299.00",
        "sales": 5000,
        "shop": "万代官方旗舰店",
        "image_url": "https://example.com/image.jpg",
        "detail_url": "https://detail.tmall.com/item.htm?id=xxx",
        "brand": "万代",
        "category": "模型手办",
        "batch_no": "20260207-001",
        "crawl_time": "2026-02-07T10:00:00Z",
        "created_at": "2026-02-07T10:00:00Z",
        "updated_at": "2026-02-07T10:00:00Z"
    }
}
```

---

### 3.3 创建商品（管理员）

**接口**: `POST /api/`

**请求体**:

```json
{
    "title": "高达模型 RX-78-2 1/60",
    "price": 299.00,
    "sales": 5000,
    "shop": "万代官方旗舰店",
    "image_url": "https://example.com/image.jpg",
    "detail_url": "https://detail.tmall.com/item.htm?id=xxx",
    "brand": "万代",
    "category": "模型手办",
    "batch_no": "20260207-001",
    "crawl_time": "2026-02-07T10:00:00Z"
}
```

**成功响应** (201):

```json
{
    "code": 0,
    "message": "商品创建成功",
    "data": { ... }
}
```

---

### 3.4 更新商品（管理员）

**接口**: `PUT /api/{id}/`

**请求体**: 同创建商品

**成功响应** (200):

```json
{
    "code": 0,
    "message": "商品更新成功",
    "data": { ... }
}
```

---

### 3.5 删除商品（管理员）

**接口**: `DELETE /api/{id}/`

**成功响应** (200):

```json
{
    "code": 0,
    "message": "商品删除成功"
}
```

---

### 3.6 获取商品历史价格

**接口**: `GET /api/{id}/price-history/`

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days | int | 否 | 天数，默认30天 |
| start_date | date | 否 | 开始日期 |
| end_date | date | 否 | 结束日期 |

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "id": "750e8400-e29b-41d4-a716-446655440000",
            "price": "299.00",
            "sales": 5000,
            "record_date": "2026-02-01",
            "created_at": "2026-02-01T10:00:00Z"
        },
        {
            "id": "750e8400-e29b-41d4-a716-446655440001",
            "price": "289.00",
            "sales": 5200,
            "record_date": "2026-02-05",
            "created_at": "2026-02-05T10:00:00Z"
        }
    ]
}
```

---

### 3.7 导出商品数据

**接口**: `GET /api/export/`

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| format | string | 否 | 导出格式，默认csv |
| search | string | 否 | 搜索条件（同列表接口） |

**成功响应** (200):

返回 CSV 文件流，文件名为 `products_export_YYYYMMDD.csv`

---

## 4. 采集日志模块

### 4.1 获取采集日志列表

**接口**: `GET /api/crawl-logs/`

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| status | string | 否 | 状态筛选: pending/running/success/failed/cancelled |

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "status": "success",
            "status_display": "成功",
            "mode": "demo",
            "source_type": "json",
            "source_type_display": "JSON接口",
            "start_time": "2026-02-07T10:00:00Z",
            "end_time": "2026-02-07T10:05:00Z",
            "items_collected": 40,
            "items_success": 38,
            "items_failed": 2,
            "created_at": "2026-02-07T10:00:00Z"
        }
    ],
    "total": 50
}
```

---

### 4.2 获取采集日志详情

**接口**: `GET /api/crawl-logs/{id}/`

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "status": "success",
        "status_display": "成功",
        "mode": "demo",
        "source_type": "json",
        "source_type_display": "JSON接口",
        "start_time": "2026-02-07T10:00:00Z",
        "end_time": "2026-02-07T10:05:00Z",
        "items_collected": 40,
        "items_success": 38,
        "items_failed": 2,
        "log_content": "开始采集...\n第1页采集成功...\n完成",
        "error_message": null,
        "created_at": "2026-02-07T10:00:00Z",
        "updated_at": "2026-02-07T10:05:00Z"
    }
}
```

---

## 5. 数据统计模块

### 5.1 统计概览

**接口**: `GET /api/statistics/overview/`

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "total_products": 10000,
        "total_shops": 500,
        "total_brands": 50,
        "avg_price": 199.5,
        "total_crawls": 100
    }
}
```

---

### 5.2 价格分布统计

**接口**: `GET /api/statistics/price-distribution/`

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        { "range": "0-50", "count": 3000, "percentage": 30 },
        { "range": "50-200", "count": 4000, "percentage": 40 },
        { "range": "200-500", "count": 2000, "percentage": 20 },
        { "range": "500+", "count": 1000, "percentage": 10 }
    ]
}
```

---

### 5.3 销量 Top 10

**接口**: `GET /api/statistics/top-sales/`

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "高达模型 RX-78-2 1/60",
            "price": "299.00",
            "sales": 50000,
            "shop": "万代官方旗舰店",
            "image_url": "https://example.com/image.jpg"
        }
    ]
}
```

---

### 5.4 店铺排行

**接口**: `GET /api/statistics/shop-ranking/`

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 返回数量，默认10 |

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "shop": "万代官方旗舰店",
            "count": 200,
            "avg_price": 299.5
        },
        {
            "shop": "泡泡玛特官方店",
            "count": 150,
            "avg_price": 59.0
        }
    ]
}
```

---

## 6. 爬虫控制模块（管理员）

### 6.1 启动爬虫任务

**接口**: `POST /api/crawler/start/`

**请求体**:

```json
{
    "mode": "demo",
    "keywords": ["高达", "手办"]
}
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mode | string | 否 | 采集模式: demo（演示，2页）/ batch（分批，每天1000页），默认demo |
| keywords | array | 否 | 搜索关键词列表 |

**成功响应** (202):

```json
{
    "code": 0,
    "message": "任务已启动",
    "data": {
        "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "mode": "demo",
        "status": "pending"
    }
}
```

**错误响应** (409):

```json
{
    "code": -1,
    "message": "已有 1 个任务正在运行，请等待完成后再启动新任务"
}
```

---

### 6.2 查询任务状态

**接口**: `GET /api/crawler/status/{task_id}/`

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| task_id | string | Celery任务ID |

**成功响应** (200) - 运行中:

```json
{
    "code": 0,
    "data": {
        "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "status": "PROGRESS",
        "progress": "50%",
        "current_stage": "正在采集第2页",
        "items_collected": 40,
        "logs": [
            "开始采集任务",
            "第1页采集成功，获取20条数据",
            "正在采集第2页..."
        ],
        "database_status": "running",
        "items_success": 38,
        "items_failed": 2
    }
}
```

**成功响应** (200) - 完成:

```json
{
    "code": 0,
    "data": {
        "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "status": "SUCCESS",
        "progress": "100%",
        "current_stage": "完成",
        "items_collected": 40,
        "items_failed": 0,
        "source_type": "json",
        "logs": [
            "采集完成",
            "成功入库40条数据"
        ]
    }
}
```

---

### 6.3 停止爬虫任务

**接口**: `POST /api/crawler/stop/{task_id}/`

**成功响应** (200):

```json
{
    "code": 0,
    "message": "任务已停止"
}
```

---

### 6.4 获取爬虫日志列表

**接口**: `GET /api/crawler/logs/`

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| status | string | 否 | 状态筛选 |
| mode | string | 否 | 模式筛选 |

**成功响应** (200):

```json
{
    "code": 0,
    "data": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "status": "success",
            "mode": "demo",
            "source_type": "json",
            "start_time": "2026-02-07T10:00:00Z",
            "items_collected": 40,
            "created_at": "2026-02-07T10:00:00Z"
        }
    ],
    "total": 50
}
```

---

### 6.5 获取爬虫日志详情

**接口**: `GET /api/crawler/logs/{id}/`

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "status": "success",
        "status_display": "成功",
        "mode": "demo",
        "source_type": "json",
        "source_type_display": "JSON接口",
        "start_time": "2026-02-07T10:00:00Z",
        "end_time": "2026-02-07T10:05:00Z",
        "items_collected": 40,
        "items_success": 38,
        "items_failed": 2,
        "log_content": "开始采集...\n第1页采集成功...\n完成",
        "error_message": null,
        "created_at": "2026-02-07T10:00:00Z",
        "updated_at": "2026-02-07T10:05:00Z"
    }
}
```

---

### 6.6 获取爬虫统计信息

**接口**: `GET /api/crawler/stats/`

**成功响应** (200):

```json
{
    "code": 0,
    "data": {
        "total_tasks": 100,
        "running_tasks": 1,
        "success_tasks": 90,
        "failed_tasks": 8,
        "total_items_collected": 15000,
        "average_duration": 125.5,
        "recent_logs": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "status": "success",
                "mode": "demo",
                "items_collected": 40,
                "created_at": "2026-02-07T10:00:00Z"
            }
        ]
    }
}
```

---

## 附录：数据模型说明

### User 模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| username | string | 用户名（唯一） |
| password | string | 加密密码 |
| email | string | 邮箱 |
| role | string | admin/user |
| status | string | active/frozen |
| avatar | string | 头像URL |
| phone | string | 手机号 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### Product 模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| title | string | 商品标题 |
| price | Decimal(10,2) | 价格 |
| sales | int | 销量 |
| shop | string | 店铺名称 |
| image_url | string | 图片URL |
| detail_url | string | 详情页URL |
| brand | string | 品牌 |
| category | string | 类目 |
| batch_no | string | 采集批次号 |
| crawl_time | datetime | 采集时间 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### CrawlLog 模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| task_id | string | Celery任务ID |
| status | string | pending/running/success/failed/cancelled |
| mode | string | demo/batch |
| source_type | string | json/playwright |
| start_time | datetime | 开始时间 |
| end_time | datetime | 结束时间 |
| items_collected | int | 采集总数 |
| items_success | int | 成功数量 |
| items_failed | int | 失败数量 |
| log_content | text | 日志内容 |
| error_message | text | 错误信息 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### PriceHistory 模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| product | UUID | 外键 → Product |
| price | Decimal(10,2) | 历史价格 |
| sales | int | 历史销量 |
| record_date | date | 记录日期 |
| created_at | datetime | 创建时间 |

---

## 联调测试建议

### 1. 用户认证流程测试

```bash
# 1. 注册新用户
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456","email":"test@example.com"}'

# 2. 登录获取Token
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'

# 3. 使用Token访问受保护接口
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <access_token>"
```

### 2. 商品列表测试

```bash
# 获取第一页商品
curl -X GET "http://localhost:8000/api/?page=1&page_size=20"

# 搜索"高达"并按价格排序
curl -X GET "http://localhost:8000/api/?search=高达&ordering=-price"

# 筛选50-200元价格区间
curl -X GET "http://localhost:8000/api/?min_price=50&max_price=200"
```

### 3. 爬虫任务测试

```bash
# 启动演示模式采集（需要管理员Token）
curl -X POST http://localhost:8000/api/crawler/start/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"mode":"demo","keywords":["高达"]}'

# 查询任务状态
curl -X GET http://localhost:8000/api/crawler/status/<task_id>/ \
  -H "Authorization: Bearer <token>"
```

---

文档版本: v1.0
更新日期: 2026-02-07
