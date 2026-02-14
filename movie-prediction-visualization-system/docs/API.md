# 票房预测与可视化系统 - API 接口文档

## 目录

- [概述](#概述)
- [通用说明](#通用说明)
- [认证接口](#认证接口)
- [用户管理接口](#用户管理接口)
- [影片管理接口](#影片管理接口)
- [影片类型接口](#影片类型接口)
- [影院管理接口](#影院管理接口)
- [地域管理接口](#地域管理接口)
- [票房数据接口](#票房数据接口)
- [预测分析接口](#预测分析接口)
- [数据可视化接口](#数据可视化接口)

---

## 概述

### 基本信息

- **Base URL**: `http://localhost:8000`
- **API 前缀**: `/api/`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

### 响应格式规范

```json
// 成功响应
{
    "code": 0,
    "data": {...},
    "total": 100  // 仅列表接口返回
}

// 错误响应
{
    "code": -1,
    "message": "错误描述",
    "errors": {...}  // 可选，验证错误时返回
}
```

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 通用说明

### 认证方式

所有需要认证的接口都需要在请求头中携带 JWT Token：

```
Authorization: Bearer <access_token>
```

### 分页参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| page_size | integer | 否 | 10 | 每页数量 |

### 权限说明

- **无需认证**: 所有用户（包括未登录）可访问
- **需要认证**: 登录用户可访问
- **管理员**: 仅管理员角色可访问

---

## 认证接口

### 1. 用户注册

创建新用户账号。

**接口地址**: `POST /api/auth/register/`

**权限**: 无需认证

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（唯一） |
| password | string | 是 | 密码（最少6位） |
| password_confirm | string | 是 | 确认密码 |
| email | string | 否 | 邮箱地址 |
| real_name | string | 否 | 真实姓名 |
| phone | string | 否 | 手机号码 |

**请求示例**:
```json
{
    "username": "testuser",
    "password": "password123",
    "password_confirm": "password123",
    "email": "test@example.com",
    "real_name": "测试用户",
    "phone": "13800138000"
}
```

**响应示例**:
```json
{
    "code": 0,
    "message": "注册成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "real_name": "测试用户",
        "email": "test@example.com",
        "phone": "13800138000",
        "role": "USER",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

---

### 2. 用户登录

验证用户凭据并返回 JWT Token。

**接口地址**: `POST /api/auth/login/`

**权限**: 无需认证

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**请求示例**:
```json
{
    "username": "admin",
    "password": "admin123"
}
```

**响应示例**:
```json
{
    "code": 0,
    "message": "登录成功",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
        "user": {
            "id": 1,
            "username": "admin",
            "real_name": "管理员",
            "role": "ADMIN"
        }
    }
}
```

**Token 说明**:
- `access_token`: 访问令牌，有效期 2 小时
- `refresh_token`: 刷新令牌，有效期 7 天

---

### 3. 刷新 Token

使用刷新令牌获取新的访问令牌。

**接口地址**: `POST /api/auth/token/refresh/`

**权限**: 无需认证

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| refresh | string | 是 | 刷新令牌 |

**请求示例**:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

### 4. 用户登出

执行登出操作（客户端需删除本地 Token）。

**接口地址**: `POST /api/auth/logout/`

**权限**: 无需认证

**响应示例**:
```json
{
    "code": 0,
    "message": "登出成功"
}
```

---

### 5. 获取当前用户信息

获取当前登录用户的个人信息。

**接口地址**: `GET /api/auth/profile/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "id": 1,
        "username": "admin",
        "real_name": "管理员",
        "email": "admin@example.com",
        "phone": "13800138000",
        "role": "ADMIN",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

---

### 6. 更新当前用户信息

更新当前登录用户的个人信息。

**接口地址**: `PUT /api/auth/profile/`

**权限**: 需要认证

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| real_name | string | 否 | 真实姓名 |
| email | string | 否 | 邮箱地址 |
| phone | string | 否 | 手机号码 |

**响应示例**:
```json
{
    "code": 0,
    "message": "信息更新成功",
    "data": {
        "id": 1,
        "username": "admin",
        "real_name": "管理员",
        "email": "admin@example.com",
        "phone": "13900139000"
    }
}
```

---

### 7. 修改密码

修改当前用户的密码。

**接口地址**: `POST /api/auth/change-password/`

**权限**: 需要认证

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| old_password | string | 是 | 原密码 |
| new_password | string | 是 | 新密码（最少6位） |

**请求示例**:
```json
{
    "old_password": "oldpassword123",
    "new_password": "newpassword456"
}
```

**响应示例**:
```json
{
    "code": 0,
    "message": "密码修改成功"
}
```

---

## 用户管理接口

> 以下接口仅管理员可访问

### 1. 获取用户列表

获取系统中所有用户列表，支持筛选和搜索。

**接口地址**: `GET /api/auth/users/`

**权限**: 管理员

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 否 | 按用户名模糊搜索 |
| role | string | 否 | 按角色筛选（ADMIN/USER） |
| is_active | boolean | 否 | 按状态筛选（true/false） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "username": "admin",
            "real_name": "管理员",
            "email": "admin@example.com",
            "phone": "13800138000",
            "role": "ADMIN",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": 10
}
```

---

### 2. 获取用户详情

获取指定用户的详细信息。

**接口地址**: `GET /api/auth/users/{id}/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

---

### 3. 创建用户

管理员创建新用户。

**接口地址**: `POST /api/auth/users/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（唯一） |
| password | string | 是 | 密码（最少6位） |
| email | string | 否 | 邮箱地址 |
| real_name | string | 否 | 真实姓名 |
| phone | string | 否 | 手机号码 |
| role | string | 否 | 角色（ADMIN/USER） |

---

### 4. 更新用户

更新指定用户的信息。

**接口地址**: `PUT /api/auth/users/{id}/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

---

### 5. 禁用用户

禁用指定的用户账号。

**接口地址**: `POST /api/auth/users/{id}/disable/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

**响应示例**:
```json
{
    "code": 0,
    "message": "用户 testuser 已禁用"
}
```

---

### 6. 启用用户

启用已被禁用的用户账号。

**接口地址**: `POST /api/auth/users/{id}/enable/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

---

### 7. 重置用户密码

重置指定用户的密码。

**接口地址**: `POST /api/auth/users/{id}/reset_password/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| new_password | string | 否 | 新密码（默认123456） |

---

### 8. 更新用户角色

更新指定用户的角色。

**接口地址**: `PUT /api/auth/users/{id}/role/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| role | string | 是 | 角色（ADMIN/USER） |

---

### 9. 删除用户

删除指定的用户账号。

**接口地址**: `DELETE /api/auth/users/{id}/delete/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |

**限制**: 不能删除当前登录的管理员账号

---

## 影片类型接口

### 1. 获取影片类型列表

获取所有影片类型的列表。

**接口地址**: `GET /api/movies/types/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| search | string | 否 | 按类型名称模糊搜索 |
| ordering | string | 否 | 排序字段（name, -name, created_at, -created_at） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "name": "动作",
            "movie_count": 15,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "name": "喜剧",
            "movie_count": 8,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": 2
}
```

---

### 2. 获取类型详情

获取指定影片类型的详细信息。

**接口地址**: `GET /api/movies/types/{id}/`

**权限**: 需要认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 类型ID |

---

### 3. 创建影片类型

创建新的影片类型。

**接口地址**: `POST /api/movies/types/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 类型名称 |

**请求示例**:
```json
{
    "name": "科幻"
}
```

**响应示例**:
```json
{
    "code": 0,
    "message": "影片类型创建成功",
    "data": {
        "id": 3,
        "name": "科幻",
        "movie_count": 0,
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

---

### 4. 更新影片类型

更新指定影片类型的信息。

**接口地址**: `PUT /api/movies/types/{id}/`

**权限**: 管理员

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 类型ID |

---

### 5. 部分更新影片类型

部分更新指定影片类型的信息。

**接口地址**: `PATCH /api/movies/types/{id}/`

**权限**: 管理员

---

### 6. 删除影片类型

删除指定的影片类型。

**接口地址**: `DELETE /api/movies/types/{id}/`

**权限**: 管理员

**限制**: 如果该类型下存在关联的影片，则无法删除

---

## 影片管理接口

### 1. 获取影片列表

获取影片列表，支持多条件筛选和排序。

**接口地址**: `GET /api/movies/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| search | string | 否 | 按标题、导演、演员模糊搜索 |
| type | integer | 否 | 按类型ID筛选 |
| status | string | 否 | 按状态筛选（RELEASED-已上映, COMING-即将上映） |
| release_date_after | date | 否 | 上映日期（之后） |
| release_date_before | date | 否 | 上映日期（之前） |
| ordering | string | 否 | 排序字段（release_date, box_office_total, created_at） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "title": "流浪地球2",
            "director": "郭帆",
            "type_name": "科幻",
            "release_date": "2023-01-22",
            "status": "RELEASED",
            "box_office_total": 402900.00
        }
    ],
    "total": 50
}
```

---

### 2. 获取影片详情

获取指定影片的完整详细信息。

**接口地址**: `GET /api/movies/{id}/`

**权限**: 需要认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 影片ID |

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "id": 1,
        "title": "流浪地球2",
        "director": "郭帆",
        "actors": "刘德华, 吴京, 李雪健",
        "release_date": "2023-01-22",
        "duration": 173,
        "type": 1,
        "type_name": "科幻",
        "poster_url": "https://example.com/poster.jpg",
        "description": "太阳即将毁灭，人类在地球表面建造出巨大的推进器...",
        "box_office_total": 402900.00,
        "status": "RELEASED",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-25T00:00:00Z"
    }
}
```

---

### 3. 创建影片

创建新的影片记录。

**接口地址**: `POST /api/movies/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 影片标题 |
| director | string | 否 | 导演 |
| actors | string | 否 | 演员 |
| release_date | date | 否 | 上映日期 |
| duration | integer | 否 | 片长（分钟） |
| type | integer | 是 | 类型ID |
| poster_url | string | 否 | 海报URL |
| description | string | 否 | 剧情简介 |
| status | string | 否 | 状态（RELEASED/COMING） |

---

### 4. 更新影片

更新指定影片的信息。

**接口地址**: `PUT /api/movies/{id}/`

**权限**: 管理员

---

### 5. 部分更新影片

部分更新指定影片的信息。

**接口地址**: `PATCH /api/movies/{id}/`

**权限**: 管理员

---

### 6. 删除影片

删除指定的影片记录。

**接口地址**: `DELETE /api/movies/{id}/`

**权限**: 管理员

---

### 7. 获取已上映影片

获取所有已上映状态的影片列表。

**接口地址**: `GET /api/movies/released/`

**权限**: 需要认证

---

### 8. 获取即将上映影片

获取所有即将上映状态的影片列表。

**接口地址**: `GET /api/movies/coming/`

**权限**: 需要认证

---

## 地域管理接口

### 1. 获取地域列表

获取地域列表，支持按层级、父级筛选。

**接口地址**: `GET /api/cinemas/regions/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| level | string | 否 | 地域层级（PROVINCE-省份/CITY-城市） |
| parent_id | integer | 否 | 父级地域ID |
| tree | boolean | 否 | 是否返回树形结构（true/false） |
| order_by | string | 否 | 排序字段 |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "name": "北京市",
            "level": "PROVINCE",
            "parent": null,
            "parent_name": null,
            "children_count": 1,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": 1
}
```

---

### 2. 获取所有省份

获取系统中所有的省份列表。

**接口地址**: `GET /api/cinemas/regions/provinces/`

**权限**: 需要认证

---

### 3. 获取省份下的城市

获取指定省份下的所有城市列表。

**接口地址**: `GET /api/cinemas/regions/{id}/cities/`

**权限**: 需要认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 省份地域ID |

---

### 4. 创建地域

创建新的地域记录（省份或城市）。

**接口地址**: `POST /api/cinemas/regions/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 地域名称 |
| parent | integer | 否 | 父级地域ID（省份为null，城市必填） |
| level | string | 是 | 地域层级（PROVINCE/CITY） |

**验证规则**:
- 省份（level=PROVINCE）不能有父级
- 城市（level=CITY）必须指定父级省份
- 父级地域必须是省份级别

---

### 5. 更新地域

更新指定地域的信息。

**接口地址**: `PUT /api/cinemas/regions/{id}/`

**权限**: 管理员

---

### 6. 删除地域

删除指定的地域记录。

**接口地址**: `DELETE /api/cinemas/regions/{id}/`

**权限**: 管理员

**删除限制**:
- 如果该地域下存在子地域，无法删除
- 如果该地域下存在关联的影院，无法删除

---

## 影院管理接口

### 1. 获取影院列表

获取影院列表，支持多种筛选和排序方式。

**接口地址**: `GET /api/cinemas/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region_id | integer | 否 | 地域ID |
| province_id | integer | 否 | 省份ID |
| city_id | integer | 否 | 城市ID |
| search | string | 否 | 影院名称模糊搜索 |
| is_active | boolean | 否 | 营业状态（true/false） |
| order_by | string | 否 | 排序字段（支持 - 前缀降序） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "name": "万达影城（CBD店）",
            "address": "北京市朝阳区建国路93号",
            "phone": "010-12345678",
            "region": 3,
            "region_name": "朝阳区",
            "parent_region_name": "北京市",
            "screen_count": 10,
            "seats_count": 1500,
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "box_office_total": 5000.00
        }
    ],
    "total": 50
}
```

---

### 2. 获取影院详情

获取指定影院的详细信息。

**接口地址**: `GET /api/cinemas/{id}/`

**权限**: 需要认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 影院ID |

---

### 3. 创建影院

创建新的影院记录。

**接口地址**: `POST /api/cinemas/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 影院名称 |
| address | string | 是 | 影院地址 |
| phone | string | 否 | 联系电话 |
| region | integer | 是 | 所属地域ID（必须是城市级别） |
| screen_count | integer | 是 | 屏幕数量（必须大于0） |
| seats_count | integer | 是 | 座位总数（必须大于0） |
| is_active | boolean | 否 | 是否营业中（默认true） |

---

### 4. 更新影院

更新指定影院的信息。

**接口地址**: `PUT /api/cinemas/{id}/`

**权限**: 管理员

---

### 5. 删除影院

删除指定的影院记录。

**接口地址**: `DELETE /api/cinemas/{id}/`

**权限**: 管理员

**删除限制**: 如果该影院存在关联的票房记录，无法删除

---

### 6. 获取营业中的影院

获取所有营业中的影院列表。

**接口地址**: `GET /api/cinemas/active/`

**权限**: 需要认证

---

### 7. 按地域统计影院数量

按地域统计影院数量，包括总数和营业中的数量。

**接口地址**: `GET /api/cinemas/by_region/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region_id | integer | 否 | 地域ID（不指定则统计全部） |

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "total": 100,
        "active": 85
    }
}
```

---

## 票房数据接口

### 1. 获取票房记录列表

获取票房记录列表，支持多维度筛选和排序。

**接口地址**: `GET /api/boxoffice/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| movie | integer | 否 | 影片ID |
| cinema | integer | 否 | 影院ID |
| cinema__region | integer | 否 | 地域ID |
| record_date_start | date | 否 | 记录日期开始（YYYY-MM-DD） |
| record_date_end | date | 否 | 记录日期结束（YYYY-MM-DD） |
| min_daily_box_office | number | 否 | 最低日票房（元） |
| max_daily_box_office | number | 否 | 最高日票房（元） |
| ordering | string | 否 | 排序字段（如：-record_date） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "movie": 1,
            "movie_title": "流浪地球2",
            "cinema": 1,
            "cinema_name": "万达影城（CBD店）",
            "region_name": "朝阳区",
            "record_date": "2023-01-22",
            "daily_box_office": 500000.00,
            "screening_count": 10,
            "audience_count": 500,
            "created_at": "2023-01-23T00:00:00Z"
        }
    ],
    "total": 100
}
```

---

### 2. 获取票房记录详情

获取单条票房记录的详细信息。

**接口地址**: `GET /api/boxoffice/{id}/`

**权限**: 需要认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| id | integer | 票房记录ID |

---

### 3. 创建票房记录

创建新的票房记录。

**接口地址**: `POST /api/boxoffice/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| movie | integer | 是 | 关联影片ID |
| cinema | integer | 是 | 关联影院ID |
| record_date | date | 是 | 记录日期 |
| daily_box_office | number | 是 | 日票房（元） |
| screening_count | integer | 否 | 场次 |
| audience_count | integer | 否 | 人次 |

