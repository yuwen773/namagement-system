# 问题记录

## 2026-02-12

### 1. 公告管理分页功能不工作
- **问题**：前端无法正确显示分页数据
- **原因**：
  1. 前端响应处理错误：`res.data` 已是完整响应对象，不是 `{ code: 0, data: [...] }`
  2. 分页组件显示条件 `total > 10` 过于严格
- **修复**：
  - 前端改用 `res.data?.data` 获取列表
  - 分页条件改为 `total > 0`
- **文件**：`frontend/src/views/admin/AnnouncementManage.vue`

### 2. 公告管理 SVG 路径错误
- **问题**：控制台报错 `<path> attribute d: Unexpected end of attribute`
- **原因**：SVG path `d` 属性有语法错误，多余的路径指令
- **修复**：移除错误的路径片段 `-9-9 0 0 0-3 3.87`
- **文件**：`frontend/src/views/admin/AnnouncementManage.vue`

### 3. Dashboard 热门景点图表不显示
- **问题**：TOP 10 热门景点图表无数据
- **原因**：前端响应拦截器已提取 data，前端代码错误检查 `res.data?.code === 0`
- **修复**：改为检查 `Array.isArray(res.data)`
- **文件**：`frontend/src/views/admin/Dashboard.vue`

### 4. Dashboard 图表加载慢 (10s)
- **问题**：月度趋势和热门景点图表加载很慢
- **原因**：后端存在 N+1 查询问题
  - `AttractionHotView`：每个景点执行多次数据库查询
  - `MonthlyReportView`：循环6次，每次3个查询
- **修复**：
  - 热门景点：先获取前50景点，再批量查询评论统计（2次查询）
  - 月度统计：恢复稳定代码
- **文件**：`backend/stats/views.py`

### 5. Dashboard 月度统计接口 500 错误
- **问题**：调用 `/statistics/monthly/` 返回 500
- **原因**：优化代码有语法错误和重复代码块
- **修复**：移除未使用的 import，恢复原有逻辑
- **文件**：`backend/stats/views.py`
