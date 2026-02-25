# Architecture

## 系统边界
- 后端先行：先完成数据模型、导入链路、统计 API，再推进前端可视化。
- 鉴权默认开启：`admin` 可写，`user` 只读。
- API 统一前缀：`/api/v1`。
- 响应统一结构：`{ code, message, data, total? }`。

## 核心数据关系
- `Category -> HeritageItem -> Inheritor`：分类驱动项目，项目关联传承人。
- `Region -> HeritageItem/Inheritor`：地图分布与国家排行按国家聚合。
- `ImportJob -> ImportError`：导入任务与行级错误追踪。

## 后端关键文件职责
- `backend/heritage_system/settings.py`：Django/DRF/JWT/数据库/异常处理总配置。
- `backend/heritage_system/urls.py`：聚合各业务模块路由入口。
- `backend/utils/response.py`：统一成功/失败响应与全局异常转换。
- `backend/utils/pagination.py`：统一分页策略（默认每页 20）。
- `backend/apps/importer/services.py`：离线导入（解析、清洗、校验、入库、错误落库）。
- `backend/apps/dashboard/views.py`：驾驶舱聚合接口实现：
  - `GET /api/v1/dashboard/overview/`
  - `GET /api/v1/dashboard/map-distribution/`
  - `GET /api/v1/dashboard/category-distribution/`
  - `GET /api/v1/dashboard/country-ranking/`
- `backend/apps/dashboard/urls.py`：驾驶舱路由定义。
- `backend/apps/dashboard/tests/test_views.py`：驾驶舱接口测试（鉴权、统计准确性、筛选/排序/limit）。

## memory-bank 文档职责
- `memory-bank/pre-prd.md`：需求原点（一句话）。
- `memory-bank/PRD.md`：产品目标、范围、模块与验收标准。
- `memory-bank/implementation-plan.md`：分阶段实施步骤与测试要点。
- `memory-bank/tech-stack.md`：技术选型基线。
- `memory-bank/IMPORT_REPORT.md`：数据源质量评估与导入策略。
- `memory-bank/terminology-api-alignment.md`：术语与 API 命名对齐规范。
- `memory-bank/progress.md`：阶段进展与验证记录。
- `memory-bank/architecture.md`：系统边界、数据关系、关键文件职责。

## 当前状态
- 已完成并验证：阶段 1~5、阶段 6.1~6.4。
- 未开始：阶段 7.1（接口文档生成）。

---
Last updated: 2026-02-25
