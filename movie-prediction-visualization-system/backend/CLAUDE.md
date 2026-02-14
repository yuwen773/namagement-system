# 后端开发指南

## 项目结构

```
backend/
├── movie_prediction/          # 项目配置
│   ├── __init__.py
│   ├── settings.py             # Django 配置
│   ├── urls.py                 # 路由入口
│   ├── wsgi.py                 # WSGI 应用
│   ├── asgi.py                 # ASGI 应用
│   └── exceptions.py           # 自定义异常处理
├── accounts/                   # 用户认证应用
│   ├── models.py               # 用户模型
│   ├── views.py                # 视图逻辑
│   ├── serializers.py          # 序列化器
│   ├── permissions.py         # 权限类
│   ├── urls.py                 # 路由配置
│   └── apps.py
├── movies/                     # 影片管理应用
├── cinemas/                    # 影院地域应用
├── boxoffice/                  # 票房数据应用
├── prediction/                 # 预测算法应用
├── visualization/              # 可视化接口应用
├── sql/                        # 数据库脚本
│   └── init_db.sql             # 初始化脚本
├── requirements.txt            # Python 依赖
└── manage.py                   # Django 管理脚本
```

## 开发规范

### API 响应格式

```json
// 成功
{ "code": 0, "data": {...}, "total": n }

// 错误
{ "code": -1, "message": "错误描述" }
```

### 视图命名规范
- 列表视图：`get_xxx_list`
- 详情视图：`get_xxx_detail`
- 创建视图：`create_xxx`
- 更新视图：`update_xxx`
- 删除视图：`delete_xxx`

### 模型字段命名
- 使用中文拼音或英文（如 `movie_name`, `box_office`）
- 关联字段使用 `_id` 后缀（如 `movie_id`）

## 常用命令

```bash
# 创建迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver
```

## 应用职责

| 应用 | 职责 |
|------|------|
| accounts | 用户认证、JWT Token、权限 |
| movies | 影片 CRUD、类型管理 |
| cinemas | 影院、地域层级管理 |
| boxoffice | 票房记录管理 |
| prediction | 票房预测算法 |
| visualization | ECharts 图表数据 |
