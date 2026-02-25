# 非物质文化遗产数据可视化系统 - 实施计划

## 文档说明
- **目标读者**: AI 开发者（Claude Code）
- **实施原则**: 先后端完整开发 → 提供接口文档 → 前端开发
- **复用原则**: 参考 `Enterprise-HRMS` 和 `canteen-management-system` 的现有实现，避免重复造轮子

---

## 阶段一：后端基础架构搭建

### 步骤 1.1：创建 Django 项目结构
**指示**:
1. 在项目根目录创建 `backend/` 文件夹
2. 在 `backend/` 下创建 Django 项目 `heritage_system`
3. 创建以下 apps 目录结构：
   - `apps/users/` - 用户认证与权限
   - `apps/heritage/` - 非遗项目管理
   - `apps/inheritors/` - 传承人管理
   - `apps/categories/` - 分类字典管理
   - `apps/regions/` - 地理区域管理
   - `apps/importer/` - 数据导入处理
   - `apps/dashboard/` - 驾驶舱统计
4. 创建 `utils/` 目录用于通用工具（JWT、权限类、响应格式化）
5. 创建 `media/` 和 `logs/` 目录

**测试验证**:
- 执行 `python manage.py runserver` 确保项目启动无报错
- 访问 http://127.0.0.1:8000/ 能看到 Django 默认页面
- 执行 `python manage.py check` 无错误输出

---

### 步骤 1.2：配置 MySQL 数据库连接
**指示**:
1. 修改 `heritage_system/settings.py` 中的数据库配置
2. 数据库名称：`heritage_db`
3. 使用 MySQL 8.0+，端口 3306，字符集 UTF8MB4
4. 参考 `Enterprise-HRMS/backend/HRMS/settings.py` 的配置格式
5. 添加时区设置 `TIME_ZONE = 'Asia/Shanghai'`

**测试验证**:
- 执行 `python manage.py dbshell` 能成功连接数据库
- 在数据库中创建 `heritage_db` 数据库
- 执行 `python manage.py migrate`（初始状态）生成 auth 等基础表

---

### 步骤 1.3：安装并配置依赖包
**指示**:
1. 创建 `requirements.txt`，包含以下依赖：
   - Django 5.2
   - djangorestframework
   - djangorestframework-simplejwt
   - mysqlclient
   - pandas
   - openpyxl
   - Pillow
   - django-cors-headers
2. 安装依赖：`pip install -r requirements.txt`
3. 在 `settings.py` 的 `INSTALLED_APPS` 中注册：
   - `rest_framework`
   - `rest_framework_simplejwt.token_blacklist`
   - `corsheaders`
   - 各个自定义 app

**测试验证**:
- 执行 `pip list` 确认所有包已安装
- 执行 `python manage.py check` 无配置错误

---

### 步骤 1.4：创建数据库初始化脚本
**指示**:
1. 在项目根目录创建 `sql/` 目录
2. 创建 `sql/init_db.sql` 脚本，包含：
   - 创建数据库 `heritage_db`
   - 创建初始管理员用户（INSERT INTO auth_user 或使用自定义用户表）
   - 创建基础分类数据（国家级、省级、市县级类别）
   - 创建基础地区数据（部分常用国家）
3. 脚本应包含事务处理和回滚机制

**测试验证**:
- 执行 `mysql -u root -p < sql/init_db.sql` 成功
- 登录数据库确认表和数据已创建
- 能使用管理员账号登录（后续步骤验证）

---

## 阶段二：用户认证与权限模块

### 步骤 2.1：创建用户模型与权限系统
**指示**:
1. 在 `apps/users/models.py` 创建扩展用户模型（如需要）或直接使用 Django User
2. 添加 role 字段：`USER_ROLE = [('admin', '管理员'), ('user', '普通用户')]`
3. 参考 `Enterprise-HRMS/backend/apps/users/` 的权限实现
4. 创建 `permissions.py` 定义权限类：
   - `IsAdmin` - 仅管理员
   - `IsAdminOrReadOnly` - 管理员可写，用户只读
5. 在 `settings.py` 配置 REST_FRAMEWORK 权限默认设置

**测试验证**:
- 执行 `python manage.py makemigrations users && python manage.py migrate`
- Django Admin 后台能看到用户模型
- 创建测试用户验证 role 字段正常工作

---

