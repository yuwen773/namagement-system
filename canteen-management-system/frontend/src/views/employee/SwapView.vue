<template>
  <div class="swap-view">
    <el-card>
      <template #header>
        <h2>调班申请</h2>
      </template>
      <div class="placeholder-content">
        <el-empty description="调班申请功能开发中，敬请期待">
          <el-icon :size="64" color="#F7C52D"><Switch /></el-icon>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { Switch } from '@element-plus/icons-vue'
</script>

<style scoped>
.swap-view {
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder-content {
  padding: 60px 20px;
  text-align: center;
}
</style>
