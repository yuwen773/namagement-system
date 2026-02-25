# 项目进度记录

## 2026-02-25

### 阶段一：后端基础架构搭建 ✓

#### 步骤 1.1：创建 Django 项目结构 ✓
**完成内容**：
- 创建 `backend/` 目录
- 使用 Django 5.2 创建 `heritage_system` 项目
- 创建以下应用模块：
  - `apps/users/` - 用户认证与权限
  - `apps/heritage/` - 非遗项目管理
  - `apps/inheritors/` - 传承人管理
  - `apps/categories/` - 分类字典管理
  - `apps/regions/` - 地理区域管理
  - `apps/importer/` - 数据导入处理
  - `apps/dashboard/` - 驾驶舱统计
- 创建 `utils/` 目录用于通用工具
- 创建 `media/` 和 `logs/` 目录
- 为每个应用创建 `apps.py` 配置文件，设置中文 verbose_name
- 为每个应用创建基础 `models.py` 文件

**验证结果**：
- ✓ `python manage.py check` 无错误输出
- ✓ 项目结构清晰，符合 Django 最佳实践

#### 步骤 1.2：配置 MySQL 数据库连接 ✓
**完成内容**：
- 修改 `heritage_system/settings.py` 配置：
  - 数据库引擎：MySQL
  - 数据库名称：`heritage_db`
  - 字符集：UTF8MB4
  - 端口：3306
  - 时区：`Asia/Shanghai`
  - 语言：`zh-hans`
- 在 `INSTALLED_APPS` 中注册所有自定义应用
- 配置 MEDIA 和 STATIC 文件路径
- 创建 `create_db.py` 脚本用于初始化数据库
- 安装 `mysqlclient` 依赖

**验证结果**：
- ✓ 数据库 `heritage_db` 创建成功
- ✓ `python manage.py migrate` 成功执行，生成基础表
- ✓ `python manage.py runserver` 成功启动，访问 http://127.0.0.1:8000/ 正常

**文件清单**：
```
backend/
├── heritage_system/          # Django 项目配置
│   ├── settings.py          # 已配置 MySQL、时区、应用注册
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                     # 应用模块
│   ├── users/               # 用户管理
│   ├── heritage/            # 非遗项目
│   ├── inheritors/          # 传承人
│   ├── categories/          # 分类字典
│   ├── regions/             # 地理区域
│   ├── importer/            # 数据导入
│   └── dashboard/           # 驾驶舱统计
├── utils/                    # 通用工具
├── media/                    # 媒体文件目录
├── logs/                     # 日志目录
├── create_db.py             # 数据库初始化脚本
├── manage.py                # Django 管理脚本
└── .gitignore               # Git 忽略配置
```

---

## 待完成任务

### 下一步：步骤 1.3 - 安装并配置依赖包
等待用户验证测试结果后继续。

需要安装的依赖：
- djangorestframework
- djangorestframework-simplejwt
- pandas
- openpyxl
- Pillow
- django-cors-headers

并在 `settings.py` 中配置 REST Framework 和 CORS。
