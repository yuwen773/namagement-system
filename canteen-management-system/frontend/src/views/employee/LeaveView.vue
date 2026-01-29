<template>
  <div class="leave-view">
    <el-card>
      <template #header>
        <h2>请假申请</h2>
      </template>
      <div class="placeholder-content">
        <el-empty description="请假申请功能开发中，敬请期待">
          <el-icon :size="64" color="#FF6B35"><DocumentAdd /></el-icon>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { DocumentAdd } from '@element-plus/icons-vue'
</script>

<style scoped>
.leave-view {
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder-content {
  padding: 60px 20px;
  text-align: center;
}
</style>
