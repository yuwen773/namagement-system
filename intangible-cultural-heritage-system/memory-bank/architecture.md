# Architecture

## 系统边界
- 后端：Django 5.2 + DRF，API 前缀 `/api/v1`
- 前端：Vue 3 + TypeScript + Element Plus
- 响应格式：`{ code: 0, data: {...}, total?: n }`
- 鉴权：JWT，admin 可写，user 只读

## 核心数据关系
```
Category (分类)
    ↓
HeritageItem (非遗项目)
    ↓
Inheritor (传承人)

Region (地区) → HeritageItem/Inheritor
```

## 后端模块
| 模块 | 职责 |
|------|------|
| `apps.accounts` | 用户认证（JWT） |
| `apps.heritage` | 非遗项目 CRUD |
| `apps.inheritors` | 传承人 CRUD |
| `apps.categories` | 分类管理（树形结构） |
| `apps.regions` | 地区管理 |
| `apps.dashboard` | 驾驶舱聚合接口 |
| `apps.importer` | 数据导入服务 |

## 前端模块
| 模块 | 职责 |
|------|------|
| `src/api/` | API 请求封装 |
| `src/stores/` | Pinia 状态管理 |
| `src/router/` | 路由与守卫 |
| `src/views/` | 页面组件 |
| `src/utils/request.ts` | Axios 拦截器 |

## 关键配置
- **数据库**：MySQL 8.0，UTF8MB4
- **后端端口**：8000
- **前端端口**：5173
- **代理**：`/api` → `http://127.0.0.1:8000`
