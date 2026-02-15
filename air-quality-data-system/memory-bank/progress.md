# 开发进度记录

## 当前状态（2026-02-15）
- 阶段一 `1.1` 到 `1.7` 已完成。
- 阶段二 `2.1` 未开始（按用户要求冻结，待下一次明确指令）。
- 当前可交付：后端 API、认证鉴权、导入链路、管理端能力、OpenAPI/Swagger 文档与 `API_DOCS.md`。

## 里程碑摘要
| 日期 | 阶段 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-15 | `1.1` 项目初始化 | 已完成 | Django 工程、MySQL 配置、DRF 基础组件就绪 |
| 2026-02-15 | `1.2` 数据模型设计 | 已完成 | accounts/airquality/rules/articles/logs 全部模型落地 |
| 2026-02-15 | `1.3` 数据导入功能 | 已完成 | 文件上传、导入任务、导入日志、批量入库 |
| 2026-02-15 | `1.4` 用户端 API | 已完成 | 概览、详情、历史、分析、防护、文章公告 |
| 2026-02-15 | `1.5` 管理端 API | 已完成 | 仪表盘、数据管理、规则、用户、内容、日志 |
| 2026-02-15 | `1.6` 认证与权限 | 已完成 | 登录/注册、Token 鉴权、管理端统一权限 |
| 2026-02-15 | `1.7` API 文档生成 | 已完成 | `/api/schema/`、`/api/docs/`、`API_DOCS.md` 导出 |

## 阶段一 `1.7` 详细记录
### 完成范围
- 完成 `1.7.1`：`drf-spectacular` 路由与配置完善，补齐视图文档说明。
- 完成 `1.7.2`：新增自动导出命令，生成 `API_DOCS.md` 和 `backend/openapi-schema.json`。

### 关键变更文件
- `backend/air_quality_system/urls.py`
- `backend/air_quality_system/settings.py`
- `backend/apps/accounts/views.py`
- `backend/apps/airquality/views.py`
- `backend/apps/rules/views.py`
- `backend/apps/articles/views.py`
- `backend/apps/logs/views.py`
- `backend/apps/airquality/management/commands/export_api_docs.py`
- `backend/apps/airquality/tests_api_docs.py`
- `API_DOCS.md`
- `backend/openapi-schema.json`

### 验证记录
- `python backend/manage.py check --settings=air_quality_system.settings_migrations`：通过。
- `python backend/manage.py test apps.airquality.tests_api_docs --settings=air_quality_system.settings_migrations`：通过。
- `python backend/manage.py export_api_docs --output API_DOCS.md --schema-json backend/openapi-schema.json --settings=air_quality_system.settings_migrations`：执行成功。
- 用户回归结果：通过。

### 给后续开发者的注意事项
- 文档导出以命令为准，避免手工维护不一致：
  - `python backend/manage.py export_api_docs --output API_DOCS.md --schema-json backend/openapi-schema.json --settings=air_quality_system.settings_migrations`
- 当前 `APIView` 中部分接口仍可能在生成 Schema 时提示 `unable to guess serializer` 警告；不阻断文档生成，但后续可继续细化 request/response serializer 提升文档精度。
- 在收到新的用户确认前，不进入阶段二 `2.1`。
