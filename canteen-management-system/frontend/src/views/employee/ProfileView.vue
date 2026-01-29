<template>
  <div class="profile-view">
    <el-card>
      <template #header>
        <h2>个人信息</h2>
      </template>
      <div class="placeholder-content">
        <el-empty description="个人信息功能开发中，敬请期待">
          <el-icon :size="64" color="#FF6B35"><User /></el-icon>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { User } from '@element-plus/icons-vue'
</script>

<style scoped>
.profile-view {
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder-content {
  padding: 60px 20px;
  text-align: center;
}
</style>