**验证规则**:
- 记录日期不能早于影片上映日期
- 票房金额必须大于等于0

---

### 4. 更新票房记录

更新指定票房记录的信息。

**接口地址**: `PUT /api/boxoffice/{id}/`

**权限**: 管理员

**注意**: 不支持修改关联的影片、影院和记录日期

---

### 5. 删除票房记录

删除指定的票房记录。

**接口地址**: `DELETE /api/boxoffice/{id}/`

**权限**: 管理员

---

### 6. 批量删除票房记录

根据ID列表批量删除多条票房记录。

**接口地址**: `POST /api/boxoffice/batch_delete/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | array | 是 | 要删除的票房记录ID列表 |

**请求示例**:
```json
{
    "ids": [1, 2, 3, 4, 5]
}
```

---

### 7. 批量录入票房记录

批量创建多条票房记录，每次最多支持100条。

**接口地址**: `POST /api/boxoffice/batch_input/`

**权限**: 管理员

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| records | array | 是 | 票房记录列表，每次最多100条 |

**请求示例**:
```json
{
    "records": [
        {
            "movie": 1,
            "cinema": 1,
            "record_date": "2024-01-01",
            "daily_box_office": 500000,
            "screening_count": 10,
            "audience_count": 500
        },
        {
            "movie": 2,
            "cinema": 1,
            "record_date": "2024-01-01",
            "daily_box_office": 300000
        }
    ]
}
```

**响应示例**:
```json
{
    "code": 0,
    "message": "成功录入 2 条票房记录",
    "data": {
        "created_count": 2,
        "error_count": 0,
        "created_records": [...]
    }
}
```

---

### 8. 获取票房统计数据

获取票房数据的统计汇总信息。

**接口地址**: `GET /api/boxoffice/stats/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_date | date | 否 | 开始日期（YYYY-MM-DD） |
| end_date | date | 否 | 结束日期（YYYY-MM-DD） |
| movie_id | integer | 否 | 影片ID |

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "total_box_office": 15000000.00,
        "total_screening_count": 300,
        "total_audience_count": 15000,
        "record_count": 50
    }
}
```

---

## 预测分析接口

### 1. 影片票房预测

根据影片历史票房数据，使用指定算法预测未来票房。

**接口地址**: `GET /api/prediction/movie/{movie_id}/`

**权限**: 无需认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| movie_id | integer | 影片ID |

**查询参数**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| predict_days | integer | 否 | 7 | 预测天数（1-30） |
| algorithm | string | 否 | combined | 预测算法（linear_regression, moving_average, combined） |

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "success": true,
        "movie_id": 1,
        "linear_regression": {
            "success": true,
            "movie_id": 1,
            "predictions": [
                {
                    "day": 1,
                    "predicted_box_office": 4500.5
                },
                {
                    "day": 2,
                    "predicted_box_office": 4480.3
                }
            ],
            "history": [...],
            "algorithm": "linear_regression"
        },
        "moving_average": {
            "success": true,
            "movie_id": 1,
            "predictions": [
                {
                    "day": 1,
                    "predicted_box_office": 4520.1
                }
            ],
            "history": [...],
            "algorithm": "moving_average"
        },
        "history": [...]
    },
    "message": "success"
}
```

