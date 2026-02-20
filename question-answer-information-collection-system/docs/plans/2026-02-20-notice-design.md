# 公告功能设计方案

## 1. 功能概述

为问答信息采集系统添加公告功能，支持管理员发布公告，所有登录用户可查看。

## 2. 后端设计

### 2.1 数据模型

```python
# apps/notices/models.py
class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告列表'
        ordering = ['-created_at']
        db_table = 'notices'
```

### 2.2 API 端点

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| GET | /api/notices/ | 登录用户 | 获取公告列表 |
| GET | /api/notices/{id}/ | 登录用户 | 获取公告详情 |
| POST | /api/notices/ | 管理员 | 创建公告 |
| PUT | /api/notices/{id}/ | 管理员 | 更新公告 |
| DELETE | /api/notices/{id}/ | 管理员 | 删除公告 |

### 2.3 响应格式

```javascript
// 列表
{ "code": 0, "data": [...], "total": n }

// 详情
{ "code": 0, "data": {...} }

// 错误
{ "code": -1, "message": "错误信息" }
```

## 3. 前端设计

### 3.1 管理员页面

- 路由: `/notices`
- 功能: 公告列表展示、搜索、添加、编辑、删除
- 权限: 仅管理员可访问

### 3.2 用户端展示

- 位置: 顶部导航栏右侧消息图标
- 交互: 点击图标弹出公告列表弹窗
- 功能: 查看所有公告（仅阅读，无已读记录）

## 4. 目录结构

```
backend/apps/notices/
├── __init__.py
├── apps.py
├── models.py
├── serializers.py
├── views.py
├── urls.py
└── migrations/

frontend/src/
├── api/notices.js
├── views/NoticeManagement.vue
└── components/AppLayout.vue (修改)
```

## 5. 实施步骤

1. 创建 notices app 并注册
2. 实现 Model、Serializer、ViewSet、URLs
3. 创建前端 API 模块
4. 实现管理员公告管理页面
5. 在 AppLayout 集成消息图标和弹窗
