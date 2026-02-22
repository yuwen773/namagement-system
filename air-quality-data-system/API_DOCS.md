# Air Quality Data System API 文档

## 基本信息

- **版本**：`1.0.0`
- **更新时间**：`2026-02-15`
- **Schema 地址**：`/api/schema/`
- **Swagger UI**：`/api/docs/`
- **OpenAPI JSON**：`backend/openapi-schema.json`
- **Base URL**：`http://127.0.0.1:8000/api/`

## 认证方式

本项目使用 Token Authentication，请求头需包含：

```http
Authorization: Token <your_token_here>
```

登录成功后返回的 token 需要在后续请求中携带。

## 通用响应格式

### 成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "total": 100
}
```

### 错误响应

```json
{
  "code": 400,
  "message": "错误描述",
  "field": "错误字段（可选）"
}
```

### 常见错误码

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数格式错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

# 用户端接口

## 1. 用户认证 (Auth)

### 1.1 用户登录

**端点**：`POST /api/auth/login/`

**权限**：无需认证

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（最大150字符） |
| password | string | 是 | 密码（最大128字符） |

**请求示例**：
```json
{
  "username": "admin",
  "password": "password123"
}
```

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "phone": "+86-138-0000-0000",
      "role": "ADMIN",
      "status": true,
      "date_joined": "2025-01-01T00:00:00Z",
      "last_login": "2025-02-15T10:30:00Z"
    }
  }
}
```

---

### 1.2 用户注册

**端点**：`POST /api/auth/register/`

**权限**：无需认证

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（3-20字符，不可重复） |
| password | string | 是 | 密码（6-20字符） |
| email | string | 是 | 邮箱地址 |
| phone | string | 否 | 手机号（最大20字符） |

**请求示例**：
```json
{
  "username": "newuser",
  "password": "password123",
  "email": "newuser@example.com",
  "phone": "+86-139-0000-0000"
}
```

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "phone": "+86-139-0000-0000",
    "role": "USER",
    "status": true
  }
}
```

---

## 2. 空气质量概览 (Overview)

### 2.1 查询全国概览

**端点**：`GET /api/overview/`

**权限**：无需认证

**缓存**：60秒

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "national": {
      "aqi": 75,
      "pm25": 35.5,
      "pm10": 45.0,
      "so2": 15.0,
      "no2": 25.0,
      "co": 0.9,
      "o3": 60.0,
      "quality_level": "GOOD"
    },
    "map_data": [
      {
        "province_code": "110000",
        "province_name": "北京市",
        "city_code": "110101",
        "city_name": "东城区",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "aqi": 75,
        "quality_level": "GOOD"
      }
    ],
    "city_count": 50
  }
}
```

---

### 2.2 查询 Top 城市

**端点**：`GET /api/overview/top-cities/`

**权限**：无需认证

**缓存**：60秒

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| limit | integer | 否 | 10 | 1-50 | 返回城市数量 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "best": [
      {
        "city_code": "110101",
        "city_name": "东城区",
        "aqi": 35,
        "quality_level": "EXCELLENT"
      }
    ],
    "worst": [
      {
        "city_code": "130101",
        "city_name": "石家庄市",
        "aqi": 150,
        "quality_level": "LIGHT_POLLUTION"
      }
    ]
  }
}
```

---

## 3. 城市数据 (City)

### 3.1 查询城市详情

**端点**：`GET /api/cities/{code}/`

**权限**：无需认证

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 城市编码 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "city_code": "110101",
    "city_name": "东城区",
    "province_code": "110000",
    "province_name": "北京市",
    "longitude": 116.4074,
    "latitude": 39.9042,
    "snapshot": {
      "monitor_time": "2026-02-15T14:00:00Z",
      "aqi": 75,
      "pm25": 35.5,
      "pm10": 45.0,
      "so2": 15.0,
      "no2": 25.0,
      "co": 0.9,
      "o3": 60.0,
      "quality_level": "GOOD",
      "station_count": 5
    }
  }
}
```

---

### 3.2 查询城市趋势

**端点**：`GET /api/cities/{code}/trend/`

