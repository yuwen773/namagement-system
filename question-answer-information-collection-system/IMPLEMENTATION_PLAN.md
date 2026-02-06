# 网络问答平台信息采集系统 - 实施计划

本文档为 AI 开发者提供逐步实施指南，遵循"后端优先、前端后行、数据最后"的开发顺序。

---

## 第一阶段：项目初始化与后端基础架构

### 步骤 1：初始化 Django 项目结构

**目标**：创建符合本项目规范的后端项目结构

**操作步骤**：
1. 在项目根目录创建 `backend` 文件夹
2. 使用 `django-admin startproject qa_project .` 创建主项目
3. 使用 `python manage.py startapp accounts` 创建用户认证应用
4. 使用 `python manage.py startapp crawler` 创建爬虫应用
5. 使用 `python manage.py startapp api` 创建接口应用
6. 创建 `backend/apps/` 目录，统一管理各应用

**验证方法**：
- 运行 `python manage.py runserver` 确认项目启动无报错
- 访问 `http://127.0.0.1:8000/admin/` 能看到 Django admin 登录页

---

### 步骤 2：配置 MySQL 数据库连接

**目标**：建立与 MySQL 8.0+ 的稳定连接

**操作步骤**：
1. 安装 MySQL 驱动：`pip install mysqlclient` 或 `pymysql`
2. 安装 Redis 驱动：`pip install redis`（用于 Celery broker）
3. 在 `settings.py` 中配置 DATABASES：
   - 设置 ENGINE 为 `django.db.backends.mysql`
   - 配置 NAME 为 `qa_database`
   - 配置 USER、PASSWORD、HOST、PORT
4. 配置 TIME_ZONE 为 `Asia/Shanghai`
5. 配置 LANGUAGE_CODE 为 `zh-hans`

**验证方法**：
- 执行 `python manage.py check` 无数据库相关错误
- 执行 `python manage.py migrate` 成功创建系统表

---

### 步骤 3：配置 Django REST Framework 和 API 文档

**目标**：建立 API 框架基础，自动生成 Swagger 文档

**操作步骤**：
1. 安装依赖：`pip install djangorestframework django-cors-headers drf-spectacular`
2. 在 `INSTALLED_APPS` 添加：
   - `rest_framework`
   - `rest_framework_simplejwt`
   - `corsheaders`
   - `drf_spectacular`
3. 在 `MIDDLEWARE` 添加 `corsheaders.middleware.CorsMiddleware`（置于顶部）
4. 配置 CORS_ALLOW_ALL_ORIGINS = True（开发环境）
5. 在 `settings.py` 配置 REST_FRAMEWORK：
   - DEFAULT_AUTHENTICATION_CLASSES 添加 JWTAuthentication
   - DEFAULT_PERMISSION_CLASSES
   - DEFAULT_PAGINATION_CLASS
   - PAGE_SIZE = 20
   - DEFAULT_SCHEMA_CLASS = 'drf_spectacular.openapi.AutoSchema'
6. 配置 drf_spectacular：
   - SERVE_INCLUDE_SCHEMA = False
   - SCHEMA_SETTINGS 项配置

**验证方法**：
- 访问 `http://127.0.0.1:8000/api/schema/swagger-ui/` 能看到 Swagger UI
- 点击接口能展开详情，参数说明完整

---

## 第二阶段：用户认证模块（后端）

### 步骤 4：设计并创建用户模型

**目标**：建立符合项目需求的用户数据模型

**操作步骤**：
1. 在 `accounts/models.py` 创建 `User` 模型（继承 AbstractUser）
2. 添加字段：
   - username（用户名，唯一）
   - password（密码，明文存储，按 PRD 要求）
   - role（角色字段：'admin' / 'user'，使用 choices 约束）
   - is_active（状态标志）
3. 在 `admin.py` 注册模型，配置 list_display 和搜索字段
4. 创建迁移文件并执行