### 步骤 2.2：实现 JWT 登录接口
**指示**:
1. 在 `apps/users/` 创建 `serializers.py` 定义登录序列化器
2. 创建 `views.py` 实现登录视图（基于 `obtain_jwt_token` 或自定义）
3. 配置 JWT 过期时间：Access Token 2小时，Refresh Token 7天
4. 在 `urls.py` 配置路由：
   - `POST /api/v1/auth/login/` - 登录获取 token
   - `POST /api/v1/auth/refresh/` - 刷新 token
   - `POST /api/v1/auth/logout/` - 登出（加入黑名单）
5. 配置 CORS 允许前端跨域访问

**测试验证**:
- 使用 Postman/curl 测试登录接口
- 验证返回格式包含 `access` 和 `refresh` token
- 使用 access token 访问受保护接口成功
- 过期 token 返回 401 错误
- refresh token 能成功刷新获取新 access token

**预期 API 响应格式**:
```json
POST /api/v1/auth/login/
请求体: { "username": "admin", "password": "password" }
成功响应 (200):
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
}
失败响应 (401):
{
  "code": 1,
  "message": "用户名或密码错误",
  "data": null
}
```

---

### 步骤 2.3：创建通用响应格式化工具
**指示**:
1. 在 `utils/` 创建 `response.py` 定义统一响应格式
2. 参考 Enterprise-HRMS 的响应格式：`{ code: 0, data: {...}, total: n }`
3. code 值约定：0 表示成功，非 0 表示失败
4. 创建自定义异常处理器

**测试验证**:
- 创建测试接口验证响应格式
- 列表接口返回包含 total 字段
- 错误接口返回正确的 code 和 message

---

## 阶段三：核心数据模型

### 步骤 3.1：创建分类和地区模型
**指示**:
1. 在 `apps/categories/models.py` 创建：
   - `Category` 模型：id, name, code, level, parent_id, created_at, updated_at
   - level 字段：国家级、省级、市县级
2. 在 `apps/regions/models.py` 创建：
   - `Region` 模型：id, country_code, country_name, latitude, longitude, continent
   - 添加 ISO-3166 标准国家代码映射
3. 为两个模型创建 admin 注册

**测试验证**:
- 执行 makemigrations 和 migrate 成功
- Django Admin 能管理分类和地区
- 创建测试数据验证字段约束

---

### 步骤 3.2：创建非遗项目模型
**指示**:
1. 在 `apps/heritage/models.py` 创建 `HeritageItem` 模型
2. 必填字段：id, name（名称）, category（外键分类）, level（级别）, region（外键地区）
3. 可选字段：area（地区）, protection_unit（保护单位）, description（简介）, created_at, updated_at
4. level 选项：国家级、省级、市县级
5. 添加索引：name, category, region

**测试验证**:
- 执行 makemigrations 和 migrate 成功
- 创建测试数据验证外键关联
- 验证必填字段的 NOT NULL 约束

---

### 步骤 3.3：创建传承人模型
**指示**:
1. 在 `apps/inheritors/models.py` 创建 `Inheritor` 模型
2. 必填字段：id, name（姓名）, heritage_item（外键非遗项目）, region（外键地区）
3. 可选字段：gender（性别）, level（级别）, area（地区）, description（简介）, created_at, updated_at
4. 添加索引：name, heritage_item
5. 添加唯一约束：同一项目下传承人姓名唯一

**测试验证**:
- 执行 makemigrations 和 migrate 成功
- 验证与 HeritageItem 的外键关联
- 测试唯一约束（同项目同名传承人应报错）

---

### 步骤 3.4：创建导入任务和错误日志模型
**指示**:
1. 在 `apps/importer/models.py` 创建 `ImportJob` 模型：
   - 字段：id, file_name, status, total_rows, success_count, error_count, created_by, created_at
   - status 选项：pending, processing, completed, failed
2. 创建 `ImportError` 模型：
   - 字段：id, import_job（外键）, row_number, field_name, error_message, raw_data
3. 添加索引：status, created_by

**测试验证**:
- 执行 makemigrations 和 migrate 成功
- 验证 ImportJob 和 ImportError 的关联关系
- 创建测试导入任务记录

---

## 阶段四：核心业务 CRUD 接口

