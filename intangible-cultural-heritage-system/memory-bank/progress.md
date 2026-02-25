# Progress

## 2026-02-25

### 本次完成（阶段 6.2）
- 新增地图分布接口 `GET /api/v1/dashboard/map-distribution/`（`backend/apps/dashboard/views.py`）。
- 返回字段：`country_code`、`country_name`、`longitude`、`latitude`、`heritage_count`、`inheritor_count`。
- 支持类别筛选参数：`category`（兼容 `category_id`）。
- 仅返回有数据国家（项目数或传承人数大于 0）。
- 新增路由：`backend/apps/dashboard/urls.py`。
- 补充测试：`backend/apps/dashboard/tests/test_views.py`（鉴权、统计准确性、筛选生效）。

### 验证结果
- 自动测试：`python manage.py test apps.dashboard.tests.test_views` 通过（5/5）。
- 用户手动测试阶段 6.2：通过。

### 当前状态
- 阶段 1~5、阶段 6.1、阶段 6.2 已完成并验证。
- 阶段 6.3（类别占比接口）未开始。
