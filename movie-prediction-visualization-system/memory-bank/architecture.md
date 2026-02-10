# 系统架构

## 项目结构

```
movie-prediction-visualization-system/
├── backend/
│   ├── movie_prediction/   # Django 配置 (settings.py, urls.py)
│   │   └── settings.py     # REST_FRAMEWORK, JWT, SPECTACULAR_SETTINGS
│   ├── accounts/           # 用户认证
│   ├── movies/             # 影片管理
│   ├── cinemas/            # 影院地域
│   ├── boxoffice/          # 票房数据
│   ├── prediction/         # 预测算法
│   ├── visualization/      # 可视化接口
│   ├── docs/
│   │   └── api-docs.md     # API 接口文档
│   └── requirements.txt
└── frontend/               # Vue 3 (待开发)
```

## 数据库表

| 表名 | 说明 |
|------|------|
| users | 用户 (role: ADMIN/USER) |
| movie_types | 影片类型 |
| movies | 影片信息 |
| regions | 地域 (省/市，自关联 parent) |
| cinemas | 影院 |
| boxoffice_records | 票房记录 (unique: movie+cinema+date) |

## API 响应格式

```json
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "..." }
```

## API 端点

| 模块 | 前缀 | 说明 |
|------|------|------|
| accounts | /api/auth/ | 注册/登录/用户管理 |
| movies | /api/movies/ | 影片/类型 CRUD |
| cinemas | /api/cinemas/ | 影院/地域 CRUD |
| boxoffice | /api/boxoffice/ | 票房记录/统计 |
| prediction | /api/prediction/ | 预测算法 |
| visualization | /api/visualization/ | 图表数据 |

## 模块职责

### accounts
- `models.py`: User(AbstractBaseUser), role字段
- `views.py`: RegisterView, LoginView, UserViewSet
- `permissions.py`: IsAdmin, IsUserOrAdmin

### movies
- `models.py`: MovieType, Movie (type外键)
- `views.py`: MovieTypeViewSet, MovieViewSet (released/coming actions)
- `filters.py`: search, type, status, release_date筛选

### cinemas
- `models.py`: Region (自关联), Cinema
- `views.py`: RegionViewSet (provinces/cities actions), CinemaViewSet

### boxoffice
- `models.py`: BoxOfficeRecord (unique_together)
- `views.py`: BoxOfficeRecordViewSet (batch_delete/batch_input), BoxOfficeStatsView
- 业务逻辑: 创建/删除/更新票房记录时自动更新 movie.box_office_total

### prediction
- `services.py`: PredictionService (线性回归/移动平均算法)
- `views.py`: MoviePredictionView, PredictionHistoryView

### visualization
- `views.py`: Top10, Today, Champion, Type, Region, TimeSeries, Dashboard
- 数据聚合: 使用 Django ORM 的 aggregate() 和 Sum()

## 配置说明

### settings.py 关键配置
```python
# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT (Access: 2h, Refresh: 7d)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# drf-spectacular (API文档生成)
SPECTACULAR_SETTINGS = {
    'TITLE': '电影票房预测与可视化系统 API',
    'TAGS': [
        {'name': '认证'}, {'name': '影片管理'}, {'name': '影院管理'},
        {'name': '票房数据'}, {'name': '预测分析'}, {'name': '数据可视化'},
    ],
}
```

## 文档说明

| 文件 | 作用 |
|------|------|
| `backend/docs/api-docs.md` | 完整的 API 接口文档 |
| `memory-bank/architecture.md` | 系统架构 |
| `memory-bank/PRD.md` | 产品需求 |
| `memory-bank/IMPLEMENTATION_PLAN.md` | 实施计划 |
