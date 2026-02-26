# Progress

## 2026-02-26

### 本次完成（阶段 8.1 ~ 8.4）
- 创建 Vue 3 + TypeScript 前端项目（使用 Vite）
- 安装并配置依赖：
  - vue-router（路由管理）
  - pinia（状态管理）
  - element-plus（UI 组件库）
  - @element-plus/icons-vue（图标库）
  - axios（HTTP 客户端）
  - echarts（图表库）
  - tailwindcss + @tailwindcss/postcss（样式工具）
- 配置 Element Plus 主题色（暖色调：橙色系 + 金色 + 青铜色）
- 配置 Tailwind CSS 和 PostCSS
- 创建项目目录结构：
  - `src/api/` - API 请求封装（auth, dashboard, heritage, inheritor, category, region）
  - `src/stores/` - Pinia 状态管理（user store）
  - `src/router/` - 路由配置（含路由守卫）
  - `src/views/` - 页面组件（Login + 占位页面）
  - `src/components/` - 公共组件
  - `src/utils/` - 工具函数（axios 拦截器）
  - `src/types/` - TypeScript 类型定义
- 实现路由守卫：
  - 认证检查（未登录跳转登录页）
  - 权限检查（非管理员无法访问管理页面）
- 创建 user store：管理用户信息和 token
- 实现 API 请求封装：
  - 请求拦截器（自动添加 Authorization header）
  - 响应拦截器（统一处理响应格式和错误）
  - 401 自动跳转登录页
- 创建登录页面（Login.vue）：
  - 使用 Element Plus 表单组件
  - 表单验证
  - 登录成功后保存 token 并跳转
- 配置 Vite 别名（@ 指向 src）
- 配置代理（/api 代理到后端 http://127.0.0.1:8000）

### 验证结果
- TypeScript 编译通过
- 前端项目构建成功（`npm run build`）
- 所有路由配置正确
- API 封装完整

### 当前状态
- 阶段 1~6、阶段 8.1 ~ 8.4 已完成并验证
- 阶段 7（后端接口文档）已完成
- 阶段 9.1（登录页面）已完成
- 待测试：前端开发服务器启动和登录功能

---

## 2026-02-25

### 本次完成（阶段 6.3 ~ 6.4）
- 新增类别占比接口 `GET /api/v1/dashboard/category-distribution/`（`backend/apps/dashboard/views.py`）。
- 返回字段：`category_name`、`heritage_count`、`percentage`；按数量降序；百分比总和校准为 100%。
- 新增国家排行接口 `GET /api/v1/dashboard/country-ranking/`（`backend/apps/dashboard/views.py`）。
- 返回字段：`rank`、`country_name`、`heritage_count`；默认 Top 20，支持 `limit` 参数。
- 更新路由：`backend/apps/dashboard/urls.py`。
- 补充测试：`backend/apps/dashboard/tests/test_views.py`（鉴权、排序、占比计算、`limit` 生效、Top 20 默认行为）。

### 验证结果
- 自动测试：`python manage.py test apps.dashboard.tests.test_views` 通过（10/10）。
- 用户手动测试阶段 6.3 ~ 6.4：通过。

### 当前状态
- 阶段 1~5、阶段 6.1 ~ 6.4 已完成并验证。
- 阶段 7.1 未开始。
