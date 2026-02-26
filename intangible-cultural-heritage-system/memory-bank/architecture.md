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

## 前端关键文件职责
- `frontend/src/main.ts`：应用入口，注册 Vue Router、Pinia、Element Plus。
- `frontend/src/App.vue`：根组件，渲染路由视图。
- `frontend/vite.config.ts`：Vite 配置（路径别名、代理设置）。
- `frontend/tailwind.config.js`：Tailwind CSS 主题配置（暖色调）。
- `frontend/postcss.config.js`：PostCSS 配置（Tailwind + Autoprefixer）。
- `frontend/src/style.css`：全局样式（Element Plus 主题定制、滚动条样式）。
- `frontend/src/router/index.ts`：路由配置与守卫（认证检查、权限检查）。
- `frontend/src/stores/user.ts`：用户状态管理（登录、登出、token 管理）。
- `frontend/src/utils/request.ts`：Axios 封装（请求/响应拦截器、错误处理）。
- `frontend/src/types/index.ts`：全局 TypeScript 类型定义。
- `frontend/src/api/`：API 请求封装模块：
  - `auth.ts`：认证接口（登录、刷新、登出、获取用户信息）
  - `dashboard.ts`：驾驶舱接口（总览、地图分布、类别占比、国家排行）
  - `heritage.ts`：非遗项目 CRUD 接口
  - `inheritor.ts`：传承人 CRUD 接口
  - `category.ts`：分类管理接口
  - `region.ts`：地区管理接口
- `frontend/src/views/`：页面组件：
  - `Login.vue`：登录页面（表单验证、token 保存）
  - `Dashboard.vue`：驾驶舱页面（待开发）
  - `HeritageList.vue`：非遗项目列表（待开发）
  - `HeritageDetail.vue`：非遗项目详情（待开发）
  - `InheritorList.vue`：传承人列表（待开发）
  - `NotFound.vue`：404 页面
  - `admin/`：管理页面（待开发）

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
- 已完成并验证：阶段 1~6、阶段 8.1~8.4。
- 阶段 7（后端接口文档）已完成。
- 阶段 9.1（登录页面）已完成。
- 待开发：阶段 9.2~9.3（主布局、API 拦截器已完成）、阶段 10（驾驶舱页面）。

---
Last updated: 2026-02-26
