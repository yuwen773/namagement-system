# 食堂管理系统技术栈文档 (Tech Stack)

## 1. 后端技术栈 (Backend)
后端采用 Python 生态中成熟稳健的框架，确保业务逻辑的高效开发与维护。

*   **框架**: **Django 5.2**
    *   利用其内置的 Admin 管理后台进行快速原型开发。
    *   强大的 ORM 系统，简化数据库操作。
*   **API 框架**: **Django REST Framework (DRF)**
    *   构建标准化的 RESTful API 接口。
    *   提供完善的序列化器 (Serializers) 和视图集 (ViewSets)。
*   **数据库**: **MySQL**
    *   用于持久化存储人员档案、排班、考勤及薪资数据。
*   **开发说明**: 
    *   开发阶段密码采用 **明文存储**。
    *   环境建议：Python 3.10+。

## 2. 前端技术栈 (Frontend)
前端采用主流的 Vue 生态体系，打造流畅的用户交互体验。

*   **核心框架**: **Vue 3 (Composition API)**
    *   利用组合式 API 提升代码的可复用性与逻辑组织。
*   **UI 组件库**: **Element Plus**
    *   提供丰富的 UI 组件，快速构建后台管理界面。
    *   适配响应式设计，兼顾 PC 端与移动端（员工端）访问。
*   **数据可视化**: **ECharts**
    *   用于“综合统计分析”模块，实现人员分布、考勤率、薪资趋势等可视化图表。
*   **构建工具**: **Vite**
    *   极速的热更新开发体验。

## 3. 核心依赖
| 类别 | 依赖项 | 用途 |
| :--- | :--- | :--- |
| 后端 | `django>=5.2` | 核心 Web 框架 |
| 后端 | `djangorestframework` | API 构建 |
| 后端 | `mysqlclient` 或 `pymysql` | 数据库驱动 |
| 前端 | `vue@latest` | 前端框架 |
| 前端 | `element-plus` | UI 库 |
| 前端 | `echarts` | 图表库 |
| 前端 | `axios` | 异步请求 |

## 4. 部署与环境
*   **开发环境**: Windows / macOS / Linux
*   **数据库**: MySQL 8.0+
*   **前端环境**: Node.js 18+
