<template>
  <div class="user-layout">
    <!-- 头部 -->
    <AppHeader />

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部 -->
    <AppFooter />

    <!-- 返回顶部按钮 -->
    <el-backtop :right="40" :bottom="60" :visibility-height="300">
      <div class="backtop-btn">
        <el-icon><CaretTop /></el-icon>
      </div>
    </el-backtop>
  </div>
</template>

<script setup>
import { CaretTop } from '@element-plus/icons-vue'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  width: 100%;
  padding: 0;
  min-height: calc(100vh - 280px);
  box-sizing: border-box;
  overflow-x: hidden;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 返回顶部按钮样式 */
.backtop-btn {
  width: 45px;
  height: 45px;
  background: #409eff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
  transition: all 0.3s;
}

.backtop-btn:hover {
  background: #66b1ff;
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.5);
}

.backtop-btn :deep(.el-icon) {
  font-size: 24px;
}

/* 响应式 */
@media (max-width: 768px) {
  .main-content {
    padding: 0;
  }
}
</style>