**验证方法**：
- 执行 `python manage.py makemigrations` 和 `migrate` 成功
- 登录 Django Admin，创建管理员账号：`python manage.py createsuperuser`
- 在 Admin 中能正常创建、编辑、删除用户

---

### 步骤 5：创建用户认证 API

**目标**：提供登录、注册、登出接口

**操作步骤**：
1. 在 `accounts/serializers.py` 创建 `UserSerializer`：
   - 包含 username、role 字段
   - password 为 write_only
2. 在 `accounts/views.py` 创建视图：
   - `RegisterView`: POST 创建新用户
   - `UserDetailView`: GET 获取当前用户信息
   - `UserListView`: GET 列出所有用户（仅管理员）
3. 在 `accounts/urls.py` 定义路由：
   - `POST /api/auth/register/`
   - `GET /api/auth/users/`（管理员）
   - `GET/PUT/PATCH/DELETE /api/auth/users/<id>/`（管理员）
   - `GET /api/auth/me/`
   - `PUT/PATCH /api/auth/me/`（修改个人信息）
4. 配置路由保护（IsAuthenticated、IsAdminUser）

**API 响应格式要求**：
```
成功：{ "code": 0, "data": {...}, "message": "..." }
失败：{ "code": 400/401/403/404, "message": "错误描述", "data": null }
```

**验证方法**：
- 使用 Postman 或 curl 测试：
  - POST 注册新用户，返回 201 状态码
  - GET 获取用户列表（无 Token 返回 401）
  - 使用管理员 Token 能获取所有用户
  - 普通用户 Token 只能获取自己信息

---

### 步骤 6：实现 JWT 认证

**目标**：为 API 添加 Token 认证

**操作步骤**：
1. 安装 `djangorestframework-simplejwt`
2. 在 `settings.py` 配置：
   - DEFAULT_AUTHENTICATION_CLASSES 添加 JWTAuthentication
   - 配置 SIMPLE_JWT：
     - ACCESS_TOKEN_LIFETIME = timedelta(hours=2)
     - REFRESH_TOKEN_LIFETIME = timedelta(days=7)
     - AUTH_HEADER_TYPES = ('Bearer',)
3. 在 `accounts/urls.py` 添加路由：
   - `POST /api/auth/login/`（获取 Token）
   - `POST /api/auth/logout/`（刷新 Token Blacklist）
4. 创建自定义 Token 响应序列化器，返回用户信息

**验证方法**：
- POST /api/auth/login/ 传入正确用户名密码，返回 access 和 refresh Token
- 使用 access Token 访问需要认证的接口，成功返回数据
- 使用过期 Token 访问，返回 401 错误

---

## 第三阶段：爬虫模块（后端）

### 步骤 7：设计问答数据模型和标签模型

**目标**：建立采集数据的存储结构

**操作步骤**：
1. 在 `crawler/models.py` 创建 `Tag` 模型：
   - name（标签名，唯一）
   - created_at
2. 在 `crawler/models.py` 创建 `Question` 模型：
   - title（问题标题）
   - description（问题描述，可为空）
   - answer_content（回答内容）
   - answer_time（回答时间）
   - answerer（回答者，可为空）
   - tags（ManyToMany 关联 Tag，便于按标签查询）
   - source_url（来源链接）
   - created_at（入库时间）
   - updated_at（更新时间）
3. 添加联合唯一约束：`unique_together = (title, source_url)` 防止重复
4. 添加索引：在 title、created_at、answerer 上创建数据库索引
5. 在 `admin.py` 注册模型，配置 list_display 和搜索
6. 创建迁移文件并执行

**验证方法**：
- 执行迁移成功
- 在 Django Admin 能创建、编辑、删除问答记录
- 检查数据库表结构，确认索引和联合唯一约束已创建
- 测试标签关联功能正常

---

### 步骤 8：实现数据清洗工具（Pipeline）

