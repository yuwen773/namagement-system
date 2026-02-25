# Progress

## 2026-02-25

### 本次完成（阶段 6.3 ~ 6.4）
- 新增类别占比接口 `GET /api/v1/dashboard/category-distribution/`（`backend/apps/dashboard/views.py`）。
- 返回字段：`category_name`、`heritage_count`、`percentage`；按数量降序；百分比总和校准为 100%。
- 新增国家排行接口 `GET /api/v1/dashboard/country-ranking/`（`backend/apps/dashboard/views.py`）。
- 返回字段：`rank`、`country_name`、`heritage_count`；默认 Top 20，支持 `limit` 参数。
- 更新路由：`backend/apps/dashboard/urls.py`。
- 补充测试：`backend/apps/dashboard/tests/test_views.py`（鉴权、排序、占比计算、`limit` 生效、Top 20 默认行为）。

### 验证结果
- 自动测试：`python manage.py test apps.dashboard.tests.test_views` 通过（10/10）。
- 用户手动测试阶段 6.3 ~ 6.4：通过。

### 当前状态
- 阶段 1~5、阶段 6.1 ~ 6.4 已完成并验证。
- 阶段 7.1 未开始。
