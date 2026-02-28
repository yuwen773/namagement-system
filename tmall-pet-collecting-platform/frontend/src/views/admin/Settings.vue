<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">系统设置</h2>
      <p class="page-subtitle">配置系统参数</p>
    </div>
    <div class="placeholder-content">
      <div class="placeholder-icon">⚙️</div>
      <p>系统设置页面开发中...</p>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  padding: 0;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.placeholder-content p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}
</style>
