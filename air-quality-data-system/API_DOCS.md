# Air Quality Data System API

- 版本：`1.0.0`
- 生成时间：`2026-02-15 21:04:32 +0800`
- Schema 地址：`/api/schema/`
- Swagger UI：`/api/docs/`
- OpenAPI JSON 文件：`backend\openapi-schema.json`

本文档由 `drf-spectacular` 生成的 OpenAPI Schema 自动整理。

## 用户端接口

- 接口数量：`18`

### `POST /api/analysis/compare/`

- 概要：城市对比分析
- 描述：对多个城市进行趋势对比分析。
- 标签：User - Analysis
- 查询/路径参数：
- 无
- 请求体：
- `application/json`（必填：否，Schema：`object`）
- `application/x-www-form-urlencoded`（必填：否，Schema：`object`）
- `multipart/form-data`（必填：否，Schema：`object`）
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/analysis/correlation/`

- 概要：污染物相关性分析
- 描述：计算两个污染物之间的相关系数并返回散点数据。
- 标签：User - Analysis
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/analysis/distribution/`

- 概要：AQI 分布统计
- 描述：统计空气质量等级分布及占比。
- 标签：User - Analysis
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/announcements/`

- 概要：查询系统公告
- 描述：获取最新已发布系统公告，默认返回 5 条，最多 10 条。
- 标签：User - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/articles/`

- 概要：查询文章列表
- 描述：分页查询已发布的科普文章（不含公告），支持按分类过滤。
- 标签：User - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/articles/{id}/`

- 概要：查询文章详情
- 描述：获取单篇已发布科普文章详情。
- 标签：User - Articles
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| id | path | 是 | integer | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `POST /api/auth/login/`

- 概要：用户登录
- 描述：使用用户名和密码登录，返回 Token 与当前用户信息。
- 标签：Auth
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `POST /api/auth/register/`

- 概要：用户注册
- 描述：创建普通用户账号并返回用户信息。
- 标签：Auth
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/categories/`

- 概要：查询文章分类
- 描述：获取用户端可用的文章分类列表。
- 标签：User - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/cities/{code}/`

- 概要：查询城市详情
- 描述：根据城市编码查询城市最新空气质量快照。
- 标签：User - City
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| code | path | 是 | string | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/cities/{code}/trend/`

- 概要：查询城市趋势
- 描述：根据城市编码查询指定小时窗口内的趋势数据。
- 标签：User - City
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| code | path | 是 | string | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/historical-data/`

- 概要：查询历史数据
- 描述：分页查询历史空气质量数据，支持过滤与排序。
- 标签：User - Historical
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/historical-data/export/`

- 概要：导出历史数据
- 描述：按筛选条件导出历史数据文件，支持 CSV/XLSX。
- 标签：User - Historical
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |
| 400 | - |

### `GET /api/overview/`

- 概要：查询全国概览
- 描述：返回全国平均指标、地图数据与城市数量。
- 标签：User - Overview
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/overview/top-cities/`

- 概要：查询 Top 城市
- 描述：返回空气质量最佳/最差城市排行榜。
- 标签：User - Overview
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/protection-guide/`

- 概要：获取防护指南
- 描述：根据城市当前 AQI 与趋势预测，返回分人群防护建议和未来预警信息。
- 标签：User - Protection
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/stations/{code}/`

- 概要：查询站点详情
- 描述：根据站点编码查询站点最新空气质量快照。
- 标签：User - Station
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| code | path | 是 | string | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/stations/{code}/trend/`

- 概要：查询站点趋势
- 描述：根据站点编码查询指定小时窗口内的趋势数据。
- 标签：User - Station
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| code | path | 是 | string | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

## 管理端接口

- 接口数量：`25`

### `GET /api/admin/air-quality/`

- 概要：查询空气质量数据（管理端）
- 描述：管理员分页查询空气质量记录，支持多条件过滤与排序。
- 标签：Admin - AirQuality
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `PUT /api/admin/air-quality/`

- 概要：更新空气质量数据
- 描述：管理员按 id 更新空气质量记录。
- 标签：Admin - AirQuality
- 查询/路径参数：
- 无
- 请求体：
- `application/json`（必填：否，Schema：`object`）
- `application/x-www-form-urlencoded`（必填：否，Schema：`object`）
- `multipart/form-data`（必填：否，Schema：`object`）
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `DELETE /api/admin/air-quality/`

- 概要：删除空气质量数据
- 描述：管理员按 id 或 ids 删除空气质量记录。
- 标签：Admin - AirQuality
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 204 | No response body |

