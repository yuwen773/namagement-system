# 公告功能设计文档

**日期**: 2026-02-28
**状态**: 设计完成

---

## 1. 需求概述

为天猫宠物用品数据采集系统新增公告功能，管理员可发布系统通知（维护、更新、采集通知等），用户可查看已发布公告。

---

## 2. 数据模型

### Announcement 模型

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | UUID | 主键 |
| `title` | String(200) | 公告标题 |
| `content` | Text | 公告内容（纯文本） |
| `priority` | Integer | 优先级：1=普通，2=重要，3=紧急 |
| `status` | String(20) | 状态：draft=草稿，published=已发布 |
| `is_pinned` | Boolean | 是否置顶 |
| `created_by` | FK(User) | 创建人 |
| `created_at` | DateTime | 创建时间 |
| `updated_at` | DateTime | 更新时间 |
| `published_at` | DateTime | 发布时间（可空） |

**排序规则**：置顶优先 → 优先级高优先 → 发布时间倒序

---

## 3. 后端 API

### 文件结构
```
backend/announcements/
├── __init__.py
├── models.py          # Announcement 模型
├── serializers.py     # DRF 序列化器
├── views.py           # ViewSets
├── urls.py            # 路由
└── admin.py           # Django Admin
```

### API 端点

| 端点 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/announcements/` | GET | 全部用户 | 获取已发布公告列表 |
| `/api/announcements/{id}/` | GET | 全部用户 | 获取公告详情 |
| `/api/admin/announcements/` | GET | 管理员 | 获取所有公告（含草稿） |
| `/api/admin/announcements/` | POST | 管理员 | 创建公告 |
| `/api/admin/announcements/{id}/` | PUT | 管理员 | 更新公告 |
| `/api/admin/announcements/{id}/` | DELETE | 管理员 | 删除公告 |
| `/api/admin/announcements/{id}/publish/` | POST | 管理员 | 发布草稿 |

### 权限
- 普通用户：只能访问 `status=published` 的公告
- 管理员：可管理所有公告
- 复用 `users/permissions.py` 中的 `IsAdmin` 权限类

---

## 4. 前端页面

### API 封装
```
frontend/src/api/announcementApi.js
```

### 管理端页面

| 路由 | 组件 | 功能 |
|------|------|------|
| `/admin/announcements` | AnnouncementList.vue | 公告列表（CRUD表格） |
| `/admin/announcements/edit` | AnnouncementEdit.vue | 新增/编辑公告 |

**AnnouncementList.vue**:
- 顶部：状态筛选（全部/草稿/已发布）、新建按钮
- 表格：标题、优先级标签、状态、置顶、发布时间、操作
- 操作列：编辑、删除、发布/取消发布

**AnnouncementEdit.vue**:
- 标题输入框
- 优先级下拉选择（普通/重要/紧急）
- 内容多行文本框
- 置顶开关
- 保存草稿 / 立即发布 按钮

### 用户端页面

| 路由 | 组件 | 功能 |
|------|------|------|
| `/user/announcements` | AnnouncementCenter.vue | 公告中心 |

**AnnouncementCenter.vue**:
- 卡片式展示
- 置顶公告高亮区域
- 优先级标签显示
- 按时间线展示

---

## 5. UI 设计规范

### 优先级标签颜色

| 优先级 | Element Plus 类型 | 颜色 |
|--------|-----------------|------|
| 普通 | `info` | 灰蓝色 |
| 重要 | `warning` | 橙色 |
| 紧急 | `danger` | 红色 |

### 状态标签

| 状态 | Element Plus 类型 |
|------|-----------------|
| 草稿 | `info` |
| 已发布 | `success` |

---

## 6. 关键业务逻辑

### 发布操作
- 将 `status` 改为 `published`
- 设置 `published_at` 为当前时间
- 如果之前已发布过，保持原 `published_at`

### 列表排序
```python
queryset = Announcement.objects.filter(status='published')
queryset = queryset.order_by('-is_pinned', '-priority', '-published_at')
```

---

## 7. 测试检查点

- [ ] 管理员创建草稿，普通用户不可见
- [ ] 发布后普通用户可见
- [ ] 置顶公告排在最前
- [ ] 优先级排序正确
- [ ] 编辑后时间更新正确
- [ ] 删除操作正确级联

---

## 8. 文件清单

### 后端
- `backend/announcements/__init__.py`
- `backend/announcements/models.py`
- `backend/announcements/serializers.py`
- `backend/announcements/views.py`
- `backend/announcements/urls.py`
- `backend/announcements/admin.py`
- `backend/tmall_project/urls.py` (更新)

### 前端
- `frontend/src/api/announcementApi.js`
- `frontend/src/views/admin/AnnouncementList.vue`
- `frontend/src/views/admin/AnnouncementEdit.vue`
- `frontend/src/views/user/AnnouncementCenter.vue`
- `frontend/src/router/index.js` (更新)
- `frontend/src/components/Layout/AdminLayout.vue` (更新菜单)

---

## 9. 数据库迁移

```sql
CREATE TABLE announcements (
    id CHAR(32) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority INT NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    is_pinned BOOLEAN NOT NULL DEFAULT FALSE,
    created_by_id CHAR(32),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    published_at DATETIME,
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);
```
