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

## 前端页面架构（阶段十一新增）

### 数据展示页面
| 文件 | 功能 | 关键特性 |
|------|------|----------|
| `views/HeritageList.vue` | 非遗项目列表 | 多维度筛选（关键词/分类/级别/国家）、分页、行点击跳转详情 |
| `views/HeritageDetail.vue` | 非遗项目详情 | 完整信息展示、关联传承人列表、返回导航 |
| `views/InheritorList.vue` | 传承人列表 | 多维度筛选（姓名/级别/国家/所属项目）、分页、项目链接跳转 |

### 设计理念
- **视觉风格**: 采用棕色系渐变（#8b4513, #a0522d）呼应文化遗产主题
- **布局策略**: 
  - 列表页：顶部渐变 header + 筛选表单 + 数据表格 + 分页器
  - 详情页：返回按钮 + 渐变 header 卡片 + 信息卡片网格 + 关联数据展示
- **交互设计**: 
  - 表格行悬停效果（背景色变化 + 轻微上移）
  - 卡片悬停效果（阴影加深 + 上移动画）
  - 平滑过渡动画（0.3s ease）
- **响应式适配**: 移动端优化（单列布局、字体缩放、间距调整）

### API 集成
- 使用统一的 API 响应格式处理
- 实现错误提示和加载状态
- 支持分页参数传递
- 支持多条件筛选组合

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