**支持的算法**:
- `linear_regression`: 线性回归算法，使用最小二乘法拟合趋势
- `moving_average`: 移动平均算法，基于历史数据的加权平均值
- `combined`: 综合预测，同时返回两种算法结果供对比

---

### 2. 获取影片历史票房数据

获取指定影片的历史票房数据，用于趋势分析。

**接口地址**: `GET /api/prediction/movie/{movie_id}/history/`

**权限**: 无需认证

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| movie_id | integer | 影片ID |

**查询参数**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| days | integer | 否 | 30 | 获取天数（1-365） |

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "movie_id": 1,
        "history": [
            {
                "date": "2023-01-22",
                "box_office": 5000.0,
                "screening_count": 10,
                "audience_count": 500
            }
        ],
        "total_days": 30
    },
    "total": 30
}
```

---

### 3. 获取支持的预测算法列表

获取系统支持的所有预测算法信息。

**接口地址**: `GET /api/prediction/algorithms/`

**权限**: 无需认证

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": "linear_regression",
            "name": "线性回归",
            "description": "使用最小二乘法拟合历史数据趋势，预测未来票房",
            "params": {
                "predict_days": "预测天数 (1-30)"
            }
        },
        {
            "id": "moving_average",
            "name": "移动平均",
            "description": "基于历史数据的加权移动平均值进行预测",
            "params": {
                "predict_days": "预测天数 (1-30)",
                "window": "平均窗口大小 (默认3)"
            }
        },
        {
            "id": "combined",
            "name": "综合预测",
            "description": "同时返回线性回归和移动平均两种预测结果，方便对比",
            "params": {
                "predict_days": "预测天数 (1-30)"
            }
        }
    ],
    "total": 3
}
```

