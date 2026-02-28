# Management System

多业务管理系统项目仓库，基于现代 Web 技术栈构建，涵盖企业人力资源、食堂运营、汽车配件销售、电商数据采集、空气质量监测、能耗管理等多个业务领域。

## 项目总览

| 序号 | 项目名称 | 状态 | 技术栈 | 端口 |
|:----:|:---------|:-----|:-------|:-----|
| 1 | Enterprise-HRMS | Active | Django 5.2 + DRF + Vue 3.5 | 8000/5173 |
| 2 | Canteen Management | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 3 | Recipe Analysis | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 4 | Car Parts Sales | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 5 | Air Quality Data | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 6 | Energy Consumption | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 7 | Intangible Cultural Heritage | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 8 | Movie Prediction | Active | Django 5.2 + DRF + Vue 3 | 8000/5173 |
| 9 | Tourist Attraction | Active | Django 5.2 + DRF + Vue 3 | 8123/5173 |
| 10 | Tmall Collecting | Active | Django 5.2 + DRF + Scrapy + Vue 3 | 8000/5173 |
| 11 | Tmall Pet Collecting | Active | Django 5.2 + DRF + Scrapy + Vue 3 | 8000/5173 |

---

## 项目结构

```
management-system/
├── Enterprise-HRMS/                        # 企业 HRMS 系统
├── canteen-management-system/              # 食堂管理系统
├── recipe-data-analysis-system/            # 菜谱数据分析系统
├── car-parts-sales-platform/                # 汽车配件销售平台
├── air-quality-data-system/                 # 空气质量数据系统
├── energy-consumption-monitoring/           # 能耗监测管理系统
├── intangible-cultural-heritage-system/     # 非物质文化遗产系统
├── movie-prediction-visualization-system/  # 电影票房预测系统
├── tourist-attraction-recommendation-system/ # 旅游景点推荐系统
├── tmall-collecting-platform/              # 天猫潮玩电商数据采集系统
├── tmall-pet-collecting-platform/           # 天猫宠物电商数据采集系统
└── question-answer-information-collection-system/ # 问答信息采集系统
```

---

## 子项目详情

### 1. Enterprise HRMS

企业人力资源管理系统 - 现代化人事管理平台。

| 特性 | 说明 |
|:-----|:-----|
| **数据驱动** | 部门-岗位-员工-考勤-薪资层层关联 |
| **可视化** | ECharts 驾驶舱视图，直观呈现运营数据 |
| **审批流** | 请假/加班在线审批 |
| **自动化** | 薪资、考勤自动核算 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Vue 3.5 + Vite + Element Plus + ECharts | JWT

**功能模块**: 用户认证、组织架构、员工档案、考勤管理、审批中心、薪资管理、公告管理、绩效管理、数据中心

详细文档: [Enterprise-HRMS/CLAUDE.md](Enterprise-HRMS/CLAUDE.md)

---

### 2. Canteen Management System

食堂管理与排班系统 - 专为食堂行业定制的人力资源与运营管理。

