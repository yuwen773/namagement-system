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
├── apps/
│   ├── accounts/        # 账号管理
│   ├── attractions/     # 景点管理
│   ├── comments/        # 评论收藏
│   ├── notifications/   # 消息通知
│   ├── statistics/     # 数据统计
│   └── recommendations/ # 推荐算法
└── sql/init_db.sql      # 测试数据

frontend/src/
├── api/        # API集成
├── components/ # 公共组件
├── layouts/    # 布局组件
├── router/      # 路由守卫
├── stores/      # Pinia状态
└── views/       # 页面组件
```

## 数据模型

| 模型 | 关键字段 | 说明 |
|------|----------|------|
| UserProfile | role, is_active, is_deleted | 用户，逻辑删除 |
| Attraction | category, region, view_count | 景点 |
| Comment | rating, status | 评论，审核状态机 |
| Favorite | user + attraction | 收藏，联合唯一 |
| Notification | type, is_read, user | 通知 |

## API 路由

| 基础路径 | 职责 |
|----------|------|
| `/api/accounts/` | 认证 |
| `/api/attractions/` | 景点 |
| `/api/comments/` | 评论/收藏 |
| `/api/notifications/` | 通知 |
| `/api/statistics/` | 统计 |
| `/api/recommendations/` | 推荐 |

## 推荐算法

| 场景 | 策略 |
|------|------|
| 热度 | `浏览×0.2 + 评论×0.3 + 评分×浏览×0.5` |
| 个性化 | 基于收藏/评分推荐同类景点 |
| 相似 | 同类别+同地区优先 |

## 关键设计

- **认证**: JWT双token
- **删除**: 逻辑删除 (`is_deleted`)
- **评论**: 待审核机制 (PENDING/APPROVED/REJECTED)
- **权限**: 自定义 `IsAdmin` 类

## 响应格式

```json
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "错误描述" }
```
