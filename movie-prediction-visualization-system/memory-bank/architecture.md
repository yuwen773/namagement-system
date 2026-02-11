# 系统架构

## 项目结构

```
movie-prediction-visualization-system/
├── backend/
│   ├── movie_prediction/       # Django配置 (settings, urls)
│   ├── accounts/              # 用户认证 (JWT)
│   ├── movies/                # 影片管理
│   ├── cinemas/               # 影院地域
│   ├── boxoffice/             # 票房数据
│   ├── prediction/            # 预测算法
│   ├── visualization/         # 可视化接口
│   └── requirements.txt
└── frontend/
    └── src/
        ├── api/               # API接口封装
        ├── router/            # 路由配置
        ├── stores/            # Pinia状态管理
        ├── views/
        │   ├── layouts/       # 布局组件
        │   ├── auth/          # 认证页面
        │   ├── admin/         # 管理端页面
        │   └── user/          # 用户端页面
        ├── utils/             # 工具函数
        └── main.js
```

## 管理端页面 (src/views/admin/)

| 文件 | 功能 |
|------|------|
| `Dashboard.vue` | 统计卡片（影片/影院/票房/用户总数）、快捷入口、最近票房记录 |
| `Movies.vue` | 影片CRUD、搜索、分页、类型选择、编辑/删除 |
| `MovieTypes.vue` | 类型CRUD、搜索、分页 |
| `Cinemas.vue` | 影院CRUD、地域筛选、分页、地址/电话 |
| `Regions.vue` | 地域CRUD、上级地域选择、编码 |
| `BoxOffice.vue` | 票房录入/编辑/删除、批量操作、日期/影片/影院筛选 |
| `Prediction.vue` | ECharts预测图表、算法选择、预测历史 |
| `Users.vue` | 用户CRUD、角色管理、状态切换(禁用/启用) |

**通用功能**:
- el-table 分页组件
- el-dialog 表单编辑
- el-form 表单验证
- ElMessage 错误提示

## 基础设施

### 路由 (src/router/index.js)
- `meta.requiresAuth`: 需要登录
- `meta.roles`: ['ADMIN'] 限定管理员

### 状态管理 (src/stores/)
| 文件 | 作用 |
|------|------|
| `user.js` | token、user信息、登录/登出 |
| `app.js` | 侧边栏折叠、主题 |

### API封装 (src/api/)
| 文件 | 作用 |
|------|------|
| `auth.js` | 登录、注册、Token管理 |
| `movie.js` | 影片/类型 CRUD |
| `cinema.js` | 影院/地域 CRUD |
| `boxoffice.js` | 票房记录 CRUD |
| `prediction.js` | 预测算法 |
| `visualization.js` | 图表数据 |
| `user.js` | 用户管理 |

### HTTP工具 (src/utils/request.js)
- Bearer Token 自动携带
- 401 自动跳转登录页
- 错误提示 ElMessage

## API响应格式

```json
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "..." }
```

## 数据库表

| 表名 | 说明 |
|------|------|
| users | 用户 (role: ADMIN/USER) |
| movie_types | 影片类型 |
| movies | 影片信息 |
| regions | 地域 (自关联parent) |
| cinemas | 影院 |
| boxoffice_records | 票房记录 |

## 文档索引

| 文件 | 作用 |
|------|------|
| `backend/docs/api-docs.md` | 完整API文档 |
| `progress.md` | 项目进度 |
| `IMPLEMENTATION_PLAN.md` | 实施计划 |
