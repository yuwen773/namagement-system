# 项目进度记录（Progress）

## 文档目的
仅记录里程碑结果、当前状态与下一步。

## 当前状态（2026-02-24）
- 当前阶段：第三阶段（后端 API 开发）
- 已完成步骤：`1.1` ~ `2.9`、`3.1`、`3.2`、`3.3`
- 用户验收：`3.1`、`3.2`、`3.3` 已测试通过

## 本次更新（阶段 3.1 / 3.2 / 3.3）
- 完成 DRF 全局配置（分页、JWT 鉴权、过滤、统一响应与异常处理）
- 完成认证接口：`/api/auth/register/`、`/api/auth/login/`、`/api/auth/refresh/`、`/api/auth/user-info/`、`/api/auth/change-password/`
- 完成建筑域接口：
  - `/api/campuses/`、`/api/campuses/{id}/`
  - `/api/buildings/`、`/api/buildings/{id}/`、`/api/buildings/tree/`
  - `/api/floors/`、`/api/rooms/`
- 关键检查：`python manage.py check` 通过

## 下一步
- 等待进入阶段 `3.4`（devices 应用 API）
