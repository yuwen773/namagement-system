# 校园智慧后勤能耗监测可视化系统 - 实施计划

## 计划概述

本计划遵循**后端优先**的开发策略：先完成后端开发和API接口文档，再进行前端开发。每个步骤都包含具体的测试验证方法。

架构约束：
1. 数据库采用 **MySQL 单体架构**（不引入 InfluxDB 等额外时序数据库）。
2. `pre-prd.md` 中提到的 InfluxDB 混合存储要求，在本项目统一落地为 MySQL 单体实现。
3. Spark 作为**可选增强**，不作为本期硬性验收门槛。
4. 同时满足 `pre-prd.md` 与 `PRD.md`，并通过需求追踪矩阵（RTM）和自动化测试/CI 进行验收。

决策冻结（本实施计划执行口径）：
1. 显式建模校区维度（Campus），与数据集 `campus_id` 对齐。
2. 角色体系采用 `ADMIN/USER` 两级，基于 `UserProfile.role` + 自定义权限类实现。
3. 充值仅做模拟支付，但必须写入充值记录并更新系统内账务数据。
4. 预测口径按数据集先落地“日粒度 + 7/30天 + campus/building/meter 维度”。
5. API 统一响应格式遵循技能规范（`code`、`data`、`message`、`total`）。
6. RTM 统一维护在 `docs/rtm.md`。
7. 监控大屏地图能力以 2D 为必做，3D 为可选增强。

---

# 第一阶段：项目初始化与基础设施

## 步骤 1.1：创建项目目录结构

### 操作说明
在项目根目录下创建以下目录结构（**注意：`frontend` 目录将在第七阶段使用 Vite 自动生成，此处无需手动创建**）：

```
energy-consumption-monitoring/
├── backend/                 # Django 后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── energy_monitoring/   # Django 项目配置目录
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── apps/                # 应用目录
│       ├── accounts/        # 用户认证
│       ├── buildings/       # 建筑档案
│       ├── devices/         # 设备管理
│       ├── energy/          # 能耗数据
│       ├── analysis/        # 数据分析
│       ├── alarms/          # 告警管理
│       └── system/          # 系统管理
├── frontend/                # Vue 前端（将在步骤 7.1 通过 npm create vite 生成）
├── sql/                     # 数据库脚本
│   └── init_db.sql
├── scripts/                 # 数据导入脚本
├── docs/                    # 接口文档
└── memory-bank/             # 项目文档
```

### 测试验证
- [ ] 所有目录均已创建
- [ ] 在各目录下创建 `__init__.py`（Python 包需要）
- [ ] 在终端中运行 `tree` 命令验证目录结构

---

## 步骤 1.2：配置后端虚拟环境

### 操作说明
1. 在 `backend/` 目录下创建 Python 虚拟环境
2. 安装 Django 5.2 和相关依赖

### 测试验证
- [ ] 虚拟环境激活成功
- [ ] 运行 `django-admin --version` 输出 5.2.x
- [ ] 运行 `python --version` 确保使用虚拟环境的 Python

---

## 步骤 1.3：配置 MySQL 数据库

### 操作说明
1. 安装 MySQL 8.0+
2. 创建数据库 `energy_monitoring`
3. 配置字符集为 UTF8MB4

### 测试验证
- [ ] MySQL 服务正在运行
- [ ] 数据库 `energy_monitoring` 已创建
- [ ] 运行 `SHOW CREATE DATABASE energy_monitoring;` 确认字符集为 utf8mb4

---

## 步骤 1.4：配置 Django 项目

### 操作说明
1. 创建 Django 项目 `energy_monitoring`
2. 配置 `settings.py`：
   - 设置 `DATABASES` 连接到 MySQL
   - 设置 `ALLOWED_HOSTS`
   - 配置 `INSTALLED_APPS` 包含 `rest_framework`、`corsheaders`
   - 配置时区为 `Asia/Shanghai`
3. 配置 `requirements.txt`

### 测试验证
- [ ] 运行 `python manage.py check` 无错误
- [ ] 运行 `python manage.py migrate` 初始迁移成功
- [ ] 运行 `python manage.py runserver` 访问 http://127.0.0.1:8000 显示 Django 欢迎页

---

## 步骤 1.5：工业协议采集环境准备（Modbus/BACnet）

### 操作说明
1. 确认采集网关方案（直连仪表或网关转发），整理点位映射（仪表ID -> 设备ID -> 房间）。
2. 准备 Modbus/BACnet 测试环境（真实设备或模拟器）。
3. 定义采集频率、超时重试、断线重连策略。

### 测试验证
- [ ] Modbus 模拟设备可被读取，返回稳定测点值
- [ ] BACnet 模拟设备可被读取，返回稳定测点值
- [ ] 断网后自动重连并恢复采集
- [ ] 采集数据字段与 `em_energy_data` 模型字段一致
- [ ] 在无实物设备场景下，使用协议模拟器也可完成验收

---

# 第二阶段：数据库设计与模型开发

## 步骤 2.1：设计数据库表结构

### 操作说明
在 `sql/init_db.sql` 中编写以下表结构：

**核心表清单**：
1. `em_users` - 用户表（继承 Django User 或自定义）
2. `em_roles` - 角色表（ADMIN、USER）
3. `em_campuses` - 校区表（与数据集 `campus_meta.csv` 对齐）
4. `em_buildings` - 建筑档案表（关联校区）
5. `em_floors` - 楼层表
6. `em_rooms` - 房间表
7. `em_energy_types` - 能源类型表（水、电、气）
8. `em_devices` - 设备台账表
9. `em_energy_data` - 能耗原始数据表
10. `em_energy_statistics` - 能耗统计表（日/月/年）
11. `em_alarms` - 告警记录表
12. `em_alarm_rules` - 告警规则表
13. `em_bills` - 账单表
14. `em_recharge_records` - 充值记录表
15. `em_notices` - 通知公告表
16. `em_operation_logs` - 操作日志表
17. `em_energy_forecasts` - 能耗预测结果表（用于趋势预测）

### 测试验证
- [ ] SQL 文件语法正确（在 MySQL 中运行无语法错误）
- [ ] 所有表都包含 `id` 主键、`created_at`、`updated_at` 字段
- [ ] 外键关系正确建立
- [ ] 运行 `SHOW TABLES;` 显示所有表

---

## 步骤 2.2：创建 Django 应用

### 操作说明
在 `backend/apps/` 下创建以下应用：

```bash
python manage.py startapp accounts
python manage.py startapp buildings
python manage.py startapp devices
python manage.py startapp energy
python manage.py startapp analysis
python manage.py startapp alarms
python manage.py startapp system
```

### 测试验证
- [ ] 每个应用目录都有 `models.py`、`views.py`、`urls.py`、`serializers.py`
- [ ] 在 `settings.py` 的 `INSTALLED_APPS` 中注册所有应用
- [ ] 运行 `python manage.py check` 无错误

---

## 步骤 2.3：实现 accounts 应用模型

### 操作说明
在 `apps/accounts/models.py` 中定义：

1. **UserProfile 模型**：
   - `user` - OneToOneField 到 User
   - `phone` - 手机号
   - `avatar` - 头像
   - `role` - 角色选择（ADMIN/USER）
   - `bind_rooms` - 多对多关联房间（用户可绑定多个房间）