### 步骤 4.1：非遗项目 CRUD 接口
**指示**:
1. 在 `apps/heritage/serializers.py` 创建序列化器
2. 在 `apps/heritage/views.py` 创建 ModelViewSet
3. 权限控制：admin 完整 CRUD，user 仅 GET
4. 配置路由：`/api/v1/heritage/`
5. 支持筛选：category, level, region, name（模糊搜索）
6. 支持分页：每页 20 条

**测试验证**:
- POST 创建项目（admin）成功
- GET 列表返回正确格式和分页
- GET 详情返回完整数据
- PUT 更新（admin）成功
- DELETE 删除（admin）成功
- user 角色 POST/PUT/DELETE 返回 403
- 筛选参数生效（?category=1&level=national）

**预期 API 响应格式**:
```
GET /api/v1/heritage/
成功响应 (200):
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "name": "京剧",
      "category": {"id": 1, "name": "传统戏剧"},
      "level": "national",
      "region": {"id": 1, "country_name": "中国"},
      "area": "北京",
      "protection_unit": "中国京剧研究院",
      "description": "中国国粹..."
    }
  ],
  "total": 1
}
```

---

### 步骤 4.2：传承人 CRUD 接口
**指示**:
1. 在 `apps/inheritors/` 创建 serializers, views, urls
2. ModelViewSet 配置与heritage相同
3. 关联序列化：返回时包含关联的heritage_item信息
4. 支持筛选：name, level, region, heritage_item
5. 支持分页

**测试验证**:
- CRUD 四个操作完整测试
- 关联数据正确返回（heritage_item 包含 name 字段）
- 筛选参数生效
- 权限控制正确

---

### 步骤 4.3：分类字典管理接口
**指示**:
1. 在 `apps/categories/` 创建 serializers, views, urls
2. 支持树形结构查询（parent_id 关联）
3. 添加 `@action` 获取树形结构接口：`/api/v1/categories/tree/`
4. 仅 admin 可增删改，所有用户可查看

**测试验证**:
- 获取列表成功
- 获取树形结构正确显示层级关系
- admin 增删改成功
- user 增删改返回 403

---

### 步骤 4.4：地区管理接口
**指示**:
1. 在 `apps/regions/` 创建 serializers, views, urls
2. 基础 CRUD
3. 添加搜索功能：按国家名称或代码搜索
4. 仅 admin 可编辑

**测试验证**:
- CRUD 完整测试
- 搜索功能正常（?search=China）

---

## 阶段五：数据导入模块

### 步骤 5.1：创建文件上传接口
**指示**:
1. 在 `apps/importer/views.py` 创建上传视图
2. 支持 Excel (.xlsx) 和 CSV (.csv) 格式
3. 文件保存到 `media/uploads/` 目录
4. 返回文件 ID 用于后续处理
5. 限制文件大小（最大 10MB）
6. 路由：`POST /api/v1/importer/upload/`

**测试验证**:
- 上传 Excel 文件成功，返回文件 ID
- 上传 CSV 文件成功
- 超过大小限制返回错误
- 不支持的格式返回错误

---

### 步骤 5.2：实现数据解析服务
**指示**:
1. 在 `apps/importer/services.py` 创建解析服务类
2. 使用 pandas 读取 Excel/CSV
3. 验证必需列：项目表需 name, category, level, country
4. 验证数据类型和格式
5. 返回解析结果：成功行数、失败行数、错误详情

**测试验证**:
- 解析有效数据文件成功
- 缺失必需列时返回错误
- 数据类型不正确时标记错误行
- 返回结构化的错误报告

---

### 步骤 5.3：实现数据清洗与增强
**指示**:
1. 创建数据清洗服务
2. 清洗规则：
   - 去除字段首尾空格
   - 全半角转换
   - 国家名称标准化（映射到 ISO-3166）
   - 空值处理
3. 增强规则：
   - 根据国家名称自动补全经纬度（查询 Region 表）
   - 根据类别名称自动匹配 Category
   - 根据级别名称映射到标准值
4. 无法匹配的行标记为错误

**测试验证**:
- 输入包含空格的数据能正确清洗
- 能识别并映射标准国家名称
- 能自动补全经纬度
- 无法匹配的数据正确标记错误

---

### 步骤 5.4：实现批量导入事务处理
**指示**:
1. 创建导入服务类
2. 使用数据库事务确保原子性
3. 批处理策略：每 100 条提交一次
4. 记录导入日志（ImportJob）
5. 记录错误详情（ImportError）
6. 支持异步导入（使用 Celery 或后台线程，首版可选）

