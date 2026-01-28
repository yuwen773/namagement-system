# 食堂管理系统 - 架构文档

> 本文档说明项目架构和各文件作用，供开发者理解系统结构

---

## 项目总体结构

```
canteen-management-system/
├── backend/               # Django 后端项目
│   ├── config/           # Django 项目配置
│   ├── accounts/         # 用户账号与认证
│   ├── employees/        # 员工档案管理
│   ├── schedules/        # 排班管理
│   ├── attendance/       # 考勤管理
│   ├── leaves/           # 请假管理
│   ├── salaries/         # 薪资管理
│   ├── analytics/        # 统计分析
│   ├── static/           # 静态文件
│   ├── media/            # 媒体文件
│   └── manage.py         # 命令行工具
├── frontend/             # Vue 3 前端项目
├── sql/                  # 数据库参考脚本
├── memory-bank/          # 文档仓库
├── .gitignore
└── CLAUDE.md             # AI 开发指南
```

---

## 后端架构

### 核心设计原则

1. **模块化设计**：每个应用对应一个业务领域
2. **API 优先**：Django REST Framework 构建 RESTful API
3. **前后端分离**：通过 CORS 通信
4. **业务分离**：User（登录账号）与 EmployeeProfile（员工档案）独立

### 应用职责划分

| 应用 | 职责 | 主要模型 |
|------|------|---------|
| `accounts` | 用户登录、注册、认证 | User |
| `employees` | 员工档案管理 | EmployeeProfile |
| `schedules` | 排班计划、调班申请 | Shift, Schedule, ShiftSwapRequest |
| `attendance` | 签到/签退、考勤记录 | AttendanceRecord |
| `leaves` | 请假申请、审批 | LeaveRequest |
| `salaries` | 薪资计算、申诉 | SalaryRecord, Appeal |
| `analytics` | 数据统计（无模型） | - |

---

## 核心业务模型

### User（登录账号）
```python
username       # 登录账号（唯一）
password       # 密码（开发阶段明文）
employee_id    # 关联员工档案（可选）
role           # ADMIN/EMPLOYEE
status         # ENABLED/DISABLED
```

### EmployeeProfile（员工档案）
```python
# 基础信息
name, gender, phone, id_card, address
# 岗位信息
position (CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER)
entry_date, status (ACTIVE/INACTIVE/LEAVE_WITHOUT_PAY)
# 资质证书
health_certificate_no, health_certificate_expiry
chef_certificate_level
```

### 考勤状态判断规则
- **缺卡**：无签到或无签退记录
- **迟到**：签到时间 > 班次开始 + 5分钟
- **早退**：签退时间 < 班次结束 - 5分钟
- **正常**：其他情况

### 薪资计算公式
```
日工资 = 月基本工资 ÷ 21.75
时薪 = 日工资 ÷ 8
加班费 = 时薪 × 1.5 × 加班小时数
岗位津贴 = CHEF(800)/PASTRY(700)/PREP(500)/CLEANER(300)/SERVER(400)/MANAGER(1000)
迟到扣款 = 20 × 迟到次数
缺卡扣款 = 50 × 缺卡次数
实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款 - 缺卡扣款
```

### 数据流
```
排班 → 考勤 → 薪资
```

---

## 前端架构

### 项目结构
```
frontend/src/
├── views/
│   ├── admin/       # 管理员端（Dashboard/员工/排班/考勤/请假/薪资/统计）
│   ├── employee/    # 员工端（首页/个人/签到/考勤/请假/调班/薪资）
│   └── auth/        # 登录/注册
├── api/             # API 请求封装
├── router/          # 路由配置
├── stores/          # Pinia 状态管理
└── components/      # 公共组件
```

### 核心技术栈
- **Vue 3** + **Vite** + **Element Plus** + **ECharts**
- **Axios** + **Vue Router** + **Pinia**

### UI 主题配色
| 用途 | 色值 |
|------|------|
| 主色 | #FF6B35（橙色） |
| 辅助色 | #F7C52D（黄）、#4CAF50（绿） |
| 背景色 | #FFF8F0（浅米色） |

---

## API 端点

| 模块 | 端点 | 说明 |
|------|------|------|
| accounts | `/api/accounts/login/` | 登录 |
| employees | `/api/employees/` | 员工 CRUD |
| schedules | `/api/schedules/schedules/batch_create/` | 批量排班 |
| attendance | `/api/attendance/clock_in/` | 签到 |
| leaves | `/api/leaves/{id}/approve/` | 审批请假 |
| salaries | `/api/salaries/salaries/generate/` | 生成薪资 |
| analytics | `/api/analytics/overview/` | 总览统计 |

---

## 重要文件

### 后端
- `settings.py` - 数据库、CORS、静态文件配置
- `urls.py` - API 路由配置
- `requirements.txt` - Python 依赖
- `manage.py` - Django 命令行工具

### 前端
- `vite.config.js` - API 代理配置
- `package.json` - 项目依赖
- `src/api/request.js` - Axios 实例配置
- `src/router/index.js` - 路由与导航守卫
- `src/stores/user.js` - 用户状态管理

---

## 开发工作流

```bash
# 后端
python manage.py makemigrations    # 创建迁移
python manage.py migrate           # 应用迁移
python manage.py runserver         # 启动服务器

# 前端
npm run dev                        # 启动开发服务器
npm run build                      # 构建生产版本
```

---

## 注意事项

1. **analytics 应用**：避免与 Python 内置 `statistics` 模块冲突
2. **数据库迁移**：始终使用 Django migrations，不直接执行 SQL
3. **密码存储**：开发阶段明文，生产环境需加密
4. **CORS 配置**：前端开发需配置跨域
5. **User vs EmployeeProfile**：员工档案与登录账号是两个独立概念
