# API 接口说明（Markdown 版）

## 文档与调试入口
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`
- 导出规范文件: `docs/api-spec.json`

## 认证约定
- 认证方式: `Bearer <access_token>`
- 登录/注册后可获取 `access` 与 `refresh`
- 刷新令牌接口: `POST /api/auth/refresh/`

## 1. 认证模块（accounts）
- `POST /api/auth/register/`: 用户注册
- `POST /api/auth/login/`: 用户登录
- `POST /api/auth/refresh/`: 刷新 access token
- `GET /api/auth/user-info/`: 当前用户信息
- `POST /api/auth/change-password/`: 修改当前用户密码

## 2. 建筑档案模块（buildings）
- `GET /api/campuses/`: 校区列表
- `GET /api/campuses/{id}/`: 校区详情
- `GET /api/buildings/`: 建筑列表（支持搜索/排序/筛选）
- `POST /api/buildings/`: 创建建筑（管理员）
- `GET /api/buildings/{id}/`: 建筑详情
- `PUT/PATCH /api/buildings/{id}/`: 更新建筑（管理员）
- `DELETE /api/buildings/{id}/`: 删除建筑（管理员）
- `GET /api/buildings/tree/`: 校区-建筑-楼层-房间树
- `GET /api/floors/`: 楼层列表
- `POST /api/floors/`: 创建楼层（管理员）
- `GET /api/rooms/`: 房间列表
- `POST /api/rooms/`: 创建房间（管理员）

## 3. 设备模块（devices）
- `GET /api/energy-types/`: 能源类型列表
- `POST /api/energy-types/`: 创建能源类型（管理员）
- `GET /api/energy-types/{id}/`: 能源类型详情
- `PUT/PATCH/DELETE /api/energy-types/{id}/`: 管理员维护
- `GET /api/devices/`: 设备列表（支持按房间、能源类型、状态筛选）
- `POST /api/devices/`: 创建设备（管理员）
- `GET /api/devices/{id}/`: 设备详情（含 latest_data）
- `PUT/PATCH/DELETE /api/devices/{id}/`: 管理员维护
- `GET /api/devices/data-status/`: 设备数据状态总览
- `POST /api/devices/{id}/bind-room/`: 绑定/解绑设备房间（管理员）

## 4. 能耗数据模块（energy）
- `GET /api/energy-data/`: 原始能耗数据列表（支持时间范围筛选）
- `POST /api/energy-data/`: 新增单条能耗数据
- `POST /api/energy-data/batch-import/`: 批量导入（CSV/Excel/JSON）
- `GET /api/energy-data/latest/`: 各设备最新采样值
- `GET /api/energy-data/export/?format=excel|pdf`: 导出数据
- `GET /api/energy-statistics/`: 统计数据列表（日/月/年）

## 5. 分析模块（analysis）
- `GET /api/analysis/dashboard/`: 大屏概览（总能耗、覆盖率、告警统计）
- `GET /api/analysis/trend/`: 趋势分析（日/月/年）
- `GET /api/analysis/distribution/`: 分布分析（区域/能源类型）
- `GET /api/analysis/ranking/`: 排名分析（楼宇/房间/部门）
- `GET /api/analysis/comparison/`: 同比环比对比
- `GET /api/analysis/forecast/`: 7/30 天趋势预测

## 6. 告警模块（alarms）
- `GET /api/alarm-rules/`: 告警规则列表
- `POST /api/alarm-rules/`: 创建规则（管理员）
- `GET /api/alarm-rules/{id}/`: 规则详情
- `PUT/PATCH/DELETE /api/alarm-rules/{id}/`: 管理员维护
- `GET /api/alarms/`: 告警列表
- `GET /api/alarms/{id}/`: 告警详情
- `POST /api/alarms/{id}/handle/`: 告警处理（管理员）
- `GET /api/alarms/statistics/`: 告警统计概览

## 7. 系统模块（system）
- 用户与角色管理
- `GET/POST /api/users/`, `GET/PUT/PATCH/DELETE /api/users/{id}/`
- `POST /api/users/{id}/reset-password/`
- `GET/POST /api/roles/`, `GET/PUT/PATCH/DELETE /api/roles/{id}/`

- 账单与充值
- `GET /api/bills/`: 管理员账单列表
- `GET /api/bills/my/`: 当前用户账单
- `GET /api/recharges/`: 充值记录
- `POST /api/recharges/simulate/`: 模拟充值并冲抵账单

- 通知与日志
- `GET /api/notices/`, `GET /api/notices/{id}/`: 用户通知
- `GET/POST /api/admin/notices/`, `GET/PUT/PATCH/DELETE /api/admin/notices/{id}/`: 管理员公告维护
- `GET /api/logs/`: 操作日志

- 个人中心
- `GET /api/profile/`: 获取个人资料
- `PUT /api/profile/`: 更新个人资料
- `POST/DELETE /api/profile/bind-rooms/`: 绑定/解绑房间
- `GET/PUT /api/profile/alarm-subscriptions/`: 告警订阅配置

## 响应格式
接口统一响应结构由后端渲染器包装：
- `code`: 业务状态码（`0` 表示成功）
- `data`: 响应数据主体
- `message`: 文本消息
- `total`: 总数（列表/分页场景）
