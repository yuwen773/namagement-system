# 管理端概览统计接口设计

**日期**: 2025-02-13
**主题**: 统一管理端概览统计接口

## 背景

当前管理端 Dashboard 页面分别调用多个独立接口获取数据，导致：
- 6+ 次 HTTP 请求
- 获取累计票房需要传输 1000 条记录到前端计算
- 性能浪费

## 目标

将 Dashboard 所需数据整合为单一接口，一次请求获取全部数据。

## API 设计

### 端点
`GET /api/visualization/stats/overview/`

### 权限
`IsAuthenticated` (需要登录)

### 返回数据

```json
{
  "code": 0,
  "data": {
    "total_movies": 120,
    "total_cinemas": 45,
    "total_box_office": 50000000,
    "total_users": 25,
    "recent_records": [
      {
        "id": 1,
        "date": "2024-01-15",
        "movie_title": "流浪地球2",
        "cinema_name": "万达影城",
        "box_office": 1500000,
        "show_times": 30,
        "viewer_count": 4500
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| total_movies | int | 影片总数 |
| total_cinemas | int | 影院总数 |
| total_box_office | decimal | 历史累计票房总额（元） |
| total_users | int | 注册用户数 |
| recent_records | array | 最近5条票房记录 |

## 实现方案

### 后端
1. 在 `backend/visualization/views.py` 新增 `OverviewStatsView`
2. 使用 Django ORM 聚合查询一次获取所有统计数据
3. 累计票房直接后端 `SUM()` 计算，避免数据传输
4. 在 `backend/visualization/urls.py` 添加路由

### 前端
1. 在 `frontend/src/api/visualization.js` 新增 `getOverviewStats()` 函数
2. 修改 `Dashboard.vue`，改为调用一次接口获取全部数据

## 性能优化

| 优化项 | 优化前 | 优化后 |
|-------|-------|-------|
| HTTP 请求数 | 6+ 次 | 1 次 |
| 数据传输 | 1000 条票房记录 | 仅需 5 条记录 |
| 计算位置 | 前端 | 后端 |
