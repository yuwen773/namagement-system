# Architecture

## 系统边界
- 目标：先完成后端数据底座与统计 API，再推进前端可视化。
- 权限：默认鉴权；`admin` 可写，`user` 只读。
- API：统一前缀 `/api/v1`，统一响应 `{ code, message, data, total? }`。
- 导入：当前仅提供离线导入链路（脚本 + 服务层），不提供 Web 上传入口。

## 核心数据关系
- `Category -> HeritageItem -> Inheritor`：分类驱动项目，项目关联传承人。
- `Region -> HeritageItem/Inheritor`：地图统计按国家维度聚合。
- `ImportJob -> ImportError`：导入任务与行级错误可追踪。

## 代码文件职责（核心）
- `backend/heritage_system/settings.py`：Django、DRF、JWT、数据库和异常处理总配置。
- `backend/heritage_system/urls.py`：聚合 `users/heritage/inheritors/categories/regions/dashboard` 路由。
- `backend/utils/response.py`：统一成功/失败响应结构与全局异常转换。
- `backend/utils/pagination.py`：统一分页策略（默认每页 20）。
- `backend/apps/importer/services.py`：离线导入解析、清洗、校验、幂等写入、错误落库。
- `backend/apps/dashboard/views.py`：仪表盘聚合接口（已实现 `overview`、`map-distribution`，后者支持类别筛选）。
- `backend/apps/dashboard/urls.py`：仪表盘接口路由定义。
- `backend/apps/dashboard/tests/test_views.py`：仪表盘接口测试（鉴权、统计准确性、筛选逻辑）。

## memory-bank 文档职责
- `memory-bank/pre-prd.md`：一句话需求原点。
- `memory-bank/PRD.md`：产品目标、范围、模块、接口、验收标准。
- `memory-bank/implementation-plan.md`：按阶段的可执行实施步骤。
- `memory-bank/tech-stack.md`：技术选型基线。
- `memory-bank/IMPORT_REPORT.md`：数据源质量与导入策略评估。
- `memory-bank/terminology-api-alignment.md`：术语和 API 命名规范基线。
- `memory-bank/progress.md`：阶段进度和验证记录。
- `memory-bank/architecture.md`：系统边界、数据关系、关键文件职责。

## 当前实现状态
- 已完成阶段 1~5、阶段 6.1、阶段 6.2。
- 阶段 6.3 尚未开始。

---
Last updated: 2026-02-25
