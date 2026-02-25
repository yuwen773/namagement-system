# 术语 / API 对齐表（v1）

> 适用范围：`memory-bank/PRD.md`、`memory-bank/implementation-plan.md`、后续接口文档与代码实现。  
> 对齐原则：**以本表“标准写法”优先**，旧写法仅用于兼容识别。

## 1. 术语对齐

| 领域 | 标准写法 | 旧写法/别名 | 说明 |
|---|---|---|---|
| 数据目录 | `dataSource` | `dataSouce` | 统一为 `dataSource`（修正拼写）。 |
| 非遗项目 | `heritage item` | `heritage` | 文档中可简称“项目”，接口资源名统一为 `heritage-items`。 |
| 传承人 | `inheritor` | `inheritors`（模块） | 资源名使用复数，单体对象语义为 `inheritor`。 |
| 分类字典 | `categories` | `taxonomy` | 首版按 `categories` 落地，`taxonomy` 仅作概念描述。 |
| 地理区域 | `regions` | `geo` | `geo` 作为能力层（映射/补全），`regions` 作为数据资源。 |
| 导入模块 | `import` | `importer` | 对外 API 用 `import`，内部应用名可保留 `importer`。 |

## 2. API 路径对齐（标准）

统一前缀：`/api/v1`

| 能力 | 标准路径 | 旧写法/候选 |
|---|---|---|
| 登录 | `POST /auth/login` | `/auth/login/` |
| 刷新 token | `POST /auth/refresh` | `/auth/refresh/` |
| 仪表盘总览 | `GET /dashboard/overview` | `/dashboard/overview/` |
| 地图分布 | `GET /dashboard/map-distribution` | `/dashboard/map-distribution/` |
| 趋势 | `GET /dashboard/trends` | `/dashboard/trends/` |
| 非遗项目 CRUD | `/heritage-items` | `/heritage` |
| 传承人 CRUD | `/inheritors` | `/inheritor` |
| 导入上传 | `POST /import/upload` | `/importer/upload` |
| 导入任务列表 | `GET /import/jobs` | `/importer/jobs` |
| 导入错误明细 | `GET /import/jobs/{id}/errors` | `/importer/jobs/{id}/errors` |

## 3. 执行约束

1. 新代码、新文档一律使用“标准路径”与“标准写法”。  
2. 若后端需兼容旧路径，必须在网关或路由层做 301/兼容映射，并标注废弃时间。  
3. 前后端联调、测试用例、Postman 集合以本表为唯一基线。  