**测试验证**:
- 导入 100 条数据全部成功
- 部分失败场景：成功行入库，失败行不入库
- 全失败场景：数据库无变化
- ImportError 正确记录所有错误
- ImportJob 状态正确更新

---

### 步骤 5.5：导入查询和错误下载接口
**指示**:
1. 创建导入任务列表接口：`GET /api/v1/importer/jobs/`
2. 创建导入详情接口：`GET /api/v1/importer/jobs/{id}/`
3. 创建错误下载接口：`GET /api/v1/importer/jobs/{id}/errors/`
4. 错误下载返回 CSV 格式错误报告

**测试验证**:
- 导入任务列表正确分页显示
- 导入详情包含统计信息
- 错误下载返回可读的 CSV 文件
- 仅 admin 可访问

**预期 API 响应格式**:
```
GET /api/v1/importer/jobs/
成功响应 (200):
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "file_name": "heritage_data.xlsx",
      "status": "completed",
      "total_rows": 1000,
      "success_count": 950,
      "error_count": 50,
      "created_at": "2026-02-25T10:00:00Z"
    }
  ],
  "total": 1
}
```

---

## 阶段六：驾驶舱统计接口

### 步骤 6.1：总览统计接口
**指示**:
1. 在 `apps/dashboard/views.py` 创建总览视图
2. 路由：`GET /api/v1/dashboard/overview/`
3. 返回数据：
   - 项目总数
   - 传承人总数
   - 分类总数
   - 覆盖国家数
4. 使用数据库聚合查询优化性能

**测试验证**:
- 接口返回四个统计数据
- 数据与数据库实际值一致
- 响应时间 < 100ms（1000 条数据以内）

**预期 API 响应格式**:
```
GET /api/v1/dashboard/overview/
成功响应 (200):
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "heritage_count": 1200,
    "inheritor_count": 3500,
    "category_count": 10,
    "country_count": 50
  }
}
```

---

### 步骤 6.2：地图分布接口
**指示**:
1. 创建地图分布视图
2. 路由：`GET /api/v1/dashboard/map-distribution/`
3. 返回数据：
   - 国家代码
   - 国家名称
   - 经度
   - 纬度
   - 项目数量
   - 传承人数量
4. 支持按类别筛选

**测试验证**:
- 返回所有有数据的国家
- 经纬度数据正确
- 数值统计准确
- 筛选参数生效

**预期 API 响应格式**:
```
GET /api/v1/dashboard/map-distribution/
成功响应 (200):
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "country_code": "CN",
      "country_name": "中国",
      "longitude": 104.1954,
      "latitude": 35.8617,
      "heritage_count": 800,
      "inheritor_count": 2500
    },
    {
      "country_code": "JP",
      "country_name": "日本",
      "longitude": 138.2529,
      "latitude": 36.2048,
      "heritage_count": 200,
      "inheritor_count": 500
    }
  ]
}
```

---

### 步骤 6.3：类别占比接口
**指示**:
1. 创建类别占比视图
2. 路由：`GET /api/v1/dashboard/category-distribution/`
3. 返回数据：
   - 分类名称
   - 项目数量
   - 占比（百分比）
4. 按数量降序排列

**测试验证**:
- 返回所有分类的统计数据
- 占比计算正确（总和 100%）
- 排序正确

---

### 步骤 6.4：国家排行接口
**指示**:
1. 创建国家排行视图
2. 路由：`GET /api/v1/dashboard/country-ranking/`
3. 返回数据：
   - 排名
   - 国家名称
   - 项目数量
4. 默认 Top 20，支持 limit 参数

**测试验证**:
- 返回 Top 20 国家
- 按项目数量降序
- limit 参数生效

---

## 阶段七：后端接口文档生成

### 步骤 7.1：生成接口文档
**指示**:
1. 安装 drf-spectacular 或 drf-yasg
2. 在 settings.py 配置文档生成
3. 配置接口描述和标签
4. 访问 `/api/docs/` 或 `/api/swagger/` 查看文档

**测试验证**:
- 文档页面可访问
- 所有接口都在文档中列出
- 请求/响应示例正确显示

---

