# 天猫潮玩电商数据采集系统 - 实施计划

## 项目概述

本项目采用 Django + DRF 后端、Vue 3 + Element Plus 前端的技术栈，实现天猫潮玩商品数据采集、存储与可视化分析。实施顺序为：后端开发 → 接口文档 → 前端开发 → 数据爬取与导入。

---

## 第一阶段：后端开发

### 步骤 1：项目初始化与配置

**任务描述**：
1. 创建 Django 5.2 项目，命名为 `backend`
2. 创建应用 `products`（商品管理）、`users`（用户管理）、`crawler`（爬虫管理）
3. 配置 MySQL 8.0 数据库连接（数据库名：`tmall_collecting`，字符集：`utf8mb4`）
4. 配置环境变量管理（数据库密码、密钥等敏感信息）
5. 配置 CORS 允许前端跨域访问
6. **安装 Celery + Redis**：
   - 安装依赖：`pip install celery redis django-celery-results`
   - 配置 Redis 为 Celery broker
7. 安装爬虫依赖：`pip install scrapy scrapy-playwright playwright-stealth`

**测试验证**：
- [ ] 运行 `python manage.py check` 无报错
- [ ] 确认能成功连接 MySQL 数据库（`python manage.py dbshell` 可正常进入）
- [ ] 确认 CORS 配置生效（使用 curl 测试 OPTIONS 请求返回 204）
- [ ] 确认 Redis 服务正常运行（`redis-cli ping` 返回 PONG）
- [ ] 确认 Celery Worker 能正常启动（`celery -A crawler worker`）

---

### 步骤 2：用户模块开发

**任务描述**：
1. 设计并创建 `users` 应用
2. 创建用户模型 `User`：
   - 用户名（唯一）
   - 密码（加密存储）
   - 邮箱
   - 角色（管理员/普通用户）
   - 状态（启用/冻结）
   - 创建时间、更新时间
3. 实现用户注册 API（`POST /api/users/register/`）
4. 实现用户登录 API（`POST /api/users/login/`）
5. 实现 JWT 认证（使用 `djangorestframework-simplejwt`）
6. 实现管理员用户管理 API（用户列表、冻结、解冻）

**测试验证**：
- [ ] 注册新用户后，检查数据库密码字段是否 bcrypt 加密
- [ ] 使用正确密码登录，返回 JWT Access Token 和 Refresh Token
- [ ] 访问需认证的 API 时，携带有效 Token 返回 200，无效 Token 返回 401
- [ ] 管理员可列出所有用户、冻结指定用户
- [ ] 冻结用户使用原密码登录返回 403

**接口文档**：
```
POST /api/users/register/
请求体：{"username": "test", "password": "123456", "email": "test@example.com"}
响应：{"code": 0, "message": "注册成功", "data": {"id": 1, "username": "test", "role": "user"}}

POST /api/users/login/
请求体：{"username": "test", "password": "123456"}
响应：{"code": 0, "message": "登录成功", "data": {"access_token": "xxx", "refresh_token": "xxx", "user": {...}}}

GET /api/users/
请求头：{"Authorization": "Bearer <token>"}
响应：{"code": 0, "data": [...]}
```

---

### 步骤 3：商品数据模块开发

**任务描述**：
1. 创建 `products` 应用
2. 设计并创建商品模型 `Product`：
   - 标题（商品名称）
   - 价格（Decimal 类型）
   - 销量（整数）
   - 店铺名称
   - 商品图片 URL
   - 商品详情页 URL
   - 品牌/类目（可选）
   - 采集批次号
   - 采集时间
   - 创建时间、更新时间
3. 创建采集日志模型 `CrawlLog`：
   - 任务 ID
   - 状态（进行中/成功/失败）
   - 采集来源（JSON API / Playwright 渲染）
   - 开始时间、结束时间
   - 日志内容
   - 采集数量
4. 实现商品 CRUD API（列表、查询、删除）
5. 实现商品搜索筛选 API（按标题、价格区间、店铺）
6. 实现商品导出功能（CSV 格式）

**测试验证**：
- [ ] 创建商品记录，验证价格 Decimal 类型存储正确
- [ ] 列表 API 支持分页（`page` 和 `page_size` 参数）
- [ ] 搜索 "高达"，返回标题包含"高达"的商品
- [ ] 价格区间筛选（如 50-200 元）返回正确结果
- [ ] 导出 API 返回正确的 CSV 文件头和内容