**目标**：确保入库数据质量，集成到 Scrapy Pipeline

**操作步骤**：
1. 在 `crawler/utils.py` 创建 `DataCleaner` 类：
   - `clean_html()`: 使用 lxml/parsel 移除 HTML 标签
   - `remove_duplicates()`: 基于 title 或 source_url 判断重复
   - `normalize_text()`: 处理特殊字符、空格、换行
   - `validate_data()`: 验证必填字段
2. 在 `crawler/pipelines.py` 创建 QuestionPipeline：
   - 实现 `process_item()` 方法调用 DataCleaner
   - 实现 `open_spider()` 和 `close_spider()` 生命周期方法
   - 使用 Django ORM 批量插入优化（每 100 条批量写入）

**验证方法**：
- 测试输入含 HTML 标签的内容，输出纯文本
- 测试重复数据能被正确识别（MySQL 唯一约束触发）
- 测试空值和边界情况处理
- 批量插入性能测试：1000 条数据 < 5 秒

---

### 步骤 9：实现 360问答 爬虫脚本（混合模式：JSON API + Playwright）

**目标**：构建高可用、高效率的混合爬虫系统，优先使用 API，具备反爬对抗能力

**操作步骤**：
1. 安装依赖：
   ```
   pip install scrapy scrapy-playwright scrapy-rotating-proxies 2captcha-python httpx
   playwright install
   pip install scrapy-stealth
   ```
2. 创建 `crawler/items.py` 定义 QuestionItem
3. 创建 `crawler/spiders/wenda_spider.py`：
   - **优先策略**：使用 `httpx` 尝试调用隐藏 JSON API（如 `/api/search.json`），效率比渲染页高 10 倍
   - **降级策略**：若 API 失效或加密，自动切换至 Playwright 浏览器渲染模式
   - 实现 `start_requests()`：支持从 Redis 读取断点（last_page/last_id）
   - 实现 `parse()`：处理 JSON 响应或 HTML 结构
   - 登录模拟（可选）：若需查看完整回答，使用 Playwright 模拟登录并 `save_state()` 保存 Cookie
4. 配置 `crawler/settings.py`：
   - **代理增强**：集成付费代理（如 Bright Data）或免费池，编写 Middleware 在使用前 ping/test 代理可用性
   - **验证码处理**：集成 `2captcha` 服务，当检测到验证码时自动调用 API 识别
   - 配置 User-Agent 旋转列表
   - 配置请求延迟（DOWNLOAD_DELAY = 3-8 秒随机）
   - 配置重试次数（RETRY_TIMES = 5）
   - 启用 scrapy-stealth 中间件
5. 添加 robots.txt 检查（ROBOTSTXT_OBEY = True）
6. 配置限频：每小时不超过 5000 条请求

**反爬增强策略**：
- **API 优先**：最大化利用 JSON 接口，减少浏览器特征暴露
- **智能代理池**：设置失败阈值，自动剔除失效代理，保留高分代理
- **行为模拟**：Playwright 模式下增加随机点击、鼠标轨迹、页面滚动
- **验证码熔断**：如果验证码绕过失败率 > 20%，暂停任务并发送报警

**验证方法**：
- 抓包分析 360 问答 API 接口，验证 JSON 数据结构
- 运行 `scrapy crawl wenda_360 -o output.json` 测试采集 20 条
- 模拟 API 封禁，验证是否自动降级为 Playwright 模式
- 模拟高频访问触发验证码，验证 2Captcha 自动处理流程
- 验证采集速度：演示采集（20条）应在 1 分钟内完成（API 模式）

---

### 步骤 10：配置 Celery 异步任务与断点续传

**目标**：实现可靠的异步采集任务，支持断点续传和实时进度反馈

**操作步骤**：
1. 安装 Celery 和 Redis：`pip install celery django-celery-results`
2. 配置 `qa_project/celery.py`：
   - 创建 Celery 实例，配置 broker/backend 为 Redis
   - 设置时区为 Asia/Shanghai
   - 配置 `CELERY_TASK_TRACK_STARTED = True`
