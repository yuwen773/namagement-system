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

### 1. 环境变量配置

复制 `.env.example` 并修改数据库配置：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，修改以下配置：
# DB_NAME=recipe_analysis_db      # 数据库名
# DB_USER=root                    # 用户名
# DB_PASSWORD=your_password       # 密码
# DB_HOST=127.0.0.1               # 主机
# DB_PORT=3306                    # 端口
```

**重要**: `.env` 文件包含敏感信息，已被 `.gitignore` 排除，不会被提交到版本控制。

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
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户

```bash
python manage.py createsuperuser
```

### 5. 验证配置

```bash
# 检查配置是否正确
python manage.py check

# 测试数据库连接
python manage.py dbshell
```

## 启动服务器

```bash
cd backend
python manage.py runserver
```

服务器将在 `http://localhost:8000/` 启动。

**可选参数**：
- `python manage.py runserver 0.0.0.0:8000` - 允许外部访问
- `python manage.py runserver 8001` - 使用其他端口

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

## 环境变量说明

`.env` 文件支持的配置项：

| 配置项 | 说明 | 默认值 |
|:------|:-----|:-------|
| `SECRET_KEY` | Django 密钥 | 自动生成 |
| `DEBUG` | 调试模式 | `True` |
| `ALLOWED_HOSTS` | 允许的主机 | `localhost,127.0.0.1` |
| `DB_NAME` | 数据库名 | `recipe_analysis_db` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_HOST` | 数据库主机 | `127.0.0.1` |
| `DB_PORT` | 数据库端口 | `3306` |
| `LANGUAGE_CODE` | 语言代码 | `zh-hans` |
| `TIME_ZONE` | 时区 | `Asia/Shanghai` |

## 数据库切换

### 切换到 SQLite

如需使用 SQLite 而非 MySQL，修改 `config/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 切换到不同 MySQL 端口

在 `.env` 文件中修改 `DB_PORT`：

```bash
DB_PORT=3307  # 使用 3307 端口
```

## 注意事项

1. **环境变量**: 所有敏感配置通过 `.env` 文件管理
2. **PyMySQL 驱动**: 使用 PyMySQL 作为 MySQL 驱动
3. **Django 版本**: 5.2.10
4. **JWT Token**: 有效期 24 小时
5. **CORS**: 已配置允许本地开发服务器访问（5173-5175 端口）
6. **字符集**: 数据库使用 `utf8mb4` 支持中文和表情符号