2. **扩展 Django User**：如需自定义用户模型，使用 AbstractUser

### 测试验证
- [ ] 运行 `python manage.py makemigrations accounts`
- [ ] 运行 `python manage.py migrate accounts`
- [ ] 在 Django Admin 中能看到 UserProfile 模型

---

## 步骤 2.4：实现 buildings 应用模型

### 操作说明
在 `apps/buildings/models.py` 中定义：

1. **Campus 模型**：
   - `name` - 校区名称
   - `code` - 校区编码（唯一）
   - `capacity` - 校区容量（可选）

2. **Building 模型**：
   - `campus` - ForeignKey 到 Campus
   - `name` - 建筑名称
   - `code` - 建筑编码（唯一）
   - `area_type` - 区域类型（教学区/生活区/办公区）
   - `address` - 地址
   - `floors_count` - 楼层数

3. **Floor 模型**：
   - `building` - ForeignKey 到 Building
   - `floor_number` - 楼层号
   - `name` - 楼层名称

4. **Room 模型**：
   - `floor` - ForeignKey 到 Floor
   - `room_number` - 房间号
   - `room_type` - 房间类型（宿舍/办公室/教室）
   - `area` - 面积（平方米）
   - `department` - 所属部门

### 测试验证
- [ ] 运行 makemigrations 和 migrate
- [ ] 在 Django Admin 中创建测试数据：1个校区 → 1栋楼 → 3层 → 每层5个房间
- [ ] 验证级联删除：删除建筑时，楼层和房间也被删除

---

## 步骤 2.5：实现 devices 应用模型

### 操作说明
在 `apps/devices/models.py` 中定义：

1. **EnergyType 模型**：
   - `name` - 能源名称（水/电/气）
   - `code` - 能源编码（WATER/ELECTRICITY/GAS）
   - `unit` - 计量单位
   - `icon` - 图标

2. **Device 模型**：
   - `device_id` - 设备ID（唯一，对应数据集中的设备标识）
   - `name` - 设备名称
   - `energy_type` - ForeignKey 到 EnergyType
   - `room` - ForeignKey 到 Room（可为空，室外设备）
   - `model` - 设备型号
   - `status` - 设备状态（在线/离线/故障）
   - `last_data_time` - 最后数据时间

### 测试验证
- [ ] 运行 makemigrations 和 migrate
- [ ] 创建3种能源类型（水、电、气）
- [ ] 创建测试设备并绑定到房间
- [ ] 验证设备能正确关联能源类型和房间

---

## 步骤 2.6：实现 energy 应用模型

### 操作说明
在 `apps/energy/models.py` 中定义：

1. **EnergyData 模型**（原始数据）：
   - `device` - ForeignKey 到 Device
   - `energy_type` - ForeignKey 到 EnergyType
   - `timestamp` - 时间戳（建立索引）
   - `value` - 读数
   - `voltage` - 电压（电表专用）
   - `current` - 电流（电表专用）
   - `power` - 功率（电表专用）
   - `flow_rate` - 流速（水表专用）

2. **EnergyStatistics 模型**（统计数据）：
   - `device` - ForeignKey 到 Device
   - `energy_type` - ForeignKey 到 EnergyType
   - `period_type` - 统计周期（DAY/MONTH/YEAR）
   - `period_date` - 统计日期
   - `total_value` - 总用量
   - `peak_value` - 峰值
   - `peak_time` - 峰值时间
   - `avg_value` - 平均值
   - `cost` - 费用

### 测试验证
- [ ] 运行 makemigrations 和 migrate
- [ ] 验证 timestamp 字段已建立索引
- [ ] 插入100条测试数据，查询响应时间 < 100ms

---

## 步骤 2.7：实现 alarms 应用模型

### 操作说明
在 `apps/alarms/models.py` 中定义：

1. **AlarmRule 模型**：
   - `name` - 规则名称
   - `energy_type` - ForeignKey 到 EnergyType
   - `condition_type` - 条件类型（阈值/突变）
   - `threshold_value` - 阈值
   - `is_active` - 是否启用

2. **Alarm 模型**：
   - `device` - ForeignKey 到 Device
   - `rule` - ForeignKey 到 AlarmRule
   - `alarm_type` - 告警类型（超限/突变/离线）
   - `alarm_value` - 告警时的值
   - `alarm_time` - 告警时间（建立索引）
   - `status` - 处理状态（待处理/已处理/已忽略）
   - `handler` - 处理人
   - `handle_time` - 处理时间
   - `remark` - 处理备注

### 测试验证
- [ ] 运行 makemigrations 和 migrate
- [ ] 创建测试规则：日用电量 > 100 kWh
- [ ] 创建测试告警记录
- [ ] 验证告警时间字段已建立索引

---

## 步骤 2.8：实现 system 应用模型（账单、通知、日志）

### 操作说明
在 `apps/system/models.py` 中定义：

1. **Bill 模型**：
   - `room` - ForeignKey 到 Room
   - `energy_type` - ForeignKey 到 EnergyType
   - `bill_period` - 账单周期（如：2024-01）
   - `usage` - 用量
   - `amount` - 金额
   - `status` - 状态（未支付/已支付）
   - `due_date` - 截止日期

2. **RechargeRecord 模型**：
   - `room` - ForeignKey 到 Room
   - `amount` - 充值金额
   - `payment_method` - 支付方式
   - `recharge_time` - 充值时间

3. **Notice 模型**：
   - `title` - 标题
   - `content` - 内容
   - `notice_type` - 类型（通知/公告/节能知识）
   - `priority` - 优先级
   - `publish_time` - 发布时间
   - `is_published` - 是否发布

4. **OperationLog 模型**：
   - `user` - ForeignKey 到 User
   - `action` - 操作类型
   - `resource` - 操作资源
   - `ip_address` - IP地址
   - `user_agent` - 用户代理
   - `create_time` - 操作时间

### 测试验证
- [ ] 运行 makemigrations 和 migrate
- [ ] 创建测试账单数据
- [ ] 创建测试通知数据
- [ ] 运行 `python manage.py showmigrations` 确认所有迁移已应用

---

## 步骤 2.9：创建数据库初始化脚本

### 操作说明
在 `sql/init_db.sql` 中编写：

1. 创建所有表的 SQL
2. 插入初始化数据：
   - 管理员账号（admin/admin123）
   - 示例校区数据（与 `campus_meta.csv` 对齐）
   - 3种能源类型
   - 示例建筑、楼层、房间数据
   - 示例设备数据
   - 示例告警规则

### 测试验证
- [ ] 在 MySQL 中运行 `source sql/init_db.sql`
- [ ] 验证管理员账号能登录 Django Admin
- [ ] 验证初始化数据已正确插入

---

# 第三阶段：后端 API 开发

## 步骤 3.1：配置 DRF 全局设置

### 操作说明
在 `settings.py` 中配置：

1. REST_FRAMEWORK 配置：
   - `DEFAULT_PAGINATION_CLASS` - 分页类
   - `PAGE_SIZE` - 每页10条
   - `DEFAULT_AUTHENTICATION_CLASSES` - JWT 认证
   - `DEFAULT_PERMISSION_CLASSES` - 默认权限
   - `DEFAULT_FILTER_BACKENDS` - 搜索过滤
   - 统一响应包装器与异常处理（确保返回 `code/data/message/total`）