3. 在 `settings.py` 添加 celery 配置
4. 创建 `crawler/tasks.py`：
   - 增加 `--resume` 参数支持
   - 细粒度进度更新：每采集 50 条调用 `self.update_state()`
   ```python
   @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
   def run_spider(self, mode='demo', limit=20, resume=False):
       # 逻辑伪代码
       # 1. 构造 Scrapy 命令参数
       # 2. 监听 Scrapy 信号或通过 Pipeline 更新 Redis 进度 key
       # 3. 周期性读取 Redis 进度并 update_state
       return {'status': 'completed', 'collected': limit}
   ```
5. 增强日志记录：在 `update_state` 中包含 timestamp、current_page、failed_count

**验证方法**：
- 启动 Celery Worker：`celery -A qa_project worker -l info`
- 启动任务运行 1 分钟后强制中断（Ctrl+C 或 kill）
- 重新触发任务（带 resume=True），确认从中断处继续采集（检查 Redis 记录的 last_id）
- 前端轮询状态 API，确认进度条平滑更新（如 "30%" -> "35%"）
- 检查 Celery 结果后端，确认包含详细的执行日志

---

### 步骤 11：创建爬虫状态 API（Celery 集成）

**目标**：提供前端调用的爬虫控制接口，实时反馈状态

**操作步骤**：
1. 创建 `CrawlerTask` 模型（存储 task_id、状态、进度、结果）
2. 创建 `CrawlerStatusView`：
   - `GET /api/crawler/status/`：获取当前任务状态
   - `POST /api/crawler/start/`：触发 Celery 任务，返回 task_id
   - `POST /api/crawler/stop/`：终止爬虫任务
   - `GET /api/crawler/logs/<task_id>/`：获取实时日志
3. 配置限流：普通用户不能调用爬虫接口
4. 添加合规检查：记录采集频率，超限返回警告

**API 响应示例**：
```json
{
  "task_id": "abc123",
  "status": "running",
  "progress": 45,
  "collected": 9000,
  "total": 10000
}
```

**验证方法**：
- POST /api/crawler/start/ 返回 task_id
- GET /api/crawler/status/ 返回实时进度
- 任务完成返回最终统计
- 非管理员调用返回 403 错误
- 限频检查生效

---

## 第四阶段：数据管理 API

### 步骤 12：创建问答数据 API 接口

**目标**：提供数据的增删改查接口

**操作步骤**：
1. 在 `api/serializers.py` 创建 `QuestionSerializer`：
   - 定义所有字段
   - read_only_fields（created_at、updated_at）
2. 在 `api/views.py` 创建 `QuestionViewSet`：
   - 使用 `ModelViewSet`
   - 添加过滤：title 模糊搜索（SearchFilter）
   - 添加排序：created_at 降序
   - 配置分页：PageNumberPagination
3. 在 `api/urls.py` 注册 ViewSet：
   - `/api/questions/`
   - `/api/questions/<id>/`
4. 添加权限：所有用户可查看，管理员可删除

**API 响应格式**：
```json
{
  "code": 0,
  "data": [...],
  "total": 10000,
  "page": 1,
  "page_size": 20
}
```

**验证方法**：
- GET /api/questions/ 返回分页数据
- GET /api/questions/?search=关键词 能过滤数据
- 管理员 DELETE /api/questions/1/ 删除成功
- 普通用户 DELETE 返回 403

---

### 步骤 13：创建统计分析 API

**目标**：为前端可视化提供数据接口

**操作步骤**：
1. 创建 `StatisticsView` 包含以下接口：
   - `GET /api/statistics/trend/`：每日问答数量趋势
   - `GET /api/statistics/tags/`：标签词频统计（前 50）
   - `GET /api/statistics/answerers/`：高频回答者排名（前 20）
