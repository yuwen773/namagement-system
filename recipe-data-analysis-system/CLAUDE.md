# CLAUDE.md

指导 Claude Code 在此仓库中工作。

---

## IMPORTANT

- 编码前必读 `memory-bank/architecture.md`（含完整数据库结构）
- 编码前必读 `memory-bank/PRD.md`
- 完成重大功能后更新 `memory-bank/architecture.md`

---

## 项目

**菜谱数据分析系统** - 10,000-20,000 菜谱记录，数据可视化 + 行为分析 + 管理后台

**技术栈**: Django 5.2 + DRF | Vue 3 + Element Plus + Tailwind | MySQL 8.0+ | ECharts | JWT

---

## 开发规范

### 后端 API（严格遵循 `backend-api-standards.md`）

**响应格式**:
```json
{ "code": 200, "message": "操作成功", "data": {} }
```

**异常**: `BusinessError`, `ValidationError`, `NotFoundError`, `PermissionDeniedError`

**分页**: `page`, `page_size` (默认 20, 最大 100)

**路由**: `/api/{module}/{resource}/`，自定义动作用 kebab-case

**序列化器命名**: `RecipeSerializer` | `RecipeListSerializer` | `RecipeCreateSerializer` | `RecipeUpdateSerializer`

### 模块命名

- Django apps: 小写复数 (`recipes`, `categories`, `analytics`)
- 路由: `/api/recipes/{id}/favorite/`

---

## 数据库

**核心表**: users, user_profiles, categories, ingredients, recipes, recipe_ingredients, recipe_steps, user_favorites, user_behavior_logs

初始化: `mysql -u root -p < init.sql`

---

## 命令

**后端**:
```bash
python manage.py runserver      # 开发服务器
python manage.py makemigrations # 迁移
python manage.py migrate
```

**前端**:
```bash
npm run dev    # 开发服务器
npm run build  # 构建
```

---

## 权限模型

| 角色 | 权限 |
|:-----|:-----|
| user | 浏览/搜索/收藏菜谱，查看只读统计 |
| admin | 用户管理、菜谱 CRUD、分类/食材管理、深度分析 |

---

## 数据可视化

**用户端**: 菜系分布(饼图)、难度统计(柱状图)、口味偏好(雷达图)、食材频率(词云)

**管理端**: 概览指标、趋势图、用户行为分析(DAU/WAU/MAU、转化漏斗)

---

## 性能要求

搜索 < 500ms | 详情页 < 1s | 大盘 < 2s | 100+ 并发

---

## 重要文档

| 文档 | 用途 |
|:-----|:-----|
| `memory-bank/architecture.md` | 架构设计 |
| `memory-bank/PRD.md` | 产品需求 |
| `implementation-plan.md` | 实施计划(22阶段) |
| `backend-api-standards.md` | 后端开发标准 |
| `init.sql` | 数据库初始化 |
