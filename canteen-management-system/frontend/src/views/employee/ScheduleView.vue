<template>
  <div class="schedule-view">
    <el-card>
      <template #header>
        <h2>我的排班</h2>
      </template>
      <div class="placeholder-content">
        <el-empty description="排班查看功能开发中，敬请期待">
          <el-icon :size="64" color="#FF6B35"><Calendar /></el-icon>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { Calendar } from '@element-plus/icons-vue'
</script>

<style scoped>
.schedule-view {
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder-content {
  padding: 60px 20px;
  text-align: center;
}
</style>
