# 前端设计系统文档
## Frontend Design System Documentation

> 汽车改装件销售推荐平台 - Industrial Performance Aesthetic

---

## 目录

1. [设计原则](#1-设计原则)
2. [颜色系统](#2-颜色系统)
3. [排版系统](#3-排版系统)
4. [间距系统](#4-间距系统)
5. [组件规范](#5-组件规范)
6. [布局系统](#6-布局系统)
7. [响应式设计](#7-响应式设计)
8. [动画与交互](#8-动画与交互)
9. [代码规范](#9-代码规范)
10. [图标系统](#10-图标系统)

---

## 1. 设计原则

### 1.1 核心设计理念

**Industrial Performance Aesthetic** - 工业性能美学

- **专业性**: 体现汽车改装行业的专业性和技术感
- **现代感**: 使用深色主题配合玻璃态效果
- **性能感**: 强调速度、动力、改装的性能特质
- **可信赖**: 通过清晰的层次和一致的设计建立信任

### 1.2 设计关键词

```
专业 · 现代 · 性能 · 可信赖
```

### 1.3 设计目标

1. **视觉一致性**: 所有页面和组件遵循统一的设计语言
2. **用户体验**: 直观、高效、愉悦的交互体验
3. **性能优先**: 快速加载、流畅动画
4. **可访问性**: 清晰的对比度、易读的文字大小
5. **响应式**: 适配所有设备尺寸

---

## 2. 颜色系统

### 2.1 主色调

| 颜色名称 | HEX | RGB | 用途 |
|---------|-----|-----|------|
| 主色 | `#f97316` | `rgb(249, 115, 22)` | 主要操作、按钮、链接、强调 |
| 主色深 | `#ea580c` | `rgb(234, 88, 12)` | 渐变、悬停状态 |

```css
--primary: #f97316;
--primary-dark: #ea580c;
--primary-gradient: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
```

### 2.2 中性色

| 颜色名称 | HEX | 用途 |
|---------|-----|------|
| 背景深 | `#0f172a` | 主背景 |
| 背景浅 | `#1e293b` | 次级背景 |
| 背景卡片 | `rgba(30, 41, 59, 0.5)` | 卡片背景 |
| 边框 | `rgba(71, 85, 105, 0.5)` | 边框线条 |

```css
--bg-dark: #0f172a;
--bg-light: #1e293b;
--bg-card: rgba(30, 41, 59, 0.5);
--border: rgba(71, 85, 105, 0.5);
```

### 2.3 文字颜色

| 颜色名称 | HEX | 用途 |
|---------|-----|------|
| 主文字 | `#e2e8f0` | 标题、正文 |
| 次文字 | `#94a3b8` | 描述、次要信息 |
| 辅助文字 | `#64748b` | 提示、占位符 |
| 禁用文字 | `#475569` | 禁用状态 |

```css
--text-primary: #e2e8f0;
--text-secondary: #94a3b8;
--text-tertiary: #64748b;
--text-disabled: #475569;
```

### 2.4 功能色

| 颜色 | HEX | 用途 |
|-----|-----|------|
| 成功 | `#22c55e` | 成功提示、确认 |
| 警告 | `#fbbf24` | 警告提示 |
| 错误 | `#ef4444` | 错误、删除 |
| 信息 | `#3b82f6` | 信息提示 |

```css
--success: #22c55e;
--warning: #fbbf24;
--error: #ef4444;
--info: #3b82f6;
```

---

## 3. 排版系统

### 3.1 字体家族

```css
/* 系统字体栈 */
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
               'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
               sans-serif;
```

### 3.2 字体大小

| 级别 | 大小 | 字重 | 行高 | 用途 |
|-----|------|------|------|------|
| H1 | 56px | 800 | 1.1 | 页面主标题 |
| H2 | 36px | 700 | 1.2 | 区块标题 |
| H3 | 24px | 700 | 1.3 | 小节标题 |
| H4 | 18px | 600 | 1.4 | 卡片标题 |
| Body | 14px | 400 | 1.6 | 正文 |
| Small | 12px | 400 | 1.5 | 辅助文字 |
| Tiny | 11px | 600 | 1.4 | 标签、徽章 |

```css
--font-size-h1: clamp(36px, 6vw, 56px);
--font-size-h2: clamp(28px, 4vw, 36px);
--font-size-h3: 20px;
--font-size-h4: 16px;
--font-size-body: 14px;
--font-size-small: 12px;
--font-size-tiny: 11px;
```

### 3.3 字重

```css
--font-weight-light: 300;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-extrabold: 800;
```

### 3.4 文字样式

```css
/* 大写 */
.text-uppercase {
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* 渐变文字 */
.text-gradient {
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## 4. 间距系统

### 4.1 间距比例

基于 4px 基础单位的间距系统：

| 名称 | 大小 | 用途 |
|-----|------|------|
| xs | 4px | 紧凑元素间距 |
| sm | 8px | 小元素内间距 |
| md | 16px | 标准间距 |
| lg | 24px | 卡片内边距 |
| xl | 32px | 区块间距 |
| 2xl | 40px | 大区块间距 |
| 3xl | 60px | 页面级间距 |

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-2xl: 40px;
--spacing-3xl: 60px;
```

### 4.2 容器宽度

```css
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1200px;
--container-2xl: 1400px;
```

### 4.3 圆角

```css
--radius-sm: 6px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-full: 9999px;
```

---

## 5. 组件规范

### 5.1 按钮

#### 主要按钮

```html
<button class="btn btn-primary">
  <span>立即购买</span>
</button>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

#### 次要按钮

```html
<button class="btn btn-secondary">
  <span>取消</span>
</button>
```

```css
.btn-secondary {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  color: #e2e8f0;
}

.btn-secondary:hover {
  border-color: #f97316;
  color: #f97316;
}
```

#### 尺寸变体

```css
.btn-sm { padding: 8px 16px; font-size: 12px; }
.btn-lg { padding: 16px 32px; font-size: 16px; }
```

### 5.2 输入框

```html
<div class="input-group">
  <svg class="input-icon">...</svg>
  <input type="text" class="input-field" placeholder="请输入..." />
</div>
```

```css
.input-group {
  display: flex;
  align-items: center;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  padding: 4px;
  transition: all 0.3s ease;
}

.input-group:focus-within {
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.input-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
  margin: 0 12px;
}

.input-field {
  flex: 1;
  background: none;
  border: none;
  color: #e2e8f0;
  font-size: 14px;
  outline: none;
}

.input-field::placeholder {
  color: #64748b;
}
```

### 5.3 卡片

```html
<div class="card">
  <div class="card-header">标题</div>
  <div class="card-body">内容</div>
  <div class="card-footer">底部</div>
</div>
```

```css
.card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
}

.card-body {
  padding: 24px;
}

.card-footer {
  padding: 16px 24px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}
```

### 5.4 徽章

```html
<span class="badge badge-hot">HOT</span>
<span class="badge badge-new">NEW</span>
```

```css
.badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.badge-hot {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
}

.badge-new {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: #ffffff;
}
```

### 5.5 面包屑

```css
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
}

.breadcrumb-item {
  color: #94a3b8;
  font-size: 13px;
}

.breadcrumb-item:hover {
  color: #f97316;
}

.breadcrumb-separator {
  color: #475569;
  font-size: 12px;
}
```

---

## 6. 布局系统

### 6.1 页面结构

```
UserLayout
├── AppHeader
│   ├── TopBar
│   ├── MainHeader (Logo + Search + Cart)
│   └── NavBar
├── Main Content (router-view)
└── AppFooter
```

### 6.2 容器

```css
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.container-sm { max-width: 640px; }
.container-md { max-width: 768px; }
.container-lg { max-width: 1024px; }
.container-xl { max-width: 1200px; }
```

### 6.3 网格系统

```css
.grid {
  display: grid;
  gap: 24px;
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }

.grid-auto {
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}
```

### 6.4 Flex 布局

```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.gap-sm { gap: 8px; }
.gap-md { gap: 16px; }
.gap-lg { gap: 24px; }
```

---

## 7. 响应式设计

### 7.1 断点系统

```css
/* 移动设备 */
@media (max-width: 640px) { /* sm */ }

/* 平板设备 */
@media (max-width: 768px) { /* md */ }

/* 小型桌面 */
@media (max-width: 1024px) { /* lg */ }

/* 桌面设备 */
@media (max-width: 1280px) { /* xl */ }

/* 大屏设备 */
@media (min-width: 1281px) { /* 2xl */ }
```

### 7.2 响应式字体

```css
h1 { font-size: clamp(36px, 6vw, 56px); }
h2 { font-size: clamp(28px, 4vw, 36px); }
h3 { font-size: clamp(20px, 3vw, 24px); }
```

### 7.3 响应式间距

```css
.section {
  padding: clamp(40px, 8vw, 80px) 20px;
}
```

### 7.4 移动端适配策略

1. **隐藏次要元素**: 在小屏幕上隐藏装饰性元素
2. **堆叠布局**: 将多列布局转换为单列
3. **简化导航**: 使用汉堡菜单或水平滚动
4. **调整间距**: 减少移动端的内边距和外边距
5. **触控优化**: 增大可点击区域（最小 44x44px）

---

## 8. 动画与交互

### 8.1 过渡时长

```css
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
```

### 8.2 缓动函数

```css
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

### 8.3 常用动画

#### 淡入淡出

```css
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
```

#### 滑动

```css
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(100%);
}
```

#### 缩放

```css
.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
```

### 8.4 悬停效果

```css
/* 按钮悬停 */
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

/* 卡片悬停 */
.card:hover {
  border-color: rgba(249, 115, 22, 0.5);
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* 图片悬停 */
.card-image {
  transition: transform 0.4s ease;
}

.card:hover .card-image {
  transform: scale(1.08);
}
```

### 8.5 加载动画

```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

---

## 9. 代码规范

### 9.1 文件组织

```
frontend/src/
├── api/
│   ├── request.ts          # Axios 配置
│   └── modules/
│       ├── auth.ts
│       ├── product.ts
│       └── ...
├── assets/
│   ├── images/
│   └── styles/
│       └── global.css
├── components/
│   ├── common/
│   │   ├── AppHeader.vue
│   │   ├── AppFooter.vue
│   │   └── ...
│   └── layouts/
│       ├── UserLayout.vue
│       └── AdminLayout.vue
├── router/
│   └── index.ts
├── stores/
│   ├── auth.ts
│   ├── cart.ts
│   └── ...
├── utils/
│   ├── format.ts
│   └── validate.ts
├── views/
│   ├── HomeView.vue
│   ├── ProductListView.vue
│   └── ...
├── App.vue
└── main.ts
```

### 9.2 Vue 组件规范

#### 组件命名

```vue
<!-- 文件名：PascalCase -->
ProductCard.vue

<!-- 组件名：PascalCase -->
<script setup>
defineOptions({
  name: 'ProductCard'
})
</script>
```

#### 组合式 API

```vue
<script setup>
// 导入
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 状态
const loading = ref(false)
const items = ref([])

// 计算属性
const total = computed(() => items.value.length)

// 方法
function handleClick() {
  // ...
}

// 生命周期
onMounted(() => {
  // ...
})
</script>
```

#### Props 定义

```vue
<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>
```

### 9.3 CSS 规范

#### BEM 命名

```css
/* Block */
.card { }

/* Element */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier */
.card--highlight { }
.card--disabled { }
```

#### CSS 变量

```css
:root {
  /* Colors */
  --primary: #f97316;

  /* Spacing */
  --spacing-md: 16px;

  /* Radius */
  --radius-lg: 12px;

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 20px 40px rgba(0, 0, 0, 0.3);
}
```

#### Scoped Styles

```vue
<style scoped>
.component-name {
  /* 样式 */
}

:deep(.child-class) {
  /* 深度选择器 */
}
</style>
```

### 9.4 TypeScript 规范

```typescript
// 接口定义
interface Product {
  id: number
  name: string
  price: number
  image: string
}

// 类型别名
type ProductStatus = 'draft' | 'pending' | 'published' | 'archived'

// 函数签名
function fetchProduct(id: number): Promise<Product> {
  // ...
}
```

---

## 10. 图标系统

### 10.1 图标使用原则

1. **优先使用内联 SVG**: 性能最佳，可自定义样式
2. **统一风格**: 使用线条风格（stroke）的图标
3. **适当大小**: 根据使用场景选择合适的尺寸
4. **颜色继承**: 图标颜色应从父元素继承

### 10.2 内联 SVG 模板

```vue
<template>
  <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
    <path
      d="..."
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>
```

### 10.3 常用图标

| 图标 | 用途 | 尺寸 |
|-----|------|------|
| Logo | 品牌 Logo | 32px |
| Search | 搜索 | 18px |
| Cart | 购物车 | 22px |
| User | 用户 | 16px |
| Heart | 收藏 | 18px |
| Star | 评分 | 16px |
| Settings | 设置 | 18px |
| Close | 关闭 | 14px |
| Check | 确认 | 16px |
| Chevron | 箭头 | 14px |

---

## 附录 A：快速开始

### 创建新页面

```vue
<template>
  <div class="page-view">
    <!-- 页面内容 -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(false)

onMounted(() => {
  // 初始化
})
</script>

<style scoped>
.page-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 40px 20px;
}
</style>
```

### 创建新组件

```vue
<template>
  <div class="custom-component" :class="{ 'is-active': active }">
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  active?: boolean
}

withDefaults(defineProps<Props>(), {
  active: false
})
</script>

<style scoped>
.custom-component {
  /* 样式 */
}

.custom-component.is-active {
  /* 激活状态 */
}
</style>
```

---

## 附录 B：设计检查清单

### 发布前检查

- [ ] 所有页面遵循统一的设计系统
- [ ] 颜色对比度符合可访问性标准
- [ ] 所有交互元素有明确的悬停/焦点状态
- [ ] 移动端适配完整测试
- [ ] 加载状态和错误处理完整
- [ ] 动画流畅且性能良好
- [ ] 表单验证提示清晰
- [ ] 图片使用正确的尺寸和格式

---

## 附录 C：资源链接

### 设计工具
- Figma: https://www.figma.com
- Sketch: https://www.sketch.com
- Adobe XD: https://www.adobe.com/products/xd.html

### 图标资源
- Heroicons: https://heroicons.com
- Feather Icons: https://feathericons.com
- Tabler Icons: https://tabler-icons.io

### 颜色工具
- Coolors: https://coolors.co
- Adobe Color: https://color.adobe.com

### 字体资源
- Google Fonts: https://fonts.google.com
- Font Squirrel: https://www.fontsquirrel.com

---

**版本**: 1.0.0
**最后更新**: 2026-02-04
**维护者**: 前端开发团队
