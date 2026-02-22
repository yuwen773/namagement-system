<script setup>
</script>

<template>
  <router-view />
</template>

<style>
/* ==================== 全局变量 ==================== */
:root {
  /* 响应式断点 */
  --breakpoint-xl: 1440px;
  --breakpoint-lg: 1200px;
  --breakpoint-md: 992px;
  --breakpoint-sm: 768px;
  --breakpoint-xs: 480px;

  /* 主题色 */
  --primary-orange: #FF6B35;
  --primary-light: #FF8C42;
  --primary-dark: #E55A2B;
  --bg-cream: #FFF8F0;
  --bg-light: #FFFDF8;
  --text-primary: #333333;
  --text-secondary: #606266;
  --text-muted: #909399;
  --border-color: #E8DCC8;

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Microsoft YaHei', 'PingFang SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#app {
  height: 100%;
}

/* ==================== 响应式工具类 ==================== */

/* 大桌面及以上显示 */
@media (min-width: 1440px) {
  .responsive-show-xl { display: block !important; }
  .responsive-hide-xl { display: none !important; }
}

/* 桌面及以上显示 */
@media (min-width: 1200px) {
  .responsive-show-lg { display: block !important; }
  .responsive-hide-lg { display: none !important; }
}

/* 小桌面及以上显示 */
@media (min-width: 992px) {
  .responsive-show-md { display: block !important; }
  .responsive-hide-md { display: none !important; }
}

/* 平板及以上显示 */
@media (min-width: 768px) {
  .responsive-show-sm { display: block !important; }
  .responsive-hide-sm { display: none !important; }
}

/* 默认隐藏，通过媒体查询显示 */
.responsive-show-xs { display: none !important; }
.responsive-show-xxs { display: none !important; }

@media (max-width: 767px) {
  .responsive-show-xs { display: block !important; }
}

@media (max-width: 479px) {
  .responsive-show-xxs { display: block !important; }
}

/* 响应式间距工具类 */
.responsive-p-sm { padding: var(--spacing-sm); }
.responsive-p-md { padding: var(--spacing-md); }
.responsive-p-lg { padding: var(--spacing-lg); }

@media (max-width: 767px) {
  .responsive-p-sm { padding: var(--spacing-xs); }
  .responsive-p-md { padding: var(--spacing-sm); }
  .responsive-p-lg { padding: var(--spacing-md); }
}

/* 响应式文字大小 */
.responsive-text-lg { font-size: 18px; }
.responsive-text-md { font-size: 16px; }
.responsive-text-sm { font-size: 14px; }
.responsive-text-xs { font-size: 12px; }

@media (max-width: 767px) {
  .responsive-text-lg { font-size: 16px; }
  .responsive-text-md { font-size: 14px; }
  .responsive-text-sm { font-size: 13px; }
  .responsive-text-xs { font-size: 11px; }
}

/* 响应式Grid布局 */
.responsive-grid {
  display: grid;
  gap: var(--spacing-md);
}

@media (min-width: 1440px) {
  .responsive-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1200px) and (max-width: 1439px) {
  .responsive-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .responsive-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 991px) {
  .responsive-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .responsive-grid {
    grid-template-columns: 1fr;
  }
}

/* 响应式表格容器 */
.responsive-table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (min-width: 768px) {
  .responsive-table-container {
    overflow-x: visible;
  }
}
</style>
