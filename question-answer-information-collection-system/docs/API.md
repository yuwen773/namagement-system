# 问答信息采集系统 API 接口文档

## 目录

- [基本信息](#基本信息)
- [认证方式](#认证方式)
- [响应格式](#响应格式)
- [错误码说明](#错误码说明)
- [认证接口](#认证接口)
- [爬虫控制接口](#爬虫控制接口)
- [问答数据接口](#问答数据接口)
- [统计分析接口](#统计分析接口)

---

## 基本信息

| 项目 | 说明 |
|------|------|
| 基础 URL | `http://localhost:8000` |
| API 前缀 | `/api` |
| 认证方式 | JWT Token (Bearer) |
| 数据格式 | JSON |

---

## 认证方式

### 获取 Token

登录获取 Access Token 和 Refresh Token：

```
POST /api/auth/login/
Content-Type: application/json
```

**请求体：**

```json
{
    "username": "用户名",
    "password": "密码"
}
```

**响应示例：**

```json
{
    "code": 0,
    "message": "登录成功",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "role": "admin"
        }
    }
}
```

### 刷新 Token

当 Access Token 过期时，使用 Refresh Token 获取新的 Token：

```
POST /api/auth/token/refresh/
Content-Type: application/json
```

**请求体：**

```json
{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 使用 Token

在请求头中携带 Token：

```
Authorization: Bearer <access_token>
```

---

## 响应格式

### 成功响应

```json
{
    "code": 0,
    "message": "success",
    "data": { ... },
    "total": 100
}
```

### 错误响应

```json
{
    "code": -1,
    "message": "错误信息",
    "data": null
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码，0=成功，-1=失败 |
| message | string | 提示信息 |
| data | object/null | 响应数据 |
| total | int | 数据总数（列表时返回） |

---

## 错误码说明

| code | 说明 |
|------|------|
| 0 | 成功 |
| -1 | 失败（详见 message） |

### 常见错误信息

| message | 说明 |
|---------|------|
| 请先登录后再访问 | 未提供 Token 或 Token 无效 |
| 用户名或密码错误 | 登录凭证错误 |
| 仅管理员可以启动爬虫任务 | 权限不足 |
| 您没有权限执行此操作 | 权限不足 |
| 请求的资源不存在 | 资源未找到 |
| 参数 xxx 必须是整数 | 参数类型错误 |
| 参数 xxx 超出范围 | 参数值超出允许范围 |
| 系统繁忙，请稍后重试 | 服务器内部错误 |

---

## 认证接口

### 用户注册

```
POST /api/auth/register/
Content-Type: application/json
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（至少 3 个字符） |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码（至少 6 位） |

**响应示例：**

```json
{
    "code": 0,
    "message": "注册成功",
    "data": {
        "id": 2,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "is_active": true,
        "date_joined": "2026-02-20T10:00:00Z"
    }
}
```

### 获取当前用户信息

```
GET /api/auth/me/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "is_active": true,
        "date_joined": "2026-01-01T00:00:00Z"
    }
}
```

### 更新当前用户信息

```
PUT /api/auth/me/
Authorization: Bearer <token>
Content-Type: application/json
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 否 | 用户名 |
| email | string | 否 | 邮箱地址 |

**响应示例：**

```json
{
    "code": 0,
    "message": "更新成功",
    "data": { ... }
}
```

### 获取用户列表（仅管理员）

```
GET /api/auth/users/
Authorization: Bearer <admin_token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "role": "admin",
            "is_active": true,
            "date_joined": "2026-01-01T00:00:00Z"
        }
    ],
    "total": 1
}
```

### 删除用户（仅管理员）

```
DELETE /api/auth/users/<id>/
Authorization: Bearer <admin_token>
```

**响应：**

```json
{
    "code": 0,
    "message": "删除成功"
}
```

---

## 爬虫控制接口

> 所有爬虫接口需要登录认证，部分接口仅管理员可执行

### 获取爬虫状态

```
GET /api/crawler/status/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "has_active_task": true,
        "current_task": {
            "task_id": "abc123-uuid",
            "status": "running",
            "progress": 45,
            "collected": 9000,
            "total": 10000,
            "start_time": "2026-02-07T10:30:00",
            "message": "正在采集第 90 页..."
        },
        "resume_available": true,
        "resume_info": {
            "mode": "full",
            "has_resume": true,
            "last_page": 90,
            "last_id": "abc123"
        }
    }
}
```

### 启动爬虫任务

```
POST /api/crawler/start/
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**请求参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| mode | string | 否 | demo | 采集模式：demo（演示，20条）/ full（全量） |
| limit | int | 否 | 20 | 采集数量限制（1-50000） |
| api_only | bool | 否 | false | 是否使用纯 API 模式 |
| resume | bool | 否 | false | 是否断点续传 |

**响应示例：**

```json
{
    "code": 0,
    "message": "爬虫任务已启动",
    "data": {
        "task_id": "abc123-uuid",
        "status": "pending",
        "mode": "demo",
        "limit": 20,
        "message": "任务已提交，请稍后查询状态"
    }
}
```

**错误响应：**

```json
{
    "code": -1,
    "message": "参数 mode 无效，仅支持 'demo' 或 'full'",
    "data": null
}
```

```json
{
    "code": -1,
    "message": "已有任务正在运行 (task_id: abc123)",
    "data": {
        "existing_task_id": "abc123"
    }
}
```

### 停止爬虫任务

```
POST /api/crawler/stop/
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | string | 否 | 要停止的任务ID，不提供则停止所有运行中的任务 |

**响应示例：**

```json
{
    "code": 0,
    "message": "爬虫任务已停止",
    "data": {
        "task_id": "abc123-uuid",
        "status": "stopped"
    }
}
```

### 获取任务进度

```
GET /api/crawler/progress/<task_id>/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "timestamp": "2026-02-07T10:30:00",
        "current_page": 90,
        "collected": 9000,
        "failed": 5,
        "message": "已采集 9000 条数据"
    }
}
```

### 获取任务日志

```
GET /api/crawler/logs/<task_id>/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "task_id": "abc123-uuid",
        "logs": "2026-02-07 10:30:00 - 正在采集第 1 页...\n2026-02-07 10:30:05 - 采集完成，共 10 条"
    }
}
```

### 获取断点信息

```
GET /api/crawler/resume/
Authorization: Bearer <token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| mode | string | 否 | full | 采集模式 |

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "mode": "full",
        "has_resume": true,
        "last_page": 90,
        "last_id": "abc123"
    }
}
```

### 获取操作日志

```
GET /api/crawler/operation-logs/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": [
        {
            "timestamp": "2026-02-07T10:30:00",
            "action": "start",
            "mode": "demo",
            "limit": 20,
            "user_id": 1,
            "task_id": "abc123-uuid"
        },
        {
            "timestamp": "2026-02-07T10:35:00",
            "action": "stop",
            "user_id": 1,
            "task_id": "abc123-uuid"
        }
    ],
    "total": 2
}
```

---

## 问答数据接口

### 获取问答列表

```
GET /api/questions/
Authorization: Bearer <token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 20 | 每页数量（最大100） |
| search | string | 否 | - | 搜索关键词（标题模糊搜索） |
| ordering | string | 否 | -created_at | 排序字段 |

**响应示例：**

```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "question_id": "123456",
            "title": "如何学习Python编程？",
            "category": "教育",
            "publish_time": "2026-01-15",
            "location": "北京",
            "answer_count": 5,
            "created_at": "2026-02-07T10:00:00Z"
        }
    ],
    "total": 100
}
```

### 获取问答详情

```
GET /api/questions/<id>/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "id": 1,
        "question_id": "123456",
        "title": "如何学习Python编程？",
        "description": "我想学习Python，但不知道从哪开始...",
        "category": "教育",
        "publish_time": "2026-01-15",
        "location": "北京",
        "answer_count": 5,
        "crawl_page": 1,
        "source_url": "https://wenda.so.com/q/123456",
        "answers": [
            {
                "id": 1,
                "content": "建议先学习基础语法...",
                "answerer": "python专家",
                "answer_time": "2026-01-15T12:00:00Z",
                "source_order": 1,
                "created_at": "2026-02-07T10:00:00Z"
            }
        ],
        "created_at": "2026-02-07T10:00:00Z",
        "updated_at": "2026-02-07T10:00:00Z"
    }
}
```

### 获取问答完整详情

```
GET /api/questions/<id>/detail/
Authorization: Bearer <token>
```

**响应示例：** 同上，包含所有字段

### 删除问答（仅管理员）

```
DELETE /api/questions/<id>/
Authorization: Bearer <admin_token>
```

**响应示例：**

```json
{
    "code": 0,
    "message": "删除成功"
}
```

---

## 统计分析接口

> 所有统计分析接口需要登录认证

### 数据总览

```
GET /api/statistics/overview/
Authorization: Bearer <token>
```

**响应示例：**

```json
{
    "code": 0,
    "data": {
        "total_questions": 10000,
        "total_categories": 200,
        "total_answerers": 500,
        "total_answers": 15000,
        "today_questions": 150,
        "avg_daily": 100.5
    }
}
```

### 每日问答数量趋势

```
GET /api/statistics/trend/
Authorization: Bearer <token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| days | int | 否 | 30 | 返回最近天数（最大365） |

**响应示例：**

```json
{
    "code": 0,
    "data": [
        {"date": "2026-02-01", "count": 120},
        {"date": "2026-02-02", "count": 150},
        {"date": "2026-02-03", "count": 100}
    ]
}
```

### 分类统计

```
GET /api/statistics/categories/
Authorization: Bearer <token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| limit | int | 否 | 50 | 返回数量（最大100） |

**响应示例：**

```json
{
    "code": 0,
    "data": [
        {"name": "影视", "value": 150},
        {"name": "烦恼", "value": 120},
        {"name": "教育", "value": 100}
    ]
}
```

### 高频回答者排名

```
GET /api/statistics/answerers/
Authorization: Bearer <token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| limit | int | 否 | 20 | 返回数量（最大50） |

**响应示例：**

```json
{
    "code": 0,
    "data": [
        {"name": "user123", "count": 50},
        {"name": "expert456", "count": 35},
        {"name": "helper789", "count": 20}
    ]
}
```

---

## 附录

### 用户角色

| 角色 | 说明 |
|------|------|
| admin | 管理员，可执行所有操作 |
| user | 普通用户，可查看数据、修改个人信息 |

### 权限说明

| 接口 | 管理员 | 普通用户 |
|------|--------|----------|
| 爬虫启动/停止 | ✅ | ❌ |
| 问答删除 | ✅ | ❌ |
| 用户管理 | ✅ | ❌ |
| 其他查询接口 | ✅ | ✅ |
