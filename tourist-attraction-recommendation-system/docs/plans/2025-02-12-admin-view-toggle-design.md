# 管理端双视图模式设计方案

> 2025-02-12

## 概述

为管理端的四个页面（用户管理、景点管理、评论审核、公告管理）添加卡片/列表双视图切换功能，提升管理员在不同场景下的工作效率。

## 核心设计

### 视图切换位置
- **位置**：搜索栏旁边
- **组件**：通用 `ViewToggle.vue`
- **默认视图**：列表视图
- **状态持久化**：不需要，每次刷新恢复默认

## 各页面列表视图列配置

### 1. UserManage.vue - 用户管理（精简模式）

| 列名 | 字段 | 宽度 | 说明 |
|------|------|------|------|
| 头像 | - | 80px | 显示首字母圆形头像 |
| 用户名 | username | 150px | 可点击查看详情 |
| 真实姓名 | realName | 150px | - |
| 角色 | role | 120px | Badge样式显示 |
| 状态 | isActive | 100px | 使用 `el-switch` |
| 操作 | - | 120px | 编辑/禁用按钮 |

### 2. AttractionManage.vue - 景点管理（标准模式）

| 列名 | 字段 | 宽度 | 说明 |
|------|------|------|------|
| 封面图 | coverImage | 100px | 圆角缩略图 |
| 景点名称 | name | 200px | 主标题 |
| 分类 | category | 120px | Badge标签样式 |
| 地区 | region | 150px | - |
| 评分 | rating | 100px | 星星图标+数字 |
| 浏览量 | viewCount | 120px | 数字格式化 |
| 评论数 | commentCount | 100px | 数字显示 |
| 操作 | - | 150px | 编辑/删除按钮 |

### 3. CommentReview.vue - 评论审核（精简模式）

| 列名 | 字段 | 宽度 | 说明 |
|------|------|------|------|
| 用户 | user | 150px | 头像+用户名组合列 |
| 景点名称 | attraction.name | 180px | 可点击跳转 |
| 评分 | rating | 120px | 5星评分组件 |
| 评论内容 | content | 300px | 限制显示100字，超出省略 |
| 状态 | status | 120px | Badge样式（待审核/已通过/已驳回） |
| 操作 | - | 180px | 通过/驳回按钮 |

### 4. AnnouncementManage.vue - 公告管理（标准模式）

| 列名 | 字段 | 宽度 | 说明 |
|------|------|------|------|
| 标题 | title | 250px | 主标题 |
| 内容预览 | content | 350px | 限制80字，超出省略 |
| 发布时间 | createdAt | 180px | 格式化时间显示 |
| 发布人 | - | 150px | 显示"管理员" |
| 操作 | - | 120px | 删除按钮 |

## 组件设计

### ViewToggle.vue

```vue
<template>
  <div class="view-toggle">
    <button
      v-for="mode in modes"
      :key="mode.value"
      :class="['toggle-button', { active: modelValue === mode.value }]"
      @click="$emit('update:modelValue', mode.value)"
    >
      <svg viewBox="0 0 20 20" v-html="mode.icon"></svg>
      <span>{{ mode.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String
})

defineEmits(['update:modelValue'])

const modes = [
  {
    value: 'list',
    label: '列表',
    icon: '<path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>'
  },
  {
    value: 'card',
    label: '卡片',
    icon: '<path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>'
  }
]
</script>

<style scoped>
.view-toggle {
  display: flex;
  gap: 8px;
  padding: 4px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
}

.toggle-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-button svg {
  width: 18px;
  height: 18px;
}

.toggle-button:hover {
  background: #f9fafb;
}

.toggle-button.active {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
}
</style>
```

## 样式规范

### 列表视图样式

```css
:deep(.el-table) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-family: 'DM Sans', sans-serif;
}

:deep(.el-table th) {
  background: #f9fafb;
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
}

:deep(.el-table tr:hover) {
  background: #fffbeb;
}

:deep(.el-table--border) {
  border: none;
}

:deep(.el-table td) {
  border-color: #f3f4f6;
}
```

### 响应式处理

```css
@media (max-width: 1024px) {
  .hide-on-tablet {
    display: none;
  }
}

@media (max-width: 768px) {
  .view-toggle {
    display: none; /* 移动端强制卡片视图 */
  }
}
```

## 文件结构

```
frontend/src/
├── components/
│   └── ViewToggle.vue          # 新增：通用视图切换组件
└── views/admin/
    ├── UserManage.vue          # 修改：添加列表视图
    ├── AttractionManage.vue    # 修改：添加列表视图
    ├── CommentReview.vue        # 修改：添加列表视图
    └── AnnouncementManage.vue   # 修改：添加列表视图
```

## 实现要点

1. **状态管理**：每个页面添加 `viewMode = ref('list')`
2. **条件渲染**：使用 `v-if="viewMode === 'list'"` 和 `v-else`
3. **逻辑复用**：搜索、筛选、分页逻辑在两种视图间共享
4. **统一样式**：列表视图延续橙色主题和圆角设计

## API 无需修改

现有 API 已满足列表视图需求，无需后端变更。
