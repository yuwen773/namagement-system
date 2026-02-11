# 系统架构

## 技术栈

| 后端 | 前端 |
|------|------|
| Django 5.2 + DRF | Vue 3 + Element Plus |
| MySQL + JWT | ECharts + Tailwind CSS |

## 目录结构

```
backend/                    # Django 后端
├── accounts/               # 登录/注册/用户信息
├── attractions/            # 景点 CRUD
├── comments/               # 评论 + 收藏
├── notifications/          # 消息/公告
├── statistics/             # 数据统计 (ADMIN)
└── recommendations/        # 推荐算法

frontend/                   # Vue 3 前端
├── src/
│   ├── api/                # Axios 请求封装
│   ├── components/         # 公共组件
│   ├── layouts/            # 布局组件
│   ├── router/             # 路由配置
│   ├── stores/             # Pinia 状态
│   ├── utils/              # 工具函数
│   └── views/              # 页面组件
│       ├── auth/           # 登录/注册
│       ├── user/           # 用户端页面
│       └── admin/          # 管理端页面
└── vite.config.js          # 开发服务器配置
```

## API 路由

| 路由 | 用途 |
|------|------|
| `/api/accounts/` | 登录/注册/个人信息 |
| `/api/attractions/` | 景点列表/详情/搜索 |
| `/api/comments/` | 评论/收藏 |
| `/api/notifications/` | 消息中心 |
| `/api/statistics/` | 数据统计 (ADMIN) |
| `/api/recommendations/` | 推荐算法 |

## 前端组件

### 布局组件
| 组件 | 用途 |
|------|------|
| `AdminLayout.vue` | 管理端：侧边栏 + 顶部栏 + 用户信息 |
| `UserLayout.vue` | 用户端：顶部导航 + 底部 |

### 公共组件
| 组件 | Props | 用途 |
|------|-------|------|
| `AttractionCard.vue` | `attraction: Object` | 景点卡片，点击跳转详情 |
| `CommentItem.vue` | `comment, showDelete, currentUserId` | 评论项，支持删除 |
| `Pagination.vue` | `v-model, pageSize, total, pageSizes` | 分页封装 |

### 工具函数
| 文件 | 导出 |
|------|------|
| `utils/date.js` | `formatDate()`, `formatRelativeTime()` |

## 推荐算法

| 场景 | 策略 |
|------|------|
| 冷启动 | 热门推荐（浏览量+评论数+评分） |
| 个性化 | 同类景点推荐 |
| 详情页 | 类别 + 地区相似 |

## 响应格式

```javascript
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "错误描述" }

// 登录
{ "code": 0, "data": { "access_token": "...", "refresh_token": "...", "user": {...} } }
```
