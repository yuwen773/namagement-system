# 菜谱数据分析系统 - 前端设计规范

> 版本：v1.0
> 更新日期：2026-01-31
> 基础主题：美食主题（Culinary Theme）

---

## 设计理念

### 核心原则

本设计遵循 **frontend-design skill** 的设计哲学：

1. **拒绝通用 AI 美学**：避免紫白渐变、Inter/Roboto 等过度使用的字体和配色
2. **主题驱动**：每个设计都应从项目本质出发，选择契合的美学方向
3. **大胆承诺**：选择明确的设计方向并精确执行，不做妥协
4. **细节至上**：每个像素、每个动画都经过深思熟虑

### 项目主题定位

| 属性 | 选择 | 理由 |
|:-----|:-----|:-----|
| **主题** | 美食/烹饪 | 菜谱数据分析系统的核心内容 |
| **氛围** | 温暖、诱人、专业 | 唤起食欲与信任感 |
| **参考** | 米其林餐厅、美食杂志 | 优雅而不失亲和力 |
| **避免** | 冷色调、科技感、过度现代 | 与美食主题不符 |

---

## 配色系统

### 主色调 - 温暖琥珀系

灵感来自熟食、香料和烘焙的金棕色调。

```css
/* 主色 - 琥珀橙渐变 */
--color-primary-light: #d4773a;  /* 渐变起点 */
--color-primary:       #c2622e;  /* 主要品牌色 */
--color-primary-dark:  #a35220;  /* 渐变终点 */

/* 中性色 - 大地色系 */
--color-text-primary:   #3d2914;  /* 巧克力棕 - 主要文字 */
--color-text-secondary: #6b5c4d;  /* 次要文字 */
--color-text-tertiary:  #8b7355;  /* 辅助文字 */
--color-text-hint:      #b8a99a;  /* 提示文字 */

/* 背景色 - 奶油色系 */
--color-bg-primary:     #faf8f5;  /* 页面背景 */
--color-bg-secondary:   #f5f0e8;  /* 卡片背景渐变 */
--color-bg-elevated:    #ffffff;  /* 悬浮层/卡片 */

/* 边框与分割线 */
--color-border-light:   #e5ddd3;
--color-border-medium:  #f0ebe3;
--color-border-dark:    #d4c8b8;

/* 功能色 */
--color-success: #4caf50;
--color-warning: #ff9800;
--color-error:   #f44336;
--color-info:    #2196f3;
```

### 渐变定义

```css
/* 主渐变 - 用于品牌区、按钮背景 */
--gradient-primary: linear-gradient(135deg, #d4773a 0%, #c2622e 50%, #a35220 100%);

/* 背景渐变 - 用于页面背景 */
--gradient-bg: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);

/* 玻璃态背景 - 用于悬浮卡片 */
--bg-glass: rgba(255, 255, 255, 0.1);
--border-glass: rgba(255, 255, 255, 0.2);
```

### 色彩应用规则

| 场景 | 使用色彩 | 说明 |
|:-----|:---------|:-----|
| 主按钮 | 主渐变 | 悬停时加深，添加阴影 |
| 链接 | `--color-primary` | 悬停时转为 `--color-primary-dark` |
| 标题 | `--color-text-primary` | 使用 Playfair Display |
| 正文 | `--color-text-secondary` | 使用 DM Sans |
| 占位符 | `--color-text-hint` | 输入框、表单提示 |
| 边框 | `--color-border-light` | 交互元素默认状态 |
| 焦点边框 | `--color-primary` | 输入框焦点时 |

---

## 字体系统

### 字体选择

**告别通用字体**：不使用 Inter、Roboto、Arial、系统字体等。

```css
/* Google Fonts 引入 */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
```

### 字体家族

| 用途 | 字体 | 风格 | 适用场景 |
|:-----|:-----|:-----|:---------|
| **标题/展示** | Playfair Display | 优雅衬线 | 页面标题、Logo、大标题 |
| **正文/UI** | DM Sans | 现代无衬线 | 表单、按钮、正文 |
| **数据/数字** | DM Sans | 清晰可读 | 统计数据、数字 |

### 字阶系统

```css
/* 标题字阶 */
--font-size-display: 3.5rem;   /* 56px - 装饰区大标题 */
--font-size-h1:      2.5rem;   /* 40px - 页面主标题 */
--font-size-h2:      1.75rem;  /* 28px - 卡片标题 */
--font-size-h3:      1.5rem;   /* 24px - 小标题 */

/* 正文字阶 */
--font-size-large:   1.1rem;   /* 18px - 重要文本 */
--font-size-base:    1rem;     /* 16px - 正文 */
--font-size-small:   0.95rem;  /* 15px - 表单输入 */
--font-size-xs:      0.9rem;   /* 14px - 辅助信息 */
--font-size-xxs:     0.85rem;  /* 13px - 版权信息 */

/* 数据字阶 */
--font-size-stat:    1.75rem;  /* 28px - 统计数值 */
--font-size-stat-label: 0.85rem; /* 13px - 统计标签 */
```

