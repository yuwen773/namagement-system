# 问答信息采集系统 - 录制爬虫设计文档

## 1. 项目概述

基于 Playwright 的可录制回放爬虫系统，集成到现有 Django 管理后台。用户通过浏览器可视化操作一遍采集流程，系统自动记录操作轨迹并批量执行采集任务。

## 2. 需求总结

| 项目 | 内容 |
|------|------|
| 目标网站 | wenda.so.com |
| 录制操作 | 滚动、点击翻页、进入详情页、切换分类 |
| 提取字段 | 标题、内容、回答列表、回答者、时间、分类、标签 |
| 采集规模 | 1万条（500页 × 20条） |
| 翻页方式 | 点击"下一页"按钮 |
| 内容类型 | 仅文字 |
| 断点存储 | JSON 文件 |
| 反爬策略 | 请求间隔逐渐增加（2s → 5s → 10s） |
| 暂停/继续 | 支持 |

## 3. 系统架构

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    Django Admin                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 录制管理    │  │ 任务管理    │  │ 数据管理    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼────────────────┼────────────────┼─────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                   API Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ /recorder/  │  │ /tasks/     │  │ /data/      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              Crawler Service                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Recorder    │  │ Runner      │  │ Extractor   │     │
│  │ (录制器)    │  │ (执行器)    │  │ (提取器)    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │          Playwright Browser Manager             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│                  Target Website                         │
│              wenda.so.com                               │
└─────────────────────────────────────────────────────────┘
```

### 3.2 模块设计

#### 3.2.1 Recorder（录制器）

- 启动无头浏览器（或有头模式供用户操作）
- 监听用户的所有交互操作
- 自动记录选择器（CSS/XPath）
- 实时预览提取的数据

**录制操作类型：**

| 操作 | 记录内容 |
|------|----------|
| 点击元素 | 选择器 + 点击坐标 |
| 滚动 | 滚动距离/位置 |
| 输入文本 | 选择器 + 输入内容 |
| 等待 | 等待条件 + 超时时间 |
| 提取数据 | 选择器 + 字段名 |

#### 3.2.2 Runner（执行器）

- 读取录制配置
- 按顺序执行操作
- 智能间隔控制
- 暂停/继续功能
- 错误处理与重试

#### 3.2.3 Extractor（提取器）

- 从列表页提取问题摘要
- 进入详情页提取完整信息
- 支持多层级字段提取

## 4. 数据结构设计

### 4.1 录制配置文件 (JSON)

```json
{
  "version": "1.0",
  "name": "360问答采集",
  "created_at": "2026-02-28T10:00:00Z",
  "steps": [
    {
      "id": 1,
      "type": "navigate",
      "url": "https://wenda.so.com/c/"
    },
    {
      "id": 2,
      "type": "extract_list",
      "selector": "ul.question-list li",
      "fields": [
        {
          "name": "title",
          "selector": "a[target='_blank']",
          "attribute": "text"
        },
        {
          "name": "url",
          "selector": "a[target='_blank']",
          "attribute": "href"
        },
        {
          "name": "answer_count",
          "selector": "::attr(data-ans)",
          "attribute": "value"
        }
      ]
    },
    {
      "id": 3,
      "type": "click",
      "selector": ".next-page",
      "description": "点击下一页"
    },
    {
      "id": 4,
      "type": "wait",
      "condition": "selector_visible",
      "target": "ul.question-list li",
      "timeout": 10000
    }
  ],
  "list_config": {
    "item_selector": "ul.question-list li",
    "pagination": {
      "type": "click",
      "selector": ".next",
      "max_pages": 500
    }
  },
  "detail_config": {
    "entry": {
      "type": "click",
      "selector": "a[target='_blank']"
    },
    "fields": [
      {
        "name": "question_title",
        "selector": "h1.title",
        "attribute": "text"
      },
      {
        "name": "question_content",
        "selector": ".question-content",
        "attribute": "text"
      },
      {
        "name": "answers",
        "selector": ".answer-item",
        "type": "list",
        "fields": [
          {
            "name": "content",
            "selector": ".answer-content",
            "attribute": "text"
          },
          {
            "name": "answerer",
            "selector": ".answerer-name",
            "attribute": "text"
          },
          {
            "name": "time",
            "selector": ".answer-time",
            "attribute": "text"
          }
        ]
      },
      {
        "name": "category",
        "selector": ".category-tag",
        "attribute": "text"
      },
      {
        "name": "tags",
        "selector": ".tag-list span",
        "attribute": "text",
        "type": "list"
      }
    ]
  }
}
```

### 4.2 任务状态文件 (task_status.json)

```json
{
  "task_id": "uuid-xxxx",
  "config_file": "config_001.json",
  "status": "running|paused|completed|failed",
  "progress": {
    "current_page": 12,
    "total_pages": 500,
    "items_collected": 240,
    "failed_items": 3
  },
  "timing": {
    "started_at": "2026-02-28T10:00:00Z",
    "paused_at": null,
    "resumed_at": null,
    "completed_at": null,
    "total_runtime_seconds": 3600
  },
  "interval_config": {
    "initial": 2,
    "increment": 1,
    "max": 10,
    "current": 4
  },
  "error_log": [
    {
      "timestamp": "2026-02-28T10:05:00Z",
      "page": 5,
      "error": "元素未找到",
      "selector": ".next"
    }
  ]
}
```

### 4.3 采集数据存储

采集的数据存入数据库（已有 Question 模型），字段映射：

| 采集字段 | 数据库字段 |
|----------|------------|
| title | title |
| content | question_content |
| answers | answer_list (JSON) |
| answerer | answer_list[0].answerer |
| publish_time | publish_time |
| category | category |
| tags | tags |

## 5. 核心流程

### 5.1 录制流程

```
┌──────────────┐
│  用户点击    │
│  "开始录制"  │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  启动        │     │  用户操作    │
│  Playwright  │────►│  浏览器     │
│  浏览器窗口  │     │  (点击/滚动) │
└──────┬───────┘     └──────┬───────┘
       │                    │
       │◄───────────────────┘
       │   记录操作步骤
       │
       ▼