**权限**：无需认证

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 城市编码 |

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| hours | integer | 否 | 24 | 1-168 | 小时窗口（最多7天） |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "city_code": "110101",
    "city_name": "东城区",
    "hours": 24,
    "trend": [
      {
        "time": "2026-02-15T00:00:00Z",
        "aqi": 65,
        "pm25": 30.5,
        "pm10": 40.0
      }
    ]
  }
}
```

---

## 4. 站点数据 (Station)

### 4.1 查询站点详情

**端点**：`GET /api/stations/{code}/`

**权限**：无需认证

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 站点编码 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "station_code": "ST001",
    "station_name": "东城监测站",
    "station_type": "国控",
    "address": "北京市东城区某街道",
    "city_code": "110101",
    "city_name": "东城区",
    "snapshot": {
      "monitor_time": "2026-02-15T14:00:00Z",
      "aqi": 75,
      "pm25": 35.5,
      "quality_level": "GOOD"
    }
  }
}
```

---

### 4.2 查询站点趋势

**端点**：`GET /api/stations/{code}/trend/`

**权限**：无需认证

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 站点编码 |

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| hours | integer | 否 | 24 | 1-168 | 小时窗口 |

---

## 5. 历史数据 (Historical)

### 5.1 查询历史数据

**端点**：`GET /api/historical-data/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | 1-100000 | 页码 |
| page_size | integer | 否 | 20 | 1-200 | 每页数量 |
| ordering | string | 否 | -monitor_time | - | 排序字段 |
| city_code | string | 否 | - | - | 城市编码 |
| station_code | string | 否 | - | - | 站点编码 |
| start_date | string | 否 | - | - | 起始日期（YYYY-MM-DD） |
| end_date | string | 否 | - | - | 结束日期（YYYY-MM-DD） |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "province_code": "110000",
      "province_name": "北京市",
      "city_code": "110101",
      "city_name": "东城区",
      "station_code": "ST001",
      "station_name": "东城监测站",
      "monitor_time": "2026-02-15T14:00:00Z",
      "aqi": 75,
      "pm25": 35.5,
      "pm10": 45.0,
      "so2": 15.0,
      "no2": 25.0,
      "co": 0.9,
      "o3": 60.0,
      "quality_level": "GOOD"
    }
  ],
  "total": 100
}
```

---

### 5.2 导出历史数据

**端点**：`GET /api/historical-data/export/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| format | string | 否 | csv | 导出格式（csv/xlsx） |
| city_code | string | 否 | - | 城市编码 |
| station_code | string | 否 | - | 站点编码 |
| start_date | string | 否 | - | 起始日期 |
| end_date | string | 否 | - | 结束日期 |

---

## 6. 数据分析 (Analysis)

### 6.1 城市对比分析

**端点**：`POST /api/analysis/compare/`

**权限**：无需认证

**请求体**：

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| city_codes | array[string] | 是 | 2-10个 | 城市编码数组 |
| hours | integer | 否 | 1-168 | 小时窗口（默认24） |

**请求示例**：
```json
{
  "city_codes": ["110101", "130101", "310101"],
  "hours": 24
}
```

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "hours": 24,
    "series": [
      {
        "city_code": "110101",
        "city_name": "东城区",
        "province_name": "北京市",
        "trend": [
          {
            "time": "2026-02-15T00:00:00Z",
            "aqi": 65,
            "pm25": 30.5
          }
        ]
      }
    ]
  }
}
```

---

### 6.2 污染物相关性分析

**端点**：`GET /api/analysis/correlation/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| pollutant_x | string | 否 | pm25 | X轴污染物 |
| pollutant_y | string | 否 | pm10 | Y轴污染物 |
| city_code | string | 否 | - | 城市编码 |
| start_date | string | 否 | - | 起始日期 |
| end_date | string | 否 | - | 结束日期 |
| max_points | integer | 否 | 2000 | 100-20000 | 散点数据最大数量 |

**污染物选项**：pm25, pm10, so2, no2, co, o3

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "pollutant_x": "pm25",
    "pollutant_y": "pm10",
    "sample_count": 5000,
    "correlation": 0.8542,
    "scatter_data": [
      {"x": 35.5, "y": 45.0},
      {"x": 40.2, "y": 52.1}
    ]
  }
}
```

---

### 6.3 AQI 分布统计

