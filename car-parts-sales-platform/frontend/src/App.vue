<script setup>
// App 根组件 - 布局组件已在路由中处理
// 路由守卫已处理用户信息获取
</script>

<template>
  <router-view />
</template>

<style>
/* 全局样式重置 */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  background-color: #f5f5f5;
}

#app {
  height: 100%;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 链接样式 */
a {
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s;
}

a:hover {
  color: #66b1ff;
}

/* 图片默认样式 */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* 按钮点击动画 */
.el-button {
  transition: all 0.3s;
}

/* 表格样式优化 */
.el-table {
  font-size: 13px;
}

/* 表单样式优化 */
.el-form-item__label {
  font-weight: 500;
}

/* 卡片样式优化 */
.el-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* 分页样式优化 */
.el-pagination {
  justify-content: center;
  margin-top: 20px;
}
</style>
