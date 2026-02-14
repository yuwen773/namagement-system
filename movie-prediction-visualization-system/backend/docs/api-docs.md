# 电影票房预测与可视化系统 API 文档

## 概述

本文档描述了电影票房预测与可视化系统的 RESTful API 接口。

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **认证方式**: JWT Bearer Token

## 统一响应格式

### 成功响应
```json
{
  "code": 0,
  "data": {...},
  "total": n  // 列表接口返回总数
}
```

### 错误响应
```json
{
  "code": -1,
  "message": "错误描述",
  "errors": {...}  // 可选，详细错误信息
}
```

### 认证响应
```json
{
  "code": 0,
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "user": {...}
  }
}
```

---

## 1. 认证模块 (`/api/auth/`)

### 1.1 用户注册
- **URL**: `POST /api/auth/register/`
- **权限**: 公开
- **请求体**:
```json
{
  "username": "string (required, unique)",
  "password": "string (required, min_length=6)",
  "real_name": "string (required)",
  "email": "string (optional)",
  "phone": "string (optional)"
}
```
- **响应**: 201 Created

### 1.2 用户登录
- **URL**: `POST /api/auth/login/`
- **权限**: 公开
- **请求体**:
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```
- **响应**: 200 OK (返回 access_token 和 refresh_token)

### 1.3 刷新 Token
- **URL**: `POST /api/auth/token/refresh/`
- **权限**: 需要有效的 refresh_token
- **请求体**:
```json
{
  "refresh": "string (required)"
}
```
- **响应**: 200 OK (返回新的 access_token)

### 1.4 获取当前用户信息
- **URL**: `GET /api/auth/profile/`
- **权限**: 需要登录
- **响应**: 200 OK (返回用户信息)

### 1.5 修改密码
- **URL**: `POST /api/auth/change-password/`
- **权限**: 需要登录
- **请求体**:
```json
{
  "old_password": "string (required)",
  "new_password": "string (required, min_length=6)"
}
```
- **响应**: 200 OK

### 1.6 用户列表（管理员）
- **URL**: `GET /api/auth/users/`
- **权限**: 管理员
- **查询参数**: `page`, `page_size`, `search`
- **响应**: 200 OK

### 1.7 创建用户（管理员）
- **URL**: `POST /api/auth/users/`
- **权限**: 管理员
- **请求体**: 同用户注册
- **响应**: 201 Created

### 1.8 禁用/启用用户（管理员）
- **URL**: `POST /api/auth/users/{id}/disable/`
- **URL**: `POST /api/auth/users/{id}/enable/`
- **权限**: 管理员
- **响应**: 200 OK

### 1.9 重置用户密码（管理员）
- **URL**: `POST /api/auth/users/{id}/reset_password/`
- **权限**: 管理员
- **响应**: 200 OK

---

## 2. 影片管理模块 (`/api/movies/`)

### 2.1 影片类型列表
- **URL**: `GET /api/movies/types/`
- **权限**: 需要登录
- **查询参数**: `search`, `page`, `page_size`
- **响应**: 200 OK

### 2.2 创建影片类型（管理员）
- **URL**: `POST /api/movies/types/`
- **权限**: 管理员
- **请求体**:
```json
{
  "name": "string (required, unique)"
}
```
- **响应**: 201 Created

### 2.3 更新影片类型（管理员）
- **URL**: `PUT /api/movies/types/{id}/`
- **权限**: 管理员
- **请求体**:
```json
{
  "name": "string (required)"
}
```
- **响应**: 200 OK

### 2.4 删除影片类型（管理员）
- **URL**: `DELETE /api/movies/types/{id}/`
- **权限**: 管理员
- **响应**: 204 No Content

### 2.5 影片列表
- **URL**: `GET /api/movies/`
- **权限**: 需要登录
- **查询参数**:
  - `search`: 标题、导演、演员搜索
  - `type`: 类型ID
  - `status`: 状态筛选 (RELEASED/COMING/OFF)
  - `release_date_after`: 上映日期（之后）
  - `release_date_before`: 上映日期（之前）
  - `ordering`: 排序字段 (release_date, box_office_total, created_at)
  - `page`, `page_size`
- **响应**: 200 OK

### 2.6 创建影片（管理员）
- **URL**: `POST /api/movies/`
- **权限**: 管理员
- **请求体**:
```json
{
  "title": "string (required)",
  "director": "string (required)",
  "actors": "string (required)",
  "release_date": "date (required)",
  "duration": "integer (required, 单位:分钟)",
  "type": "integer (required, 影片类型ID)",
  "poster_url": "string (optional)",
  "description": "string (optional)",
  "status": "string (optional, RELEASED/COMING/OFF)"
}
```
- **响应**: 201 Created

### 2.7 影片详情
- **URL**: `GET /api/movies/{id}/`
- **权限**: 需要登录
- **响应**: 200 OK

### 2.8 更新影片（管理员）
- **URL**: `PUT /api/movies/{id}/`
- **权限**: 管理员
- **请求体**: 同创建影片
- **响应**: 200 OK

### 2.9 删除影片（管理员）
- **URL**: `DELETE /api/movies/{id}/`
- **权限**: 管理员
- **响应**: 204 No Content

### 2.10 已上映影片列表
- **URL**: `GET /api/movies/released/`
- **权限**: 需要登录
- **响应**: 200 OK

### 2.11 即将上映影片列表
- **URL**: `GET /api/movies/coming/`
- **权限**: 需要登录
- **响应**: 200 OK

---

## 3. 影院管理模块 (`/api/cinemas/`)

### 3.1 地域列表
- **URL**: `GET /api/cinemas/regions/`
- **权限**: 需要登录
- **查询参数**: `parent`, `level`, `search`
- **响应**: 200 OK

### 3.2 创建地域（管理员）
- **URL**: `POST /api/cinemas/regions/`
- **权限**: 管理员
- **请求体**:
```json
{
  "name": "string (required)",
  "parent": "integer (optional, 父级地域ID)",
  "level": "string (required, PROVINCE/CITY)"
}
```
- **响应**: 201 Created

### 3.3 省份列表
- **URL**: `GET /api/cinemas/regions/provinces/`
- **权限**: 需要登录
- **响应**: 200 OK

### 3.4 城市列表
- **URL**: `GET /api/cinemas/regions/{id}/cities/`
- **权限**: 需要登录
- **响应**: 200 OK

### 3.5 影院列表
- **URL**: `GET /api/cinemas/cinemas/`
- **权限**: 需要登录
- **查询参数**: `region`, `province`, `city`, `search`, `is_active`, `ordering`
- **响应**: 200 OK

### 3.6 创建影院（管理员）
- **URL**: `POST /api/cinemas/cinemas/`
- **权限**: 管理员
- **请求体**:
```json
{
  "name": "string (required)",
  "address": "string (required)",
  "phone": "string (required)",
  "region": "integer (required, 地域ID)",
  "screen_count": "integer (optional)",
  "seats_count": "integer (optional)",
  "is_active": "boolean (optional)"
}
```
- **响应**: 201 Created

### 3.7 营业中影院列表
- **URL**: `GET /api/cinemas/cinemas/active/`
- **权限**: 需要登录
- **响应**: 200 OK

---

## 4. 票房数据模块 (`/api/boxoffice/`)

### 4.1 票房记录列表
- **URL**: `GET /api/boxoffice/boxoffice/`
- **权限**: 需要登录
- **查询参数**:
  - `movie`: 影片ID
  - `cinema`: 影院ID
  - `cinema__region`: 地域ID
  - `record_date_start`: 记录日期开始 (YYYY-MM-DD)
  - `record_date_end`: 记录日期结束 (YYYY-MM-DD)
  - `min_daily_box_office`: 最低日票房
  - `max_daily_box_office`: 最高日票房
  - `ordering`: 排序字段
  - `page`, `page_size`
- **响应**: 200 OK

### 4.2 录入票房记录（管理员）
- **URL**: `POST /api/boxoffice/boxoffice/`
- **权限**: 管理员
- **请求体**:
```json
{
  "movie": "integer (required, 影片ID)",
  "cinema": "integer (required, 影院ID)",
  "record_date": "date (required, YYYY-MM-DD)",
  "daily_box_office": "number (required, 单位:元)",
  "screening_count": "integer (optional)",
  "audience_count": "integer (optional)"
}
```
- **响应**: 201 Created

### 4.3 票房记录详情
- **URL**: `GET /api/boxoffice/boxoffice/{id}/`
- **权限**: 需要登录
- **响应**: 200 OK

### 4.4 更新票房记录（管理员）
- **URL**: `PUT /api/boxoffice/boxoffice/{id}/`
- **权限**: 管理员
- **请求体**: 仅支持更新 daily_box_office, screening_count, audience_count
- **响应**: 200 OK

### 4.5 删除票房记录（管理员）
- **URL**: `DELETE /api/boxoffice/boxoffice/{id}/`
- **权限**: 管理员
- **响应**: 204 No Content

### 4.6 批量删除票房记录（管理员）
- **URL**: `POST /api/boxoffice/boxoffice/batch_delete/`
- **权限**: 管理员
- **请求体**:
```json
{
  "ids": [1, 2, 3, ...]
}
```
- **响应**: 200 OK

### 4.7 批量录入票房记录（管理员）
- **URL**: `POST /api/boxoffice/boxoffice/batch_input/`
- **权限**: 管理员
- **请求体**:
```json
{
  "records": [
    {
      "movie": "integer",
      "cinema": "integer",
      "record_date": "date",
      "daily_box_office": "number",
      "screening_count": "integer",
      "audience_count": "integer"
    }
  ]
}
```
- **响应**: 201 Created (或 207 Multi-Status 表示部分成功)

### 4.8 票房统计
- **URL**: `GET /api/boxoffice/boxoffice/stats/`
- **权限**: 需要登录
- **查询参数**: `start_date`, `end_date`, `movie_id`
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": {
    "total_box_office": 0.0,
    "total_screening_count": 0,
    "total_audience_count": 0,
    "record_count": 0
  }
}
```

