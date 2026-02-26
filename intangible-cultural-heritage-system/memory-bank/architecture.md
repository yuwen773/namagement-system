# Architecture

## 系统边界
- **后端**: Django 5.2 + DRF，`/api/v1`
- **前端**: Vue 3 + TypeScript + Element Plus + ECharts
- **响应**: `{ code: 0, data: {...}, total?: n }`
- **鉴权**: JWT，admin 可写，user 只读

## 数据模型关系
```
Category (分类) → HeritageItem (非遗项目) → Inheritor (传承人)
                                              ↑
Region (地区) ────────────────────────────────┘
```

## 后端模块
| 模块 | 职责 |
|------|------|
| `apps.accounts` | 用户认证（JWT） |
| `apps.heritage` | 非遗项目 CRUD |
| `apps.inheritors` | 传承人 CRUD |
| `apps.categories` | 分类管理（树形） |
| `apps.regions` | 地区管理 |
| `apps.dashboard` | 驾驶舱聚合接口 |
| `apps.importer` | 数据导入服务 |

## 前端模块
| 路径 | 职责 |
|------|------|
| `src/api/` | API 请求封装 |
| `src/stores/user.ts` | 用户状态和认证 |
| `src/router/index.ts` | 路由配置和权限守卫 |
| `src/layouts/MainLayout.vue` | 主布局（顶栏+侧栏） |
| `src/components/StatCard.vue` | 统计卡片组件 |
| `src/utils/request.ts` | Axios 拦截器 |

## 前端页面架构

### 数据展示页面（阶段十一）
| 文件 | 功能 | 关键特性 |
|------|------|----------|
| `views/HeritageList.vue` | 非遗项目列表 | 多维度筛选（关键词/分类/级别/国家）、分页、行点击跳转详情 |
| `views/HeritageDetail.vue` | 非遗项目详情 | 完整信息展示、关联传承人列表、返回导航 |
| `views/InheritorList.vue` | 传承人列表 | 多维度筛选（姓名/级别/国家/所属项目）、分页、项目链接跳转 |

### 管理功能页面（阶段十二）
| 文件 | 功能 | 关键特性 |
|------|------|----------|
| `views/admin/HeritageManage.vue` | 非遗项目管理 | 完整 CRUD、表单验证、二次确认删除、多维度筛选、权限控制 |
| `views/admin/InheritorManage.vue` | 传承人管理 | 完整 CRUD、所属项目下拉选择、表格内项目链接、性别/级别可选 |
| `views/admin/CategoryManage.vue` | 分类字典管理 | 双视图（列表/树形）、父分类选择、防循环引用、悬停操作 |
| `views/admin/DataImport.vue` | 数据导入 | 文件上传（拖拽/点击）、进度显示、结果统计、导入记录、错误下载 |

### 设计理念
- **视觉风格**: 采用棕色系渐变（#8b4513, #a0522d）呼应文化遗产主题
- **布局策略**: 
  - 列表页：顶部渐变 header + 筛选表单 + 数据表格 + 分页器
  - 详情页：返回按钮 + 渐变 header 卡片 + 信息卡片网格 + 关联数据展示
  - 管理页：渐变 header + 操作按钮 + 筛选区 + 数据表格 + 对话框表单
- **交互设计**: 
  - 表格行悬停效果（背景色变化 + 轻微上移）
  - 卡片悬停效果（阴影加深 + 上移动画）
  - 按钮悬停效果（颜色变化 + 上移）
  - 平滑过渡动画（0.3s ease）
  - 二次确认删除（防止误操作）
  - 表单验证（实时反馈）
- **响应式适配**: 移动端优化（单列布局、字体缩放、间距调整）

### API 集成
- 使用统一的 API 响应格式处理
- 实现错误提示和加载状态
- 支持分页参数传递
- 支持多条件筛选组合
- CRUD 操作完整实现
- 权限控制（admin/user）

### 组件复用
- Element Plus 组件深度定制
- 统一的颜色主题变量
- 统一的表格样式
- 统一的按钮样式
- 统一的卡片样式

## 配置
| 项目 | 值 |
|------|------|
| 数据库 | MySQL 8.0 (UTF8MB4) |
| 后端端口 | 8000 |
| 前端端口 | 5173 |
| API 代理 | `/api` → `http://127.0.0.1:8000` |
| 主题色 | 棕色系 #8b4513, #a0522d |

## 测试账号
- 用户名: `admin`
- 密码: `password123`

## 文件说明

### 后端核心文件
- `backend/apps/heritage/models.py` - 非遗项目数据模型
- `backend/apps/heritage/serializers.py` - 非遗项目序列化器
- `backend/apps/heritage/views.py` - 非遗项目视图（CRUD API）
- `backend/apps/inheritors/models.py` - 传承人数据模型
- `backend/apps/inheritors/serializers.py` - 传承人序列化器
- `backend/apps/inheritors/views.py` - 传承人视图（CRUD API）
- `backend/apps/categories/models.py` - 分类数据模型
- `backend/apps/categories/serializers.py` - 分类序列化器
- `backend/apps/categories/views.py` - 分类视图（包含树形结构 API）
- `backend/apps/regions/models.py` - 地区数据模型
- `backend/apps/regions/views.py` - 地区视图
- `backend/apps/dashboard/views.py` - 驾驶舱聚合统计 API
- `backend/apps/users/views.py` - 用户认证（JWT 登录/刷新/登出）
- `backend/utils/response.py` - 统一响应格式工具
- `backend/utils/pagination.py` - 分页工具

### 前端核心文件
- `frontend/src/main.ts` - 应用入口，注册 Element Plus 和路由
- `frontend/src/App.vue` - 根组件
- `frontend/src/router/index.ts` - 路由配置和权限守卫
- `frontend/src/stores/user.ts` - 用户状态管理（Pinia）
- `frontend/src/utils/request.ts` - Axios 实例和拦截器
- `frontend/src/api/*.ts` - API 请求封装（heritage, inheritor, category, region, dashboard, auth）
- `frontend/src/types/index.ts` - TypeScript 类型定义
- `frontend/src/layouts/MainLayout.vue` - 主布局（顶栏+侧栏+内容区）
- `frontend/src/views/Login.vue` - 登录页
- `frontend/src/views/Dashboard.vue` - 驾驶舱（统计卡片+地图+图表）
- `frontend/src/views/HeritageList.vue` - 非遗项目列表页
- `frontend/src/views/HeritageDetail.vue` - 非遗项目详情页
- `frontend/src/views/InheritorList.vue` - 传承人列表页
- `frontend/src/views/admin/HeritageManage.vue` - 非遗项目管理页（admin）
- `frontend/src/views/admin/InheritorManage.vue` - 传承人管理页（admin）
- `frontend/src/views/admin/CategoryManage.vue` - 分类字典管理页（admin）
- `frontend/src/views/admin/DataImport.vue` - 数据导入页（admin）
- `frontend/src/components/StatCard.vue` - 统计卡片组件

### 配置文件
- `backend/heritage_system/settings.py` - Django 配置（数据库、JWT、CORS、REST Framework）
- `backend/heritage_system/urls.py` - 后端路由配置
- `backend/requirements.txt` - Python 依赖
- `frontend/package.json` - Node.js 依赖
- `frontend/vite.config.ts` - Vite 配置（代理、别名）
- `frontend/tailwind.config.js` - Tailwind CSS 配置
- `frontend/tsconfig.json` - TypeScript 配置
