# Management System

多业务管理系统项目仓库，包含企业人力资源、食堂管理、菜谱数据分析等业务模块。

## 项目结构

```
management-system/
├── Enterprise-HRMS/              # 企业 HRMS 系统
│   ├── backend/                  # Django 后端
│   ├── frontend/                 # Vue 3 前端
│   ├── docs/                     # 项目文档
│   ├── memory-bank/              # 开发记忆库
│   └── sql/                      # 数据库脚本
│
├── canteen-management-system/    # 食堂管理系统
│   ├── backend/                  # Django 后端
│   ├── frontend/                 # Vue 前端
│   ├── memory-bank/              # 开发记忆库
│   └── sql/                      # 数据库脚本
│
└── recipe-data-analysis-system/  # 菜谱数据分析系统
    ├── backend/                  # Python 后端
    ├── frontend/                 # 前端界面
    ├── data-scripts/             # 数据爬取脚本
    ├── docs/                     # 项目文档
    └── memory-bank/              # 开发记忆库
```

## 子项目

### Enterprise HRMS

基于 Django + Vue 3 的人力资源管理系统。

- **后端**: Django 5.2 + Django REST Framework + MySQL
- **前端**: Vue 3 + Element Plus + ECharts
- **功能**: 用户认证、组织架构、考勤管理、薪资计算、审批流程、绩效管理、数据中心

详细文档请参考 [Enterprise-HRMS/README.md](Enterprise-HRMS/README.md)。

### Canteen Management System

食堂管理与排班系统。

- **后端**: Django + Django REST Framework
- **前端**: Vue 3
- **功能**: 员工管理、排班管理、考勤管理、数据分析

### Recipe Data Analysis System

菜谱数据采集与分析系统。

- **后端**: Python
- **前端**: Web 界面
- **功能**: 菜谱爬取、数据清洗、可视化分析、API 服务

详细文档请参考 [recipe-data-analysis-system/README.md](recipe-data-analysis-system/README.md)。

## License

MIT