2. 使用 Django ORM 聚合查询：
   - `Count()`、`Sum()`、`Group By`
   - `TruncDate()` 按日期分组
3. 返回格式与前端 ECharts 兼容

**验证方法**：
- 各接口返回数据格式正确
- 在数据库有 10000+ 条数据时，响应时间 < 2 秒
- 返回空数据时格式仍然正确

---

## 第五阶段：前端基础架构

### 步骤 14：初始化 Vue 3 前端项目

**目标**：建立前端项目结构

**操作步骤**：
1. 使用 Vite 创建项目：`npm create vite@latest frontend -- --template vue`
2. 安装依赖：
   - `npm install element-plus echarts vue-router pinia axios @vueuse/core`
   - `npm install -D tailwindcss postcss autoprefixer`
   - `初始化 Tailwind：npx tailwindcss init -p`
3. 配置 `vite.config.js`：
   - 设置代理：`/api` 转发到后端
   - 配置路径别名 `@`
4. 配置 `tailwind.config.js`：
   - 添加 content 路径
   - 自定义主题色（与后端风格一致）

**验证方法**：
- 运行 `npm run dev` 启动开发服务器
- 访问 `http://localhost:5173/` 能看到欢迎页
- Element Plus 组件能正常显示

---

### 步骤 15：配置前端路由

**目标**：建立 SPA 路由结构

**操作步骤**：
1. 创建 `router/index.js`：
   - 配置路由表（Login、Dashboard、DataCenter、Users、Profile）
   - 设置路由元信息 `meta: { requiresAuth, roles }`
2. 创建视图组件占位文件：
   - `views/Login.vue`
   - `views/Dashboard.vue`
   - `views/DataCenter.vue`
   - `views/UserManagement.vue`
   - `views/Profile.vue`
3. 创建 `router/permission.js` 路由守卫：
   - 未登录跳转 /login
   - 普通用户访问 /users 返回 403
4. 配置路由懒加载

**验证方法**：
- 未登录访问 /dashboard 跳转 /login
- 登录后访问 /login 跳转 /dashboard
- 各路由能正常切换

---

### 步骤 16：配置前端状态管理

**目标**：建立全局状态管理

**操作步骤**：
1. 创建 `stores/auth.js`：
   - user 信息
   - token 存储（localStorage）
   - login、logout、fetchUser 方法
2. 创建 `stores/app.js`：
   - sidebar 状态
   - 全局配置
3. 在 `main.js` 注册 Pinia

**验证方法**：
- 登录后刷新页面，用户信息不丢失
- 退出登录后，用户信息和 Token 清除

---

## 第六阶段：前端页面开发

### 步骤 17：开发登录页面

**目标**：实现用户登录功能

**操作步骤**：
1. 在 `views/Login.vue` 实现：
   - Element Plus `el-form` 绑定数据
   - 表单验证（用户名、密码必填）
   - 登录按钮调用后端 API
   - 成功后保存 Token，跳转 Dashboard
   - 错误提示使用 `ElMessage`
   - 添加登录 loading 状态防止重复提交
2. 添加路由跳转参数处理（redirect）

**验证方法**：
- 输入正确账号密码，登录成功，跳转 Dashboard
- 输入错误密码，显示错误提示
- 回车键能触发表单提交
- 登录时按钮显示 loading，结束后消失

---

### 步骤 17a：配置前端 API 请求拦截

**目标**：统一处理 Token 和错误响应

**操作步骤**：
1. 创建 `utils/request.js` 配置 Axios 实例：
   - 请求拦截器添加 Authorization Header
   - 响应拦截器统一处理错误
2. 创建 `utils/auth.js` 处理 Token 存储：
   - getToken() / setToken() / removeToken()
   - Token 过期检测，自动跳转登录
3. 配置全局错误处理

**验证方法**：
- Token 自动附加到请求头
- 401 错误自动跳转登录页
- 网络错误有统一提示