**接口文档**：
```
GET /api/products/
参数：page, page_size, search, min_price, max_price, shop
响应：{"code": 0, "data": [...], "total": 10000}

GET /api/products/{id}/
响应：{"code": 0, "data": {...}}

DELETE /api/products/{id}/
响应：{"code": 0, "message": "删除成功"}

GET /api/products/export/
参数：format=csv
响应：CSV 文件下载

GET /api/crawl-logs/
响应：{"code": 0, "data": [...]}
```

---

### 步骤 4：爬虫模块开发（优化版）

**任务描述**：
1. 创建 `crawler` 应用，集成 Scrapy + Playwright 框架：
   - 安装依赖：`pip install scrapy scrapy-playwright celery redis django-celery-results playwright-stealth`
   - 配置 Scrapy 项目结构（在 `crawler/spiders/` 下）
2. 配置 Celery + Redis 异步任务（强制使用，不可跳过）：
   - 配置 Redis 为消息 broker（`redis://localhost:6379/0`）
   - 配置 Celery 结果 backend
3. 实现爬虫 Spider（`TmallSpider`）：
   - **优先策略**：先用浏览器 DevTools 找到天猫内部 JSON API（如 `/search_product.json`），用 requests/httpx 直接请求 JSON（效率高 10 倍）
   - **Fallback 降级策略**：
     - **触发条件**：当 JSON API 返回非 200 状态码、返回非 JSON 格式、或关键数据字段为空时。
     - **自动切换**：捕获异常后自动切换至 Playwright 渲染模式（可通过环境变量 `ENABLE_FALLBACK=True` 控制）。
     - **来源记录**：在 `CrawlLog` 中记录 `source_type` ('json' 或 'playwright')。
   - 演示模式：限采集 2 页（约 20-40 条）
   - 全量模式：动态解析总页数，分批限速采集（每天限 1000 页，避免封禁）
4. 实现反爬机制：
   - **指纹伪装进阶**：
     - 组合使用 `playwright-extra` + `stealth` 插件。
     - **特征注入**：注入真实浏览器指纹（Canvas, WebGL, Fonts, AudioContext）。
     - **环境随机**：随机化 Viewport 大小、浏览器语言、时区设置。
     - **拟人操作**：模拟人类鼠标轨迹移动、随机滚动页面（使用 `PageMethod`）。
   - **代理池管理**：
     - **中间件**：推荐使用 `scrapy-rotating-proxies` 或 `scrapy-proxies`。
     - **数据源**：支持免费源（如 proxylist, free-proxy-list）及付费 API（Bright Data / Smartproxy / Oxylabs）。
     - **健康检查**：实现代理可用性检测，自动剔除失效代理。
   - **登录态管理（进阶）**：
     - 模拟登录流程并保存 Cookies/Local Storage。
     - 维护 Cookie 池/账号池，支持多账号轮换。
     - 实现 Session 失效自动重登机制。
   - **延迟随机**：每页随机等待 5-15 秒，模拟人类行为。
   - **UA 轮换**：随机 User-Agent 列表（手机/桌面端混用）。
   - **重试机制**：自动重试失败请求，切换代理。
5. 实现数据处理 Pipeline：
   - 数据清洗（去重、格式化价格、去除 HTML 标签）
   - 批量插入数据库（每 100 条批量写入，优化性能）
   - 日志记录（采集数量、失败记录）
6. 实现爬虫 API：
   - `POST /api/crawler/start/`：触发 Celery 任务，返回 task_id
   - `GET /api/crawler/status/{task_id}/`：查询任务状态。
     - **进度反馈**：Celery 任务每采集 50-100 条数据更新一次状态 (`update_state`)。
     - **返回字段**：`progress` (collected / estimated_total), `current_stage`, `items_collected`。
     - **前端轮询**：建议前端每 5-10 秒轮询一次。
7. 配置日志系统：Scrapy logger + Celery 结果存储

**测试验证**：
- [ ] 启动演示模式，返回任务 ID，任务状态从"进行中"变为"成功"
- [ ] 演示模式成功率 > 95%（连续测试 5 次）
- [ ] 检查数据库新增 20-40 条商品数据
- [ ] 验证新增数据价格字段为数字类型
- [ ] 验证爬虫日志正确记录每页抓取状态和数量
- [ ] 模拟封禁测试：确认代理切换机制工作
- [ ] 验证反爬伪装生效（使用 `about:blank` 页面检查 webdriver 特征）

