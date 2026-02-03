# 技术栈说明书 (Technology Stack)

本文档详细说明了“汽车改装件销售推荐平台”所采用的核心技术组件及版本要求。

## 1. 后端技术栈 (Backend)

| 组件 | 名称 | 版本要求 | 说明 |
| :--- | :--- | :--- | :--- |
| **Web 框架** | **Django** | 5.2+ | 提供核心业务逻辑、ORM 及管理后台功能。 |
| **API 框架** | **Django REST Framework** | Latest | 用于构建标准化的 RESTful API，前后端分离通信基础。 |
| **数据库** | **MySQL** | 8.0+ | 关系型数据库，存储用户信息、商品、订单等核心数据。 |

## 2. 前端技术栈 (Frontend)

| 组件 | 名称 | 版本要求 | 说明 |
| :--- | :--- | :--- | :--- |
| **核心框架** | **Vue.js** | 3.x | 渐进式 JavaScript 框架，采用 Composition API 进行开发。 |
| **UI 组件库** | **Element Plus** | Latest | 基于 Vue 3 的桌面端组件库，用于快速构建美观的后台及用户界面。 |
| **数据可视化** | **ECharts** | Latest | 用于营销统计、交易分析等图表展示。 |
| **CSS 框架** | **Tailwind CSS** | Latest | 实用优先（Utility-first）的 CSS 框架，用于灵活定制页面样式。 |

## 3. 开发环境建议

- **Python**: 3.10+ (适配 Django 5.x)
- **Node.js**: LTS (18+ / 20+)
- **包管理**:
    - Python: `pip` / `poetry` / `uv`
    - Node: `npm` / `pnpm` / `yarn`