---

## 数据可视化接口

### 1. 获取票房总榜 Top 10

获取历史累计票房最高的10部电影数据。

**接口地址**: `GET /api/visualization/stats/top10/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "id": 1,
            "title": "流浪地球2",
            "box_office_total": 402900.00,
            "release_date": "2023-01-22"
        }
    ]
}
```

---

### 2. 获取今日大盘票房统计

获取当日全国票房统计数据。

**接口地址**: `GET /api/visualization/stats/today/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "date": "2024-01-01",
        "total_box_office": 15000000.00,
        "total_screening_count": 300,
        "total_audience_count": 15000
    }
}
```

---

### 3. 获取本周票房冠军

获取本周（周一至当前日期）票房最高的影片信息。

**接口地址**: `GET /api/visualization/stats/champion/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "movie_id": 1,
        "movie_title": "流浪地球2",
        "weekly_box_office": 50000000.00
    }
}
```

---

### 4. 获取各类型票房占比

获取各影片类型的票房分布数据和占比信息。

**接口地址**: `GET /api/visualization/stats/type/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "type_id": 1,
            "type_name": "科幻",
            "box_office": 50000000.00,
            "percentage": 35.5
        },
        {
            "type_id": 2,
            "type_name": "动作",
            "box_office": 40000000.00,
            "percentage": 28.4
        }
    ]
}
```

