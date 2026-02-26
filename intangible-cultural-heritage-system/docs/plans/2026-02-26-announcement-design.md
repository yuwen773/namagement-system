# 通知公告功能设计方案

**创建日期**: 2026-02-26

## 一、需求概述

为非遗数据平台新增通知公告功能:
- 用户端: 查看已发布的公告列表和详情
- 管理端: CRUD 公告，支持置顶、发布/草稿状态

## 二、数据模型设计

### 公告表 (Announcement)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | 自增主键 | |
| title | Char(200) | 标题 |
| content | TextField | 富文本内容 (HTML) |
| is_published | Boolean | 发布状态 (true=已发布, false=草稿) |
| is_top | Boolean | 置顶状态 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| author | ForeignKey(User) | 发布人 |

## 三、API 接口设计

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| /api/announcements/ | GET | 登录用户 | 列表 (只返回已发布,支持分页) |
| /api/announcements/{id}/ | GET | 登录用户 | 详情 |
| /api/announcements/ | POST | 管理员 | 创建 |
| /api/announcements/{id}/ | PUT/PATCH | 管理员 | 更新 |
| /api/announcements/{id}/ | DELETE | 管理员 | 删除 |
| /api/announcements/all/ | GET | 管理员 | 全部公告(含草稿) |

**列表排序规则**: 置顶 > 发布时间 ( DESC )

## 四、前端页面设计

### 用户端
- `/announcements` - 公告列表页 (卡片式)
- `/announcements/:id` - 公告详情页 (富文本渲染)

### 管理端
- `/admin/announcements` - 公告管理页 (表格 CRUD)

### 侧边栏
新增菜单项: "通知公告" (图标: Bell)

## 五、技术方案

- **后端**: 新建 `announcements` Django app
- **前端**: 新建公告列表/详情/管理页面，复用现有风格
- **富文本**: 使用 HTML textarea + 预览，或 Element Plus 对应组件