**端点**：`GET /api/analysis/distribution/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city_code | string | 否 | 城市编码 |
| start_date | string | 否 | 起始日期 |
| end_date | string | 否 | 结束日期 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "total": 10000,
    "distribution": [
      {
        "quality_level": "EXCELLENT",
        "quality_label": "Excellent",
        "count": 2000,
        "percentage": 20.0
      },
      {
        "quality_level": "GOOD",
        "quality_label": "Good",
        "count": 5000,
        "percentage": 50.0
      }
    ]
  }
}
```

---

## 7. 防护指南 (Protection)

### 7.1 获取防护指南

**端点**：`GET /api/protection-guide/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city_code | string | 是 | 城市代码 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "city": {
      "city_code": "110101",
      "city_name": "东城区",
      "province_code": "110000",
      "province_name": "北京市"
    },
    "current": {
      "monitor_time": "2026-02-15T14:00:00Z",
      "aqi": 85,
      "quality_level": "良"
    },
    "advice": {
      "general": "空气质量变化较快，请减少不必要户外活动并关注后续预警。",
      "sensitive": "敏感人群建议减少外出并加强个人防护。",
      "children": "儿童建议减少户外活动，外出时佩戴防护口罩。",
      "elderly": "老年人建议避免剧烈活动，外出注意防护。",
      "patients": "呼吸道疾病患者建议尽量居家，按医嘱做好健康管理。"
    },
    "forecast": {
      "trend": "RISING",
      "average_hourly_change": 2.5,
      "predicted_aqi_6h": 100,
      "predicted_aqi_12h": 115,
      "predicted_quality_level_6h": "良",
      "predicted_quality_level_12h": "轻度污染",
      "warning_reference_aqi": 115,
      "warning_advice": "敏感人群建议减少外出并加强个人防护。"
    }
  }
}
```

---

## 8. 文章内容 (Articles)

### 8.1 查询文章列表

**端点**：`GET /api/articles/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| category_id | integer | 否 | - | - | 文章分类ID |
| page | integer | 否 | 1 | 1-100000 | 页码 |
| page_size | integer | 否 | 20 | 1-200 | 每页数量 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "title": "如何做好日常防护",
      "category_id": 1,
      "category_name": "防护指南",
      "is_announcement": false,
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100
}
```

---

### 8.2 查询文章详情

**端点**：`GET /api/articles/{id}/`

**权限**：无需认证

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 文章ID |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "title": "如何做好日常防护",
    "category_id": 1,
    "category_name": "防护指南",
    "content": "文章内容...",
    "is_announcement": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

### 8.3 查询文章分类

**端点**：`GET /api/categories/`

**权限**：无需认证

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "name": "防护指南",
      "sort": 0
    }
  ]
}
```

---

### 8.4 查询系统公告

**端点**：`GET /api/announcements/`

**权限**：无需认证

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| limit | integer | 否 | 5 | 5-10 | 返回数量 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "title": "系统维护通知",
      "is_announcement": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

# 管理端接口

> 所有管理端接口需要管理员权限，请求头需携带有效的 Token。

## 9. 管理仪表盘 (Dashboard)

### 9.1 查询管理端仪表盘

**端点**：`GET /api/admin/dashboard/`

**权限**：仅管理员

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "system": {
      "service_start_time": "2026-02-15T00:00:00Z",
      "current_time": "2026-02-15T14:00:00Z",
      "uptime_seconds": 50400,
      "latest_import_time": "2026-02-15T12:00:00Z"
    },
    "data_summary": {
      "total_data_count": 100000,
      "today_new_count": 5000,
      "covered_city_count": 350
    },
    "user_summary": {
      "total_user_count": 1000,
      "today_active_user_count": 200
    },
    "latest_import_task": {
      "task_id": "task-123456",
      "status": "SUCCESS",
      "file_name": "data.xlsx",
      "total_count": 1000,
      "success_count": 995,
      "failed_count": 5
    }
  }
}
```

---

## 10. 数据导入 (Import)

### 10.1 上传导入文件

**端点**：`POST /api/admin/data-import/`

**权限**：仅管理员

**请求体** (multipart/form-data)：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 上传的文件（.csv/.xlsx/.xls） |
| dataset_type | string | 否 | 数据集类型（默认：air_quality_data） |