**风险缓解措施**：
- 合规声明：仅用于学习研究，限制采集频率（每周最多一次全量采集）
- 备用方案：若天猫封禁严重，使用公开数据集或第三方数据服务

**接口文档**：
```
POST /api/crawler/start/
请求体：{"mode": "demo"}  // demo: 演示模式(2页), batch: 分批采集(每天1000页)
响应：{"code": 0, "message": "任务已启动", "task_id": "xxx"}

GET /api/crawler/status/{task_id}/
响应：{"code": 0, "data": {"status": "running", "progress": "50%", "items_collected": 500, "logs": [...]}}

GET /api/crawler/logs/
响应：{"code": 0, "data": [...]}
```

---

### 步骤 5：数据统计接口开发

**任务描述**：
1. 实现数据统计 API（用于前端图表展示）：
   - 商品总量统计
   - 价格区间分布统计（0-50, 50-200, 200-500, 500+）
   - 销量 Top 10 商品
   - 店铺/品牌商品数量排行
2. 实现历史价格趋势查询接口（按商品 ID）

**测试验证**：
- [ ] 价格分布返回正确分段数据，各分段总和等于商品总量
- [ ] 销量 Top 10 按销量降序排列
- [ ] 店铺排行按商品数量降序排列
- [ ] 响应时间 < 500ms

**接口文档**：
```
GET /api/statistics/overview/
响应：{"code": 0, "data": {"total_products": 10000, "total_shops": 500}}

GET /api/statistics/price-distribution/
响应：{"code": 0, "data": [{"range": "0-50", "count": 3000}, {"range": "50-200", "count": 4000}]}

GET /api/statistics/top-sales/
响应：{"code": 0, "data": [{"id": 1, "title": "...", "sales": 5000}, ...]}

GET /api/statistics/shop-ranking/
响应：{"code": 0, "data": [{"shop": "xxx", "count": 200}, ...]}

GET /api/products/{id}/price-history/
响应：{"code": 0, "data": [{"date": "2025-01-01", "price": 99}, ...]}
```

---

## 第二阶段：接口文档整理

### 步骤 6：API 接口文档整合

**任务描述**：
1. 整理所有 API 接口，使用 Markdown 格式编写完整文档
2. 文档包含：
   - 接口基础路径
   - 认证方式说明
   - 各接口详细说明（路径、方法、参数、响应示例）
   - 错误码说明
3. 提供 API 在线文档（可选：使用 DRF Spectacular 生成 OpenAPI 文档）

**测试验证**：
- [ ] 文档覆盖所有前端需要的接口
- [ ] 每个接口有完整的请求/响应示例
- [ ] 前端开发人员能根据文档独立完成对接

**输出文档**：
```
API 接口文档 (API.md)
├── 1. 认证相关
│   ├── POST /api/users/register/
│   └── POST /api/users/login/
├── 2. 用户管理
│   ├── GET /api/users/
│   ├── PUT /api/users/{id}/
│   └── POST /api/users/{id}/freeze/
├── 3. 商品管理
│   ├── GET /api/products/
│   ├── GET /api/products/{id}/
│   └── DELETE /api/products/{id}/
├── 4. 爬虫控制
│   ├── POST /api/crawler/start/
│   └── GET /api/crawler/status/{task_id}/
└── 5. 数据统计
    ├── GET /api/statistics/overview/
    ├── GET /api/statistics/price-distribution/
    └── GET /api/statistics/top-sales/
```

---

## 第三阶段：前端开发
> **MUST**: 前端开发使用 frontend-design skills 进行设计
### 步骤 7：前端项目初始化

**任务描述**：
1. 使用 Vite 创建 Vue 3 项目，命名为 `frontend`
2. 安装依赖：
   - Element Plus
   - Vue Router
   - Pinia
   - Axios
   - ECharts
   - Tailwind CSS
3. 配置项目路径别名（`@` 指向 `src`）
4. 配置开发服务器代理（API 请求转发到后端 8000 端口）
5. 配置 Tailwind CSS 基础样式

**测试验证**：
- [ ] 运行 `npm run dev`，浏览器访问 localhost:5173 显示欢迎页面
- [ ] Element Plus 组件正常渲染
- [ ] Axios 请求能正确代理到后端

---

### 步骤 8：公共组件开发

