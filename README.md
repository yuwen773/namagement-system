# Management System

企业人力资源管理系统项目仓库。

## 项目结构

```
management-system/
└── Enterprise-HRMS/          # 企业 HRMS 系统
    ├── backend/              # Django 后端
    ├── frontend/             # Vue 3 前端
    ├── docs/                 # 项目文档
    ├── memory-bank/          # 开发记忆库
    └── sql/                  # 数据库脚本
```

## 子项目

### Enterprise HRMS

基于 Django + Vue 3 的人力资源管理系统，包含：

- **后端**: Django 5.2 + Django REST Framework + MySQL
- **前端**: Vue 3 + Element Plus + ECharts
- **功能**: 用户认证、组织架构、考勤管理、薪资计算、审批流程、绩效管理、数据中心

详细文档请参考 [Enterprise-HRMS/README.md](Enterprise-HRMS/README.md)。

## License

MIT