### 步骤 7.2：编写接口文档（Markdown）
**指示**:
1. 在项目根目录创建 `docs/api-reference.md`
2. 包含所有接口的详细说明：
   - 请求方法和路径
   - 请求参数
   - 响应格式
   - 错误码说明
3. 添加认证说明（JWT Bearer Token）
4. 添加权限说明（admin/user）

**测试验证**:
- 文档完整覆盖所有接口
- 示例代码可直接使用
- 前端开发者能根据文档完成对接

---

### 步骤 7.3：创建 Postman Collection
**指示**:
1. 导出 Postman Collection JSON
2. 包含所有接口
3. 配置环境变量（base_url, token）
4. 添加示例请求

**测试验证**:
- 导入 Postman 后能正常使用
- 所有接口请求成功
- 环境变量正确配置

---

## 阶段八：前端项目搭建

### 步骤 8.1：创建 Vue 3 项目
**指示**:
1. 在项目根目录创建 `frontend/` 文件夹
2. 使用 Vite 创建 Vue 3 + TypeScript 项目
3. 安装依赖：
   - vue-router
   - pinia
   - element-plus
   - axios
   - echarts
   - @element-plus/icons-vue
4. 配置 Vite 别名：@ 指向 src

**测试验证**:
- `npm run dev` 启动开发服务器
- 访问 http://localhost:5173 能看到默认页面
- TypeScript 编译无错误

---

### 步骤 8.2：配置 Element Plus 和 Tailwind CSS
**指示**:
1. 在 `main.ts` 全局注册 Element Plus
2. 配置 Element Plus 主题色（参考 canteen-management-system 暖色调）
3. 安装并配置 Tailwind CSS
4. 创建全局样式文件

**测试验证**:
- Element Plus 组件能正常显示
- Tailwind CSS 类名生效
- 样式无冲突

---

### 步骤 8.3：创建目录结构和基础组件
**指示**:
1. 创建目录结构：
   - `src/api/` - API 请求封装
   - `src/stores/` - Pinia 状态管理
   - `src/router/` - 路由配置
   - `src/views/` - 页面组件
   - `src/components/` - 公共组件
   - `src/utils/` - 工具函数
   - `src/types/` - TypeScript 类型定义
2. 创建 API 请求封装（axios instance、拦截器）
3. 创建全局类型定义文件

**测试验证**:
- 目录结构清晰
- API 封装能发送请求
- 类型定义完整

---

