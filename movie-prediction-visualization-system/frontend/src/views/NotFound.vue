<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="not-found flex items-center justify-center h-screen bg-gray-50">
    <div class="text-center">
      <el-icon :size="120" class="text-gray-400 mb-4"><Warning /></el-icon>
      <h1 class="text-4xl font-bold text-gray-800 mb-4">404</h1>
      <p class="text-gray-600 mb-6">抱歉，您访问的页面不存在</p>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  min-height: 100vh;
}
</style>