### 字重与行高

```css
/* 字重 */
--font-weight-regular: 400;
--font-weight-medium:   500;
--font-weight-semibold: 600;
--font-weight-bold:     700;

/* 行高 */
--line-height-tight:   1.1;  /* 标题 */
--line-height-normal:  1.5;  /* 正文 */
--line-height-relaxed: 1.8;  /* 长文 */
```

### 字体应用规则

| 元素 | 字体 | 大小 | 字重 | 行高 |
|:-----|:-----|:-----|:-----|:-----|
| 装饰区标题 | Playfair Display | 3.5rem | 700 | 1.1 |
| 页面标题 | Playfair Display | 1.75rem | 700 | 1.1 |
| Logo | Playfair Display | 1.5rem | 700 | - |
| 正文 | DM Sans | 1rem | 400 | 1.5 |
| 表单输入 | DM Sans | 0.95rem | 400 | - |
| 按钮 | DM Sans | 1rem | 600 | - |
| 统计数值 | DM Sans | 1.75rem | 700 | - |

---

## 间距系统

### 基础间距单位

基于 `4px` 基础单位的倍数系统。

```css
--space-1:  0.25rem;  /* 4px */
--space-2:  0.5rem;   /* 8px */
--space-3:  0.75rem;  /* 12px */
--space-4:  1rem;     /* 16px */
--space-5:  1.25rem;  /* 20px */
--space-6:  1.5rem;   /* 24px */
--space-8:  2rem;     /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
```

### 组件内间距

| 组件 | 内边距 | 说明 |
|:-----|:-------|:-----|
| 卡片 | 2.5rem | 大卡片（登录页） |
| 卡片（小） | 1.75rem | 移动端或小卡片 |
| 输入框 | 0.75rem 1rem | 上下 0.75rem，左右 1rem |
| 按钮 | 0 1.5rem | 左右内边距 |
| 表单项间距 | 1.25rem | 表单元素之间 |

---

## 圆角与阴影

### 圆角系统

```css
--radius-sm:  8px;   /* 小元素 */
--radius-md:  12px;  /* 输入框、小按钮 */
--radius-lg:  16px;  /* 统计卡片 */
--radius-xl:  20px;  /* 移动端卡片 */
--radius-2xl: 24px;  /* 桌面端卡片 */
```

### 阴影系统

```css
/* 轻微阴影 - 输入框默认 */
--shadow-sm: 0 0 1px rgba(61, 41, 20, 0.1);

/* 卡片阴影 */
--shadow-card: 0 4px 24px rgba(61, 41, 20, 0.08), 0 0 1px rgba(61, 41, 20, 0.1);

/* 悬浮阴影 */
--shadow-hover: 0 8px 32px rgba(194, 98, 46, 0.25);

/* 强调阴影 - 按钮 */
--shadow-primary: 0 8px 24px rgba(194, 98, 46, 0.35);
```

---

## 组件规范

### 按钮

#### 主按钮

```css
/* 样式 */
background: var(--gradient-primary);
border: none;
border-radius: var(--radius-md);
height: 48px;
padding: 0 1.5rem;
font-size: 1rem;
font-weight: 600;
color: white;

/* 悬停状态 */
transform: translateY(-1px);
box-shadow: var(--shadow-primary);

/* 点击状态 */
transform: translateY(0);
```

#### 次按钮

```css
background: transparent;
border: 1.5px solid var(--color-primary);
color: var(--color-primary);
```

### 输入框

```css
/* 默认状态 */
border: 1.5px solid var(--color-border-light);
border-radius: var(--radius-md);
padding: 0.75rem 1rem;
font-size: 0.95rem;
color: var(--color-text-primary);

/* 悬停状态 */
border-color: var(--color-primary-light);

/* 焦点状态 */
border-color: var(--color-primary);
box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);

/* 占位符 */
color: var(--color-text-hint);
```

### 卡片

```css
background: var(--color-bg-elevated);
border-radius: var(--radius-2xl);
padding: var(--space-10);
box-shadow: var(--shadow-card);
```

---

## 动画与交互

### 动画原则

1. **克制使用**：专注关键时刻，而非分散的微交互
2. **CSS 优先**：优先使用纯 CSS 动画
3. **性能导向**：使用 transform 和 opacity，避免 layout 属性
4. **缓动函数**：使用 ease-out 或自定义贝塞尔曲线

### 标准动画

```css
/* 淡入上升 - 页面加载 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 淡入 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 悬停过渡 */
transition: all 0.3s ease;
transition: color 0.2s ease;
transition: border-color 0.2s ease;
```

### 交互状态

| 状态 | 变换 | 时长 |
|:-----|:-----|:-----|
| 按钮悬停 | translateY(-1px) | 0.3s |
| 按钮点击 | translateY(0) | - |
| 链接悬停 | color 变化 | 0.2s |
| 输入焦点 | border + shadow | 0.2s |
| 页面加载 | fadeInUp | 0.5s |