---

## 5. 数据可视化模块 (`/api/visualization/`)

### 5.1 票房 Top10
- **URL**: `GET /api/visualization/stats/top10/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": [
    {
      "movie_id": 1,
      "movie_title": "string",
      "total_box_office": 0.0
    }
  ]
}
```

### 5.2 今日大盘
- **URL**: `GET /api/visualization/stats/today/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": {
    "date": "2024-01-01",
    "total_box_office": 0.0,
    "total_screening_count": 0,
    "total_audience_count": 0,
    "movie_count": 0
  }
}
```

### 5.3 本周冠军
- **URL**: `GET /api/visualization/stats/champion/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": {
    "movie_id": 1,
    "movie_title": "string",
    "box_office": 0.0,
    "week_start": "2024-01-01",
    "week_end": "2024-01-07"
  }
}
```

### 5.4 类型占比
- **URL**: `GET /api/visualization/stats/type/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": [
    {
      "type_id": 1,
      "type_name": "string",
      "box_office": 0.0,
      "percentage": 0.0
    }
  ]
}
```

### 5.5 地域分布
- **URL**: `GET /api/visualization/stats/region/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": [
    {
      "region_id": 1,
      "region_name": "string",
      "box_office": 0.0
    }
  ]
}
```

### 5.6 时间走势
- **URL**: `GET /api/visualization/stats/timeseries/`
- **权限**: 需要登录
- **查询参数**: `interval` (day/week/month), `days` (默认30天)
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": [
    {
      "date": "2024-01-01",
      "box_office": 0.0,
      "screening_count": 0,
      "audience_count": 0
    }
  ]
}
```

### 5.7 仪表盘数据
- **URL**: `GET /api/visualization/stats/dashboard/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": {
    "total_movies": 0,
    "total_cinemas": 0,
    "total_box_office": 0.0,
    "total_users": 0,
    "today_box_office": 0.0,
    "week_champion": {...},
    "top10": [...]
  }
}
```

---

## 6. 预测分析模块 (`/api/prediction/`)

### 6.1 影片票房预测
- **URL**: `GET /api/prediction/movie/{movie_id}/`
- **权限**: 需要登录
- **查询参数**:
  - `predict_days`: 预测天数 (默认7天)
  - `algorithm`: 算法选择 (linear/moving_average/combined)
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": {
    "success": true,
    "movie_id": 1,
    "predictions": [
      {
        "day": 1,
        "predicted_box_office": 100000.0
      }
    ],
    "history": [...],
    "algorithm": "linear"
  }
}
```

