# 开发进度记录

## 当前状态（2026-02-15）
- 阶段一 `1.1` 到 `1.7` 已完成。
- 阶段二 `2.1`、`2.2` 已完成并通过测试。
- 阶段二 `2.3` 未开始（待用户确认）。
- 当前可交付：后端 API、认证鉴权、导入链路、管理端能力、OpenAPI/Swagger 文档与 `API_DOCS.md`、前端路由与状态管理、登录注册页面。

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
| 2026-02-15 | `2.1` 前端项目初始化 | 已完成 | Vue 3 + Vite 项目、依赖安装、API 请求基础配置 |
| 2026-02-15 | `2.2` 路由与状态管理 | 已完成 | Vue Router 路由守卫、Pinia 状态管理、登录注册页面 |

---

## 阶段二 `2.2` 详细记录

### 完成范围
- 完成 `2.2.1`：配置路由结构（用户端 8 个路由、管理端 7 个路由、认证路由）。
- 完成 `2.2.2`：配置 Pinia 状态管理（user/city/admin 三个 store）。
- 额外完成：登录/注册页面完整实现、布局组件（UserLayout/AdminLayout）、所有页面占位组件。

### 关键变更文件
- `frontend/src/router/index.js`：路由配置与导航守卫
  - 用户端路由：overview、city、station、historical、analysis、protection、knowledge、article
  - 管理端路由：dashboard、data-import、air-quality、rules、users、articles、logs
  - 认证路由：login、register
  - 导航守卫：requiresAuth 检查、requiresAdmin 检查、登录后跳转逻辑
- `frontend/src/stores/user.js`：用户状态管理
  - State：token、userInfo、isLoggedIn、isAdmin、userId、username
  - Actions：setUser、clearUser、updateUser
  - 持久化：localStorage
- `frontend/src/stores/city.js`：城市选择状态
- `frontend/src/stores/admin.js`：管理端 UI 状态
- `frontend/src/main.js`：Pinia 注册
- `frontend/src/layouts/UserLayout.vue`：用户端布局
- `frontend/src/layouts/AdminLayout.vue`：管理端布局
- `frontend/src/views/auth/Login.vue`：登录页（完整实现）
- `frontend/src/views/auth/Register.vue`：注册页（完整实现）
- `frontend/src/views/user/`：用户端页面占位组件（8 个）
- `frontend/src/views/admin/`：管理端页面占位组件（7 个）

### 验证记录
- `cd frontend && npm run dev`：开发服务器启动成功
- 用户验证结果：通过（路由跳转正常、未登录访问管理端被拦截、登录后跳转正确、状态持久化生效）

### 给后续开发者的注意事项
- 路由守卫已实现：未登录访问管理端自动跳转登录页
- 登录后跳转逻辑：管理员跳转 `/admin`，普通用户跳转 `/`
- 已登录用户访问登录/注册页自动跳转对应首页
- 用户状态使用 localStorage 持久化，刷新页面后保持登录状态
- 登录/注册页面已完整实现，包含表单验证和 API 调用
- 其余页面组件当前为占位状态，待后续开发（阶段二 2.3-2.6）

---

## 阶段二 `2.1` 详细记录

### 完成范围
- 完成 `2.1.1`：创建 Vue 3 项目结构，配置 Vite 构建工具。
- 完成 `2.1.2`：安装核心依赖（Vue Router、Pinia、Axios、Element Plus、ECharts、Tailwind CSS），配置按需引入。
- 完成 `2.1.3`：配置 API 请求基础（Axios 封装、拦截器、错误处理）。
- 额外完成：路由配置与导航守卫、Pinia 状态管理（user/city/admin）、布局组件（UserLayout/AdminLayout）、所有页面占位组件。

### 关键变更文件
- `frontend/package.json`：依赖清单（Vue 3.5.13、Vue Router 4.5.0、Pinia 2.3.0、Element Plus 2.9.1、ECharts 5.6.0、Tailwind CSS 3.4.17）
- `frontend/vite.config.js`：Vite 配置（别名、Element Plus 按需引入、API 代理）
- `frontend/tailwind.config.js`：Tailwind CSS 配置
- `frontend/postcss.config.js`：PostCSS 配置
- `frontend/index.html`：HTML 模板
- `frontend/src/main.js`：应用入口
- `frontend/src/App.vue`：根组件
- `frontend/src/style.css`：全局样式
- `frontend/src/utils/request.js`：Axios 封装（请求/响应拦截器、统一错误处理、token 自动添加、401 自动跳转）
- `frontend/src/router/index.js`：路由配置（用户端、管理端、认证路由）与导航守卫（权限校验、登录状态校验）
- `frontend/src/stores/user.js`：用户状态（登录状态、用户信息、token、角色判断）
- `frontend/src/stores/city.js`：城市选择状态
- `frontend/src/stores/admin.js`：管理端 UI 状态
- `frontend/src/api/auth.js`：认证接口（login、register、logout）
- `frontend/src/api/airquality.js`：空气质量数据接口（概览、详情、历史、分析、防护、文章）
- `frontend/src/api/admin.js`：管理端接口（仪表盘、导入、数据、规则、用户、文章、日志）
- `frontend/src/layouts/UserLayout.vue`：用户端布局（顶部导航、页脚）
- `frontend/src/layouts/AdminLayout.vue`：管理端布局（侧边栏、顶部栏）
- `frontend/src/views/auth/Login.vue`：登录页（已实现完整功能）
- `frontend/src/views/auth/Register.vue`：注册页（已实现完整功能）
- `frontend/src/views/user/`：用户端页面占位组件（Overview、CityDetail、StationDetail、HistoricalData、Analysis、ProtectionGuide、KnowledgeBase、ArticleDetail）
- `frontend/src/views/admin/`：管理端页面占位组件（Dashboard、DataImport、AirQualityManage、RulesManage、UsersManage、ArticlesManage、SystemLogs）
- `frontend/README.md`：前端项目结构说明

### 验证记录
- `cd frontend && npm install`：依赖安装成功（188 个包）
- `cd frontend && npm run dev`：开发服务器启动成功（默认端口 5173，被占用时自动切换）
- 用户验证结果：通过（路由跳转正常、登录注册页面可正常使用、权限拦截生效）

### 给后续开发者的注意事项
- 前端开发服务器默认运行在 http://localhost:5173，`/api` 路径会被代理到后端 http://127.0.0.1:8000。
- Element Plus 使用自动按需引入，无需手动注册组件和 API。
- 所有 API 请求统一通过 `src/utils/request.js` 发起，自动处理 token 和错误响应。
- 路由守卫已实现：未登录访问管理端自动跳转登录页、已登录访问登录/注册页自动跳转首页。
- 登录/注册页面已完整实现，可直接使用。
- 其余页面组件当前为占位状态，待后续开发（阶段二 2.3-2.6）。

---

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