2. 配置 JWT：
   - 使用 `djangorestframework-simplejwt`
   - Access Token 有效期：2小时
   - Refresh Token 有效期：7天

### 测试验证
- [ ] 运行 `python manage.py check` 无错误
- [ ] 创建测试视图验证分页生效
- [ ] 成功/失败响应都符合统一格式（含 `code` 与 `message` 字段）

---

## 步骤 3.2：实现 JWT 认证接口

### 操作说明
在 `apps/accounts/` 中实现：

1. **Serializers**：
   - `UserRegisterSerializer` - 用户注册
   - `UserLoginSerializer` - 用户登录（返回 JWT）
   - `UserSerializer` - 用户信息

2. **ViewSets**：
   - `AuthViewSet`：
     - `register` - 注册接口
     - `login` - 登录接口
     - `refresh` - 刷新 Token
     - `user_info` - 获取当前用户信息
     - `change_password` - 修改密码

3. **URL 配置**：
   - `/api/auth/register/` - POST
   - `/api/auth/login/` - POST
   - `/api/auth/refresh/` - POST
   - `/api/auth/user-info/` - GET
   - `/api/auth/change-password/` - POST

### 测试验证
- [ ] 使用 Postman/curl 测试注册接口，返回 201
- [ ] 测试登录接口，返回 access 和 refresh token
- [ ] 使用 access token 访问受保护接口，返回 200
- [ ] Token 过期后访问受保护接口，返回 401
- [ ] 使用 refresh token 获取新的 access token，返回 200

---

## 步骤 3.3：实现 buildings 应用 API

### 操作说明
在 `apps/buildings/` 中实现：

1. **Serializers**：
   - `CampusSerializer` - 校区序列化器
   - `BuildingSerializer` - 建筑序列化器（包含楼层嵌套）
   - `FloorSerializer` - 楼层序列化器（包含房间嵌套）
   - `RoomSerializer` - 房间序列化器
   - `BuildingTreeSerializer` - 树形结构序列化器

2. **ViewSets**：
   - `CampusViewSet`：
     - `list` - 校区列表
     - `retrieve` - 校区详情
   - `BuildingViewSet`：
     - `list` - 建筑列表（支持搜索、分页）
     - `retrieve` - 建筑详情
     - `create` - 创建建筑（管理员）
     - `update` - 更新建筑（管理员）
     - `destroy` - 删除建筑（管理员）
     - `tree` - 获取建筑树形结构（校区-楼宇-楼层-房间）

3. **Filters**：
   - 按区域类型过滤
   - 按建筑名称搜索

4. **URL 配置**：
   - `/api/campuses/` - GET
   - `/api/campuses/{id}/` - GET
   - `/api/buildings/` - GET/POST
   - `/api/buildings/{id}/` - GET/PUT/DELETE
   - `/api/buildings/tree/` - GET
   - `/api/floors/` - GET/POST
   - `/api/rooms/` - GET/POST

### 测试验证
- [ ] GET `/api/campuses/` 返回校区列表
- [ ] GET `/api/buildings/` 返回建筑列表，包含分页信息
- [ ] POST `/api/buildings/` 创建建筑（需要管理员权限）
- [ ] GET `/api/buildings/tree/` 返回完整的树形结构
- [ ] GET `/api/buildings/?search=教学楼` 返回搜索结果
- [ ] 未认证用户访问 POST 接口返回 401

---

## 步骤 3.4：实现 devices 应用 API

### 操作说明
在 `apps/devices/` 中实现：

1. **Serializers**：
   - `EnergyTypeSerializer` - 能源类型
   - `DeviceSerializer` - 设备信息
   - `DeviceDetailSerializer` - 设备详情（包含最新数据）

2. **ViewSets**：
   - `EnergyTypeViewSet` - 能源类型 CRUD
   - `DeviceViewSet` - 设备 CRUD
     - `list` - 设备列表（支持按房间、能源类型过滤）
     - `data_status` - 获取设备数据状态
     - `bind_room` - 绑定房间（管理员）

3. **URL 配置**：
   - `/api/energy-types/` - GET/POST
   - `/api/devices/` - GET/POST
   - `/api/devices/{id}/` - GET/PUT/DELETE
   - `/api/devices/data-status/` - GET
   - `/api/devices/{id}/bind-room/` - POST

### 测试验证
- [ ] GET `/api/energy-types/` 返回水、电、气三种类型
- [ ] POST `/api/devices/` 创建设备
- [ ] GET `/api/devices/?room_id=1` 返回指定房间的设备
- [ ] GET `/api/devices/?energy_type=ELECTRICITY` 返回所有电表
- [ ] 验证设备ID唯一性约束生效

---

## 步骤 3.5：实现 energy 应用 API（数据录入与查询）

### 操作说明
在 `apps/energy/` 中实现：

1. **Serializers**：
    - `EnergyDataSerializer` - 原始数据
    - `EnergyDataBatchSerializer` - 批量导入（CSV/Excel/JSON）
    - `EnergyStatisticsSerializer` - 统计数据

2. **ViewSets**：
   - `EnergyDataViewSet`：
     - `create` - 单条数据录入
      - `batch_import` - 批量导入
      - `list` - 数据列表（支持时间范围过滤）
      - `latest` - 获取最新数据
      - `export` - 导出数据（支持 Excel/PDF）

3. **URL 配置**：
   - `/api/energy-data/` - GET/POST
   - `/api/energy-data/batch-import/` - POST
   - `/api/energy-data/latest/` - GET
   - `/api/energy-data/export/` - GET
   - `/api/energy-statistics/` - GET

### 测试验证
- [ ] POST `/api/energy-data/` 录入单条数据，返回 201
- [ ] POST `/api/energy-data/batch-import/` 上传CSV文件，成功导入100条数据
- [ ] POST `/api/energy-data/batch-import/` 上传JSON文件，成功导入100条数据
- [ ] GET `/api/energy-data/?device_id=1&start_date=2024-01-01&end_date=2024-01-31` 返回指定时间范围数据
- [ ] GET `/api/energy-data/latest/` 返回各设备最新读数
- [ ] GET `/api/energy-data/export/?format=excel` 导出 xlsx 文件成功
- [ ] GET `/api/energy-data/export/?format=pdf` 导出 pdf 文件成功
- [ ] 批量导入1000条数据，响应时间 < 3秒

---

## 步骤 3.6：实现 analysis 应用 API（统计分析）

### 操作说明
在 `apps/analysis/` 中实现：

1. **Serializers**：
   - 主要是响应数据的序列化，不需要模型序列化器

2. **ViewSets**：
   - `AnalysisViewSet`（只读，使用 `@action` 装饰器）：
     - `dashboard` - 大屏概览数据
       - 总能耗、平均功率、数据覆盖率
       - 告警数量统计
     - `trend` - 能耗趋势
       - 按日/月/年统计
       - 支持多设备聚合
     - `distribution` - 能耗分布
       - 按区域统计
       - 按能源类型统计
      - `ranking` - 能耗排名
        - Top10 楼宇/房间/部门
      - `comparison` - 同比环比分析
      - `forecast` - 趋势预测（近7天/30天）

