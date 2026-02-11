# 系统架构

> 2026-02-11

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Django 5.2 + DRF + MySQL |
| 前端 | Vue 3 + Element Plus + Pinia |
| 认证 | JWT (Access: 2h, Refresh: 7d) |

## 项目结构

```
backend/
├── accounts/           # 账号管理 (注册/登录/JWT)
├── attractions/        # 景点管理 (CRUD/搜索)
├── comments/           # 评论收藏 (审核机制)
├── notifications/      # 消息通知 (公告/私信)
├── statistics/         # 数据统计 (看板)
├── recommendations/   # 推荐算法 (热度/个性化)
└── sql/init_db.sql     # 测试数据

frontend/src/
├── api/                # API集成层 (axios封装)
├── components/         # 公共组件 (AttractionCard等)
├── layouts/            # 布局组件 (AdminLayout/UserLayout)
├── router/             # 路由守卫 (权限控制)
├── stores/             # Pinia状态管理 (user/auth)
└── views/              # 页面组件 (admin/user/auth)
```

## 文件作用说明

### 后端 (Django Apps)

| 文件/目录 | 作用 |
|-----------|------|
| `accounts/models.py` | UserProfile模型，角色(ADMIN/USER) |
| `accounts/views.py` | JWT登录/注册/Token刷新 |
| `attractions/models.py` | Attraction景点模型 |
| `attractions/serializers.py` | 景点序列化器 |
| `comments/models.py` | Comment/Favorite模型 |
| `comments/permissions.py` | 评论审核权限 |
| `statistics/views.py` | 统计数据API |
| `recommendations/views.py` | 推荐算法接口 |

### 前端 (Vue Components)

| 文件路径 | 作用 |
|----------|------|
| `api/request.js` | Axios实例，响应拦截器(展平data) |
| `api/auth.js` | 认证API封装 |
| `api/comments.js` | 评论/收藏API封装 |
| `stores/user.js` | 用户状态管理(Token/角色) |
| `router/index.js` | 路由配置+导航守卫 |
| `views/admin/*.vue` | 管理端页面(8个) |
| `views/user/*.vue` | 用户端页面(8个) |
| `views/auth/*.vue` | 登录/注册页面 |
| `components/AttractionCard.vue` | 景点卡片通用组件 |

## API路由

| 基础路径 | 职责 |
|----------|------|
| `/api/accounts/` | 认证 (登录/注册/token刷新) |
| `/api/attractions/` | 景点 (列表/详情/搜索) |
| `/api/comments/` | 评论/收藏 (审核/Favorite) |
| `/api/notifications/` | 通知 (公告/私信) |
| `/api/statistics/` | 统计 (用户/评论/景点) |
| `/api/recommendations/` | 推荐 (热门/个性化/相似) |

## 数据模型

| 模型 | 关键字段 | 作用 |
|------|----------|------|
| UserProfile | `role`, `is_active`, `is_deleted` | 用户账号，逻辑删除 |
| Attraction | `category`, `region`, `view_count` | 景点信息，浏览量统计 |
| Comment | `rating`, `status` | 评论，审核状态机 |
| Favorite | `user` + `attraction` (联合唯一) | 收藏，防止重复 |
| Notification | `type`, `is_read`, `user` | 通知，null=全员 |

## 响应格式

```javascript
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "错误描述" }

// 认证成功
{ "code": 0, "data": { "access_token": "...", "refresh_token": "...", "user": {...} } }
```

## 推荐算法

| 场景 | 策略 |
|------|------|
| 热度 | `浏览×0.2 + 评论×0.3 + 评分×浏览×0.5` |
| 个性化 | 基于收藏/评分推荐同类景点 |
| 相似 | 同类别+同地区优先 |

## 关键设计

| 设计点 | 说明 |
|--------|------|
| 认证 | JWT双token，Access(2h)/Refresh(7d) |
| 删除 | 逻辑删除 (`is_deleted`) |
| 评论 | 待审核机制 (PENDING/APPROVED/REJECTED) |
| 权限 | 自定义 `IsAdmin` 类，角色分流 |
| API响应 | axios拦截器展平 `{data, total}` 结构 |
