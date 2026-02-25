# 非物质文化遗产系统 - 后端

## 项目状态

✓ 阶段一步骤 1.1-1.2 已完成：Django 项目结构搭建和 MySQL 数据库配置

## 快速开始

### 1. 环境要求
- Python 3.12+
- MySQL 8.0+
- pip

### 2. 数据库初始化
```bash
# 创建数据库（如果尚未创建）
python create_db.py
```

### 3. 运行迁移
```bash
python manage.py migrate
```

### 4. 启动开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 查看 Django 欢迎页面

### 5. 验证配置
```bash
# 检查项目配置
python manage.py check
```

## 项目结构

```
backend/
├── heritage_system/          # Django 项目配置
│   ├── settings.py          # 已配置 MySQL、时区、应用
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                     # 业务应用模块
│   ├── users/               # 用户管理
│   ├── heritage/            # 非遗项目
│   ├── inheritors/          # 传承人
│   ├── categories/          # 分类字典
│   ├── regions/             # 地理区域
│   ├── importer/            # 数据导入
│   └── dashboard/           # 驾驶舱统计
├── utils/                    # 通用工具（待实现）
├── media/                    # 媒体文件目录
├── logs/                     # 日志目录
├── create_db.py             # 数据库初始化脚本
└── manage.py                # Django 管理脚本
```

## 已完成配置

### 数据库配置
- 数据库名称：`heritage_db`
- 字符集：UTF8MB4
- 时区：Asia/Shanghai
- 语言：zh-hans

### 已注册应用
- apps.users - 用户管理
- apps.heritage - 非遗项目管理
- apps.inheritors - 传承人管理
- apps.categories - 分类字典管理
- apps.regions - 地理区域管理
- apps.importer - 数据导入处理
- apps.dashboard - 驾驶舱统计

## 下一步

等待用户验证测试结果后，将继续步骤 1.3：安装并配置依赖包

需要安装的依赖：
- djangorestframework
- djangorestframework-simplejwt
- pandas
- openpyxl
- Pillow
- django-cors-headers

## 测试验证

### 验证项目启动
```bash
python manage.py runserver
```
预期：服务器在 http://127.0.0.1:8000/ 启动成功

### 验证数据库连接
```bash
python manage.py dbshell
```
预期：成功连接到 MySQL heritage_db 数据库

### 验证配置
```bash
python manage.py check
```
预期：System check identified no issues (0 silenced).

## 注意事项

1. 数据库密码已配置在 `settings.py` 中，生产环境应使用环境变量
2. SECRET_KEY 使用默认值，生产环境需更换
3. DEBUG 模式已开启，生产环境需关闭
4. 所有应用已创建基础结构，但模型、视图、序列化器等待后续实现

## 相关文档

- [实施计划](../memory-bank/implementation-plan.md)
- [架构文档](../memory-bank/architecture.md)
- [进度记录](../memory-bank/progress.md)