**数据集类型选项**：
- provinces - 省份数据
- cities - 城市数据
- stations - 站点数据
- air_quality_data - 空气质量数据

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": {
    "task_id": "task-123456",
    "status": "PENDING",
    "dataset_type": "air_quality_data"
  }
}
```

---

### 10.2 查询导入任务列表

**端点**：`GET /api/admin/data-import/tasks/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | 1-10000 | 页码 |
| page_size | integer | 否 | 20 | 1-200 | 每页数量 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "task_id": "task-123456",
      "file_name": "data.xlsx",
      "file_type": "xlsx",
      "status": "SUCCESS",
      "total_count": 1000,
      "success_count": 995,
      "failed_count": 5,
      "start_time": "2026-02-15T12:00:00Z",
      "end_time": "2026-02-15T12:05:00Z"
    }
  ],
  "total": 50
}
```

**任务状态**：
- PENDING - 等待中
- RUNNING - 执行中
- SUCCESS - 成功
- FAILED - 失败

---

### 10.3 查询导入任务详情

**端点**：`GET /api/admin/data-import/tasks/{task_id}/`

**权限**：仅管理员

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | string | 是 | 导入任务ID |

---

### 10.4 查询导入任务日志

**端点**：`GET /api/admin/data-import/tasks/{task_id}/logs/`

**权限**：仅管理员

**路径参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | string | 是 | 导入任务ID |

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | 1-10000 | 页码 |
| page_size | integer | 否 | 50 | 1-200 | 每页数量 |

---

## 11. 空气质量管理 (AirQuality)

### 11.1 查询空气质量数据

**端点**：`GET /api/admin/air-quality/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | 1-100000 | 页码 |
| page_size | integer | 否 | 20 | 1-200 | 每页数量 |
| ordering | string | 否 | -monitor_time | - | 排序字段 |
| city_code | string | 否 | - | - | 城市编码 |
| station_code | string | 否 | - | - | 站点编码 |
| quality_level | string | 否 | - | - | 空气质量等级 |
| start_date | string | 否 | - | - | 起始日期 |
| end_date | string | 否 | - | - | 结束日期 |

---

### 11.2 更新空气质量数据

**端点**：`PUT /api/admin/air-quality/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 数据记录ID |
| station_id | integer | 否 | 监测站点ID |
| monitor_time | datetime | 否 | 监测时间 |
| aqi | integer | 否 | 空气质量指数（0-500） |
| pm25 | decimal | 否 | PM2.5浓度（≥0） |
| pm10 | decimal | 否 | PM10浓度（≥0） |
| so2 | decimal | 否 | SO2浓度（≥0） |
| no2 | decimal | 否 | NO2浓度（≥0） |
| co | decimal | 否 | CO浓度（≥0） |
| o3 | decimal | 否 | O3浓度（≥0） |

---

### 11.3 删除空气质量数据

**端点**：`DELETE /api/admin/air-quality/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 条件必填 | 单个记录ID（与ids二选一） |
| ids | array[int] | 条件必填 | 批量记录ID数组（与id二选一） |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "message": "删除成功",
  "data": {
    "deleted_count": 5
  }
}
```

---

## 12. 防护规则管理 (Rules)

### 12.1 查询防护规则

**端点**：`GET /api/admin/rules/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| population_type | string | 否 | 人群类型 |
| is_enabled | boolean | 否 | 启用状态 |
| keyword | string | 否 | 关键字搜索 |

**人群类型选项**：
- GENERAL - 普通人群
- CHILDREN - 儿童
- ELDERLY - 老年人
- PATIENTS - 患者
- SENSITIVE - 敏感人群

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "rule_name": "儿童防护-轻度污染",
      "min_aqi": 51,
      "max_aqi": 100,
      "population_type": "CHILDREN",
      "advice": "儿童建议减少户外活动，外出时佩戴防护口罩。",
      "is_enabled": true
    }
  ]
}
```

---

### 12.2 新增防护规则

**端点**：`POST /api/admin/rules/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| rule_name | string | 是 | 规则名称（最大100字符） |
| min_aqi | integer | 是 | AQI最小值（0-500） |
| max_aqi | integer | 是 | AQI最大值（0-500） |
| population_type | string | 是 | 人群类型 |
| advice | string | 是 | 防护建议 |
| is_enabled | boolean | 否 | 是否启用（默认true） |