| 特性 | 说明 |
|:-----|:-----|
| **行业定制** | 针对厨师、面点师、切配工等特殊岗位管理 |
| **资质管理** | 健康证、厨师等级证有效期追踪 |
| **排班系统** | 周/月排班计划、日历视图、调班审核 |
| **食堂主题** | 暖色调配色方案 (#FF6B35) |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts + Vite + Pinia

**功能模块**:

| 管理员端 | 员工端 |
|:---------|:-------|
| 仪表盘、人员档案 | 今日排班、快捷入口 |
| 排班管理、考勤管理 | 签到/签退、考勤查询 |
| 请假审批、薪资管理 | 请假申请、调班申请 |
| 统计分析、系统管理 | 薪资查询、密码修改 |

详细文档: [canteen-management-system/CLAUDE.md](canteen-management-system/CLAUDE.md)

---

### 3. Recipe Data Analysis System

菜谱数据采集与分析系统 - 爬取、清洗、分析菜谱数据。

| 特性 | 说明 |
|:-----|:-----|
| **数据采集** | 自动化爬取菜谱数据 |
| **数据清洗** | 结构化处理与存储 |
| **可视化分析** | 菜系分布、难度统计、口味偏好 |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts + Pandas

**功能模块**: accounts, recipes, categories, ingredients, favorites, analytics, admin_panel, behavior_logs

详细文档: [recipe-data-analysis-system/CLAUDE.md](recipe-data-analysis-system/CLAUDE.md)

---

### 4. Car Parts Sales Platform

汽车改装件销售推荐平台 - 汽车配件在线销售与管理系统，支持个性化推荐。

| 特性 | 说明 |
|:-----|:-----|
| **商品管理** | 配件分类、库存管理、产品状态工作流 |
| **订单系统** | 订单状态机、购物车、售后服务 |
| **个性化推荐** | 热门/新品/个性化/分类推荐规则 |
| **营销工具** | 优惠券、满减活动 |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + Tailwind CSS | JWT

**后端模块**: users, products, orders, marketing, recommendations, content, system

**状态**: Phase 5 - 后端已完成，前端开发中

详细文档: [car-parts-sales-platform/CLAUDE.md](car-parts-sales-platform/CLAUDE.md)

---

### 5. Air Quality Data System

空气质量数据监测与分析系统 - 全国空气质量数据采集与可视化平台。

| 特性 | 说明 |
|:-----|:-----|
| **全景可视化** | 全国空气质量地图时空分布展示 |
| **多维度分析** | 城市对比、相关性分析、趋势分析 |
| **智能防护** | 基于 AQI 的个性化健康防护建议 |
| **大批量导入** | 支持单次导入 10万+ 条记录 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Vue 3 + Element Plus + ECharts + Tailwind CSS

**功能模块**:

| 用户端 | 管理端 |
|:-------|:-------|
| 首页概览、城市详情 | 控制台、数据导入 |
| 历史数据查询、数据分析 | 数据管理、规则管理 |
| 防护指南、科普知识 | 用户管理、内容管理、系统日志 |

详细文档: [air-quality-data-system/CLAUDE.md](air-quality-data-system/CLAUDE.md)

---

### 6. Energy Consumption Monitoring System

能耗监测管理系统 - 建筑物与设备能耗实时监测与数据分析。

| 特性 | 说明 |
|:-----|:-----|
| **多能源类型** | 水、电、燃气计量 |
| **建筑层级** | 校区 -> 楼宇 -> 楼层 -> 房间 |
| **智能分析** | 日/月/年统计、同比/环比分析 |
| **异常告警** | 异常检测与实时告警 |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts + Pandas

**功能模块**: accounts, buildings, devices, energy, analysis, alarms, system

详细文档: [energy-consumption-monitoring/CLAUDE.md](energy-consumption-monitoring/CLAUDE.md)

---

### 7. Intangible Cultural Heritage System

非物质文化遗产管理系统 - 非遗项目与传承人数字化管理平台。

| 特性 | 说明 |
|:-----|:-----|
| **驾驶舱总览** | 统计卡片、世界地图分布、类别占比 |
| **数据导入** | Excel/CSV 批量导入与清洗 |
| **权限控制** | 管理员与普通用户双角色 |
| **数据关联** | Category → HeritageItem → Inheritor |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + TypeScript + Element Plus + ECharts + Tailwind CSS

**功能模块**: users, heritage, inheritors, categories, regions, dashboard, importer

详细文档: [intangible-cultural-heritage-system/CLAUDE.md](intangible-cultural-heritage-system/CLAUDE.md)

---

### 8. Movie Prediction Visualization System

电影票房预测与可视化系统 - 票房数据分析与趋势预测平台。

| 特性 | 说明 |
|:-----|:-----|
| **票房预测** | 线性回归/移动平均法预测 |
| **数据可视化** | 地域分布、类型偏好、时间走势 |
| **双角色系统** | 管理员(数据管理)与用户(浏览/预测) |
| **完整流程** | 影片管理 -> 票房录入 -> 预测分析 |

**技术栈**: Django 5.2 + DRF + MySQL | Vue 3 + Element Plus + ECharts + Scikit-learn

**功能模块**: accounts, movies, cinemas, boxoffice, prediction, visualization

详细文档: [movie-prediction-visualization-system/CLAUDE.md](movie-prediction-visualization-system/CLAUDE.md)

---

### 9. Tourist Attraction Recommendation System

旅游景点推荐系统 - 景点信息管理与个性化推荐平台。

| 特性 | 说明 |
|:-----|:-----|
| **个性化推荐** | 协同过滤算法 (Item-based CF / User-based CF) |
| **热度计算** | 浏览量、评论数、平均评分加权 |
| **评论评分** | 景点评分、评论审核、评论统计 |
| **双重角色** | 管理员与普通用户 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Vue 3 + Element Plus + ECharts + Tailwind CSS

**后端模块**: accounts, attractions, comments, notifications, stats, recommendations

详细文档: [tourist-attraction-recommendation-system/CLAUDE.md](tourist-attraction-recommendation-system/CLAUDE.md)

---

### 10. Tmall Collecting Platform

天猫潮玩电商数据采集系统 - 天猫平台潮玩/手办商品数据采集与可视化分析。

| 特性 | 说明 |
|:-----|:-----|
| **多层降级爬虫** | mtop API → 真实API → Playwright → 演示数据 |
| **异步任务** | Celery + Redis 任务队列 |
| **可视化** | 价格趋势、销售分布、品牌占比 |
| **数据规模** | 10,000+ 真实潮玩商品数据 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Scrapy + Playwright | Celery + Redis | Vue 3 + Element Plus + ECharts

**功能模块**: 商品采集、价格监控、数据分析、任务调度

详细文档: [tmall-collecting-platform/CLAUDE.md](tmall-collecting-platform/CLAUDE.md)

---

### 11. Tmall Pet Collecting Platform

天猫宠物电商数据采集系统 - 天猫平台宠物商品数据采集与可视化分析。

| 特性 | 说明 |
|:-----|:-----|
| **多层降级爬虫** | mtop API → 真实API → Playwright → 演示数据 |
| **异步任务** | Celery + Redis 任务队列 |
| **可视化** | 价格分布、销量排行、品牌统计 |
| **智能反爬** | 完整请求头、随机延迟、Cookie 管理 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Scrapy + Playwright | Celery + Redis | Vue 3 + Element Plus + ECharts

**功能模块**: 用户认证、商品管理、爬虫控制、数据可视化

详细文档: [tmall-pet-collecting-platform/CLAUDE.md](tmall-pet-collecting-platform/CLAUDE.md)

---

### 12. Q&A Information Collection System

问答信息采集系统 - 360 问答数据采集与管理平台。

| 特性 | 说明 |
|:-----|:-----|
| **双模式爬虫** | Scrapy 传统模式 + Playwright JS 渲染 |
| **异步任务** | Celery + Redis 后台执行 |
| **演示友好** | 默认采集 20 条快速演示 |
| **可视化** | 热门话题词云、问答趋势图 |

**技术栈**: Django 5.2 + DRF + MySQL (3307) | Scrapy + Playwright | Celery + Redis | Vue 3 + Element Plus + ECharts

**功能模块**: 认证管理、数据采集、数据管理、数据可视化、用户管理

详细文档: [question-answer-information-collection-system/CLAUDE.md](question-answer-information-collection-system/CLAUDE.md)

---

## 快速启动

### 环境要求

- **Python**: 3.10 ~ 3.12
- **Node.js**: 16.x 或更高
- **MySQL**: 8.0 (端口 3306 或 3307)
- **Redis**: 6.x+ (用于 Celery 任务队列)

### 通用启动命令

```bash
# 后端
cd <project>/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# 前端
cd <project>/frontend
npm install
npm run dev
```

### 各项目端口

| 项目 | 后端端口 | 前端端口 | 数据库端口 |
|:-----|:---------|:---------|:-----------|
| Enterprise-HRMS | 8000 | 5173 | 3307 |
| Canteen Management | 8000 | 5173 | 3306 |
| Recipe Analysis | 8000 | 5173 | 3306 |
| Car Parts Sales | 8000 | 5173 | 3306 |
| Air Quality | 8000 | 5173 | 3307 |
| Energy Consumption | 8000 | 5173 | 3306 |
| Intangible Heritage | 8000 | 5173 | 3306 |
| Movie Prediction | 8000 | 5173 | 3306 |
| Tourist Attraction | 8123 | 5173 | 3307 |
| Tmall Collecting | 8000 | 5173 | 3307 |
| Tmall Pet | 8000 | 5173 | 3307 |
| Q&A Collection | 8000 | 5173 | 3307 |

---

## 公共技术栈

### 后端

- **框架**: Django 5.2 + Django REST Framework
- **认证**: JWT (djangorestframework-simplejwt)
- **数据库**: MySQL 8.0+ (UTF8MB4)
- **任务队列**: Celery + Redis

### 前端

- **框架**: Vue 3.5 + Vite
- **UI**: Element Plus + Tailwind CSS
- **状态**: Pinia
- **图表**: ECharts

---

## License

MIT