---

### 步骤 18：开发仪表盘页面

**目标**：展示统计图表和爬虫控制

**操作步骤**：
1. 创建 `views/Dashboard.vue`：
   - 获取统计 API 数据
   - 使用 ECharts 展示三个图表：
     - 词云图（热门标签）
     - 折线图（问答趋势）
     - 柱状图（高频回答者）
   - 管理员角色显示爬虫控制卡片：
     - "开始爬取"按钮
     - 爬虫状态显示（空闲/运行中/已完成）
     - 进度条显示采集进度
2. 图表组件封装（`components/ECharts.vue`）：
   - 实现 `onMounted()` 初始化图表
   - 实现 `onUnmounted()` 销毁图表（防止内存泄漏）
   - **关键**：添加 `window.addEventListener('resize', handler)` 监听窗口大小变化
   - 调用 `chart.resize()` 自适应容器大小
3. 图表数据为空时显示友好提示
4. 添加骨架屏 Loading 状态

**ECharts 组件优化**：
```javascript
// 组件关键代码
import * as echarts from 'echarts'
const chartRef = ref(null)
let chartInstance = null

onMounted(() => {
  chartInstance = echarts.init(chartRef.value)
  // 绑定 resize 事件
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})

const handleResize = () => chartInstance?.resize()
```

**验证方法**：
- 图表正常渲染，数据正确显示
- 调整浏览器窗口大小，图表自动适应
- 管理员能看到爬虫控制卡片和进度
- 普通用户不显示爬虫控制卡片
- 点击"开始爬取"按钮显示 loading 状态
- 切换路由后无内存泄漏（控制台无警告）

---

### 步骤 19：开发数据中心页面

**目标**：展示和管理问答数据

**操作步骤**：
1. 创建 `views/DataCenter.vue`：
   - Element Plus `el-table` 展示数据列表
   - 分页组件（el-pagination）
   - 搜索框：按标题关键词筛选（防抖 300ms）
   - 管理员显示操作列（删除按钮）
   - 添加表格 loading 状态
2. 实现详情查看：
   - 点击行或按钮弹出 `el-dialog`
   - 显示完整的问题和回答内容
   - 使用 `el-skeleton` 加载详情数据
3. **大数据量优化**：
   - 安装 `el-table-virtual-scroll` 或使用 Element Plus 内置虚拟滚动
   - 配置 `max-height` 固定表格区域
   - 虚拟滚动支持大数据量渲染

**虚拟滚动配置**：
```html
<el-table-virtual-scroll
  :data="tableData"
  :item-size="60"
  :height="400"
  key="id"
>
  <el-table-column prop="title" label="标题" />
  <!-- 其他列 -->
</el-table-virtual-scroll>
```

**优化策略**：
- 后端分页 + 前端虚拟滚动（滚动条平滑）
- 节流搜索输入（防抖 300ms）
- 表格列固定（左侧固定标题，右侧固定操作列）

**验证方法**：
- 数据列表分页正常
- 搜索关键词能正确过滤（带防抖）
- 详情弹窗显示完整内容
- 管理员能删除记录
- 10000+ 数据时滚动流畅，无卡顿
- 表格切换列宽不抖动

---

### 步骤 20：开发个人中心页面

**目标**：用户个人信息管理

**操作步骤**：
1. 创建 `views/Profile.vue`：
   - 显示当前用户信息（用户名、角色）
   - 修改密码表单：
     - 旧密码、新密码、确认密码
     - 表单验证（两次密码一致）
2. 调用后端 API 更新密码
3. 密码修改成功后退出登录

**验证方法**：
- 显示当前用户信息
- 输入正确旧密码和新密码，修改成功
- 新旧密码一致验证生效
- 修改后退出登录，需重新登录

---

### 步骤 21：开发用户管理页面

**目标**：管理员管理所有用户