---

## 布局系统

### 容器

```css
/* 页面容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

/* 表单容器 */
.form-wrapper {
  max-width: 420px;
  margin: 0 auto;
}
```

### Flexbox 工具

```css
/* 居中 */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 垂直居中 */
.flex-col-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}
```

---

## 响应式设计

### 断点系统

```css
/* 移动端优先 */
/* 默认 < 480px */

--breakpoint-sm:  480px;   /* 小屏手机 */
--breakpoint-md:  768px;   /* 平板 */
--breakpoint-lg:  1024px;  /* 桌面端 */
--breakpoint-xl:  1280px;  /* 大屏幕 */
```

### 响应式规则

| 元素 | 移动端 | 平板+ |
|:-----|:-------|:------|
| 装饰区 | 隐藏 | 显示（55% 宽度） |
| 卡片内边距 | 1.75rem | 2.5rem |
| 标题字号 | 1.5rem | 1.75rem |
| 页面内边距 | 1rem | 2rem |

---

## Element Plus 样式覆盖

### 颜色变量覆盖

```css
:root {
  --el-color-primary: #c2622e;
  --el-color-primary-light-3: #d4773a;
  --el-color-primary-dark-2: #a35220;
  --el-border-radius: 12px;
}
```

### 组件覆盖规则

| 组件 | 覆盖属性 | 新值 |
|:-----|:---------|:-----|
| el-input | 边框颜色、圆角 | #e5ddd3, 12px |
| el-checkbox | 选中颜色 | #c2622e |
| el-button | 主色渐变 | 琥珀橙渐变 |

---

## CSS 变量清单（完整）

```css
:root {
  /* === 颜色 === */
  --color-primary-light: #d4773a;
  --color-primary: #c2622e;
  --color-primary-dark: #a35220;
  --color-text-primary: #3d2914;
  --color-text-secondary: #6b5c4d;
  --color-text-tertiary: #8b7355;
  --color-text-hint: #b8a99a;
  --color-bg-primary: #faf8f5;
  --color-bg-secondary: #f5f0e8;
  --color-bg-elevated: #ffffff;
  --color-border-light: #e5ddd3;
  --color-border-medium: #f0ebe3;

  /* === 字体 === */
  --font-display: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-size-h2: 1.75rem;
  --font-size-base: 1rem;
  --font-size-small: 0.95rem;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* === 间距 === */
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;

  /* === 圆角 === */
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-2xl: 24px;

  /* === 阴影 === */
  --shadow-card: 0 4px 24px rgba(61, 41, 20, 0.08), 0 0 1px rgba(61, 41, 20, 0.1);
  --shadow-primary: 0 8px 24px rgba(194, 98, 46, 0.35);

  /* === 渐变 === */
  --gradient-primary: linear-gradient(135deg, #d4773a 0%, #c2622e 50%, #a35220 100%);
  --gradient-bg: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
}
```

---

## 设计检查清单

开发新页面时，确保：

- [ ] 使用主题配色（琥珀橙系），而非紫色或蓝色
- [ ] 使用规定字体（Playfair Display + DM Sans），而非 Inter 或 Roboto
- [ ] 应用 CSS 变量，避免硬编码颜色值
- [ ] 组件圆角符合规范（12px/16px/24px）
- [ ] 添加页面加载动画
- [ ] 响应式设计覆盖移动端
- [ ] Element Plus 组件样式已覆盖
- [ ] 悬停/焦点状态有反馈
- [ ] 过渡动画时长 0.2-0.3s

---

## 设计示例参考

### 登录页面（已实现）

- **布局**：双栏（装饰区 55% + 表单区）
- **装饰**：渐变背景 + SVG 图标 + 统计数据 + 装饰圆圈
- **表单**：白色卡片，圆角 24px，柔和阴影
- **动画**：fadeInUp 入场，按钮悬停上浮

### 待实现页面建议

| 页面 | 布局建议 | 特色元素 |
|:-----|:---------|:---------|
| 注册页 | 单栏居中卡片 | 食材图标装饰 |
| 菜谱列表 | 网格卡片 | 卡片悬停阴影 |
| 菜谱详情 | 左图片右内容 | 食材标签云 |
| 数据概览 | 仪表盘布局 | ECharts 图表 |

---

## 设计资源

### Google Fonts

- [Playfair Display](https://fonts.google.com/specimen/Playfair+Display)
- [DM Sans](https://fonts.google.com/specimen/DM+Sans)

### 配色参考

- [Coolors - 琥珀色调](https://coolors.co/palettes/popular/amber)
- [Adobe Color - 食物主题](https://color.adobe.com/explore/?q=food)

### 图标库

- Element Plus Icons
- 自定义 SVG 图标（保持简洁风格）

---

**设计规范版本**：v1.0
**最后更新**：2026-01-31
**维护者**：Claude (frontend-design skill)
