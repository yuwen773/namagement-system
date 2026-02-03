# Management System

多业务管理系统项目仓库，基于现代 Web 技术栈构建，涵盖企业人力资源、食堂运营、汽车配件销售等多个业务领域。

## 技术栈概览

| 领域 | 后端技术 | 前端技术 |
|:-----|:---------|:---------|
| **HRMS** | Django 5.2 + DRF + MySQL | Vue 3.5 + Vite + Element Plus |
| **食堂管理** | Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts |
| **菜谱分析** | Python + Flask/FastAPI | Vue 3 + ECharts |
| **汽配销售** | Django + DRF + MySQL | Vue 3 + Element Plus |

---

## 项目结构

```
management-system/
├── Enterprise-HRMS/                  # 企业 HRMS 系统
│   ├── backend/                      # Django 后端 (端口 8000)
│   ├── frontend/                     # Vue 3 前端 (端口 5173)
│   └── sql/                          # 数据库脚本
│
├── canteen-management-system/        # 食堂管理系统
│   ├── backend/                      # Django 后端
│   ├── frontend/                     # Vue 3 前端
│   └── sql/                          # 数据库脚本
│
├── recipe-data-analysis-system/      # 菜谱数据分析系统
│   ├── backend/                      # Python 后端
│   ├── frontend/                     # Vue 前端
│   └── data-scripts/                 # 数据爬取脚本
│
└── auto-parts-sales-platform/        # 汽配销售平台
    ├── backend/                      # Django 后端
    └── frontend/                     # Vue 前端
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

### Auto Parts Sales Platform

汽配销售平台 - 汽车配件在线销售与管理系统。

| 特性 | 说明 |
|:-----|:-----|
| **商品管理** | 配件分类、库存管理 |
| **订单系统** | 订单处理、状态追踪 |
| **客户管理** | 客户信息、联系记录 |

**技术栈**: Django + DRF + MySQL | Vue 3 + Element Plus

---

## 快速启动

### 环境要求

- **Python**: 3.10 ~ 3.12
- **Node.js**: 16.x 或更高
- **MySQL**: 8.0 (端口 3306 或 3307)

### 启动项目

```bash
# HRMS 系统
cd Enterprise-HRMS/backend && pip install -r requirements.txt && python manage.py runserver
cd Enterprise-HRMS/frontend && npm install && npm run dev

# 食堂管理系统
cd canteen-management-system/backend && pip install -r requirements.txt && python manage.py runserver
cd canteen-management-system/frontend && npm install && npm run dev
```

---

## License

MIT
