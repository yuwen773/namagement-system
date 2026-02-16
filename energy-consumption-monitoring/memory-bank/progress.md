# 项目进度记录（Progress）

## 文档目的
记录“完成了什么、如何验收、下一步是什么”；不记录实现细节和讨论过程。

## 当前状态（2026-02-16）
- 当前阶段：第二阶段（数据库设计与模型开发）
- 已完成步骤：`1.1`、`1.2`、`1.3`、`1.4`、`1.5`、`2.1`、`2.2`
- 当前门禁：`2.2` 已通过用户测试；按约定未开始 `2.3`

## 本次更新（阶段 2.2）
- 已创建并初始化 7 个 Django 应用：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`
- 每个应用已具备基础文件：`apps.py`、`models.py`、`views.py`、`serializers.py`、`urls.py`、`admin.py`、`tests.py`、`migrations/__init__.py`
- 已在 `backend/energy_monitoring/settings.py` 注册全部应用
- 已执行并通过检查：`python manage.py check`（0 issues）

## 历史里程碑（摘要）
- `1.1`：完成目录结构与 Python 包边界
- `1.2`：完成后端虚拟环境与依赖安装
- `1.3`：完成 MySQL `energy_monitoring` 与 `utf8mb4` 基线
- `1.4`：完成 Django 项目初始化与全局配置
- `1.5`：完成 Modbus/BACnet 采集脚手架与模拟验收脚本
- `2.1`：完成 `sql/init_db.sql`（17 张核心表、约束与索引）

## 下一步（待执行）
- 阶段 `2.3`：实现 `accounts` 应用模型（UserProfile 等）
- 触发条件：收到用户继续执行指令