**业务规则**：
- min_aqi 必须 <= max_aqi
- 同一人群类型的 AQI 范围不能重叠

---

### 12.3 更新防护规则

**端点**：`PUT /api/admin/rules/`

**权限**：仅管理员

#### 单条更新

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 规则ID |
| rule_name | string | 否 | 规则名称 |
| min_aqi | integer | 否 | AQI最小值 |
| max_aqi | integer | 否 | AQI最大值 |
| population_type | string | 否 | 人群类型 |
| advice | string | 否 | 防护建议 |
| is_enabled | boolean | 否 | 是否启用 |

#### 批量更新启用状态

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | array[int] | 是 | 规则ID列表 |
| is_enabled | boolean | 是 | 启用状态 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "message": "批量更新完成",
  "data": {
    "updated_count": 3
  }
}
```

---

### 12.4 删除防护规则

**端点**：`DELETE /api/admin/rules/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 条件必填 | 单个规则ID（与ids二选一） |
| ids | array[int] | 条件必填 | 规则ID数组（与id二选一） |

---

## 13. 文章管理 (Articles)

### 13.1 查询文章列表（管理端）

**端点**：`GET /api/admin/articles/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 文章状态（DRAFT/PUBLISHED/OFFLINE） |
| category_id | integer | 否 | 文章分类ID |
| is_announcement | boolean | 否 | 是否为公告 |
| keyword | string | 否 | 标题或内容关键字 |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

---

### 13.2 新增文章

**端点**：`POST /api/admin/articles/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 文章标题（最大255字符） |
| category_id | integer | 是 | 文章分类ID |
| content | string | 是 | 文章内容 |
| status | string | 否 | 状态（默认DRAFT） |
| is_announcement | boolean | 否 | 是否为公告（默认false） |
| sort_order | integer | 否 | 排序字段（默认0） |

**文章状态选项**：
- DRAFT - 草稿
- PUBLISHED - 已发布
- OFFLINE - 已下线

---

### 13.3 更新文章

**端点**：`PUT /api/admin/articles/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 文章ID |
| 其他字段 | - | 否 | 部分更新，只传需要修改的字段 |

---

### 13.4 删除文章

**端点**：`DELETE /api/admin/articles/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 条件必填 | 单个文章ID（与ids二选一） |
| ids | array[int] | 条件必填 | 文章ID数组（与id二选一） |

---

## 14. 分类管理 (Categories)

### 14.1 查询分类列表

**端点**：`GET /api/admin/categories/`

**权限**：仅管理员

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "name": "防护指南",
      "sort": 0
    }
  ]
}
```

---

### 14.2 新增分类

**端点**：`POST /api/admin/categories/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 分类名称（最大100字符，必须唯一） |
| sort | integer | 否 | 排序字段（默认0） |

---

### 14.3 更新分类

**端点**：`PUT /api/admin/categories/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 分类ID |
| name | string | 否 | 分类名称 |
| sort | integer | 否 | 排序字段 |

---

### 14.4 删除分类

**端点**：`DELETE /api/admin/categories/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 条件必填 | 单个分类ID（与ids二选一） |
| ids | array[int] | 条件必填 | 分类ID数组（与id二选一） |

**错误响应** (400)：
```json
{
  "code": 400,
  "message": "该分类下存在文章，无法删除",
  "field": "id"
}
```

---

## 15. 用户管理 (Users)

### 15.1 查询用户列表

**端点**：`GET /api/admin/users/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 默认值 | 范围 | 说明 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | 1-100000 | 页码 |
| page_size | integer | 否 | 20 | 1-200 | 每页数量 |
| keyword | string | 否 | - | - | 搜索关键词 |
| role | string | 否 | - | - | 角色过滤（USER/ADMIN） |
| status | boolean | 否 | - | - | 状态过滤 |
| include_deleted | boolean | 否 | false | - | 是否包含已删除用户 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "phone": "+86-138-0000-0000",
      "role": "ADMIN",
      "status": true,
      "is_staff": true,
      "date_joined": "2025-01-01T00:00:00Z",
      "last_login": "2025-02-15T10:30:00Z"
    }
  ],
  "total": 100
}
```

