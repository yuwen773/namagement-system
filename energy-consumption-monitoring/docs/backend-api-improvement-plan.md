# 基于 `docs/todo.md` 的后端接口完善计划（用户端）

## 一、计划摘要
- 目标：将 `Dashboard`、`Comparison`、`CostPayment`、`Notices`、`UsageHistory` 中仍使用 Mock 的数据替换为真实后端接口。
- 范围：仅覆盖后端接口、模型与返回结构，不包含前端样式改造。
- 原则：优先复用现有模块（`analysis`、`system`、`accounts`），减少前后端改动成本并保持兼容。

## 二、接口与数据结构变更

### 1. 节能知识接口（覆盖 Dashboard + Notices）
- 新增用户接口：`GET /api/tips/`
  - 查询参数：`category`（可选）、`limit`（可选）、`is_published=true`（默认）
  - 返回字段：`id`、`title`、`content`、`category`、`publish_time`
- 新增管理接口：`/api/admin/tips/`（GET/POST/PUT/DELETE）
- 落库方案：复用 `em_notices`，约定 `notice_type=KNOWLEDGE` 表示节能知识。

### 2. Comparison 页面数据真实化
- 扩展 `GET /api/analysis/comparison/`，增加 `view` 参数：
  - `view=radar`：返回雷达图指标与对比序列
  - `view=trend`：返回同比/环比趋势序列
  - `view=history_rank`：返回历史排名序列
  - `view=summary`（默认）：保留现有汇总能力（兼容）
- 扩展 `GET /api/analysis/ranking/` 返回：
  - `my_rank`、`my_rank_change`、`my_target_id`
  - `items[].is_me`（用于前端定位当前用户）

### 3. CostPayment 页面数据真实化
- 数据库变更：`UserProfile` 新增 `balance`（Decimal，默认 `0.00`）。
- 新增接口：`GET /api/profile/balance/`
  - 返回：`balance`、`currency`
- 新增接口：`GET /api/bills/my/summary/`
  - 返回：`month_cost`、`unpaid_bill_count`、`total_recharge`、`energy_saving_reward`
- 调整 `POST /api/recharges/simulate/`
  - 在事务中更新余额并自动冲抵账单
  - 新增返回字段：`account_balance`
  - 保留现有字段 `remaining_amount` 以兼容旧前端

### 4. UsageHistory 时段分析真实化
- 新增接口：`GET /api/analysis/hourly-distribution/`
  - 查询参数：`start_date`、`end_date`、`room_id`、`energy_type`
  - 返回：6个时段桶（`00-04`、`04-08`、`08-12`、`12-16`、`16-20`、`20-24`）的 `total_value` / `avg_value`

## 三、实施步骤

1. 模型与迁移
- 在 `accounts.UserProfile` 添加 `balance` 字段。
- 生成并执行迁移；历史数据默认回填为 `0.00`。

2. system 模块改造
- 新增 `TipsViewSet` 与 `AdminTipsViewSet`（基于 `Notice`）。
- 新增 `profile/balance` 接口 action。
- 新增 `bills/my/summary` 接口 action。
- 改造 `recharges/simulate`：补充余额更新与并发安全。

3. analysis 模块改造
- 扩展 `comparison` 多视图输出能力。
- 扩展 `ranking` 的本人排名信息输出。
- 新增 `hourly-distribution` action 与对应 query serializer。

4. 路由与文档
- 更新 `apps/system/urls.py` 与 `apps/analysis/urls.py`。
- 补充 drf-spectacular schema 与示例响应。

5. 联调准备
- 提供字段映射表（旧字段 -> 新字段）给前端。
- 兼容字段保留至少一个迭代周期。

## 四、测试与验收

### 1. tips
- 仅返回 `KNOWLEDGE + 已发布` 数据。
- `limit` 与 `category` 过滤生效。

### 2. comparison
- `view=radar/trend/history_rank/summary` 均返回预期结构。
- 无数据时返回空数组或空对象，不返回 500。

### 3. ranking
- `items[].is_me` 标记正确。
- 用户无绑定房间时，`my_rank` 与 `my_rank_change` 返回 `null`。

### 4. balance + recharge
- 充值后 `account_balance` 正确更新。
- 自动冲抵账单后余额与账单状态一致。
- 并发场景下无重复扣款、无负余额。

### 5. bills summary
- `month_cost`、`unpaid_bill_count`、`total_recharge`、`energy_saving_reward` 与明细一致。

### 6. hourly distribution
- 固定返回 6 个时段桶。
- 聚合结果与查询条件一致。

### 7. 权限
- 普通用户仅可访问自身相关数据。
- `admin/tips` 仅管理员可访问。

## 五、默认假设
- 节能知识不新建独立表，使用 `Notice(notice_type=KNOWLEDGE)` 统一管理。
- `my_rank` 基于“用户绑定房间集合”参与对应维度排名。
- `energy_saving_reward` 若无独立奖励数据源，先返回 `0`。
- 本计划优先保证接口可用性与字段稳定性，前端交互优化后置。
