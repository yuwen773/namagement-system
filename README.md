# Management System

多业务管理系统项目仓库，基于现代 Web 技术栈构建，涵盖企业人力资源、食堂运营、汽车配件销售、电商数据采集等多个业务领域。

## 技术栈概览

| 领域 | 后端技术 | 前端技术 |
|:-----|:---------|:---------|
| **HRMS** | Django 5.2 + DRF + MySQL | Vue 3.5 + Vite + Element Plus |
| **食堂管理** | Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts |
| **菜谱分析** | Python + Flask/FastAPI | Vue 3 + ECharts |
| **汽配销售** | Django 5.2 + DRF + MySQL | Vue 3 + Element Plus |
| **天猫采集** | Django 5.2 + DRF + Scrapy + Celery | Vue 3 + Element Plus + ECharts |
| **问答采集** | Django + DRF + MySQL | Vue 3 + Element Plus |

---

## 项目结构

```
management-system/
├── Enterprise-HRMS/                        # 企业 HRMS 系统
│   ├── backend/                            # Django 后端 (端口 8000)
│   ├── frontend/                           # Vue 3 前端 (端口 5173)
│   └── sql/                                # 数据库脚本
│
├── canteen-management-system/              # 食堂管理系统
│   ├── backend/                            # Django 后端
│   ├── frontend/                           # Vue 3 前端
│   └── sql/                                # 数据库脚本
│
├── recipe-data-analysis-system/            # 菜谱数据分析系统
│   ├── backend/                            # Python 后端
│   ├── frontend/                           # Vue 前端
│   └── data-scripts/                        # 数据爬取脚本
│
├── car-parts-sales-platform/               # 汽配销售平台
│   ├── backend/                            # Django 后端 (端口 8000)
│   └── frontend/                           # Vue 3 前端
│
├── tmall-collecting-platform/              # 天猫潮玩电商数据采集系统
│   ├── backend/                            # Django 后端 (端口 8000)
│   │   ├── crawler/                         # Scrapy + Playwright 爬虫
│   │   └── products/users/                  # Django 应用
│   └── frontend/                            # Vue 3 前端
│
└── question-answer-information-collection-system/  # 问答信息采集系统
    ├── backend/                            # Django 后端
    └── frontend/                           # Vue 3 前端
```

---

## 子项目

### Enterprise HRMS

企业人力资源管理系统 - 现代化人事管理平台。

| 特性 | 说明 |
|:-----|:-----|
| **数据驱动** | 部门-岗位-员工-考勤-薪资层层关联 |
| **可视化** | ECharts 驾驶舱视图，直观呈现运营数据 |
| **审批流** | 请假/加班在线审批 |
| **自动化** | 薪资、考勤自动核算 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Vue 3.5 + Vite + Element Plus + ECharts | JWT

**功能模块**: 用户认证、组织架构、员工档案、考勤管理、审批中心、薪资管理、公告管理、绩效管理、数据中心

详细文档: [Enterprise-HRMS/README.md](Enterprise-HRMS/README.md)

---

### Canteen Management System

食堂管理与排班系统 - 专为食堂行业定制的人力资源与运营管理。

| 特性 | 说明 |
|:-----|:-----|
| **行业定制** | 针对厨师、面点师、切配工等特殊岗位管理 |
| **资质管理** | 健康证、厨师等级证有效期追踪 |
| **排班系统** | 周/月排班计划、日历视图、调班审核 |
| **食堂主题** | 暖色调配色方案 |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts + Vite + Pinia

**功能模块**:

| 管理员端 | 员工端 |
|:---------|:-------|
| 仪表盘、人员档案 | 今日排班、快捷入口 |
| 排班管理、考勤管理 | 签到/签退、考勤查询 |
| 请假审批、薪资管理 | 请假申请、调班申请 |
| 统计分析、系统管理 | 薪资查询、密码修改 |

详细文档: [canteen-management-system/README.md](canteen-management-system/README.md)

---

### Recipe Data Analysis System

菜谱数据采集与分析系统 - 爬取、清洗、分析菜谱数据。

| 特性 | 说明 |
|:-----|:-----|
| **数据采集** | 自动化爬取菜谱数据 |
| **数据清洗** | 结构化处理与存储 |
| **可视化分析** | 营养成分、菜系分布等图表 |

**技术栈**: Python 后端 | Vue 前端 | ECharts 可视化

**功能模块**: 菜谱爬取、数据清洗、可视化分析、API 服务

---

### Car Parts Sales Platform

汽车改装件销售推荐平台 - 汽车配件在线销售与管理系统，支持个性化推荐。

| 特性 | 说明 |
|:-----|:-----|
| **商品管理** | 配件分类、库存管理、产品状态工作流 |
| **订单系统** | 订单状态机、购物车、售后服务 |
| **个性化推荐** | 热门/新品/个性化/分类推荐规则 |
| **营销工具** | 优惠券、满减活动 |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus | JWT

**后端模块**: users, products, orders, marketing, recommendations, content, system

**状态**: Phase 5 (API 文档完善中) | Swagger: http://localhost:8000/swagger/

详细文档: [car-parts-sales-platform/CLAUDE.md](car-parts-sales-platform/CLAUDE.md)

---

### Tmall Collecting Platform

天猫潮玩电商数据采集系统 - 天猫平台潮玩/手办商品数据采集与可视化分析。

| 特性 | 说明 |
|:-----|:-----|
| **数据采集** | Scrapy + Playwright 混合爬虫 |
| **异步任务** | Celery + Redis 任务队列 |
| **可视化** | 价格趋势、销售分布、商品对比 |
| **数据管理** | 商品库、历史价格追踪 |

**技术栈**: Django 5.2 + DRF + MySQL | Scrapy + Playwright | Celery + Redis | Vue 3 + Element Plus + ECharts

**功能模块**: 商品采集、价格监控、数据分析、任务调度

详细文档: [tmall-collecting-platform/CLAUDE.md](tmall-collecting-platform/CLAUDE.md)

---

### Q&A Information Collection System

问答信息采集系统 - 360 问答数据采集与管理平台。

| 特性 | 说明 |
|:-----|:-----|
| **数据采集** | 自动化爬取问答数据 |
| **数据管理** | MySQL 持久化存储 |
| **后台管理** | Vue + Element Plus 管理界面 |
| **可视化** | 数据统计与分析图表 |

**技术栈**: Django + DRF + MySQL | Vue 3 + Element Plus

**状态**: 规划阶段 - 文档完成，待开发

详细文档: [question-answer-information-collection-system/CLAUDE.md](question-answer-information-collection-system/CLAUDE.md)

---

## 快速启动

### 环境要求

- **Python**: 3.10 ~ 3.12
- **Node.js**: 16.x 或更高
- **MySQL**: 8.0 (端口 3306 或 3307)
- **Redis**: 6.x+ (用于 Celery 任务队列)

### 启动项目

```bash
# HRMS 系统
cd Enterprise-HRMS/backend && pip install -r requirements.txt && python manage.py runserver
cd Enterprise-HRMS/frontend && npm install && npm run dev

# 食堂管理系统
cd canteen-management-system/backend && pip install -r requirements.txt && python manage.py runserver
cd canteen-management-system/frontend && npm install && npm run dev

# 汽配销售平台
cd car-parts-sales-platform/backend && pip install -r requirements.txt && python manage.py runserver
cd car-parts-sales-platform/frontend && npm install && npm run dev

# 天猫采集平台
cd tmall-collecting-platform/backend && pip install -r requirements.txt && python manage.py runserver
cd tmall-collecting-platform/frontend && npm install && npm run dev
```

---

## License

MIT
