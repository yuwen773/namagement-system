# 旅游景点推荐系统

基于 Django + Vue 3 的智能化旅游景点推荐平台，提供个性化景点推荐、评论管理和数据统计功能。

## 功能特点

### 用户端
- 个性化推荐 - 基于用户偏好智能推荐景点
- 景点浏览 - 支持分类筛选和关键词搜索
- 评论评分 - 发表评论并为景点评分
- 收藏管理 - 收藏喜欢的景点
- 消息通知 - 接收系统公告和互动通知

### 管理端
- 数据看板 - 可视化统计图表和热门排行
- 用户管理 - 查看/禁用/启用用户账号
- 景点管理 - 景点信息CRUD
- 评论审核 - 审核用户评论
- 公告发布 - 发布系统公告

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.2 + DRF + MySQL |
| 前端 | Vue 3 + Element Plus + Pinia |
| 认证 | JWT (Access: 2h, Refresh: 7d) |

## 项目结构

```
tourist-attraction-recommendation-system/
├── backend/                    # Django 后端
│   ├── apps/
│   │   ├── accounts/           # 账号管理
│   │   ├── attractions/        # 景点管理
│   │   ├── comments/           # 评论收藏
│   │   ├── notifications/      # 消息通知
│   │   ├── stats/              # 数据统计
│   │   └── recommendations/    # 推荐算法
│   ├── sql/
│   │   └── init_db.sql         # 数据库初始化脚本
│   └── requirements.txt
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── api/                # API 接口封装
│   │   ├── components/         # 公共组件
│   │   ├── views/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   └── stores/             # Pinia 状态管理
│   └── package.json
└── README.md
```

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd tourist-attraction-recommendation-system
```

### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
> 可以使用 清华大学的镜像安装源
>pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
# 配置数据库
# 创建 MySQL 数据库: tourist_attraction_db
mysql -u root -p < sql/init_db.sql

# 运行迁移
python manage.py migrate

# 启动服务
python manage.py runserver 8123
```

后端服务运行在 `http://127.0.0.1:8000`

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务运行在 `http://localhost:5173`

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 普通用户 | user | user123 |

## API 文档

启动后端服务后，访问 Swagger 文档：
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`

### 主要 API 端点

| 端点 | 描述 |
|------|------|
| `/api/accounts/register/` | 用户注册 |
| `/api/accounts/login/` | 用户登录 |
| `/api/attractions/` | 景点列表 |
| `/api/comments/` | 评论管理 |
| `/api/favorites/` | 收藏管理 |
| `/api/notifications/` | 通知管理 |
| `/api/statistics/` | 数据统计 |
| `/api/recommendations/` | 推荐服务 |

## 推荐算法

### 热度计算
```
热度值 = (浏览量 × 0.2) + (评论数 × 0.3) + (平均评分 × 浏览量 × 0.5)
```

### 推荐策略
- **冷启动**: 新用户推荐热门景点
- **个性化**: 基于收藏/评分推荐同类景点
- **相似景点**: 同类别+同地区优先

## 开发规范

- 遵循 CLAUDE.md 中的项目规范
- API 响应格式: `{ code: 0, data: {...}, total: n }`
- 使用中文字段命名
- 前端页面使用 `frontend-design` skill 设计

## 文档

- [产品需求文档](./memory-bank/PRD.md)
- [系统架构](./memory-bank/architecture.md)
- [实施计划](./memory-bank/IMPLEMENTATION_PLAN.md)
- [进度追踪](./memory-bank/progress.md)

## 许可证

MIT License