### 6.2 预测历史数据
- **URL**: `GET /api/prediction/movie/{movie_id}/history/`
- **权限**: 需要登录
- **查询参数**: `days` (默认30天)
- **响应**: 200 OK

### 6.3 算法列表
- **URL**: `GET /api/prediction/algorithms/`
- **权限**: 需要登录
- **响应**: 200 OK
```json
{
  "code": 0,
  "data": [
    {
      "id": "linear",
      "name": "线性回归预测",
      "description": "..."
    },
    {
      "id": "moving_average",
      "name": "移动平均预测",
      "description": "..."
    },
    {
      "id": "combined",
      "name": "综合预测",
      "description": "..."
    }
  ]
}
```

---

## 认证说明

### Token 使用

所有需要认证的接口都需要在请求头中携带 JWT Token：

```
Authorization: Bearer <access_token>
```

### Token 有效期

- **Access Token**: 2小时
- **Refresh Token**: 7天

### 权限说明

- **公开接口**: 无需登录即可访问
- **需要登录**: 需要有效的 Access Token
- **管理员专用**: 需要登录且用户角色为 ADMIN

---

## 错误代码

| Code | Message | 说明 |
|------|---------|------|
| 0 | 成功 | 请求成功 |
| -1 | 错误 | 请求失败，具体错误见 message 字段 |
| 401 | 未认证 | 缺少或无效的认证 Token |
| 403 | 权限不足 | 缺乏访问该资源的权限 |
| 404 | 资源不存在 | 请求的资源不存在 |

---

## 分页说明

所有列表接口都支持分页：

- `page`: 页码（从1开始）
- `page_size`: 每页数量（默认20，最大100）

分页响应格式：
```json
{
  "code": 0,
  "data": [...],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```