3. **URL 配置**：
   - `/api/analysis/dashboard/` - GET
   - `/api/analysis/trend/` - GET
    - `/api/analysis/distribution/` - GET
    - `/api/analysis/ranking/` - GET
    - `/api/analysis/comparison/` - GET
    - `/api/analysis/forecast/` - GET

### 测试验证
- [ ] GET `/api/analysis/dashboard/` 返回大屏所需的全部指标数据
- [ ] GET `/api/analysis/trend/?period=day&device_id=1` 返回按日统计的趋势数据
- [ ] GET `/api/analysis/distribution/?type=area` 返回按区域分布的饼图数据
- [ ] GET `/api/analysis/ranking/?type=building&limit=10` 返回Top10建筑
- [ ] GET `/api/analysis/ranking/?type=department&limit=10` 返回Top10部门
- [ ] GET `/api/analysis/forecast/?target=building&period=30d` 返回预测序列
- [ ] 所有分析接口响应时间 < 2秒

---

## 步骤 3.7：实现 alarms 应用 API

### 操作说明
在 `apps/alarms/` 中实现：

1. **Serializers**：
   - `AlarmRuleSerializer` - 告警规则
   - `AlarmSerializer` - 告警记录
   - `AlarmHandleSerializer` - 告警处理

2. **ViewSets**：
   - `AlarmRuleViewSet` - 规则 CRUD
   - `AlarmViewSet`：
     - `list` - 告警列表（支持状态过滤）
     - `retrieve` - 告警详情
     - `handle` - 处理告警
     - `statistics` - 告警统计

3. **URL 配置**：
   - `/api/alarm-rules/` - GET/POST
   - `/api/alarms/` - GET
   - `/api/alarms/{id}/` - GET
   - `/api/alarms/{id}/handle/` - POST
   - `/api/alarms/statistics/` - GET

### 测试验证
- [ ] POST `/api/alarm-rules/` 创建告警规则
- [ ] GET `/api/alarms/?status=pending` 返回待处理告警
- [ ] POST `/api/alarms/{id}/handle/` 处理告警，状态变为已处理
- [ ] GET `/api/alarms/statistics/` 返回告警统计数据
- [ ] 只有管理员能处理告警

---

## 步骤 3.8：实现 system 应用 API

### 操作说明
在 `apps/system/` 中实现：

1. **用户管理**：
   - `UserViewSet` - 用户 CRUD
   - `/api/users/` - GET/POST
   - `/api/users/{id}/` - GET/PUT/DELETE
   - `/api/users/{id}/reset-password/` - POST

2. **角色管理**：
   - `RoleViewSet` - 角色 CRUD
   - `/api/roles/` - GET/POST

3. **账单管理**：
   - `BillViewSet` - 账单查询
   - `/api/bills/` - GET
   - `/api/bills/my/` - GET（当前用户账单）

4. **通知管理**：
   - `NoticeViewSet` - 通知 CRUD
   - `/api/notices/` - GET（用户端）
   - `/api/admin/notices/` - GET/POST/PUT/DELETE（管理端）

5. **操作日志**：
   - `OperationLogViewSet` - 只读
   - `/api/logs/` - GET（管理员）

6. **费用与充值**：
   - `RechargeViewSet` - 充值记录与模拟充值
   - `/api/recharges/` - GET（历史记录）
   - `/api/recharges/simulate/` - POST（模拟充值，不做真实支付，但写入充值流水并更新账务状态）

7. **个人中心**：
   - `ProfileViewSet` - 个人信息、绑定关系、告警订阅
   - `/api/profile/` - GET/PUT
   - `/api/profile/bind-rooms/` - POST/DELETE
   - `/api/profile/alarm-subscriptions/` - GET/PUT

### 测试验证
- [ ] 管理员能创建用户，返回 201
- [ ] 普通用户访问 `/api/users/` 返回 403
- [ ] 用户只能查看自己的账单 `/api/bills/my/`
- [ ] 管理员能发布通知
- [ ] 只有管理员能查看操作日志
- [ ] 用户调用 `/api/recharges/simulate/` 返回模拟充值结果
- [ ] 调用 `/api/recharges/simulate/` 后，`em_recharge_records` 新增记录且账务数据同步变化
- [ ] 用户可通过 `/api/profile/` 更新头像和联系方式
- [ ] 用户绑定/解绑房间接口生效
- [ ] 用户告警订阅设置保存成功

---

## 步骤 3.9：实现权限控制

### 操作说明
创建 `backend/energy_monitoring/permissions.py`：

1. **权限类**：
   - `IsAdmin` - 仅管理员
   - `IsAdminOrReadOnly` - 管理员写，只读
   - `IsOwnerOrAdmin` - 资源所有者或管理员

2. **在 ViewSets 中应用**：
   - 角色来源：`UserProfile.role`（`ADMIN`/`USER`）
   - 建筑管理：`IsAdminOrReadOnly`
   - 设备管理：`IsAdminOrReadOnly`
   - 告警处理：`IsAdmin`
   - 个人信息：`IsOwnerOrAdmin`

### 测试验证
- [ ] 使用普通用户 token 访问 `/api/buildings/`（GET）成功
- [ ] 使用普通用户 token 访问 `/api/buildings/`（POST）返回 403
- [ ] 使用管理员 token 访问 `/api/buildings/`（POST）成功
- [ ] 用户访问自己的 `/api/bills/my/` 成功
- [ ] 用户访问别人的 `/api/bills/` 返回 403

---

## 步骤 3.10：配置 CORS

### 操作说明
1. 安装 `django-cors-headers`
2. 在 `settings.py` 中配置：
   - 添加 `corsheaders` 到 `INSTALLED_APPS`
   - 添加 `CorsMiddleware` 到 `MIDDLEWARE`
   - 配置 `CORS_ALLOWED_ORIGINS`
   - 配置 `CORS_ALLOW_CREDENTIALS`

### 测试验证
- [ ] 前端开发服务器（http://localhost:5173）能访问后端 API
- [ ] 浏览器控制台无 CORS 错误
- [ ] preflight 请求返回正确的 CORS 头

---

# 第四阶段：后端接口文档

## 步骤 4.1：安装接口文档工具

### 操作说明
1. 选择文档工具：推荐使用 `drf-spectacular` 或 `drf-yasg`
2. 安装并配置到 Django

### 测试验证
- [ ] 访问 `/api/docs/` 显示 Swagger UI
- [ ] 访问 `/api/redoc/` 显示 ReDoc

---

## 步骤 4.2：编写 API 文档注释

### 操作说明
为每个 ViewSet 和 Action 添加：

1. **类级别文档字符串**：描述接口用途
2. **方法级别文档字符串**：描述每个操作
3. **Schema 注解**：使用 `@extend_schema` 装饰器

### 测试验证
- [ ] Swagger 文档显示所有接口
- [ ] 每个接口有清晰的描述
- [ ] 请求/响应示例正确显示
- [ ] 可以直接在 Swagger UI 中测试接口

---

## 步骤 4.3：导出接口文档

### 操作说明
1. 导出 OpenAPI JSON/YAML 文件
2. 保存到 `docs/api-spec.json`
3. 创建 Markdown 版本的接口说明文档

### 测试验证
- [ ] `docs/api-spec.json` 文件存在
- [ ] JSON 格式正确，可以被导入到其他工具
- [ ] Markdown 文档包含所有主要接口的说明

