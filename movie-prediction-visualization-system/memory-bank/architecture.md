# 系统架构

## 项目结构

```
movie-prediction-visualization-system/
├── backend/                    # Django 5.2 + DRF
│   ├── movie_prediction/       # 项目配置
│   ├── accounts/               # 用户认证
│   ├── movies/                 # 影片管理
│   ├── cinemas/                # 影院地域
│   ├── boxoffice/              # 票房数据
│   ├── prediction/             # 预测算法
│   └── visualization/          # 可视化接口
└── frontend/                   # Vue 3 + Vite
```

## 关键文件说明

| 文件 | 作用 |
|------|------|
| `boxoffice/serializers.py` | 票房序列化器，含业务验证（日期、金额） |
| `boxoffice/views.py` | 票房 CRUD + 批量删除 + 统计接口 |
| `boxoffice/urls.py` | 路由 `/api/boxoffice/*` |

## 数据库表

| 表名 | 说明 |
|------|------|
| users | 用户 (role: ADMIN/USER) |
| movie_types | 影片类型 |
| movies | 影片信息 |
| regions | 地域 (省/市) |
| cinemas | 影院信息 |
| boxoffice_records | 票房记录 |

## API 响应格式

```json
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "错误描述" }
```
