<template>
  <div class="salary-view">
    <el-card>
      <template #header>
        <h2>工资条</h2>
      </template>
      <div class="placeholder-content">
        <el-empty description="工资条查看功能开发中，敬请期待">
          <el-icon :size="64" color="#42A5F5"><Wallet /></el-icon>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { Wallet } from '@element-plus/icons-vue'
</script>

<style scoped>
.salary-view {
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder-content {
  padding: 60px 20px;
  text-align: center;
}
</style>