---

## 步骤 4.4：建立需求追踪矩阵（RTM）

### 操作说明
创建 `docs/rtm.md`，逐条追踪：
1. 字段模板：`需求ID`、`来源文档`、`需求描述`、`实施步骤`、`代码位置`、`测试用例`、`证据链接`、`状态`
2. `pre-prd.md` 需求ID -> 实施步骤 -> API/页面 -> 测试用例
3. `PRD.md` 需求ID -> 实施步骤 -> API/页面 -> 测试用例
4. 标注状态（未开始/进行中/已完成/已验收）

### 测试验证
- [ ] `pre-prd.md` 所有需求在 RTM 中可追踪
- [ ] `PRD.md` 所有需求在 RTM 中可追踪
- [ ] 每条需求至少关联1个测试用例
- [ ] 需求变更后 RTM 在24小时内更新
- [ ] `docs/rtm.md` 中每条“已验收”需求均有可访问证据

---

# 第五阶段：数据导入工具开发

## 步骤 5.1：创建数据导入脚本框架

### 操作说明
在 `scripts/` 目录下创建：

1. `data_importer.py` - 主导入脚本
2. `data_cleaner.py` - 数据清洗模块
3. `config.py` - 导入配置

### 测试验证
- [ ] 脚本能正常运行，显示帮助信息
- [ ] 配置文件能正确读取

---

## 步骤 5.2：实现多格式数据读取（CSV/Excel/JSON）

### 操作说明
使用 Pandas 实现：

1. 读取 CSV/Excel/JSON 文件
2. 检测数据格式
3. 数据类型转换
4. 缺失值处理

### 测试验证
- [ ] 能读取示例 CSV 文件
- [ ] 能读取示例 Excel 文件
- [ ] 能读取示例 JSON 文件
- [ ] 正确识别列名
- [ ] 处理包含1000行的测试文件
- [ ] 显示数据预览

---

## 步骤 5.3：实现数据清洗

### 操作说明
在 `data_cleaner.py` 中实现：

1. **数据验证**：
   - 检查必填字段
   - 验证数值范围
   - 验证时间格式
2. **异常值处理**：
   - 识别异常值（如负数功率）
   - 标记或删除异常数据
3. **数据标准化**：
   - 时间戳统一格式
   - 单位统一转换

### 测试验证
- [ ] 包含异常值的测试数据被正确标记
- [ ] 清洗后的数据符合模型要求
- [ ] 生成清洗报告（多少条有效、多少条异常）

---

## 步骤 5.4：实现批量导入 API 调用

### 操作说明
1. 将清洗后的数据批量写入数据库
2. 使用 `bulk_create` 提高效率
3. 添加进度显示
4. 添加错误处理和回滚
5. 支持百万级数据分批导入（分片、断点续传）

### 测试验证
- [ ] 导入100条测试数据成功
- [ ] 数据库中数据正确
- [ ] 导入过程中显示进度
- [ ] 部分数据错误时，正确数据仍能导入
- [ ] 百万级数据（可分批）导入任务稳定完成并输出性能报告

---

## 步骤 5.5：创建管理命令

### 操作说明
创建 Django 管理命令：

1. `python manage.py import_energy_data <file_path>` - 导入数据
2. `python manage.py generate_statistics` - 生成统计数据
3. `python manage.py check_alarms` - 检查告警

### 测试验证
- [ ] `python manage.py import_energy_data test.csv` 成功导入
- [ ] `python manage.py generate_statistics` 生成统计表数据
- [ ] `python manage.py check_alarms` 生成告警记录
- [ ] 命令有详细的输出信息

---

## 步骤 5.6：实现 Modbus/BACnet 自动采集服务

### 操作说明
在 `scripts/protocol_collectors/` 下实现：
1. `modbus_collector.py` - 周期读取 Modbus 仪表数据
2. `bacnet_collector.py` - 周期读取 BACnet 设备数据
3. `collector_runner.py` - 统一调度、重试、故障恢复
4. 采集后统一写入 `em_energy_data`（MySQL）

### 测试验证
- [ ] Modbus 采集任务按周期写入数据
- [ ] BACnet 采集任务按周期写入数据
- [ ] 采集服务异常后可自动恢复
- [ ] 采集数据可被监测中心页面实时读取
- [ ] 支持通过 Modbus/BACnet 模拟器完成联调与验收

---

# 第六阶段：数据分析与告警

## 步骤 6.1：实现统计数据生成

### 操作说明
创建 `scripts/generate_statistics.py`：

1. 按设备、能源类型聚合数据
2. 计算日/月/年统计：
   - 总用量
   - 峰值/谷值
   - 平均值
   - 费用计算
3. 写入 `em_energy_statistics` 表

### 测试验证
- [ ] 运行脚本后，统计表有数据
- [ ] 统计值计算正确（手动验证几条）
- [ ] 能处理空数据集
- [ ] 生成指定时间范围的统计

---

## 步骤 6.2：实现告警检测

### 操作说明
创建 `scripts/check_alarms.py`：

1. 读取告警规则
2. 检测超限告警（超过阈值）
3. 检测突变告警（环比变化 > 设定比例）
4. 检测离线告警（长时间无数据）
5. 写入 `em_alarms` 表

### 测试验证
- [ ] 超过阈值的数据生成告警
- [ ] 突变数据生成告警
- [ ] 长时间无数据的设备生成告警
- [ ] 相同条件的重复告警不重复创建

---

## 步骤 6.3：集成 Spark 离线分析（可选增强）

### 操作说明
1. 安装 PySpark
2. 编写 Spark 分析脚本
3. 读取 MySQL 数据进行分析
4. 将结果写回 MySQL

### 测试验证
- [ ] Spark 能正确连接 MySQL
- [ ] 分析任务成功执行
- [ ] 结果正确写入数据库
- [ ] 大数据集处理延迟达到分钟级
- [ ] 若本期不启用 Spark，需提供替代说明（如仅使用 Python 离线聚合）

---

## 步骤 6.4：创建定时任务

### 操作说明
使用 Django Celery Beat 或 cron：

1. 每小时检查告警
2. 每天凌晨生成统计数据
3. 每周生成分析报告

### 测试验证
- [ ] 定时任务正常执行
- [ ] 查看日志确认执行记录
- [ ] 统计数据按时更新
- [ ] 告警及时生成

---

## 步骤 6.5：实现趋势预测任务

### 操作说明
1. 创建 `scripts/generate_forecast.py`，基于历史统计数据生成 7 天/30 天预测（按日粒度）。
2. 预测结果写入 `em_energy_forecasts`，维度优先支持 `campus/building/meter`，`room/department` 作为可空扩展字段。
3. 建议字段：`target_type`、`target_id`、`energy_type`、`forecast_date`、`forecast_value`、`model_version`、`created_at`。
4. 提供给 `/api/analysis/forecast/` 接口读取。

### 测试验证
- [ ] 运行预测任务后，`em_energy_forecasts` 有有效数据
- [ ] 可按校区/楼宇/设备查询预测结果
- [ ] 前端预测曲线与接口返回一致

---

# 第七阶段：前端项目初始化

## 步骤 7.1：创建 Vue 项目

