# 响应式设计优化方案

**项目**: 食堂管理系统前端
**日期**: 2026-02-22
**状态**: 已批准

## 1. 目标

让前端在所有屏幕尺寸下都能完美适配，重点优化桌面端（1200px-1920px）体验，同时保持平板和移动端的可用性。

## 2. 断点系统

使用 CSS 变量定义全局统一断点：

```css
:root {
  /* 响应式断点 */
  --breakpoint-xl: 1440px;  /* 大桌面 */
  --breakpoint-lg: 1200px;  /* 桌面 */
  --breakpoint-md: 992px;   /* 小桌面/平板横屏 */
  --breakpoint-sm: 768px;   /* 平板竖屏/大手机 */
  --breakpoint-xs: 480px;   /* 手机 */
}
```

## 3. 统一类名规范

| 类名 | 适用场景 | 断点 |
|------|----------|------|
| `.responsive-xl` | 仅 xl 桌面显示 | ≥1440px |
| `.responsive-lg` | 桌面及以上显示 | ≥1200px |
| `.responsive-md` | 小桌面及以上 | ≥992px |
| `.responsive-sm` | 平板及以上 | ≥768px |
| `.responsive-hide-lg` | 大屏幕隐藏 | ≥1200px |
| `.responsive-show-xs` | 小屏幕显示 | <768px |

## 4. 核心优化点

### 4.1 布局组件

- **AdminLayout**: 侧边栏折叠阈值调整（lg→1200px），内容区 padding 自适应
- **EmployeeLayout**: 水平，缩小菜单项菜单改为响应式间距

### 4.2 表格响应式

- 使用 `overflow-x: auto` + `min-width` 解决横向滚动
- 小屏幕下表格卡片化

### 4.3 卡片Grid布局

- 统一使用 `grid-template-columns: repeat(auto-fit, minmax(XXpx, 1fr))`
- 调整不同断点下的 `minmax` 值

## 5. 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `App.vue` | 添加全局 CSS 变量和响应式工具类 |
| `index.html` | 优化 viewport meta |
| `AdminLayout.vue` | 断点调整 + 布局优化 |
| `EmployeeLayout.vue` | 菜单响应式 + 布局优化 |
| `LoginView.vue` | 优化响应式细节 |
| `DashboardView.vue` | 卡片 grid 优化 |
| 其他业务页面 | 按需调整 |

## 6. 实现步骤

1. 在 `App.vue` 添加全局 CSS 变量和响应式工具类
2. 优化 `index.html` viewport 配置
3. 更新布局组件响应式断点
4. 优化业务页面（表格、卡片、弹窗）
5. 测试验证