---

### 15.2 更新用户信息

**端点**：`PUT /api/admin/users/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 用户ID |
| role | string | 否 | 角色（USER/ADMIN） |
| status | boolean | 否 | 用户状态 |
| email | string | 否 | 邮箱地址 |
| phone | string | 否 | 手机号 |

---

### 15.3 软删除用户

**端点**：`DELETE /api/admin/users/`

**权限**：仅管理员

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 条件必填 | 单个用户ID（与ids二选一） |
| ids | array[int] | 条件必填 | 用户ID数组（与id二选一） |

---

## 16. 日志管理 (Logs)

### 16.1 查询操作日志

**端点**：`GET /api/admin/logs/operations/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | integer | 否 | 按用户ID过滤 |
| operation_type | string | 否 | 按操作类型过滤 |
| start_date | string | 否 | 起始日期（YYYY-MM-DD） |
| end_date | string | 否 | 结束日期（YYYY-MM-DD） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "user": 1,
      "username": "admin",
      "operation_type": "POST /api/admin/stations/",
      "operation_content": "{\"name\":\"监测站A\",\"code\":\"ST001\"}",
      "ip_address": "192.168.1.100",
      "operation_time": "2026-02-15T10:30:00Z"
    }
  ],
  "total": 100
}
```

---

### 16.2 查询异常日志

**端点**：`GET /api/admin/logs/errors/`

**权限**：仅管理员

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| error_type | string | 否 | 按异常类型过滤 |
| start_date | string | 否 | 起始日期（YYYY-MM-DD） |
| end_date | string | 否 | 结束日期（YYYY-MM-DD） |
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页数量 |

**响应示例** (200 OK)：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "error_type": "ValidationError",
      "error_message": "格式错误，应为整数，范围 1-200",
      "stack_trace": "Traceback (most recent call last):\n  ...",
      "occurred_at": "2026-02-15T10:30:00Z"
    }
  ],
  "total": 50
}
```

---

# 数据模型

## 空气质量等级

| 等级 | 值 | AQI范围 | 说明 |
|------|-----|---------|------|
| EXCELLENT | Excellent | 0-50 | 优 |
| GOOD | Good | 51-100 | 良 |
| LIGHT_POLLUTION | Light pollution | 101-150 | 轻度污染 |
| MODERATE_POLLUTION | Moderate pollution | 151-200 | 中度污染 |
| HEAVY_POLLUTION | Heavy pollution | 201-300 | 重度污染 |
| SEVERE_POLLUTION | Severe pollution | 301-500 | 严重污染 |

## 用户角色

| 值 | 说明 |
|----|------|
| USER | 普通用户 |
| ADMIN | 管理员 |

## 文章状态

| 值 | 说明 |
|----|------|
| DRAFT | 草稿 |
| PUBLISHED | 已发布 |
| OFFLINE | 已下线 |

## 人群类型

| 值 | 说明 |
|----|------|
| GENERAL | 普通人群 |
| CHILDREN | 儿童 |
| ELDERLY | 老年人 |
| PATIENTS | 患者 |
| SENSITIVE | 敏感人群 |

---

# 附录

## 自动日志机制

系统通过中间件自动记录：

1. **操作日志自动记录条件**：
   - 路径以 `/api/admin/` 开头
   - HTTP 方法为 POST/PUT/PATCH/DELETE
   - 响应状态码 < 400
   - 用户已认证

2. **异常日志自动记录**：
   - 捕获所有未处理的异常
   - 自动记录异常类型、消息和堆栈跟踪

## 数据库配置

- **数据库**：MySQL 8.0+
- **端口**：3307
- **字符集**：UTF8MB4
- **引擎**：InnoDB

## 分页通用参数

| 参数 | 类型 | 必填 | 默认值 | 范围 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 1-100000 |
| page_size | integer | 否 | 20 | 1-200 |

## 日期格式

所有日期时间字段使用 ISO 8601 格式：
- 日期：`YYYY-MM-DD`
- 日期时间：`YYYY-MM-DDTHH:MM:SSZ`

时区：Asia/Shanghai (UTC+8)