### 步骤 8.4：实现路由和状态管理
**指示**:
1. 配置路由：
   - /login - 登录页
   - /dashboard - 驾驶舱（需要认证）
   - /heritage - 项目列表
   - /inheritors - 传承人列表
   - /admin/* - 管理功能（需要 admin 权限）
2. 实现路由守卫：检查登录状态和权限
3. 创建 user store：管理用户信息和 token

**测试验证**:
- 未登录访问受保护路由跳转登录页
- 登录后能访问受保护路由
- admin 能访问管理页面，user 不能

---

## 阶段九：前端认证与布局

### 步骤 9.1：实现登录页面
**指示**:
1. 创建 `views/Login.vue`
2. 使用 Element Plus 表单组件
3. 表单字段：用户名、密码
4. 表单验证：非空、长度限制
5. 登录成功后保存 token 到 localStorage
6. 登录成功后跳转到 dashboard

**测试验证**:
- 页面显示正常
- 表单验证生效
- 登录成功跳转
- 登录失败显示错误提示
- token 正确保存

---

### 步骤 9.2：创建主布局组件
**指示**:
1. 创建 `layouts/MainLayout.vue`
2. 包含顶部导航栏（Logo、用户信息、退出按钮）
3. 包含侧边栏菜单（根据角色显示）
4. 包含内容区域
5. 使用 Element Plus Layout 组件

**测试验证**:
- 布局显示正确
- 菜单根据角色显示
- 退出按钮清除 token 并跳转登录页

---

### 步骤 9.3：实现 API 拦截器
**指示**:
1. 在 axios instance 添加请求拦截器：自动添加 Authorization header
2. 添加响应拦截器：处理统一响应格式
3. 处理 401 错误：自动跳转登录页
4. 处理其他错误：显示错误提示

**测试验证**:
- 请求自动携带 token
- 401 自动跳转登录页
- 错误提示正确显示

---

## 阶段十：驾驶舱页面

### 步骤 10.1：创建驾驶舱布局
**指示**:
1. 创建 `views/Dashboard.vue`
2. 使用 Grid 布局分为四个区域：
   - 顶部统计卡片（4 个）
   - 左侧地图（大图）
   - 右上类别占比饼图
   - 右下国家排行条形图
3. 添加筛选器（类别、级别）

**测试验证**:
- 页面布局正确
- 响应式适配

---

### 步骤 10.2：实现统计卡片
**指示**:
1. 创建 `components/StatCard.vue`
2. 显示标题、数值、图标
3. 从 API 获取数据
4. 添加数字滚动动画

**测试验证**:
- 卡片显示正确
- 数据与 API 一致
- 动画流畅

---

### 步骤 10.3：实现世界地图
**指示**:
1. 使用 ECharts 地图组件
2. 注册世界地图（使用 ECharts 地图数据）
3. 根据项目数量渲染热力图或散点图
4. 点击国家显示详情弹窗
5. 添加缩放和拖拽功能

**测试验证**:
- 地图正确渲染
- 数据点显示正确
- 点击交互正常
- 缩放拖拽流畅
- 组件卸载时正确 dispose（防止内存泄漏）

---

### 步骤 10.4：实现类别占比饼图
**指示**:
1. 使用 ECharts 饼图
2. 从 API 获取数据
3. 添加图例和百分比标签
4. 点击扇区筛选列表

**测试验证**:
- 饼图正确显示
- 数据准确
- 交互正常
- 组件卸载时正确 dispose

---

### 步骤 10.5：实现国家排行条形图
**指示**:
1. 使用 ECharts 条形图（横向柱状图）
2. 显示 Top 20 国家
3. 添加数值标签
4. 点击条形筛选列表

**测试验证**:
- 条形图正确显示
- 排序正确
- 交互正常
- 组件卸载时正确 dispose

---

## 阶段十一：数据列表页面

### 步骤 11.1：项目列表页面
**指示**:
1. 创建 `views/HeritageList.vue`
2. 包含筛选表单（类别、级别、国家、关键词）
3. 使用 Element Plus Table 显示数据
4. 支持分页
5. 点击行查看详情

**测试验证**:
- 列表数据正确显示
- 筛选功能正常
- 分页功能正常
- 详情跳转正确

---

### 步骤 11.2：项目详情页面
**指示**:
1. 创建 `views/HeritageDetail.vue`
2. 显示项目完整信息
3. 显示关联的传承人列表
4. 添加返回按钮

**测试验证**:
- 详情信息完整
- 关联数据正确显示
- 返回功能正常

---

### 步骤 11.3：传承人列表页面
**指示**:
1. 创建 `views/InheritorList.vue`
2. 类似项目列表的布局
3. 筛选字段：姓名、级别、国家、所属项目
4. 表格显示传承人信息

**测试验证**:
- 列表数据正确显示
- 筛选功能正常
- 分页功能正常

---

## 阶段十二：管理功能页面

### 步骤 12.1：项目管理页面
**指示**:
1. 创建 `views/admin/HeritageManage.vue`
2. 仅 admin 角色可访问
3. 包含 CRUD 操作：
   - 新增按钮打开对话框
   - 编辑按钮打开对话框
   - 删除按钮二次确认
4. 表单验证
5. 操作成功/失败提示

**测试验证**:
- admin 能访问，user 不能
- 新增成功
- 编辑成功
- 删除成功并有确认提示
- 表单验证生效

---

### 步骤 12.2：传承人管理页面
**指示**:
1. 创建 `views/admin/InheritorManage.vue`
2. 类似项目管理页面
3. 所属项目使用下拉选择
4. 其他 CRUD 功能完整

**测试验证**:
- CRUD 功能完整
- 项目下拉选择正确
- 权限控制正确

---

### 步骤 12.3：分类字典管理
**指示**:
1. 创建 `views/admin/CategoryManage.vue`
2. 树形表格显示分类
3. 支持拖拽排序（可选）
4. 增删改功能

**测试验证**:
- 树形结构正确显示
- CRUD 功能正常

---

### 步骤 12.4：数据导入页面
**指示**:
1. 创建 `views/admin/DataImport.vue`
2. 包含文件上传组件（Element Plus Upload）
3. 上传后显示预览
4. 执行导入按钮
5. 显示导入进度
6. 导入完成后显示结果统计
7. 错误数据可下载

**测试验证**:
- 文件上传成功
- 预览数据正确
- 导入进度显示
- 完成后统计正确
- 错误下载正常

---

### 步骤 12.5：导入记录页面
**指示**:
1. 创建 `views/admin/ImportHistory.vue`
2. 显示历史导入记录
3. 包含状态筛选
4. 点击查看详情
5. 错误下载按钮

**测试验证**:
- 记录列表正确显示
- 状态筛选正常
- 详情查看正常

---

## 阶段十三：测试与优化

### 步骤 13.1：接口测试
**指示**:
1. 编写接口测试用例（使用 pytest 或 Django test framework）
2. 覆盖所有主要接口
3. 测试正常流程和异常情况
4. 测试权限控制

**测试验证**:
- 所有测试用例通过
- 测试覆盖率 > 80%

---

### 步骤 13.2：前端功能测试
**指示**:
1. 手动测试所有页面功能
2. 测试登录/登出流程
3. 测试权限控制
4. 测试数据展示和交互
5. 测试表单验证
6. 测试错误处理

**测试验证**:
- 所有功能正常工作
- 用户体验流畅
- 错误提示友好

---

### 步骤 13.3：性能测试
**指示**:
1. 测试大数据量场景（1000 条数据）
2. 测试导入性能（1 万条数据）
3. 测试驾驶舱渲染性能
4. 优化慢查询
5. 添加必要的索引

**测试验证**:
- 1 万条数据导入成功
- 驾驶舱首屏渲染 < 3 秒
- API 响应时间合理

---

### 步骤 13.4：安全检查
**指示**:
1. 检查 SQL 注入风险
2. 检查 XSS 风险
3. 检查 CSRF 防护
4. 检查敏感信息泄露
5. 检查权限越界

**测试验证**:
- 无明显安全漏洞
- 权限控制严格

---

## 阶段十四：部署准备

### 步骤 14.1：创建环境配置文件
**指示**:
1. 创建 `.env.example` 文件
2. 包含数据库配置、JWT 密钥等
3. 添加说明注释
4. 更新 `.gitignore`

**测试验证**:
- 配置文件完整
- 敏感信息不会被提交

---

### 步骤 14.2：编写部署文档
**指示**:
1. 创建 `docs/deployment.md`
2. 包含：
   - 环境要求
   - 依赖安装
   - 数据库配置
   - 静态文件收集
   - 运行命令

**测试验证**:
- 按照文档能完成部署
- 文档清晰易懂

---

### 步骤 14.3：创建 README
**指示**:
1. 在项目根目录创建 `README.md`
2. 包含：
   - 项目简介
   - 技术栈
   - 功能特性
   - 快速开始
   - 目录结构
   - 相关文档链接

**测试验证**:
- README 信息完整
- 新开发者能快速上手

---

## 验收标准

### 功能完整性
- [ ] 用户能登录系统
- [ ] 驾驶舱正常显示所有图表
- [ ] 项目列表和传承人列表正常查询
- [ ] 管理员能完成所有 CRUD 操作
- [ ] 数据导入功能正常工作

### 性能指标
- [ ] 1 万条数据能成功导入
- [ ] 驾驶舱首屏渲染 < 3 秒
- [ ] API 平均响应时间 < 500ms

### 权限控制
- [ ] 用户无法访问管理功能
- [ ] 管理员可访问所有功能
- [ ] 越权请求被正确拦截

### 代码质量
- [ ] 无明显代码重复
- [ ] 遵循项目代码规范
- [ ] 有适当的错误处理
- [ ] 有必要的注释

---

## 注意事项

1. **复用现有代码**：参考 Enterprise-HRMS 和 canteen-management-system 的实现，特别是：
   - JWT 认证实现
   - 权限控制类
   - 统一响应格式
   - 前端路由和状态管理

2. **ECharts 内存泄漏**：确保所有 ECharts 组件在 `onUnmounted` 时调用 `chart.dispose()`

3. **API 响应格式**：严格遵循 `{ code: 0, data: {...}, total: n }` 格式

4. **数据库事务**：数据导入必须使用事务，保证数据一致性

5. **错误处理**：所有 API 都要有适当的错误处理和友好的错误信息

6. **分页统一**：所有列表接口都支持分页，默认每页 20 条
