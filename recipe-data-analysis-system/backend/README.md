# 后端项目说明

## 项目结构

```
backend/
├── config/                    # Django 项目配置目录
│   ├── backend/              # 项目设置
│   │   ├── settings.py       # 主配置文件
│   │   ├── urls.py           # 主路由
│   │   └── wsgi.py
│   ├── manage.py             # Django 管理脚本
│   ├── utils/                # 公共工具模块
│   │   ├── response.py       # 统一响应封装
│   │   ├── exceptions.py     # 自定义异常
│   │   ├── pagination.py     # 分页配置
│   │   └── constants.py      # 常量定义
│   ├── accounts/             # 用户认证模块
│   ├── recipes/              # 菜谱模块
│   ├── categories/           # 分类模块
│   ├── ingredients/          # 食材模块
│   ├── favorites/            # 收藏模块
│   ├── analytics/            # 数据分析模块
│   ├── admin_panel/          # 管理员模块
│   └── behavior_logs/        # 行为日志模块
├── backend_venv/             # Python 虚拟环境
└── README.md                 # 本文件
```

## 环境要求

- Python 3.12+
- MySQL 8.0+
- 虚拟环境目录：`backend_venv/`

## 配置步骤

### 1. 数据库配置

编辑 `backend/config/settings.py`，修改数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recipe_analysis_db',
        'USER': 'root',
        'PASSWORD': '你的MySQL密码',  # 修改这里
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 2. 创建数据库

首先在 MySQL 中创建数据库：

```bash
mysql -u root -p
CREATE DATABASE recipe_analysis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

或者执行初始化脚本：

```bash
mysql -u root -p < sql/init.sql
```

### 3. 运行数据库迁移

```bash
cd backend
../backend_venv/Scripts/python manage.py makemigrations
../backend_venv/Scripts/python manage.py migrate
```

### 4. 创建超级用户

```bash
../backend_venv/Scripts/python manage.py createsuperuser
```

## 启动服务器

```bash
cd backend
../backend_venv/Scripts/python manage.py runserver
```

服务器将在 `http://localhost:8000/` 启动。

## API 访问

- Django Admin: `http://localhost:8000/admin/`
- API 前缀: `/api/`

## 已安装的 Django 应用

1. **accounts** - 用户认证模块
2. **recipes** - 菜谱模块
3. **categories** - 分类模块
4. **ingredients** - 食材模块
5. **favorites** - 收藏模块
6. **analytics** - 数据分析模块
7. **admin_panel** - 管理员模块
8. **behavior_logs** - 行为日志模块

## 开发规范

所有后端 API 开发必须遵循 `memory-bank/dev-standards/backend-api-standards.md` 规范。

## 注意事项

1. 当前使用 PyMySQL 作为 MySQL 驱动
2. Django 版本：5.2.10
3. JWT Token 有效期：24 小时
4. CORS 已配置允许本地开发服务器访问