### 操作说明
1. 使用 Vite 创建 Vue 3 项目
2. 配置 `package.json` 依赖：
   - vue
   - vue-router
   - pinia
   - element-plus
   - echarts
   - axios
   - tailwindcss

### 测试验证
- [ ] 运行 `npm install` 成功
- [ ] 运行 `npm run dev` 启动开发服务器
- [ ] 访问 http://localhost:5173 显示欢迎页

---

## 步骤 7.2：配置项目结构

### 操作说明
在 `frontend/src/` 下创建：

```
src/
├── api/              # API 接口封装
├── assets/           # 静态资源
├── components/       # 公共组件
├── layouts/          # 布局组件
├── router/           # 路由配置
├── stores/           # Pinia 状态管理
├── utils/            # 工具函数
├── views/            # 页面组件
│   ├── admin/        # 管理端页面
│   └── user/         # 用户端页面
├── App.vue
└── main.js
```

### 测试验证
- [ ] 所有目录创建成功
- [ ] `main.js` 能正常挂载 Vue 应用
- [ ] 路由配置生效

---

## 步骤 7.3：配置 Tailwind CSS

### 操作说明
1. 安装 Tailwind CSS
2. 配置 `tailwind.config.js`
3. 配置主题颜色（建议使用温暖的橙色/绿色系）

### 测试验证
- [ ] Tailwind 类名生效
- [ ] 自定义主题颜色可用
- [ ] 组件样式正确渲染

---

## 步骤 7.4：配置 Element Plus

### 操作说明
1. 按需引入 Element Plus
2. 配置主题色
3. 注册常用组件

### 测试验证
- [ ] Element Plus 组件正常显示
- [ ] 主题色应用成功
- [ ] 图标正常显示

---

## 步骤 7.5：配置 Axios

### 操作说明
创建 `src/utils/request.js`：

1. 创建 axios 实例
2. 配置 baseURL
3. 配置请求拦截器（添加 token）
4. 配置响应拦截器（统一处理错误）
5. 配置超时时间

### 测试验证
- [ ] 请求能正确发送到后端
- [ ] 请求头包含 Authorization
- [ ] 401 响应自动跳转登录页
- [ ] 其他错误显示提示信息

---

## 步骤 7.6：配置路由

### 操作说明
创建 `src/router/index.js`：

1. 定义路由结构：
   - 登录页（`/login`）
   - 管理端布局（`/admin`）
     - 综合监控大屏
     - 监测中心
     - 统计分析
     - 异常告警
     - 设备管理
     - 基础配置
     - 系统管理
   - 用户端布局（`/user`）
     - 个人首页
     - 用能查询
     - 费用充值
     - 能耗对比
     - 节能公告
     - 个人中心

2. 配置路由守卫：
   - 检查登录状态
   - 根据角色权限跳转

### 测试验证
- [ ] 未登录访问 `/admin` 跳转到登录页
- [ ] 登录后访问 `/login` 跳转到管理端首页
- [ ] 普通用户访问管理页面返回 403
- [ ] 路由参数正确传递

---

## 步骤 7.7：配置 Pinia Store

### 操作说明
创建 `src/stores/` 下的 stores：

1. `user.js` - 用户状态：
   - userInfo - 用户信息
   - token - 认证令牌
   - role - 用户角色
   - login() - 登录方法
   - logout() - 退出方法

2. `building.js` - 建筑数据：
   - buildingTree - 建筑树
   - currentBuilding - 当前选中建筑

3. `energy.js` - 能耗数据：
   - selectedDevices - 选中的设备
   - dateRange - 时间范围

### 测试验证
- [ ] 登录后 store 中有用户信息
- [ ] 刷新页面状态保持（使用 pinia-plugin-persistedstate）
- [ ] 退出登录状态清空
- [ ] Store 数据在组件间共享

---

## 步骤 7.8：创建 API 模块

### 操作说明
在 `src/api/` 下创建模块：

1. `auth.js` - 认证接口
2. `building.js` - 建筑接口
3. `device.js` - 设备接口
4. `energy.js` - 能耗数据接口
5. `analysis.js` - 分析接口
6. `alarm.js` - 告警接口
7. `system.js` - 系统接口
8. `recharge.js` - 充值与模拟充值接口
9. `profile.js` - 个人中心接口

每个模块封装对应的 API 调用函数。

### 测试验证
- [ ] 每个 API 函数能正确调用后端接口
- [ ] 参数正确传递
- [ ] 响应数据正确返回
- [ ] 错误被正确处理

---

# 第八阶段：前端 - 管理端开发

## 步骤 8.1：开发登录页面

### 操作说明
创建 `src/views/Login.vue`：

1. 登录表单：用户名、密码
2. 记住密码选项
3. 登录按钮
4. 表单验证
5. 调用登录 API
6. 保存 token，跳转首页

### 测试验证
- [ ] 输入正确账号密码，登录成功跳转
- [ ] 输入错误账号密码，显示错误提示
- [ ] 表单验证生效（必填、格式）
- [ ] 记住密码功能正常
- [ ] 登录后 Header 显示用户名

---

## 步骤 8.2：开发管理端布局组件

### 操作说明
创建 `src/layouts/AdminLayout.vue`：

1. **侧边栏**：
   - Logo
   - 菜单项（对应各功能模块）
   - 菜单折叠功能
2. **顶部栏**：
   - 面包屑导航
   - 用户信息下拉菜单
   - 退出登录
3. **内容区**：
   - 路由视图
   - 页面标题

### 测试验证
- [ ] 侧边栏菜单点击正确跳转
- [ ] 菜单折叠/展开正常
- [ ] 面包屑正确显示当前路径
- [ ] 退出登录清空状态

---

## 步骤 8.3：开发综合监控大屏

### 操作说明
创建 `src/views/admin/Dashboard.vue`：

1. **顶部指标卡片**：
   - 总能耗（水/电/气）
   - 平均功率
   - 数据覆盖率
   - 今日告警数

2. **中部图表**：
   - 能耗趋势折线图（ECharts）
   - 能耗分布饼图（ECharts）
   - 实时功率柱状图（ECharts）
   - 校园 2D 地图热力分布图（楼宇能耗热力，3D 为可选增强）

3. **底部表格**：
   - 最新告警列表
   - 设备状态概览

### 测试验证
- [ ] 页面加载后从 API 获取数据
- [ ] 所有图表正常渲染
- [ ] 图表支持交互（提示框、缩放）
- [ ] 数据自动刷新（每30秒）
- [ ] 组件销毁时 ECharts 实例被释放
- [ ] 2D 地图热力分布正常显示并支持楼宇点击联动
- [ ] 如实现 3D，需与 2D 使用同一数据源并保持口径一致

---

## 步骤 8.4：开发监测中心页面

### 操作说明
创建 `src/views/admin/Monitoring.vue`：

1. **左侧树形导航**：
   - 显示校区-楼宇-楼层-房间树
   - 支持搜索
   - 点击选择监测点

2. **右侧数据看板**：
   - 选中位置的基本信息
   - 实时数据卡片（电压、电流、功率等）
   - 数据趋势折线图
   - 时间范围选择器

### 测试验证
- [ ] 树形结构正确加载
- [ ] 选择节点后右侧数据更新
- [ ] 搜索功能正常
- [ ] 图表支持时间范围切换
- [ ] 实时数据自动更新

---

