<template>
  <div class="attendance-view">
    <el-card>
      <template #header>
        <h2>考勤签到</h2>
      </template>
      <div class="placeholder-content">
        <el-empty description="考勤签到功能开发中，敬请期待">
          <el-icon :size="64" color="#4CAF50"><CircleCheck /></el-icon>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { CircleCheck } from '@element-plus/icons-vue'
</script>

<style scoped>
.attendance-view {
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder-content {
  padding: 60px 20px;
  text-align: center;
}
</style>