**任务描述**：
1. 开发登录/注册页面组件
2. 开发公共布局组件（侧边栏、顶部导航）
3. 开发权限指令/守卫（根据用户角色显示不同菜单）
4. 开发通用组件：
   - 分页组件
   - 表格组件
   - 图表容器组件（ECharts 封装）
   - Loading 加载组件
   - 消息提示组件

**测试验证**：
- [ ] 未登录访问任何页面重定向到登录页
- [ ] 普通用户访问管理端页面提示无权限
- [ ] 登录成功后跳转到对应角色仪表盘
- [ ] Loading 组件正确显示和隐藏

---

### 步骤 9：管理端页面开发

**任务描述**：
1. **系统仪表盘**：
   - 数据总量统计卡片
   - 价格分布饼图（ECharts）
   - 店铺占比柱状图
   - 系统运行状态
2. **数据采集控制台**：
   - "开始采集"按钮（支持演示/全量模式）
   - 日志滚动面板
   - 状态指示器
3. **商品数据管理**：
   - 商品列表表格（分页、搜索）
   - 编辑/删除功能
   - 批量导出按钮
4. **用户权限管理**：
   - 用户列表
   - 冻结/解冻操作
   - 重置密码功能
5. **个人中心**：
   - 头像上传
   - 密码修改
   - 资料编辑

**测试验证**：
- [ ] 仪表盘图表正确显示后端统计数据
- [ ] 点击"开始采集"显示日志面板，实时滚动
- [ ] 商品列表分页正确（切换页码数据更新）
- [ ] 搜索筛选返回正确结果
- [ ] 冻结用户后该用户无法登录
- [ ] 修改密码后需重新登录

---

### 步骤 10：用户端页面开发

**任务描述**：
1. **市场行情大屏**：
   - 销量 Top 10 榜单
   - 近期降价商品推荐
   - 热度趋势图
2. **商品资源库**：
   - 高级搜索（价格、品牌）
   - 商品卡片/列表展示
   - 分页控件
3. **商品详情页**：
   - 商品大图展示
   - 详细参数表格
   - 历史价格走势图
   - 店铺信息
   - 直达天猫链接
4. **个人中心**：
   - 查看个人信息
   - 修改密码

**测试验证**：
- [ ] 大屏展示实时数据图表
- [ ] 商品搜索按条件筛选正确
- [ ] 商品详情展示完整信息
- [ ] 点击历史价格显示正确趋势图
- [ ] 天猫链接可正确跳转

---

## 第四阶段：数据爬取与导入

### 步骤 11：预置数据准备

**任务描述**：
1. 确保系统数据库预置不少于 10,000 条真实有效的潮玩商品数据
2. 数据来源方案（**按优先级调整**）：
   - **方案 A（推荐）**：如有公开潮玩数据集（Kaggle/阿里云/ GitHub），优先批量导入 CSV
   - 方案 B：使用演示模式爬虫分批采集（每次 40 条，约 250 次）
   - 方案 C：使用分批采集模式（每天 1000 页，避免触发反爬）
3. 数据质量检查：
   - 标题不为空
   - 价格为有效数字
   - 销量为非负整数
   - 无完全重复数据（**按商品 ID 去重**，更可靠）

**测试验证**：
- [ ] 数据库商品总数 >= 10,000
- [ ] 随机抽取 100 条数据，无标题/价格为空的情况
- [ ] 验证去重后数据量变化（重复率 < 5%）
- [ ] 仪表盘图表基于 10,000+ 数据正确显示
- [ ] 若使用 CSV 导入，验证导入条数与文件行数一致

---

### 步骤 12：数据清洗与导入

**任务描述**：
1. 编写数据清洗脚本（使用 Pandas）：
   - 去除 HTML 标签
   - 统一价格格式（保留两位小数）
   - 处理缺失值（填充默认值或删除）
   - 去除重复商品（按标题+店铺+价格判断）
2. 批量导入历史数据到 MySQL
3. 创建数据库索引优化查询：
   - 标题全文索引
   - 店铺索引
   - 价格索引
   - 销量索引

**测试验证**：
- [ ] 清洗脚本处理 10,000 条数据无报错
- [ ] 清洗后数据质量检查通过
- [ ] 商品列表查询时间 < 1秒（首次加载）
- [ ] 价格区间筛选响应时间 < 500ms

---

### 步骤 13：系统联调测试

**任务描述**：
1. 前后端完整链路测试：
   - 登录 → 仪表盘 → 商品列表 → 详情页
   - 管理员登录 → 采集控制 → 日志查看
