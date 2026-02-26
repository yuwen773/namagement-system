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
| `src/layouts/MainLayout.vue` | 主布局 |
| `src/components/StatCard.vue` | 统计卡片 |
| `src/utils/request.ts` | Axios 拦截器 |

## 前端页面
| 类型 | 文件 |
|------|------|
| 认证 | `Login.vue` |
| 驾驶舱 | `Dashboard.vue` |
| 列表 | `HeritageList.vue`, `InheritorList.vue` |
| 详情 | `HeritageDetail.vue` |
| 管理 | `admin/HeritageManage.vue`, `admin/InheritorManage.vue`, `admin/CategoryManage.vue`, `admin/DataImport.vue` |

## 测试
| 模块 | 用例数 |
|------|--------|
| 认证 | 10 |
| 非遗项目 | 18 |
| 传承人 | 12 |
| 分类 | 10 |
| 地区 | 8 |
| 驾驶舱 | 6 |
| **总计** | **64** |

## 配置
| 项目 | 值 |
|------|------|
| 数据库 | MySQL 8.0 (UTF8MB4) |
| 后端端口 | 8000 |
| 前端端口 | 5173 |
| 主题色 | 棕色系 #8b4513 |

## 测试账号
- 用户名: `admin`
- 密码: `password123`