**操作步骤**：
1. 创建 `views/UserManagement.vue`：
   - `el-table` 展示用户列表
   - 搜索用户功能
   - 添加用户按钮（弹出表单对话框）
   - 编辑用户按钮
   - 删除用户按钮（确认对话框）
2. 表单字段：用户名、角色、密码
3. 调用后端用户 API

**验证方法**：
- 管理员能看到所有用户列表
- 能添加新用户
- 能编辑用户信息
- 能删除用户（删除后从列表移除）
- 普通用户访问返回 403

---

## 第七阶段：数据爬取与导入

### 步骤 22：执行演示数据采集

**目标**：快速采集演示数据（20条）

**操作步骤**：
1. 运行命令：`python manage.py crawl --mode=demo`
2. 监控采集进度和日志
3. 采集完成后检查数据完整性

**验证方法**：
- 命令执行成功，无报错
- 数据库中有 20 条新的问答数据
- 数据字段完整，无明显缺失

---

### 步骤 23：执行全量数据采集

**目标**：采集不少于 10000 条有效数据

**操作步骤**：
1. 运行命令：`python manage.py crawl --mode=full --limit=15000`
2. 若任务中断，使用 `python manage.py crawl --mode=full --limit=15000 --resume` 继续采集
3. 设置采集间隔（建议 1 秒）避免被封禁
4. 分批执行（如每批 2000 条），配合 Redis 断点记录确保数据不丢失
5. 监控错误日志，处理异常情况

**验证方法**：
- 数据库中至少有 10000 条数据
- 数据字段完整率达 95% 以上
- 检查数据库索引是否正常工作

---

### 步骤 24：数据质量检查

**目标**：确保入库数据质量

**操作步骤**：
1. 编写 SQL 检查脚本：
   - 统计空值率
   - 统计重复数据
   - 验证时间范围
2. 清理异常数据：
   - 删除重复记录
   - 补充或标记缺失数据
3. 生成数据质量报告

**验证方法**：
- 无 HTML 标签残留
- 重复数据 < 1%
- 所有数据都有有效标题

---

### 步骤 25：性能测试

**目标**：验证系统能处理 10000+ 数据

**操作步骤**：
1. 使用 JMeter 或 Locust 进行压力测试：
   - 模拟 50 并发用户访问数据列表
   - 模拟 20 并发用户访问统计 API
2. 测试场景：
   - 首次加载仪表盘（< 3 秒）
   - 搜索关键词（< 1 秒）
   - 分页切换（< 500ms）
3. 记录测试报告

**验证方法**：
- API 响应时间达标
- 无内存泄漏
- 数据库查询有索引支持

---

## 第八阶段：部署与交付

### 步骤 26：配置 Docker Compose 环境

**目标**：使用 Docker Compose 一键部署所有服务

**操作步骤**：
1. 创建 `Dockerfile.backend`：Django + Gunicorn 环境
2. 创建 `Dockerfile.frontend`：Node.js 构建环境
3. 创建 `docker-compose.yml`：
   - 后端服务（django）
   - Redis 服务（Celery Broker）
   - Celery Worker 服务
   - MySQL 服务
   - Nginx 服务（前端静态文件 + API 代理）
4. 配置 `Dockerfile` 多阶段构建（前端）
5. 创建 `.env` 环境变量模板：
   - 数据库密码
   - Redis 密码
   - Django SECRET_KEY

**docker-compose.yml 示例**：
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine

  backend:
    build: ./backend
    depends_on:
      - mysql
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
    command: gunicorn qa_project.wsgi:application --bind 0.0.0.0:8000

  celery:
    build: ./backend
    depends_on:
      - redis
    command: celery -A qa_project worker -l info

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend

volumes:
  mysql_data:
```

**验证方法**：
- 执行 `docker-compose up -d` 所有服务启动成功
- 访问 `http://localhost` 能看到前端页面
- API 接口正常响应
- `docker-compose ps` 显示所有服务 running