2. 性能测试：
   - 10,000 条数据列表页加载时间 < 1秒
   - 图表数据加载时间 < 2秒
   - 搜索响应时间 < 500ms
3. 稳定性测试：
   - 连续运行 24 小时无崩溃
   - 采集任务中断后能记录状态
4. 兼容性测试：
   - Chrome、Edge 浏览器显示正常
   - 页面响应式布局适配

**测试验证**：
| 测试项 | 预期结果 | 实际结果 | 通过/失败 |
|-------|---------|---------|----------|
| 登录流程 | 成功获取 Token | | |
| 商品列表分页 | 10,000 条分页正常 | | |
| 价格分布饼图 | 图表显示正确 | | |
| 销量 Top 10 | 排序正确 | | |
| 采集演示模式 | 新增 20-40 条数据 | | |
| 数据导出 | CSV 文件正确下载 | | |
| 浏览器兼容性 | Chrome/Edge 正常 | | |

---

## 实施检查清单

### 后端完成检查
- [ ] Django 项目结构创建
- [ ] MySQL 数据库连接配置
- [ ] Redis + Celery 异步任务配置
- [ ] 用户注册/登录 API
- [ ] JWT 认证中间件
- [ ] 商品 CRUD API
- [ ] 商品搜索筛选 API
- [ ] Scrapy + Playwright 爬虫框架集成
- [ ] 反爬机制配置（代理、UA轮换、延迟随机）
- [ ] 爬虫任务 API（Celery 异步）
- [ ] 数据统计 API
- [ ] API 文档编写完成

### 前端完成检查
- [ ] Vue 3 项目初始化
- [ ] Element Plus 集成
- [ ] Axios 请求封装
- [ ] 登录/注册页面
- [ ] 管理端仪表盘
- [ ] 爬虫控制台
- [ ] 商品管理页面
- [ ] 用户管理页面
- [ ] 用户端市场大屏
- [ ] 商品资源库
- [ ] 商品详情页

### 数据准备检查
- [ ] 预置数据 >= 10,000 条
- [ ] 数据质量检查通过
- [ ] 数据库索引创建
- [ ] 清洗脚本可用

### 联调测试检查
- [ ] 前后端 API 对接成功
- [ ] 性能指标达标
- [ ] 稳定性测试通过
- [ ] 浏览器兼容性通过

---

## 项目结构

```
tmall-collecting-platform/
├── backend/                    # Django 后端
│   ├── products/              # 商品管理应用
│   │   ├── models.py          # Product 模型
│   │   ├── serializers.py    # 序列化器
│   │   ├── views.py           # 视图函数
│   │   └── urls.py            # 路由配置
│   ├── users/                 # 用户管理应用
│   │   ├── models.py          # User 模型
│   │   ├── views.py           # 认证视图
│   │   └── urls.py            # 路由配置
│   ├── crawler/               # 爬虫应用
│   │   ├── tasks.py           # Celery 爬虫任务
│   │   ├── spiders/           # Scrapy 爬虫脚本
│   │   │   ├── __init__.py
│   │   │   └── tmall_spider.py # 天猫商品爬虫
│   │   ├── pipelines.py        # 数据处理管道
│   │   ├── middlewares.py     # Scrapy 中间件（代理、重试）
│   │   └── logs.py            # 日志模型
│   ├── tmall_project/        # Django 项目配置
│   ├── celery.py             # Celery 配置
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/              # API 接口封装
│   │   ├── components/       # 公共组件
│   │   ├── views/            # 页面组件
│   │   │   ├── admin/        # 管理端页面
│   │   │   └── user/        # 用户端页面
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── router/           # Vue Router 配置
│   │   └── utils/           # 工具函数
│   ├── package.json
│   └── vite.config.js
│
├── sql/
│   └── init_db.sql           # 数据库初始化脚本
│
├── API.md                     # 接口文档
└── IMPLEMENTATION_PLAN.md    # 本实施计划

**关键技术依赖**：
```
# backend/requirements.txt
Django>=5.2
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
mysqlclient>=2.2
python-dotenv>=1.0
celery>=5.4
redis>=5.0
django-celery-results>=2.5
scrapy>=2.11
scrapy-playwright>=0.1
playwright-stealth>=1.0
scrapy-rotating-proxies>=0.6
pandas>=2.0
httpx>=0.27
```
