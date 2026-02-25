# Architecture

## 目标与边界
- 目标：先完成后端数据底座与统计 API，再推进前端可视化。
- 角色：`admin` 可写，`user` 只读；默认接口需要认证。
- API 前缀：`/api/v1`；响应格式统一为 `{ code, message, data, total? }`。
- 导入范围：当前仅支持离线导入（脚本），不提供 Web 导入入口。

## 模块与数据
- 业务模块：`users`、`heritage`、`inheritors`、`categories`、`regions`、`importer`、`dashboard`。
- 关键关系：`Category -> HeritageItem -> Inheritor`，`Region -> HeritageItem/Inheritor`，`ImportJob -> ImportError`。
- 约束：列表默认分页 20；导入支持 `dry-run` 与 `commit`，要求幂等与可追踪。

## 关键文件职责
- `backend/heritage_system/settings.py`：Django/DRF/JWT/MySQL 全局配置。
- `backend/heritage_system/urls.py`：全局路由入口，聚合各 app 路由。
- `backend/utils/response.py`：统一成功/失败响应与异常包装。
- `backend/utils/pagination.py`：统一分页策略（每页 20）。
- `backend/apps/users/`：登录、刷新、登出、角色权限控制。
- `backend/apps/heritage/`：非遗项目模型与 CRUD、筛选查询。
- `backend/apps/inheritors/`：传承人模型与 CRUD、按项目关联。
- `backend/apps/categories/`：分类字典与树结构接口。
- `backend/apps/regions/`：国家/地区字典与检索。
- `backend/apps/importer/services.py`：导入校验、清洗、幂等写入、错误记录。
- `scripts/import_data.py`：离线导入 CLI 入口。
- `backend/apps/dashboard/views.py`：仪表盘聚合统计接口（当前已完成 overview）。
- `backend/apps/dashboard/urls.py`：仪表盘路由定义。

## 当前阶段
- 已完成阶段 1~5 与阶段 6.1（`GET /api/v1/dashboard/overview/`）。
- 阶段 6.2（地图分布接口）未开始。

---
Last updated: 2026-02-25
