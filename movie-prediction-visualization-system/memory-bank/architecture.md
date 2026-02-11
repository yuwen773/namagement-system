# 系统架构

## 技术栈
- **后端**: Django 5.2 + DRF + JWT
- **前端**: Vue 3 + Vite + Element Plus + ECharts
- **数据库**: MySQL 8.0 (UTF8MB4)

## 目录结构
```
backend/
├── accounts/       # 认证、用户
├── movies/         # 影片、类型
├── cinemas/        # 影院、地域
├── boxoffice/      # 票房
├── prediction/     # 预测
└── visualization/  # 可视化统计

frontend/src/
├── api/            # API 封装
├── router/         # 路由守卫
├── stores/         # Pinia 状态
├── views/admin/    # 管理端
└── views/user/     # 用户端
```

## 数据模型
| 模型 | 说明 |
|------|------|
| users | 用户 (ADMIN/USER) |
| movie_types | 影片类型 |
| movies | 影片 |
| regions | 地域 (自关联) |
| cinemas | 影院 |
| boxoffice_records | 票房 |

## API 规范
```json
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "..." }
```

## 关键规范
- **主题**: 深色渐变 `from-slate-950 via-slate-900`
- **组件**: 玻璃态 `backdrop-filter: blur(20px)`
- **图表**: ECharts 需 `onUnmounted.dispose()`
- **认证**: JWT (Access 2h, Refresh 7d)