---

### 5. 获取各省份票房分布

获取各省份的票房分布数据和影院数量统计。

**接口地址**: `GET /api/visualization/stats/region/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "region_id": 1,
            "region_name": "北京市",
            "box_office": 50000000.00,
            "cinema_count": 50
        }
    ]
}
```

---

### 6. 获取票房时间走势

获取指定时间范围内的票房走势数据，支持按日/周/月聚合。

**接口地址**: `GET /api/visualization/stats/timeseries/`

**权限**: 需要认证

**查询参数**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| period | string | 否 | day | 聚合周期（day/week/month） |
| days | integer | 否 | 30 | 统计天数（最近N天） |

**响应示例**:
```json
{
    "code": 0,
    "data": [
        {
            "date": "2024-01-01",
            "total_box_office": 15000000.00,
            "total_screening_count": 300,
            "total_audience_count": 15000
        },
        {
            "date": "2024-01-02",
            "total_box_office": 16000000.00,
            "total_screening_count": 320,
            "total_audience_count": 16000
        }
    ]
}
```

---

### 7. 获取仪表盘概览数据

获取仪表盘所需的综合统计数据。

**接口地址**: `GET /api/visualization/stats/dashboard/`

**权限**: 需要认证

**响应示例**:
```json
{
    "code": 0,
    "data": {
        "today_box_office": 15000000.00,
        "week_champion": {
            "movie_id": 1,
            "movie_title": "流浪地球2",
            "weekly_box_office": 50000000.00
        },
        "total_movies": 100,
        "total_cinemas": 50
    }
}
```

---

## API 文档（Swagger）

系统内置了 Swagger API 文档，启动后端服务后可访问：

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

---

## 数据模型说明

### 用户角色（User.role）

| 值 | 说明 |
|-----|------|
| ADMIN | 管理员 |
| USER | 普通用户 |

### 影片状态（Movie.status）

| 值 | 说明 |
|-----|------|
| RELEASED | 已上映 |
| COMING | 即将上映 |

### 地域层级（Region.level）

| 值 | 说明 |
|-----|------|
| PROVINCE | 省份 |
| CITY | 城市 |

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| -1 | 通用错误 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
