# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-29

---

## 系统架构

```
前端层 (Vue 3)
    │ HTTP/JSON (REST API)
    ▼
API 网关层 (Django) - 认证/权限/统一响应
    │
    ▼
业务逻辑层 (Django Apps)
    │ ORM
    ▼
数据层 (MySQL 8.0+)
```

---

## 技术栈

| 层级 | 技术选型 |
|:-----|:---------|
| 前端 | Vue 3 + Vite + Element Plus + Tailwind CSS + ECharts + Pinia + Axios |
| 后端 | Django 5.2 + DRF + JWT + Pandas + NumPy |
| 数据库 | MySQL 8.0+ (utf8mb4) |

---

## 数据库设计

### 核心表结构

| 表名 | 说明 | 记录数 |
|:-----|:-----|:-------:|
| users / user_profiles | 用户账户与资料 | 100+ |
| categories | 分类（菜系/场景/难度/口味） | 50+ |
| ingredients | 食材库 | 500+ |
| recipes | 菜谱主表 | 10,000-20,000 |
| recipe_ingredients | 菜谱-食材关联 | 50,000+ |
| recipe_steps | 制作步骤 | 30,000+ |
| user_favorites | 用户收藏 | 5,000+ |
| user_behavior_logs | 行为日志 | 10,000+ |

### 核心关系

```
users (1:1) user_profiles
  │
  ├─ (1:N) user_favorites (N:1) recipes
  │                                    │
  └─ (1:N) user_behavior_logs ────────┘
                                        │
                    ┌───────────────────┼───────────────┐
                    ▼                   ▼               ▼
            recipe_ingredients    recipe_steps    categories
                    │
                    ▼
              ingredients
```

---

## 后端架构

```
backend/
├── config/          # Django 主配置
├── utils/           # 统一响应/异常/分页
├── accounts/        # 认证模块
├── recipes/         # 菜谱模块
├── categories/      # 分类模块
├── ingredients/     # 食材模块
├── favorites/       # 收藏模块
├── analytics/       # 数据分析（用户）
├── admin_panel/     # 管理员模块
└── behavior_logs/   # 行为日志
```

### 数据脚本架构

```
data-scripts/
├── spiders/         # 爬虫脚本
│   └── recipe_spider.py      # 从下厨房、美食杰爬取菜谱数据
├── cleaning/        # 数据清洗
│   └── clean_recipes.py       # 去重、补全缺失、统一格式
├── importing/       # 数据导入
│   └── import_recipes.py      # 批量导入数据库
└── simulation/      # 行为模拟
    ├── simulate_users.py      # 生成模拟用户
    ├── simulate_behaviors.py  # 生成行为数据
    └── simulate_page_visits.py # 生成访问路径
```

**执行流程**：爬取数据 → 清洗数据 → 导入数据库 → 模拟行为

**文件作用**：
- `spiders/`：目标网站（下厨房、美食杰），爬取菜谱名称、食材、步骤、图片
- `cleaning/`：去除重复、补全缺失字段、统一难度/时长/单位格式
- `importing/`：批量插入（bulk_create）、处理外键关联、生成点击/收藏量
- `simulation/`：生成100+用户、20-100条行为/用户、时间分布过去30天

### API 规范

- 前缀: `/api/`
- 响应: `{ code, message, data }`
- 分页: `page`, `page_size` (max 100)
- 认证: JWT (24h)

---

## 前端架构

```
frontend/
├── src/
│   ├── components/    # 公共组件
│   ├── views/         # 页面组件
│   ├── api/           # API 服务层
│   ├── stores/        # Pinia 状态管理
│   └── router/        # 路由配置
```

### 路由设计

```
/                           # 首页
/login, /register           # 认证
/recipes, /recipes/:id      # 菜谱
/favorites                  # 收藏
/analytics                  # 数据概览
/admin/*                    # 管理后台
```

---

## 部署架构

**开发环境**: Vite (5173) → Django (8000) → MySQL (3306)

**生产环境**: Nginx → Gunicorn/Django → MySQL

---

## 权限模型

| 角色 | 权限 |
|:-----|:-----|
| user | 浏览/搜索/收藏菜谱，查看只读统计 |
| admin | 用户管理，菜谱/分类/食材 CRUD，深度分析 |

---

## 数据可视化

**用户端**: 菜系分布、难度统计、口味偏好、食材频率

**管理端**: 概览指标、趋势图表、用户行为分析（DAU/WAU/MAU、转化漏斗）