## 步骤 8.5：开发统计分析页面

### 操作说明
创建 `src/views/admin/Analysis.vue`：

1. **顶部筛选区**：
   - 时间范围选择（日/月/年）
   - 建筑/房间选择
   - 能源类型选择

2. **中部图表区**：
   - 历史数据趋势图
   - 同比环比对比图
   - 能耗排名柱状图
   - 趋势预测曲线图（7天/30天）

3. **底部操作区**：
   - 导出报表按钮（Excel/PDF）
   - 数据表格展示

### 测试验证
- [ ] 筛选条件改变后图表更新
- [ ] 同比环比计算正确
- [ ] 导出 Excel 文件成功
- [ ] 导出 PDF 文件成功
- [ ] 预测曲线与 `forecast` 接口返回数据一致
- [ ] 表格分页正常

---

## 步骤 8.6：开发异常告警页面

### 操作说明
创建 `src/views/admin/Alarms.vue`：

1. **告警列表**：
   - 状态标签（待处理/已处理）
   - 筛选条件（状态、类型、时间）
   - 分页表格

2. **告警详情弹窗**：
   - 告警详细信息
   - 处理表单（备注、状态）
   - 确认处理按钮

3. **告警规则配置**：
   - 规则列表
   - 新增/编辑规则弹窗

### 测试验证
- [ ] 告警列表正确显示
- [ ] 筛选功能正常
- [ ] 处理告警后状态更新
- [ ] 规则配置生效
- [ ] API 调用正确

---

## 步骤 8.7：开发设备管理页面

### 操作说明
创建 `src/views/admin/Devices.vue`：

1. **设备列表**：
   - 筛选条件（建筑、能源类型、状态）
   - 表格展示设备信息
   - 操作按钮（编辑、删除、绑定房间）

2. **设备表单弹窗**：
   - 新增/编辑设备
   - 表单验证
   - 保存按钮

3. **数据状态**：
   - 显示设备是否有数据
   - 最后数据时间

### 测试验证
- [ ] 设备列表正确加载
- [ ] 新增设备保存成功
- [ ] 编辑设备更新成功
- [ ] 删除设备有确认提示
- [ ] 绑定房间功能正常

---

## 步骤 8.8：开发基础配置页面

### 操作说明
创建 `src/views/admin/Configuration.vue`：

1. **Tab 切换**：
   - 建筑档案
   - 能源类型
   - 费率设置

2. **建筑档案 Tab**：
   - 树形表格展示
   - 新增/编辑建筑/楼层/房间

3. **能源类型 Tab**：
   - 列表展示
   - 新增/编辑

4. **费率设置 Tab**：
   - 表单设置分时电价
   - 阶梯水价设置

### 测试验证
- [ ] Tab 切换正常
- [ ] 建筑树形表格正确展示
- [ ] 新增建筑成功
- [ ] 费率设置保存成功

---

## 步骤 8.9：开发系统管理页面

### 操作说明
创建 `src/views/admin/System.vue`：

1. **Tab 切换**：
   - 用户管理
   - 角色管理
   - 操作日志

2. **用户管理 Tab**：
   - 用户列表
   - 新增/编辑用户
   - 重置密码
   - 分配角色

3. **角色管理 Tab**：
   - 角色列表
   - 权限配置

4. **操作日志 Tab**：
   - 日志列表（只读）
   - 筛选条件

### 测试验证
- [ ] 用户列表正确加载
- [ ] 新增用户成功
- [ ] 重置密码功能正常
- [ ] 角色分配生效
- [ ] 操作日志正确显示

---

# 第九阶段：前端 - 用户端开发

## 步骤 9.1：开发用户端布局组件

### 操作说明
创建 `src/layouts/UserLayout.vue`：

1. **顶部导航栏**：
   - Logo
   - 导航菜单
   - 用户下拉菜单

2. **侧边栏**（可选）：
   - 绑定的房间列表
   - 快捷切换

3. **内容区**：
   - 路由视图

### 测试验证
- [ ] 导航菜单点击正确跳转
- [ ] 用户下拉菜单正常
- [ ] 房间切换功能正常
- [ ] 退出登录正常

---

## 步骤 9.2：开发用户个人首页

### 操作说明
创建 `src/views/user/UserDashboard.vue`：

1. **顶部卡片**：
   - 当前房间
   - 今日用电量/用水量
   - 本月费用
   - 余额/预算进度

2. **中部图表**：
   - 本周用能趋势
   - 用能构成饼图

3. **底部简报**：
   - 节能建议
   - 最新通知

### 测试验证
- [ ] 页面加载后获取当前用户数据
- [ ] 图表正确渲染
- [ ] 节能建议根据数据生成
- [ ] 通知正确显示

---

## 步骤 9.3：开发用能查询明细页面

### 操作说明
创建 `src/views/user/UsageHistory.vue`：

1. **视图切换**：
   - 日历视图
   - 列表视图

2. **筛选区**：
   - 时间范围
   - 能源类型

3. **图表展示**：
   - 用能趋势折线图
   - 时段分析柱状图

4. **数据表格**：
   - 每日详细数据
   - 分页

### 测试验证
- [ ] 日历视图正确显示
- [ ] 列表视图分页正常
- [ ] 筛选功能正常
- [ ] 图表随筛选更新

---

## 步骤 9.4：开发费用与充值页面

### 操作说明
创建 `src/views/user/CostPayment.vue`：

1. **Tab 切换**：
   - 我的账单
   - 充值记录
   - 费用计算器

2. **账单 Tab**：
   - 账单列表
   - 支付状态
   - 查看详情

3. **充值记录 Tab**：
   - 充值历史列表
   - 充值金额
   - 时间
   - 模拟充值按钮（调用 `/api/recharges/simulate/`）

4. **费用计算器 Tab**：
   - 输入用量
   - 实时计算费用
   - 显示明细

### 测试验证
- [ ] 账单列表正确显示
- [ ] 充值记录正确显示
- [ ] 费用计算器计算正确
- [ ] 模拟充值接口调用成功并显示结果
- [ ] Tab 切换正常

---

## 步骤 9.5：开发能耗对比与排名页面

### 操作说明
创建 `src/views/user/Comparison.vue`：

1. **对比图表**：
   - 与全校平均水平对比雷达图
   - 与同类用户对比柱状图

2. **排名展示**：
   - 节能排名榜单
   - 当前用户位置高亮

3. **历史排名**：
   - 排名变化趋势

### 测试验证
- [ ] 雷达图正确渲染
- [ ] 排名数据正确
- [ ] 当前用户高亮显示
- [ ] 数据正确加载

---

## 步骤 9.6：开发节能公告页面

### 操作说明
创建 `src/views/user/Notices.vue`：

1. **Tab 切换**：
   - 通知公告
   - 节能知识

2. **通知列表**：
   - 标题
   - 发布时间
   - 优先级标签
   - 已读/未读状态

3. **公告详情**：
   - 点击查看详情
   - 标记已读

4. **节能知识**：
   - 分类展示
   - 搜索功能

### 测试验证
- [ ] 通知列表正确加载
- [ ] 点击查看详情
- [ ] 已读状态更新
- [ ] 节能知识分类正确

---

## 步骤 9.7：开发个人中心页面

### 操作说明
创建 `src/views/user/Profile.vue`：

