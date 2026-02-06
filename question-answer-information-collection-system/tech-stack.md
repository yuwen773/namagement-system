# 项目技术栈说明文档

本文档详细描述了“网络问答平台信息采集系统”所采用的技术选型。选型依据来源于 PRD 文档中对数据采集、存储（10,000+条）、管理及可视化的需求。

## 1. 后端技术栈 (Backend)

*   **核心框架**: [Django 5.2](https://www.djangoproject.com/)
    *   **选择理由**: Django 提供了成熟的 ORM 和强大的管理后台（Admin），非常适合快速构建数据管理系统。其安全性（尽管本项目密码要求明文，但框架本身安全机制完善）和扩展性满足 1万+ 数据量的处理需求。
*   **API 框架**: [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
    *   **选择理由**: 用于构建标准化的 RESTful API，实现前后端分离。DRF 提供了强大的序列化器（Serializers）和视图集（ViewSets），能快速开发出供前端调用的数据接口。
*   **爬虫开发**: Python `requests` + `BeautifulSoup4` (或 `lxml`)
    *   **选择理由**: 针对 360问答 这种静态或轻量动态网页，使用 `requests` 进行 HTTP 请求，配合 `BS4` 解析 HTML 是最轻量且高效的方案。便于集成到 Django 的自定义 Command 或后台任务中。

## 2. 前端技术栈 (Frontend)

*   **核心框架**: [Vue 3](https://vuejs.org/) (Composition API)
    *   **选择理由**: 现代化的前端框架，响应式性能好，配合 Composition API 代码组织更清晰，适合构建单页应用 (SPA)。
*   **UI 组件库**: [Element Plus](https://element-plus.org/)
    *   **选择理由**: 基于 Vue 3 的企业级组件库，提供了丰富的表格、表单、弹窗等组件，能极大地减少管理端页面的开发工作量，符合“最少前端页面”的开发原则。
*   **数据可视化**: [ECharts](https://echarts.apache.org/)
    *   **选择理由**: 百度开源的强大可视化库，支持词云、折线图、柱状图等多种图表，满足 PRD 中对“热门话题词云”、“趋势图”等可视化需求。
*   **CSS 框架**: [Tailwind CSS](https://tailwindcss.com/)
    *   **选择理由**: 实用优先的 CSS 框架，能快速实现响应式布局和自定义样式，无需编写大量传统 CSS 代码，提高开发效率。
*   **构建工具**: [Vite](https://vitejs.dev/)
    *   **选择理由**: 极速的开发服务器启动和热更新体验。

## 3. 数据库 (Database)

*   **数据库系统**: [MySQL 8.0+](https://www.mysql.com/)
    *   **选择理由**: 
        *   **成熟稳定**: 业界标准的关系型数据库，完全满足 10,000+ 条数据的存储需求。
        *   **性能**: 配合 Django ORM 的索引优化，能保证秒级查询响应。
        *   **兼容性**: Django 对 MySQL 支持极佳。

## 4. 开发环境建议 (Dev Environment)

*   **Python**: 3.10+
*   **Node.js**: 18.0+ (LTS)
*   **包管理**:
    *   Python: `pip` / `poetry`
    *   Frontend: `npm` / `pnpm` / `yarn`

## 5. 架构图示 (简述)

```mermaid
graph LR
    User[用户/管理员] --> Frontend[前端 (Vue 3 + Element Plus)]
    Frontend -- REST API --> Backend[后端 (Django + DRF)]
    Backend -- ORM --> DB[(MySQL 数据库)]
    Backend -- Crawling --> Target[360问答网站]
```