┌──────────────┐
│  实时预览    │
│  提取结果    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  用户点击    │
│  "完成录制"  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  保存配置    │
│  config.json │
└──────────────┘
```

### 5.2 执行流程

```
┌──────────────┐
│  用户点击    │
│  "开始采集"  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  加载配置    │
│  config.json │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  访问首页    │
└──────┬───────┘
       │
       ▼
    ┌─┴────────┐
    │  循环    │◄──────────────┐
    │  直到    │               │
    │  完成    │               │
    └─┬────────┘               │
      │                        │
      ▼                        │
┌──────────────┐               │
│  提取列表    │               │
│  数据        │               │
└──────┬───────┘               │
       │                        │
       ▼                        │
┌──────────────┐               │
│  遍历每条    │               │
│  进入详情    │               │
└──────┬───────┘               │
       │                        │
       ▼                        │
┌──────────────┐               │
│  提取详情    │               │
│  保存数据库  │               │
└──────┬───────┘               │
       │                        │
       ▼                        │
┌──────────────┐               │
│  等待间隔    │               │
│  (2s→5s→10s)│               │
└──────┬───────┘               │
       │                        │
       ▼                        │
┌──────────────┐               │
│  点击下一页  │───────────────┘
└──────────────┘
```

### 5.3 暂停/继续流程

```
┌──────────────┐
│   运行中     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  用户点击    │────►│  保存状态    │
│  "暂停"      │     │  task_status│
└──────────────┘     └──────┬───────┘
                            │
                            ▼
                       ┌──────────────┐
                       │  停止浏览器  │
                       │  关闭进程    │
                       └──────────────┘

┌──────────────┐
│   已暂停     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  用户点击    │────►│  读取状态    │
│  "继续"      │     │  task_status │
└──────┬───────┘     └──────┬───────┘
       │                     │
       ▼                     │
┌──────────────┐             │
│  恢复浏览器  │◄────────────┘
│  从断点继续  │
└──────────────┘
```

## 6. 错误处理

### 6.1 反爬处理

- 请求间隔：初始 2s，每页 +1s，最大 10s
- 连续失败 3 次：暂停 5 分钟
- IP 锁定检测：页面出现验证码/403 时自动暂停

### 6.2 错误类型与处理

| 错误类型 | 处理方式 |
|----------|----------|
| 元素未找到 | 重试 2 次，失败则记录并跳过 |
| 网络超时 | 重试 3 次 |
| 页面加载失败 | 刷新页面重试 |
| 反爬拦截 | 暂停并提示用户 |

## 7. API 设计

### 7.1 录制相关

| API | 方法 | 说明 |
|-----|------|------|
| `/api/crawler/recorder/start/` | POST | 启动录制（返回 browser_ws_url） |
| `/api/crawler/recorder/stop/` | POST | 停止录制，保存配置 |
| `/api/crawler/recorder/config/` | GET | 获取当前录制配置 |

### 7.2 任务相关

| API | 方法 | 说明 |
|-----|------|------|
| `/api/crawler/tasks/` | GET | 任务列表 |
| `/api/crawler/tasks/` | POST | 创建采集任务 |
| `/api/crawler/tasks/{id}/start/` | POST | 开始执行 |
| `/api/crawler/tasks/{id}/pause/` | POST | 暂停任务 |
| `/api/crawler/tasks/{id}/resume/` | POST | 继续任务 |
| `/api/crawler/tasks/{id}/stop/` | POST | 停止任务 |
| `/api/crawler/tasks/{id}/status/` | GET | 获取任务状态 |

## 8. 实施计划

### Phase 1: 核心功能

1. Playwright 浏览器管理模块
2. 录制器基础实现
3. 配置文件结构设计

### Phase 2: 执行器

4. 数据提取器实现
5. 翻页与详情页流程
6. 间隔控制逻辑

### Phase 3: 任务管理

7. 暂停/继续功能
8. 断点续传
9. 状态持久化

### Phase 4: 管理后台

10. 任务管理界面
11. 实时进度展示
12. 数据查看功能