---

### 步骤 27：后端生产环境配置

**目标**：配置生产环境后端

**操作步骤**：
1. 安装 gunicorn：`pip install gunicorn`
2. 创建 `start.sh` 启动脚本
3. 配置环境变量：
   - SECRET_KEY（随机生成，复杂字符串）
   - DEBUG=False
   - ALLOWED_HOSTS（前端域名）
   - 数据库生产配置（Docker 或独立 MySQL）
4. 配置静态文件收集

**验证方法**：
- 使用 gunicorn 能正常启动
- 静态文件正确收集
- DEBUG=False 时安全性配置正确

---

### 步骤 28：前端生产构建

**目标**：生成生产环境前端文件

**操作步骤**：
1. 配置 `.env.production`：
   - VITE_API_BASE_URL=生产环境 API 地址
2. 运行 `npm run build`
3. 检查生成文件：
   - `dist/index.html`
   - `dist/assets/`（JS、CSS 文件）
4. 部署到 Nginx 或静态托管

**验证方法**：
- 构建无错误
- 资源文件大小合理
- 前端能正确调用生产环境 API

---

### 步骤 29：生成初始化数据脚本

**目标**：快速复现数据库环境

**操作步骤**：
1. 创建 `scripts/seed_data.py`：
   - 包含爬虫采集逻辑
   - 支持断点续传（使用 Redis 记录进度）
   - 记录采集进度和错误日志
2. 创建 `sql/init_db.sql`：
   - 数据库创建语句
   - 表结构定义
   - 初始管理员账号
   - 示例数据
3. 配置合规检查：
   - 遵守 robots.txt
   - 限频（每小时 < 5000 条）
   - 添加 User-Agent 标识

**验证方法**：
- 执行脚本能完整重建数据库
- 新环境有 10000+ 数据
- 断点续传测试：中断后重新运行能从断点继续

---

## 验收清单

### 功能验收
- [ ] 用户能注册、登录、登出
- [ ] 管理员能启动爬虫采集数据
- [ ] 所有用户能查看数据列表
- [ ] 所有用户能搜索数据
- [ ] 管理员能删除数据
- [ ] 仪表盘显示统计图表
- [ ] 管理员能管理系统用户
- [ ] 用户能修改密码

### 数据验收
- [ ] 数据库有 10000+ 条有效数据
- [ ] 数据字段完整
- [ ] 无 HTML 标签残留
- [ ] 无重复数据（联合唯一约束生效）

### 性能验收
- [ ] 数据列表加载 < 2 秒
- [ ] 搜索响应 < 1 秒
- [ ] 图表渲染 < 3 秒
- [ ] 支持 50 并发用户
- [ ] 爬虫成功率 > 90%（15000 条目标）
- [ ] 虚拟滚动表格滚动流畅（10000+ 数据）

### 安全验收
- [ ] 未登录无法访问受保护页面
- [ ] 普通用户无法调用爬虫 API
- [ ] 普通用户无法访问用户管理页面
- [ ] Token 过期处理正确

### 部署验收
- [ ] Docker Compose 一键部署成功
- [ ] Nginx 代理配置正确
- [ ] Celery Worker 正常运行
- [ ] Swagger API 文档可访问

---

## 注意事项

1. **严格遵循项目规范**：使用中文字段名，API 响应格式为 `{ code, data, total }`
2. **不重复造轮子**：优先使用 Django、DRF、Element Plus 提供的功能
3. **后端优先**：前端开发前确保所有 API 接口已测试通过
4. **数据最后**：数据采集是收尾工作，前端功能完善后再执行
5. **测试驱动**：每个步骤都应有对应的测试验证
6. **文档同步**：接口文档随开发同步更新
7. **合规要求**：
   - 遵守目标网站 robots.txt
   - 限频采集（每小时 < 5000 条）
   - 添加标识性的 User-Agent
   - 添加服务条款免责声明