1. **Tab 切换**：
   - 基本资料
   - 账号绑定
   - 告警订阅

2. **基本资料 Tab**：
   - 头像上传
   - 信息编辑表单
   - 保存按钮

3. **账号绑定 Tab**：
   - 已绑定房间列表
   - 添加绑定按钮
   - 解绑按钮

4. **告警订阅 Tab**：
   - 余额不足提醒开关
   - 异常用能提醒开关

### 测试验证
- [ ] 基本资料保存成功
- [ ] 头像上传功能正常
- [ ] 房间绑定成功
- [ ] 解绑功能正常
- [ ] 告警订阅开关保存

---

# 第十阶段：测试与优化

## 步骤 10.1：功能测试

### 操作说明
逐页进行功能测试：

1. **管理端**：
   - 综合监控大屏
   - 监测中心
   - 统计分析
   - 异常告警
   - 设备管理
   - 基础配置
   - 系统管理

2. **用户端**：
   - 个人首页
   - 用能查询
   - 费用充值
   - 能耗对比
   - 节能公告
   - 个人中心

### 测试验证
- [ ] 所有页面正常加载
- [ ] 所有按钮功能正常
- [ ] 表单验证生效
- [ ] 权限控制正确

---

## 步骤 10.2：性能测试

### 操作说明
1. **基线环境记录（本机）**：
   - CPU：AMD Ryzen 7 7745HX（8C16T）
   - 内存：16GB
   - 系统：Windows 11 64-bit
   - 数据集规模：`dataSource/` 总计约 2050 万行

2. **API 响应时间**：
   - 统计分析接口 < 2秒
   - 列表查询 < 1秒
   - 大屏数据 < 1秒

3. **前端性能**：
   - 首屏加载时间
   - 图表渲染性能
   - 大数据量表格性能

4. **导入与计算性能**：
   - 百万级数据导入稳定性（分批导入）
   - Spark 分析任务分钟级完成（启用 Spark 时）

### 测试验证
- [ ] 所有 API 响应符合要求
- [ ] 前端首屏加载 < 3秒
- [ ] ECharts 图表渲染流畅
- [ ] 1000条数据表格滚动流畅
- [ ] 百万级导入压测有记录且任务可完成
- [ ] 启用 Spark 时，离线任务延迟达到分钟级

---

## 步骤 10.3：安全测试

### 操作说明
1. **认证测试**：
   - 未登录不能访问受保护页面
   - Token 过期自动跳转登录

2. **权限测试**：
   - 普通用户不能访问管理功能
   - 用户只能查看自己的数据

3. **数据安全**：
   - 密码**明文存储**（演示需求）
   - SQL 注入防护
   - XSS 防护

### 测试验证
- [ ] 所有未认证访问被拦截
- [ ] 跨权限访问被拒绝
- [ ] 密码在数据库中**明文可见**
- [ ] 输入过滤生效

---

## 步骤 10.4：兼容性测试

### 操作说明
测试主流浏览器：

1. Chrome
2. Firefox
3. Edge
4. Safari（如可能）

### 测试验证
- [ ] 所有浏览器页面正常显示
- [ ] 图表正常渲染
- [ ] 交互功能正常

---

## 步骤 10.5：修复 Bug 与优化

### 操作说明
1. 记录测试中发现的问题
2. 按优先级修复
3. 代码优化

### 测试验证
- [ ] 所有已知 Bug 已修复
- [ ] 代码无明显性能问题
- [ ] 无明显代码重复

---

## 步骤 10.6：自动化测试与 CI 质量门禁

### 操作说明
1. 后端：使用 `pytest + pytest-django` 建立单元测试与 API 集成测试。
2. 前端：使用 `vitest`（单元）和 `cypress/playwright`（关键流程 E2E）。
3. CI：创建流水线（如 GitHub Actions/GitLab CI）执行：
   - 代码检查（lint）
   - 自动化测试
   - 覆盖率统计与质量提示
4. 设置门禁阈值（建议）：
   - 后端覆盖率 >= 80%
   - 前端关键流程 E2E 全通过
5. 本项目阈值默认按“建议值”执行，可先采用告警模式，不强制阻断合并。

### 测试验证
- [ ] 每次提交自动触发 CI
- [ ] 测试失败时至少触发告警并保留报告
- [ ] 覆盖率报告可查看，并给出与建议阈值的对比
- [ ] 关键业务流程（登录、导入、分析、告警处理）E2E 通过

---

# 第十一阶段：部署准备

## 步骤 11.1：后端部署准备

### 操作说明
1. 配置 `settings.py` 生产环境设置：
   - `DEBUG = False`
   - 配置 `ALLOWED_HOSTS`
   - 配置静态文件路径

2. 配置 Gunicorn/uWSGI
3. 配置 Nginx

### 测试验证
- [ ] 使用 Gunicorn 能正常启动服务
- [ ] Nginx 正确代理请求
- [ ] 静态文件正常加载

---

## 步骤 11.2：前端部署准备

### 操作说明
1. 配置生产环境 API 地址
2. 运行 `npm run build`
3. 验证构建产物

### 测试验证
- [ ] 构建成功无错误
- [ ] 构建产物在 `dist/` 目录
- [ ] 本地预览正常

---

## 步骤 11.3：编写部署文档

### 操作说明
创建 `docs/deployment.md`：

1. 环境要求
2. 安装步骤
3. 配置说明
4. 启动命令
5. 常见问题

### 测试验证
- [ ] 按照文档能完成部署
- [ ] 所有步骤清晰
- [ ] 命令正确

---

## 步骤 11.4：数据库备份策略

### 操作说明
1. 编写备份脚本
2. 配置定时备份
3. 编写恢复文档

### 测试验证
- [ ] 备份脚本正常运行
- [ ] 备份文件生成
- [ ] 能够从备份恢复

---

# 第十二阶段：项目收尾

## 步骤 12.1：代码注释与文档

### 操作说明
1. 为关键代码添加注释
2. 完善 memory-bank 文档
3. 编写用户手册

### 测试验证
- [ ] 关键函数有文档字符串
- [ ] 文档内容完整
- [ ] 用户手册清晰易懂

---

## 步骤 12.2：最终测试

### 操作说明
进行完整的回归测试，确保所有功能正常。

### 测试验证
- [ ] 所有核心功能正常
- [ ] 无明显 Bug
- [ ] 性能符合要求

---

## 步骤 12.3：项目验收

### 操作说明
1. 对照 PRD 核对所有功能
2. 对照 pre-prd 核对关键技术要求（Modbus/BACnet、监控大屏，Spark 为可选增强）
3. 对照 RTM 核对每条需求的实现与测试证据
4. 准备演示数据
5. 进行项目演示

### 测试验证
- [ ] 所有 PRD 功能已实现
- [ ] 所有 pre-prd 核心要求已实现
- [ ] RTM 中所有需求状态为已验收
- [ ] 演示流畅
- [ ] 数据展示正确
- [ ] 大屏 2D 地图能力可稳定演示（若有 3D 则作为增强项展示）

---

## 步骤 12.4：项目归档

### 操作说明
1. 清理临时文件
2. 整理项目结构
3. 提交最终代码
4. 编写 README.md

### 测试验证
- [ ] 仓库结构清晰
- [ ] README 完整
- [ ] 代码已提交