### `GET /api/admin/articles/`

- 概要：查询文章列表（管理端）
- 描述：管理员分页查询文章，支持状态、分类、公告标记与关键字过滤。
- 标签：Admin - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `POST /api/admin/articles/`

- 概要：新增文章
- 描述：管理员创建文章。
- 标签：Admin - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `PUT /api/admin/articles/`

- 概要：更新文章
- 描述：管理员按 id 更新文章内容或发布状态。
- 标签：Admin - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `DELETE /api/admin/articles/`

- 概要：删除文章
- 描述：管理员按 id 或 ids 删除文章。
- 标签：Admin - Articles
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 204 | No response body |

### `GET /api/admin/categories/`

- 概要：查询分类列表（管理端）
- 描述：管理员查询全部文章分类。
- 标签：Admin - Categories
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `POST /api/admin/categories/`

- 概要：新增分类
- 描述：管理员新增文章分类。
- 标签：Admin - Categories
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `PUT /api/admin/categories/`

- 概要：更新分类
- 描述：管理员按 id 更新文章分类。
- 标签：Admin - Categories
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `DELETE /api/admin/categories/`

- 概要：删除分类
- 描述：管理员按 id 或 ids 删除分类。
- 标签：Admin - Categories
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 204 | No response body |

### `GET /api/admin/dashboard/`

- 概要：查询管理端仪表盘
- 描述：返回系统运行信息、数据统计、用户统计与最近导入任务。
- 标签：Admin - Dashboard
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `POST /api/admin/data-import/`

- 概要：上传导入文件
- 描述：管理员上传 CSV/XLS/XLSX 文件并创建导入任务，返回 task_id。
- 标签：Admin - Import
- 查询/路径参数：
- 无
- 请求体：
- `multipart/form-data`（必填：否，Schema：`object`）
- `application/x-www-form-urlencoded`（必填：否，Schema：`object`）
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/admin/data-import/tasks/`

- 概要：查询导入任务列表
- 描述：管理员分页查询导入任务状态。
- 标签：Admin - Import
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/admin/data-import/tasks/{task_id}/`

- 概要：查询导入任务详情
- 描述：管理员根据 task_id 查询单个导入任务详情。
- 标签：Admin - Import
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| task_id | path | 是 | string | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/admin/data-import/tasks/{task_id}/logs/`

- 概要：查询导入任务日志
- 描述：管理员分页查询指定导入任务的失败日志。
- 标签：Admin - Import
- 查询/路径参数：
| 参数 | 位置 | 必填 | 类型 | 说明 |
|---|---|---|---|---|
| task_id | path | 是 | string | - |
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/admin/logs/errors/`

- 概要：查询异常日志
- 描述：管理员分页查询异常日志，支持异常类型和日期区间过滤。
- 标签：Admin - Logs
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/admin/logs/operations/`

- 概要：查询操作日志
- 描述：管理员分页查询操作日志，支持用户、操作类型和日期区间过滤。
- 标签：Admin - Logs
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `GET /api/admin/rules/`

- 概要：查询防护规则
- 描述：管理员查询防护规则列表，支持人群、启用状态、关键字过滤。
- 标签：Admin - Rules
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `POST /api/admin/rules/`

- 概要：新增防护规则
- 描述：管理员新增一条防护规则。
- 标签：Admin - Rules
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `PUT /api/admin/rules/`

- 概要：更新防护规则
- 描述：管理员更新单条规则，或按 ids 批量更新启用状态。
- 标签：Admin - Rules
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `DELETE /api/admin/rules/`

- 概要：删除防护规则
- 描述：管理员按 id 或 ids 删除防护规则。
- 标签：Admin - Rules
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 204 | No response body |

### `GET /api/admin/users/`

- 概要：查询用户列表
- 描述：管理员分页查询用户，支持关键字、角色、状态与是否包含已删除用户过滤。
- 标签：Admin - Users
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `PUT /api/admin/users/`

- 概要：更新用户信息
- 描述：管理员更新用户角色、状态、邮箱或手机号。
- 标签：Admin - Users
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 200 | - |

### `DELETE /api/admin/users/`

- 概要：软删除用户
- 描述：管理员按 id 或 ids 软删除用户，删除后用户将被禁用。
- 标签：Admin - Users
- 查询/路径参数：
- 无
- 请求体：
- 无
- 响应：
| 状态码 | 说明 |
|---|---|
| 204 | No response body |
